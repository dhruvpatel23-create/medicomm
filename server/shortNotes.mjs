import { readFileSync } from 'node:fs';

import { randomUUID } from 'node:crypto';
import { decodeImage } from './uploads.mjs';
import { chargeTokens, refundTokens, updateTokenState } from './tokens.mjs';

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

export function createShortNotesHandler({ reviewStore = null, questions, readDatabase, writeDatabase, requireSessionUser, parseRequestBody, sendJson, parseAnswerImage, evaluate, saveAnswerImage, removeAnswerImage, generatePrompt }) {
  const pending = new Set();
  return async function handleShortNotes(request, response) {
    const database = readDatabase();
    const user = requireSessionUser(request, response, database);
    if (!user) return;
    const url = new URL(request.url || '/api/short-notes/reviews', 'http://localhost');

    if (url.pathname === '/api/short-notes/custom') {
      if (request.method === 'GET') {
        const subjectId = url.searchParams.get('subjectId');
        const custom = (database.customShortNotes ?? [])
          .filter(q => q.userId === user.id && (!subjectId || q.subjectId === subjectId));
        return sendJson(response, 200, { questions: custom });
      }
      if (request.method === 'POST') {
        const payload = await parseRequestBody(request);
        const prompt = String(payload?.prompt ?? '').trim();
        if (prompt.length < 3 || prompt.length > 1000) {
          return sendJson(response, 400, { message: 'Write a question between 3 and 1,000 characters.' });
        }
        const subjectId = String(payload?.subjectId ?? '').trim();
        const subjectTitle = String(payload?.subjectTitle ?? '').trim() || 'Theory';
        const kind = payload?.kind === 'long-answer' ? 'long-answer' : 'short-note';
        const newQuestion = {
          id: `custom-${randomUUID()}`,
          userId: user.id,
          subjectId,
          subjectTitle,
          topicTitle: 'Custom Notes',
          prompt,
          kind,
          isCustom: true,
          createdAt: new Date().toISOString(),
        };
        await updateTokenState(readDatabase, writeDatabase, latest => {
          latest.customShortNotes = [newQuestion, ...(latest.customShortNotes ?? [])];
        });
        return sendJson(response, 201, { question: newQuestion });
      }
      if (request.method === 'DELETE') {
        let questionId = url.searchParams.get('questionId');
        if (!questionId) {
          try {
            const body = await parseRequestBody(request);
            questionId = body?.questionId;
          } catch { /* empty */ }
        }
        if (!questionId) return sendJson(response, 400, { message: 'Specify a question ID to delete.' });
        await updateTokenState(readDatabase, writeDatabase, latest => {
          latest.customShortNotes = (latest.customShortNotes ?? []).filter(q => !(q.id === questionId && q.userId === user.id));
        });
        return sendJson(response, 200, { ok: true });
      }
      return sendJson(response, 405, { message: 'Method not allowed.' });
    }

    if (url.pathname === '/api/short-notes/generate-prompt') {
      if (request.method !== 'POST') return sendJson(response, 405, { message: 'Method not allowed.' });
      const payload = await parseRequestBody(request);
      const topic = String(payload?.topic ?? '').trim();
      const subjectTitle = String(payload?.subjectTitle ?? '').trim() || 'Theory';
      const kind = payload?.kind === 'long-answer' ? 'long-answer' : 'short-note';
      if (!topic) return sendJson(response, 400, { message: 'Please provide a topic or concept.' });
      if (!generatePrompt) {
        return sendJson(response, 200, {
          prompt: kind === 'long-answer'
            ? `${topic} – Etiopathogenesis, Clinical Features, Investigations, and Management`
            : `${topic} – Key Features, Pathophysiology, and Applied Significance`,
        });
      }
      try {
        const prompt = await generatePrompt({ subjectTitle, topic, kind });
        return sendJson(response, 200, { prompt: prompt || topic });
      } catch {
        return sendJson(response, 200, {
          prompt: kind === 'long-answer'
            ? `${topic} – Etiopathogenesis, Clinical Features, Investigations, and Management`
            : `${topic} – Key Features, Pathophysiology, and Applied Significance`,
        });
      }
    }

    if (request.method === 'GET') {
      const questionId = url.searchParams.get('questionId');
      const offset = Number(url.searchParams.get('offset') || 0);
      if (!Number.isSafeInteger(offset) || offset < 0) return sendJson(response, 400, { message: 'Invalid review page.' });
      const own = reviewStore ? (questionId ? await reviewStore.reviews(user.id, questionId, offset) : await reviewStore.summaries(user.id, offset)) : (database.shortNoteReviews ?? []).filter(review => review.userId === user.id);
      const nextOffset = reviewStore && own.length === 100 ? offset + 100 : null;
      if (questionId) return sendJson(response, 200, { nextOffset, reviews: own.filter(review => review.questionId === questionId).map(review => publicReview(review)) });
      const groups = new Map();
      for (const review of own) {
        const group = groups.get(review.questionId) || [];
        group.push(review); groups.set(review.questionId, group);
      }
      return sendJson(response, 200, { nextOffset, reviews: [...groups.values()].map(group => publicReview(group[0], group[0].attemptCount || group.length)) });
    }
    const payload = await parseRequestBody(request);
    let question = questions.get(String(payload.questionId ?? ''));
    if (!question) {
      const customList = database.customShortNotes ?? [];
      const custom = customList.find(q => q.id === payload.questionId && (q.userId === user.id || !q.userId));
      if (custom) {
        question = {
          ...custom,
          topicTitle: custom.topicTitle || 'Custom Notes',
          subjectTitle: custom.subjectTitle || 'Theory',
        };
      } else if (payload.customQuestion && payload.customQuestion.prompt) {
        const cq = payload.customQuestion;
        question = {
          id: String(payload.questionId || `custom-${randomUUID()}`),
          userId: user.id,
          subjectId: String(cq.subjectId || '').trim(),
          subjectTitle: String(cq.subjectTitle || '').trim() || 'Theory',
          topicTitle: 'Custom Notes',
          prompt: String(cq.prompt || '').trim(),
          kind: cq.kind === 'long-answer' ? 'long-answer' : 'short-note',
          isCustom: true,
          createdAt: new Date().toISOString(),
        };
        await updateTokenState(readDatabase, writeDatabase, latest => {
          const list = latest.customShortNotes ?? [];
          if (!list.some(item => item.id === question.id)) {
            latest.customShortNotes = [question, ...list];
          }
        });
      }
    }
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
    const recent = reviewStore ? await reviewStore.reviews(user.id, null, 0, new Date(Date.now() - 3600000).toISOString()) : (database.shortNoteReviews ?? []).filter(review => review.userId === user.id && Date.parse(review.submittedAt) > Date.now() - 3600000);
    if (recent.length >= 60) return sendJson(response, 429, { message: 'You have reached the hourly review limit. Please try again later.' });
    pending.add(user.id);
    const savedPages = [];
    const reviewId = randomUUID();
    const tokenKey = `review:${reviewId}`;
    let committed = false;
    try {
      await updateTokenState(readDatabase, writeDatabase, latest => chargeTokens(latest, user.id, 10, tokenKey));
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
      const review = { ...evaluation, id: reviewId, questionId: question.id, userId: user.id, answer,
        answerPages: savedPages, hasImage: images.length > 0, submittedAt: new Date().toISOString() };
      if (reviewStore) await reviewStore.saveReview(review);
      else await updateTokenState(readDatabase, writeDatabase, latest => {
        latest.shortNoteReviews = [review, ...(latest.shortNoteReviews ?? []).filter(item => item.id !== reviewId)];
      });
      const latest = readDatabase();
      committed = true;
      return sendJson(response, 201, { review: publicReview(review, reviewStore ? undefined : latest.shortNoteReviews.filter(item => item.userId === user.id && item.questionId === question.id).length) });
    } catch (error) {
      return sendJson(response, error.status || 502, { message: error instanceof Error ? error.message : 'Could not review your answer. Your draft is still here.' });
    } finally {
      if (!committed) {
        try {
          const remotelySaved = reviewStore ? await reviewStore.hasReview(user.id, reviewId) : false;
          if (remotelySaved) committed = true;
          await updateTokenState(readDatabase, writeDatabase, latest => {
            if (!remotelySaved && !(latest.shortNoteReviews ?? []).some(review => review.id === reviewId)) refundTokens(latest, user.id, tokenKey);
          });
        } catch (error) { console.warn('Could not reconcile review tokens:', error.message); }
      }
      if (!committed && removeAnswerImage) {
        // A remote write can succeed even if its response is interrupted. Only
        // remove files confirmed unreferenced by the recovered database state.
        try {
          const recovered = readDatabase();
          if (!reviewStore || !(await reviewStore.hasReview(user.id, reviewId))) await Promise.allSettled(savedPages.filter(page => !ownsTheoryAnswerImage(recovered, user.id, page.imagePath)).map(page => removeAnswerImage(page.imagePath)));
        } catch { /* Keep files if storage cannot confirm whether they committed. */ }
      }
      pending.delete(user.id);
    }
  };
}
