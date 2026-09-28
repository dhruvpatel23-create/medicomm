import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
import { createMatch, lockAnswer, settleMatch, matchProgress } from './duels.mjs';

// Exercise the actual route handlers with isolated persistence and authentication.
// No live users or production data are touched.
const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
const handlers = source.slice(source.indexOf('function findActiveRatedDuel('), source.indexOf('function handleSummary('));
const sanitizer = source.slice(source.indexOf('function sanitizeDuelQuestionForClient('), source.indexOf('let duelPoolBank'));
const questions = [0, 1, 2, 3, 4].map(i => ({ id: `q${i}`, prompt: `Q${i}`, options: ['A', 'B', 'C', 'D'], answerIndex: i % 4, answer: ['A', 'B', 'C', 'D'][i % 4], explanation: 'Private until completed' }));

function fixture() {
  let db = { users: ['alice', 'bob', 'eve'].map(id => ({ id, rating: 1480 })), duels: [], duelQueue: [] };
  let writes = 0;
  const dependencies = {
    createMatch, lockAnswer, settleMatch, matchProgress, randomBytes,
    readDatabase: () => structuredClone(db),
    writeDatabase: data => { db = structuredClone(data); writes++; return Promise.resolve(); },
    requireSessionUser: (req, res, data) => data.users.find(u => u.id === req.user),
    parseRequestBody: async req => { if (req.wait) await req.wait; return req.body ?? {}; },
    sendJson: (res, status, body) => ({ status, body }),
    sanitizeUser: u => u, sanitizeDuelOpponent: u => u,
    sanitizeDuelQuestion: q => q, pickDuelQuestions: () => questions,
    DUEL_DURATION_SECONDS: 180, DEFAULT_USER_RATING: 1480,
  };
  const api = new Function(...Object.keys(dependencies), `${sanitizer}\n${handlers}\nreturn { handleDuelQuestions, handleDuelAction, handleJoinRatedDuelQueue, handleLeaveRatedDuelQueue };`)(...Object.values(dependencies));
  const call = (name, user, body = {}, action, wait) => api[name]({ user, body, method: 'POST', wait }, {}, new URL(`http://localhost/?session=${body.sessionId ?? ''}`), action);
  const pair = async () => {
    await call('handleJoinRatedDuelQueue', 'alice');
    const response = await call('handleJoinRatedDuelQueue', 'bob');
    return response.body.duel.id;
  };
  return { call, pair, database: () => db, writes: () => writes };
}

test('simultaneous queue joins produce one shared match', async () => {
  const f = fixture();
  await Promise.all(['alice', 'bob'].map(user => f.call('handleJoinRatedDuelQueue', user)));
  assert.equal(f.database().duels.length, 1);
  assert.deepEqual(f.database().duels[0].playerIds.sort(), ['alice', 'bob']);
});

test('questions are identical for both players and contain no answer key or explanation', async () => {
  const f = fixture(); const sessionId = await f.pair();
  const a = await f.call('handleDuelQuestions', 'alice', { sessionId });
  const b = await f.call('handleDuelQuestions', 'bob', { sessionId });
  assert.deepEqual(a.body.questions, b.body.questions);
  assert.doesNotMatch(JSON.stringify(a.body.questions), /answerIndex|explanation|"answer"/);
  assert.equal((await f.call('handleDuelQuestions', 'eve', { sessionId })).status, 403);
});

test('completion ignores forged scores, ratings, question IDs and unlocked selections', async () => {
  const f = fixture(); const sessionId = await f.pair();
  await f.call('handleDuelAction', 'alice', { sessionId, questionId: 'q0', optionIndex: 0 }, 'answer');
  const pending = await f.call('handleDuelAction', 'alice', { sessionId, opponentScore: 0, opponentRating: 99999, answers: { q1: 'B' }, questionIds: ['q0', 'q0'] }, 'complete');
  assert.equal(pending.body.result, null);
  await f.call('handleDuelAction', 'bob', { sessionId }, 'complete');
  const result = await f.call('handleDuelAction', 'alice', { sessionId }, 'complete');
  assert.equal(result.body.result.userScore, 1);
  assert.equal(result.body.result.attemptedQuestions, 1);
  assert.equal(result.body.result.delta, 16);
  const before = structuredClone(f.database());
  await f.call('handleDuelAction', 'alice', { sessionId }, 'complete');
  assert.deepEqual(f.database(), before);
});

test('slow request body cannot overwrite a more recent answer', async () => {
  const f = fixture(); const sessionId = await f.pair();
  let release;
  const wait = new Promise(resolve => { release = resolve; });
  const slow = f.call('handleDuelAction', 'alice', { sessionId, questionId: 'q0', optionIndex: 0 }, 'answer', wait);
  await f.call('handleDuelAction', 'bob', { sessionId, questionId: 'q1', optionIndex: 1 }, 'answer');
  release(); await slow;
  assert.deepEqual(f.database().duels[0].answers, { bob: { q1: 1 }, alice: { q0: 0 } });
});

test('leaving queue cannot delete a match; outsiders cannot submit or see results', async () => {
  const f = fixture(); const sessionId = await f.pair();
  await f.call('handleLeaveRatedDuelQueue', 'alice');
  assert.equal(f.database().duels.length, 1);
  for (const action of ['answer', 'status', 'complete']) {
    assert.equal((await f.call('handleDuelAction', 'eve', { sessionId, questionId: 'q0', optionIndex: 0 }, action)).status, 404);
  }
});

test('bot sessions require membership and active matches cannot be evaded', async () => {
  const f = fixture();
  assert.equal((await f.call('handleDuelQuestions', 'alice', { sessionId: 'bot-one' })).status, 200);
  assert.equal((await f.call('handleDuelQuestions', 'bob', { sessionId: 'bot-one' })).status, 403);
  assert.equal((await f.call('handleDuelQuestions', 'alice', { sessionId: 'bot-two' })).status, 409);
  assert.equal((await f.call('handleJoinRatedDuelQueue', 'alice')).status, 409);
});

test('unchanged live status polling does not write the database', async () => {
  const f = fixture(); const sessionId = await f.pair(); const before = f.writes();
  await f.call('handleDuelAction', 'alice', { sessionId }, 'status');
  assert.equal(f.writes(), before);
});
