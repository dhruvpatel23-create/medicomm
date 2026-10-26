import { readFileSync, statSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { HttpError } from './security.mjs';
import { cleanQuestionPrompt } from '../src/lib/questionText.js';
import { massAttemptId } from './massTestStore.mjs';

let cachedDefinitions, definitionsMtime;
export function readFmgeTests() {
  const file = new URL('../data/fmge-practice-tests.json', import.meta.url);
  const modified = statSync(file).mtimeMs;
  if (!cachedDefinitions || modified !== definitionsMtime) {
    cachedDefinitions = JSON.parse(readFileSync(file, 'utf8'));
    definitionsMtime = modified;
  }
  return cachedDefinitions;
}
export const PART_MS = 150 * 60 * 1000;

export function massTestSchedule(test, clock) {
  if (!test.eventId) return {};
  const opens = Date.parse(test.waitingRoomOpensAt), starts = Date.parse(test.startsAt), ranks = Date.parse(test.rankReleaseAt);
  if (!Number.isFinite(opens) || !Number.isFinite(starts) || opens >= starts || !Number.isFinite(ranks) || ranks <= starts) throw new HttpError(503, 'The test schedule is unavailable.');
  return { waitingRoomOpensAt: test.waitingRoomOpensAt, startsAt: test.startsAt,
    rankReleaseAt: test.rankReleaseAt,
    stage: clock < opens ? 'locked' : clock < starts ? 'waiting' : 'open', singleAttempt: true };
}

function requireTestOpen(test, clock) {
  if (massTestSchedule(test, clock).stage !== 'open') throw new HttpError(403, 'This test opens on 27 October 2026 at 2:00 pm IST. Questions are locked until then.');
}

export function changeFmgeAttempt(attempt, method, action, body, clock) {
  const expired = advanceFmgeAttempt(attempt, clock);
  let changed = expired;
  if (method !== 'GET' && !expired) {
    if (method === 'PATCH') {
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
    } else if (action === 'finish-part') {
      if (![1, 2].includes(body.part)) throw new HttpError(400, 'Specify the part to submit.');
      if (attempt.status === 'active' && body.part === attempt.part) { finishPart(attempt, clock); changed = true; }
    } else if (action === 'next-part') {
      if (attempt.status === 'break') {
        attempt.part = 2; attempt.status = 'active'; attempt.currentIndex = 0;
        attempt.deadline = clock + PART_MS; attempt.revision++; changed = true;
      } else if (attempt.part !== 2) throw new HttpError(409, 'Finish Part 1 first.');
    }
  }
  return { changed, value: { attempt: fmgeAttemptView(attempt, clock), ...(expired && method !== 'GET'
    ? { message: 'Time expired. The last change was not saved; your previously saved answers were submitted.' } : {}) } };
}

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
    ...(attempt.rankReleaseAt ? { rankReleaseAt: attempt.rankReleaseAt } : {}),
    deadline: attempt.status === 'active' ? attempt.deadline : null, serverNow: now,
    currentIndex: attempt.currentIndex, answers: attempt.answers, marked: attempt.marked,
    questions: questions.map((q, index) => ({ id: q.id, number: complete ? index + 1 : (attempt.part - 1) * 150 + index + 1,
      prompt: cleanQuestionPrompt(q.prompt), options: q.options, imageUrls: q.imageUrls ?? [],
      ...(complete ? { subjectId: q.subjectId, subjectTitle: q.subjectTitle, answerIndex: q.answerIndex,
        explanation: q.explanation, sourceExam: q.sourceExam, sourceBank: q.sourceBank } : {}) })), result };
}

