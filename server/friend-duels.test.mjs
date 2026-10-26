import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
import { createMatch } from './duels.mjs';
import { FRIEND_DUEL_COUNTS, duelSubjectCatalog, validateFriendDuelSettings } from './friendDuelSettings.mjs';
import { shuffleQuestionOptions } from '../src/lib/shuffleQuestionOptions.js';
import { queuePush } from './push.mjs';

const pool = ['anatomy', 'pathology', 'ent'].flatMap(subjectId => Array.from({ length: 20 }, (_, i) => ({
  id: `${subjectId}-${i}`, subjectId, subjectTitle: subjectId, prompt: 'Question',
  options: ['A', 'B', 'C', 'D'], answerIndex: 0, answer: 'A',
})));
const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
const pickerSource = source.slice(source.indexOf('function pickDuelQuestions('), source.indexOf('function getValidSubjectIds('));
const pick = new Function('getDuelQuestionPool', 'randomBytes', 'DUEL_QUESTION_COUNT', 'FRIEND_DUEL_COUNTS', 'shuffleQuestionOptions',
  `${pickerSource}; return pickDuelQuestions;`)(() => pool, randomBytes, 5, FRIEND_DUEL_COUNTS, shuffleQuestionOptions);

test('friend settings reject invalid counts, subjects and insufficient questions', () => {
  for (const payload of [{ questionCount: 7 }, { questionCount: '10' }, { subjectIds: [] },
    { subjectIds: 'anatomy' }, { subjectIds: ['unknown'] }, { subjectIds: [null] }]) {
    assert.throws(() => validateFriendDuelSettings(payload, pool));
  }
  assert.throws(() => validateFriendDuelSettings({ questionCount: 15 }, pool.slice(0, 10)));
  assert.deepEqual(validateFriendDuelSettings({}, pool), { questionCount: 5, subjectIds: null });
  assert.deepEqual(duelSubjectCatalog(pool).map(s => s.questionCount), [20, 20, 20]);
});

test('actual picker returns exact counts without duplicates or unselected subjects', () => {
  for (const count of FRIEND_DUEL_COUNTS) {
    const questions = pick(count, ['pathology']);
    assert.equal(questions.length, count);
    assert.equal(new Set(questions.map(q => q.id)).size, count);
    assert.ok(questions.every(q => q.subjectId === 'pathology'));
    assert.ok(questions.every(q => q.options[q.answerIndex] === q.answer));
    assert.ok(pool.every(q => q.options[0] === 'A' && q.answerIndex === 0));
    assert.equal(pick(count).length, count);
  }
  assert.throws(() => pick(15, ['missing']));
});

function fixture() {
  let database = {
    users: [{ id: 'alice', name: 'Alice', rating: 1500 }, { id: 'bob', name: 'Bob', rating: 1500 }],
    duels: [], directConversations: [{ id: 'chat', participantIds: ['alice', 'bob'], messages: [] }],
    pushSubscriptions: [{ userId: 'bob' }],
  };
  let charges = 0;
  const dependencies = {
    readDatabase: () => structuredClone(database),
    parseRequestBody: async request => request.body,
    requireSessionUser: (request, response, db) => db.users.find(u => u.id === request.user),
    writeDatabase: async db => { database = db; },
    sendJson: (response, status, body) => ({ status, body }),
    getDuelQuestionPool: () => pool, pickDuelQuestions: pick,
    FRIEND_DUEL_COUNTS, duelSubjectCatalog, validateFriendDuelSettings, randomBytes, createMatch,
    sanitizeDuelOpponent: u => u, sanitizeDirectConversation: c => c,
    chargeTokens: () => { charges++; }, DEFAULT_USER_RATING: 1500,
    queuePush, pushService: { tick: async () => {} },
  };
  const handlers = source.slice(source.indexOf('function handleDuelChallengeOptions('), source.indexOf('async function handleDeclineDuelChallenge('));
  const api = new Function(...Object.keys(dependencies), `${handlers}; return { handleCreateDuelChallenge, handleAcceptDuelChallenge };`)(...Object.values(dependencies));
  return {
    call: (name, user, body) => api[name]({ user, body }, {}),
    db: () => database, charges: () => charges,
  };
}

test('friend request stores selection, describes it, and acceptance uses it for both players', async () => {
  for (const questionCount of FRIEND_DUEL_COUNTS) {
    const f = fixture();
    const created = await f.call('handleCreateDuelChallenge', 'alice', { opponentId: 'bob', questionCount, subjectIds: ['anatomy', 'ent'] });
    assert.equal(created.status, 201);
    assert.equal(f.db().pushQueue.length, 1);
    assert.equal(f.db().pushQueue[0].userId, 'bob');
    assert.match(f.db().pushQueue[0].title, /Alice challenged you for 1v1/);
    assert.equal(created.body.challenge.questionCount, questionCount);
    assert.match(created.body.conversation.messages[0].text, new RegExp(`${questionCount} questions`));
    assert.match(created.body.conversation.messages[0].text, /anatomy, ent/);
    const body = { challengeId: created.body.challenge.id, questionCount: 5, subjectIds: ['pathology'] };
    assert.equal((await f.call('handleAcceptDuelChallenge', 'alice', body)).status, 403);
    const accepted = await f.call('handleAcceptDuelChallenge', 'bob', body);
    assert.equal(accepted.status, 200);
    const match = f.db().duels[0];
    assert.equal(match.questions.length, questionCount);
    assert.deepEqual(match.playerIds, ['alice', 'bob']);
    assert.ok(match.questions.every(q => ['anatomy', 'ent'].includes(q.subjectId)));
    const again = await f.call('handleAcceptDuelChallenge', 'bob', body);
    assert.equal(again.body.duel.id, accepted.body.duel.id);
    assert.equal(f.db().duels.length, 1);
    assert.equal(f.charges(), 2);
  }
});

test('invalid friend selections do not send a request', async () => {
  const f = fixture();
  const result = await f.call('handleCreateDuelChallenge', 'alice', { opponentId: 'bob', questionCount: 15, subjectIds: [] });
  assert.equal(result.status, 400);
  assert.equal(f.db().directConversations[0].messages.length, 0);
});

test('notification invitations cannot start an expired challenge', async () => {
  const f = fixture();
  const created = await f.call('handleCreateDuelChallenge', 'alice', { opponentId: 'bob' });
  f.db().challengeRooms[0].createdAtMs = Date.now() - 600001;
  const accepted = await f.call('handleAcceptDuelChallenge', 'bob', { challengeId: created.body.challenge.id });
  assert.equal(accepted.status, 410);
  assert.match(accepted.body.message, /expired/);
  assert.equal(f.charges(), 0);
});
