import { readFileSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { HttpError } from './security.mjs';
import { cleanQuestionPrompt } from '../src/lib/questionText.js';

let definitions;
export function readFmgeTests() {
  return definitions ??= JSON.parse(readFileSync(new URL('../data/fmge-practice-tests.json', import.meta.url), 'utf8'));
}
export const PART_MS = 150 * 60 * 1000;

export function advanceFmgeAttempt(attempt, now) {
  if (attempt.status !== 'active' || now < attempt.deadline) return false;
  finishPart(attempt, now);
  return true;
}

function finishPart(attempt, now) {
  attempt.partFinishedAt ??= {};
  attempt.partFinishedAt[attempt.part] = now;
  attempt.status = attempt.part === 1 ? 'break' : 'completed';
  if (attempt.status === 'completed') attempt.completedAt = now;
  attempt.revision++;
}

function summary(attempt) {
  return { id: attempt.id, testId: attempt.testId, status: attempt.status, part: attempt.part,
    startedAt: attempt.startedAt, completedAt: attempt.completedAt ?? null,
    answered: Object.keys(attempt.answers).length,
    score: attempt.status === 'completed' ? attempt.questions.filter(q => attempt.answers[q.id] === q.answerIndex).length : null };
}

export function fmgeAttemptView(attempt, now) {
  const complete = attempt.status === 'completed';
  const questions = complete ? attempt.questions : attempt.status === 'break' ? [] : attempt.questions.slice((attempt.part - 1) * 150, attempt.part * 150);
  const result = complete ? {
    score: summary(attempt).score, total: 300, passMark: 150,
    correct: summary(attempt).score,
    incorrect: Object.keys(attempt.answers).length - summary(attempt).score,
    unanswered: 300 - Object.keys(attempt.answers).length,
    subjects: [...new Set(attempt.questions.map(q => q.subjectId))].map(id => {
      const qs = attempt.questions.filter(q => q.subjectId === id);
      return { id, title: qs[0].subjectTitle, total: qs.length,
        correct: qs.filter(q => attempt.answers[q.id] === q.answerIndex).length,
        answered: qs.filter(q => Object.hasOwn(attempt.answers, q.id)).length };
    }),
  } : null;
  return { ...summary(attempt), revision: attempt.revision, title: attempt.title,
    deadline: attempt.status === 'active' ? attempt.deadline : null, serverNow: now,
    currentIndex: attempt.currentIndex, answers: attempt.answers, marked: attempt.marked,
    questions: questions.map((q, index) => ({ id: q.id, number: complete ? index + 1 : (attempt.part - 1) * 150 + index + 1,
      prompt: cleanQuestionPrompt(q.prompt), options: q.options,
      ...(complete ? { subjectId: q.subjectId, subjectTitle: q.subjectTitle, answerIndex: q.answerIndex,
        explanation: q.explanation, sourceExam: q.sourceExam, sourceBank: q.sourceBank } : {}) })), result };
}

export function createFmgeTestsHandler({ readDatabase, writeDatabase, getSessionUser, hasPracticeAccess,
  parseRequestBody, sendJson, getDefinitions = readFmgeTests, now = Date.now }) {
  return async function handle(request, response, url) {
    const suffix = url.pathname.slice('/api/practice/fmge-tests'.length);
    const start = suffix.match(/^\/(fmge-practice-[123])\/start$/);
    const route = suffix.match(/^\/attempts\/([a-f0-9-]+)(?:\/(finish-part|next-part))?$/);
    const isCatalog = !suffix && request.method === 'GET';
    if (!isCatalog && !(start && request.method === 'POST') && !(route && (
      (!route[2] && ['GET', 'PATCH'].includes(request.method)) || (route[2] && request.method === 'POST')))) {
      throw new HttpError(404, 'Test route not found.');
    }
    const body = ['POST', 'PATCH'].includes(request.method) ? await parseRequestBody(request) : {};
    for (let retry = 0; retry < 4; retry++) {
      const database = readDatabase();
      const user = getSessionUser(request, database);
      if (!user) throw new HttpError(401, 'Sign in to take a test.');
      if (!hasPracticeAccess(database, user.id)) throw new HttpError(403, 'An active Practice plan is required.');
      database.fmgeTestAttempts ??= [];
      const clock = now();
      let changed = false;
      let payload;
      if (isCatalog) {
        const own = database.fmgeTestAttempts.filter(a => a.userId === user.id);
        for (const a of own) changed = advanceFmgeAttempt(a, clock) || changed;
        const defs = getDefinitions();
        payload = { blueprint: defs.blueprint, questionsPerPart: 150, minutesPerPart: 150, passMark: 150,
          tests: defs.tests.map(test => ({ id: test.id, title: test.title, questionCount: 300,
            attempts: own.filter(a => a.testId === test.id).sort((a,b) => b.startedAt - a.startedAt).map(summary) })) };
      } else if (start) {
        const test = getDefinitions().tests.find(t => t.id === start[1]);
        if (!test) throw new HttpError(404, 'Test not found.');
        if (typeof body.startKey !== 'string' || !/^[a-zA-Z0-9-]{8,80}$/.test(body.startKey)) throw new HttpError(400, 'A valid start key is required.');
        let attempt = database.fmgeTestAttempts.find(a => a.userId === user.id && a.testId === test.id && (a.startKey === body.startKey || a.status !== 'completed'));
        if (!attempt) {
          attempt = { id: randomUUID(), userId: user.id, testId: test.id, title: test.title,
            version: getDefinitions().version, startKey: body.startKey,
            questions: structuredClone(test.questions), answers: {}, marked: {}, currentIndex: 0,
            startedAt: clock, deadline: clock + PART_MS, part: 1, status: 'active', revision: 0 };
          database.fmgeTestAttempts.push(attempt);
          changed = true;
        }
        changed = advanceFmgeAttempt(attempt, clock) || changed;
        payload = { attempt: fmgeAttemptView(attempt, clock) };
      } else {
        const attempt = database.fmgeTestAttempts.find(a => a.id === route[1] && a.userId === user.id);
        if (!attempt) throw new HttpError(404, 'Attempt not found.');
        const expired = advanceFmgeAttempt(attempt, clock);
        changed = expired;
        if (request.method !== 'GET' && !expired) {
          if (request.method === 'PATCH') {
            if (attempt.status !== 'active') throw new HttpError(409, 'This part has ended. Refresh the attempt.');
            if (body.revision !== attempt.revision) throw new HttpError(409, 'This attempt changed in another tab. Reload to continue.');
            if (Object.hasOwn(body, 'currentIndex')) {
              if (!Number.isInteger(body.currentIndex) || body.currentIndex < 0 || body.currentIndex >= 150) throw new HttpError(400, 'Invalid question position.');
              attempt.currentIndex = body.currentIndex;
            }
            if (Object.hasOwn(body, 'questionId')) {
              const q = attempt.questions.slice((attempt.part - 1) * 150, attempt.part * 150).find(q => q.id === body.questionId);
              if (!q) throw new HttpError(400, 'Question is not in the active part.');
              if (Object.hasOwn(body, 'optionIndex')) {
                if (body.optionIndex !== null && (!Number.isInteger(body.optionIndex) || body.optionIndex < 0 || body.optionIndex > 3)) throw new HttpError(400, 'Choose a valid option.');
                if (body.optionIndex === null) delete attempt.answers[q.id];
                else attempt.answers[q.id] = body.optionIndex;
              }
              if (Object.hasOwn(body, 'marked')) {
                if (typeof body.marked !== 'boolean') throw new HttpError(400, 'Invalid review flag.');
                if (body.marked) attempt.marked[q.id] = true;
                else delete attempt.marked[q.id];
              }
            }
            attempt.revision++;
            changed = true;
          } else if (route[2] === 'finish-part') {
            if (![1, 2].includes(body.part)) throw new HttpError(400, 'Specify the part to submit.');
            if (attempt.status === 'active' && body.part === attempt.part) { finishPart(attempt, clock); changed = true; }
          } else if (route[2] === 'next-part') {
            if (attempt.status === 'break') {
              attempt.part = 2; attempt.status = 'active'; attempt.currentIndex = 0;
              attempt.deadline = clock + PART_MS; attempt.revision++; changed = true;
            } else if (attempt.part !== 2) throw new HttpError(409, 'Finish Part 1 first.');
          }
        }
        payload = { attempt: fmgeAttemptView(attempt, clock), ...(expired && request.method !== 'GET' ? { message: 'Time expired. The last change was not saved; your previously saved answers were submitted.' } : {}) };
      }
      if (changed) {
        try { await writeDatabase(database); }
        catch (error) { if (error.status === 409 && retry < 3) continue; throw error; }
      }
      return sendJson(response, 200, payload);
    }
  };
}