export function createFmgeTestsHandler({ readDatabase, writeDatabase, getSessionUser, hasPracticeAccess,
  parseRequestBody, sendJson, getDefinitions = readFmgeTests, now = Date.now, massStore, readAccess }) {
  const leaderboardCache = new Map();
  async function leaderboard(test) {
    const key = JSON.stringify([test.id, test.eventId]);
    let entry = leaderboardCache.get(key);
    if (!entry || entry.until <= now()) {
      entry = { until: now() + 30000 };
      entry.promise = massStore.completedRows(test).then(rows => {
        rows.sort((a, b) => b.score - a.score || a.completedAt - b.completedAt || a.attemptId.localeCompare(b.attemptId));
        let rank = 0;
        return { asOf: now(), rows: rows.map((row, index) => {
          if (index === 0 || row.score !== rows[index - 1].score) rank = index + 1;
          return { ...row, rank };
        }) };
      }).catch(error => { if (leaderboardCache.get(key) === entry) leaderboardCache.delete(key); throw error; });
      leaderboardCache.set(key, entry);
    }
    return entry.promise;
  }
  return async function handle(request, response, url) {
    const suffix = url.pathname.slice('/api/practice/fmge-tests'.length);
    const start = suffix.match(/^\/([a-zA-Z0-9_-]+)\/start$/);
    const waiting = suffix.match(/^\/([a-zA-Z0-9_-]+)\/waiting-room$/);
    const ranks = suffix.match(/^\/([a-zA-Z0-9_-]+)\/leaderboard$/);
    const route = suffix.match(/^\/attempts\/([a-f0-9-]+)(?:\/(finish-part|next-part))?$/);
    const isCatalog = !suffix && request.method === 'GET';
    if (!isCatalog && !(ranks && request.method === 'GET') && !(waiting && ['GET', 'POST'].includes(request.method)) && !(start && request.method === 'POST') && !(route && (
      (!route[2] && ['GET', 'PATCH'].includes(request.method)) || (route[2] && request.method === 'POST')))) {
      throw new HttpError(404, 'Test route not found.');
    }
    const body = ['POST', 'PATCH'].includes(request.method) ? await parseRequestBody(request) : {};
    for (let retry = 0; retry < 4; retry++) {
      let database = readAccess ? readAccess(request) : readDatabase();
      const user = getSessionUser(request, database);
      if (!user) throw new HttpError(401, 'Sign in to take a test.');
      if (!hasPracticeAccess(database, user.id)) throw new HttpError(403, 'An active Practice plan is required.');
      database.fmgeTestAttempts ??= [];
      const clock = now();
      const definitions = getDefinitions();
      const massTests = definitions.tests.filter(test => test.eventId);
      const massTest = ranks || waiting || start ? massTests.find(t => t.id === (ranks || waiting || start)[1])
        : route ? massTests.find(t => massAttemptId(t, user.id) === route[1]) : null;
      if (waiting && !massTest) throw new HttpError(404, 'Waiting room not found.');
      if (ranks && !massTest) throw new HttpError(404, 'Leaderboard not found.');
      if (massTest) {
        if (!massStore) throw new HttpError(503, 'Mass test storage is unavailable.');
        const schedule = massTestSchedule(massTest, clock);
        if (ranks) {
          const headers = { 'Cache-Control': 'private, no-store' };
          const metadata = { releasesAt: massTest.rankReleaseAt, serverNow: clock };
          if (clock < Date.parse(massTest.rankReleaseAt)) {
            // Do not even query participant scores before publication time.
            return sendJson(response, 200, { leaderboard: { ...metadata, released: false } }, headers);
          }
          const offset = Number(url.searchParams.get('offset') ?? 0);
          const limit = Number(url.searchParams.get('limit') ?? 50);
          if (!Number.isSafeInteger(offset) || offset < 0 || offset > 1000000 || !Number.isSafeInteger(limit) || limit < 1 || limit > 100) throw new HttpError(400, 'Invalid leaderboard page.');
          const snapshot = await leaderboard(massTest);
          const view = row => ({ rank: row.rank, name: row.name, score: row.score, total: 300, isYou: row.userId === user.id });
          const own = snapshot.rows.find(row => row.userId === user.id);
          return sendJson(response, 200, { leaderboard: { ...metadata, released: true, asOf: snapshot.asOf,
            rankingRule: 'Equal scores share a rank (1, 1, 3). Only completed attempts are included.',
            completedCount: snapshot.rows.length, yourRank: own ? view(own) : null, offset, limit,
            entries: snapshot.rows.slice(offset, offset + limit).map(view), hasMore: offset + limit < snapshot.rows.length } }, headers);
        }
        if (waiting) {
          if (schedule.stage === 'locked') throw new HttpError(403, 'The waiting room opens on 27 October 2026 at 1:00 pm IST.');
          const view = record => ({ waitingRoom: { testId: massTest.id, title: massTest.title, ...schedule,
            serverNow: clock, joinedAt: record.waitingJoinedAt, attemptId: record.attempt?.id ?? null } });
          const payload = request.method === 'POST' ? await massStore.transact(massTest, user.id, record => {
            const changed = !record.waitingJoinedAt;
            record.waitingJoinedAt ||= new Date(clock).toISOString();
            return { changed, value: view(record) };
          }) : view(await massStore.get(massTest, user.id));
          return sendJson(response, 200, payload, { 'Cache-Control': 'private, no-store' });
        }
        requireTestOpen(massTest, clock);
        if (start && (typeof body.startKey !== 'string' || !/^[a-zA-Z0-9-]{8,80}$/.test(body.startKey))) throw new HttpError(400, 'A valid start key is required.');
        // GETs do not lock or write while a part is still running.
        if (request.method === 'GET') {
          const record = await massStore.get(massTest, user.id);
          if (!record.attempt) throw new HttpError(404, 'Attempt not found.');
          if (record.attempt.status !== 'active' || clock < record.attempt.deadline) {
            return sendJson(response, 200, { attempt: fmgeAttemptView(record.attempt, clock) }, { 'Cache-Control': 'private, no-store' });
          }
        }
        let rankingChanged = false;
        const payload = await massStore.transact(massTest, user.id, record => {
          const transactionClock = now();
          requireTestOpen(massTest, transactionClock);
          let created = false;
          if (!record.attempt && start) {
            record.participantName = user.username || user.name || 'Participant';
            record.attempt = { id: massAttemptId(massTest, user.id), userId: user.id, testId: massTest.id,
              eventId: massTest.eventId, rankReleaseAt: massTest.rankReleaseAt, title: massTest.title, version: definitions.version, startKey: body.startKey,
              questions: massTest.questions, answers: {}, marked: {}, currentIndex: 0,
              startedAt: transactionClock, deadline: transactionClock + PART_MS, part: 1, status: 'active', revision: 0 };
            created = true;
          }
          if (!record.attempt) throw new HttpError(404, 'Attempt not found.');
          // A retry or different start key always returns the one official attempt.
          const result = changeFmgeAttempt(record.attempt, start ? 'GET' : request.method, route?.[2], body, transactionClock);
          result.changed ||= created;
          rankingChanged = result.changed && record.attempt.status === 'completed';
          return result;
        });
        if (rankingChanged) leaderboardCache.delete(JSON.stringify([massTest.id, massTest.eventId]));
        return sendJson(response, 200, payload, { 'Cache-Control': 'private, no-store' });
      }
      if (readAccess) {
        database = readDatabase();
        database.fmgeTestAttempts ??= [];
      }
      let changed = false;
      let payload;
      if (isCatalog) {
        const own = database.fmgeTestAttempts.filter(a => a.userId === user.id && !massTests.some(t => t.id === a.testId));
        for (const a of own) changed = advanceFmgeAttempt(a, clock) || changed;
        if (massStore) for (const test of massTests) {
          // Do not expose an old attempt's metadata before the scheduled opening.
          if (massTestSchedule(test, clock).stage === 'open') {
            const record = await massStore.get(test, user.id);
            if (record.attempt) own.push(record.attempt);
          }
        }
        const defs = definitions;
        payload = { serverNow: clock, blueprint: defs.blueprint, questionsPerPart: 150, minutesPerPart: 150, passMark: 150,
          tests: defs.tests.map(test => ({ id: test.id, title: test.title, category: test.category ?? 'practice',
            startsAt: test.startsAt ?? null, ...massTestSchedule(test, clock), questionCount: 300,
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
        if (massTests.some(t => t.id === attempt.testId)) throw new HttpError(410, 'Previous preview attempts have been cleared. Open the scheduled grand test.');
        const result = changeFmgeAttempt(attempt, request.method, route[2], body, clock);
        changed = result.changed;
        payload = result.value;
      }
      if (changed) {
        try { await writeDatabase(database); }
        catch (error) { if (error.status === 409 && retry < 3) continue; throw error; }
      }
      return sendJson(response, 200, payload, { 'Cache-Control': 'private, no-store' });
    }
  };
}
