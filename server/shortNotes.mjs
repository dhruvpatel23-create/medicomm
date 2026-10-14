import { readFileSync } from 'node:fs';

import { randomUUID } from 'node:crypto';
import { decodeImage } from './uploads.mjs';

export function ownsTheoryAnswerImage(database, userId, name) {
  return (database.shortNoteReviews ?? []).some(review => review.userId === userId
    && (review.answerPages ?? []).some(page => page.imagePath === name));
}

function publicReview({ userId, answerPages = [], ...review }, attemptCount) {
  return { ...review, ...(attemptCount ? { attemptCount } : {}),
    answerPages: answerPages.map(({ imagePath, ...page }) => ({ ...page, imageUrl: `/uploads/${imagePath}` })) };
}

export function loadShortNotes(file) {
  const bank = JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
  const questions = new Map();
  for (const subject of bank.subjects) for (const topic of subject.topics) for (const question of topic.questions) {
    if (questions.has(question.id)) throw new Error('Duplicate short-note question ID.');
    questions.set(question.id, { ...question, subjectId: subject.id, subjectTitle: subject.title, topicTitle: topic.title });
  }
  return questions;
}

export function createShortNotesHandler({ questions, readDatabase, writeDatabase, requireSessionUser, parseRequestBody, sendJson, parseAnswerImage, evaluate, saveAnswerImage, removeAnswerImage }) {
  const pending = new Set();
  return async function handleShortNotes(request, response) {
    const database = readDatabase();
    const user = requireSessionUser(request, response, database);
    if (!user) return;
    if (request.method === 'GET') {
      const questionId = new URL(request.url || '/api/short-notes/reviews', 'http://localhost').searchParams.get('questionId');
      const own = (database.shortNoteReviews ?? []).filter(review => review.userId === user.id);
      if (questionId) return sendJson(response, 200, { reviews: own.filter(review => review.questionId === questionId).map(review => publicReview(review)) });
      const groups = new Map();
      for (const review of own) {
        const group = groups.get(review.questionId) || [];
        group.push(review); groups.set(review.questionId, group);
      }
      return sendJson(response, 200, { reviews: [...groups.values()].map(group => publicReview(group[0], group.length)) });
    }
    const payload = await parseRequestBody(request);
    const question = questions.get(String(payload.questionId ?? ''));
    if (!question) return sendJson(response, 400, { message: 'Choose a question from the Short Notes library.' });
    if (payload.privacyAccepted !== true) return sendJson(response, 400, { message: 'Please accept the AI review notice before submitting.' });
    const answer = String(payload.answer ?? '').trim();
    let images;
    try {
      const pages = payload.answerPages ?? (payload.answerImageDataUrl ? [{ dataUrl: payload.answerImageDataUrl }] : []);
      if (!Array.isArray(pages) || pages.length > 8) throw new Error('Attach up to 8 answer pages.');
      let bytes = 0;
      images = pages.map((page, index) => {
        const parsed = parseAnswerImage(page?.dataUrl);
        if (!parsed) throw new Error('An answer page is empty.');
        const dataUrl = `data:${parsed.mimeType};base64,${parsed.data}`;
        bytes += decodeImage(dataUrl).bytes.length;
        return { parsed, dataUrl, name: String(page.name || `Page ${index + 1}`).slice(0, 160), source: page.source === 'notepad' ? 'notepad' : 'upload' };
      });
      if (bytes > 5 * 1024 * 1024) throw new Error('Prepared answer pages must total 5 MB or less.');
    }
    catch (error) { return sendJson(response, 400, { message: error.message }); }
    if (answer.length > 8000 || (!images.length && answer.length < 3)) {
      return sendJson(response, 400, { message: 'Write at least 3 characters or upload an answer photo. Typed answers can contain up to 8,000 characters.' });
    }
    if (pending.has(user.id)) return sendJson(response, 409, { message: 'Your previous answer is still being reviewed. Please wait.' });
    const recent = (database.shortNoteReviews ?? []).filter(review => review.userId === user.id && Date.parse(review.submittedAt) > Date.now() - 3600000);
    if (recent.length >= 60) return sendJson(response, 429, { message: 'You have reached the hourly review limit. Please try again later.' });
    pending.add(user.id);
    const savedPages = [];
    let committed = false;
    try {
      // The trusted source prompt is selected on the server; clients cannot substitute a rubric.
      const clinicalCase = {
        id: question.id, kind: question.kind, chapterTitle: question.topicTitle,
        difficulty: question.kind === 'long-answer' ? 'Long answer' : 'Short note',
        stem: question.prompt, subquestions: [{ label: 'A', prompt: question.prompt, marks: 10 }], keyPoints: [],
      };
      for (const image of images) {
        if (!saveAnswerImage) throw new Error('Answer image storage is unavailable. Please try again later.');
        const imagePath = await saveAnswerImage(image.dataUrl);
        savedPages.push({ imagePath, name: image.name, source: image.source });
      }
      const evaluation = await evaluate({ subjectTitle: question.subjectTitle, clinicalCase, studentAnswer: answer,
        studentAnswerImage: images[0]?.parsed ?? null, studentAnswerImages: images.map(image => image.parsed) });
      const review = { ...evaluation, id: randomUUID(), questionId: question.id, userId: user.id, answer,
        answerPages: savedPages, hasImage: images.length > 0, submittedAt: new Date().toISOString() };
      const latest = readDatabase();
      latest.shortNoteReviews = [review, ...(latest.shortNoteReviews ?? [])];
      await writeDatabase(latest);
      committed = true;
      return sendJson(response, 201, { review: publicReview(review, latest.shortNoteReviews.filter(item => item.userId === user.id && item.questionId === question.id).length) });
    } catch (error) {
      return sendJson(response, 502, { message: error instanceof Error ? error.message : 'Could not review your answer. Your draft is still here.' });
    } finally {
      if (!committed && removeAnswerImage) {
        // A remote write can succeed even if its response is interrupted. Only
        // remove files confirmed unreferenced by the recovered database state.
        try {
          const recovered = readDatabase();
          await Promise.allSettled(savedPages.filter(page => !ownsTheoryAnswerImage(recovered, user.id, page.imagePath)).map(page => removeAnswerImage(page.imagePath)));
        } catch { /* Keep files if storage cannot confirm whether they committed. */ }
      }
      pending.delete(user.id);
    }
  };
}
