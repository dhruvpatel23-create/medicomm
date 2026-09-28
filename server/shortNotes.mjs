import { readFileSync } from 'node:fs';

export function loadShortNotes(file) {
  const bank = JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
  const questions = new Map();
  for (const subject of bank.subjects) for (const topic of subject.topics) for (const question of topic.questions) {
    if (questions.has(question.id)) throw new Error('Duplicate short-note question ID.');
    questions.set(question.id, { ...question, subjectId: subject.id, subjectTitle: subject.title, topicTitle: topic.title });
  }
  return questions;
}

export function createShortNotesHandler({ questions, readDatabase, writeDatabase, requireSessionUser, parseRequestBody, sendJson, parseAnswerImage, evaluate }) {
  const pending = new Set();
  return async function handleShortNotes(request, response) {
    const database = readDatabase();
    const user = requireSessionUser(request, response, database);
    if (!user) return;
    if (request.method === 'GET') {
      return sendJson(response, 200, { reviews: (database.shortNoteReviews ?? []).filter(review => review.userId === user.id).map(({ userId, ...review }) => review) });
    }
    const payload = await parseRequestBody(request);
    const question = questions.get(String(payload.questionId ?? ''));
    if (!question) return sendJson(response, 400, { message: 'Choose a question from the Short Notes library.' });
    if (payload.privacyAccepted !== true) return sendJson(response, 400, { message: 'Please accept the AI review notice before submitting.' });
    const answer = String(payload.answer ?? '').trim();
    let answerImage;
    try { answerImage = parseAnswerImage(payload.answerImageDataUrl); }
    catch (error) { return sendJson(response, 400, { message: error.message }); }
    if (answer.length > 8000 || (!answerImage && answer.length < 3)) {
      return sendJson(response, 400, { message: 'Write at least 3 characters or upload an answer photo. Typed answers can contain up to 8,000 characters.' });
    }
    if (pending.has(user.id)) return sendJson(response, 409, { message: 'Your previous answer is still being reviewed. Please wait.' });
    const recent = (database.shortNoteReviews ?? []).filter(review => review.userId === user.id && Date.parse(review.submittedAt) > Date.now() - 3600000);
    if (recent.length >= 60) return sendJson(response, 429, { message: 'You have reached the hourly review limit. Please try again later.' });
    pending.add(user.id);
    try {
      // The trusted source prompt is selected on the server; clients cannot substitute a rubric.
      const clinicalCase = {
        id: question.id, kind: question.kind, chapterTitle: question.topicTitle,
        difficulty: question.kind === 'long-answer' ? 'Long answer' : 'Short note',
        stem: question.prompt, subquestions: [{ label: 'A', prompt: question.prompt, marks: 10 }], keyPoints: [],
      };
      const evaluation = await evaluate({ subjectTitle: question.subjectTitle, clinicalCase, studentAnswer: answer, studentAnswerImage: answerImage });
      const review = { questionId: question.id, userId: user.id, answer, hasImage: Boolean(answerImage), ...evaluation, submittedAt: new Date().toISOString() };
      const latest = readDatabase();
      latest.shortNoteReviews = [review, ...(latest.shortNoteReviews ?? []).filter(item => !(item.userId === user.id && item.questionId === question.id))];
      await writeDatabase(latest);
      const { userId, ...publicReview } = review;
      return sendJson(response, 201, { review: publicReview });
    } catch (error) {
      return sendJson(response, 502, { message: error instanceof Error ? error.message : 'Could not review your answer. Your draft is still here.' });
    } finally { pending.delete(user.id); }
  };
}
