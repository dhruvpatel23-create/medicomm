import test from 'node:test';
import assert from 'node:assert/strict';
import { createMatch, validDuelQuestion, lockAnswer, reviewMatch, settleMatch, matchProgress } from './duels.mjs';

const questions = [0, 1, 2].map(i => ({ id: `q${i}`, prompt: `Question ${i}`, options: ['A', 'B', 'C', 'D'], answerIndex: i, answer: ['A', 'B', 'C'][i], explanation: 'Saved explanation' }));
function fixture(type = 'rated') {
  const users = [{ id: 'alice', rating: 1480 }, { id: 'bob', rating: 1480 }];
  return { users, match: createMatch('match', type === 'rated' ? ['alice', 'bob'] : ['alice'], questions, { alice: 1480, bob: 1480 }, 1000, type) };
}

test('rejects conflicting answer keys, duplicate options and invalid indexes', () => {
  assert.equal(validDuelQuestion({ ...questions[0], answer: 'B' }), false);
  assert.equal(validDuelQuestion({ ...questions[0], options: ['A', 'A', 'C', 'D'] }), false);
  assert.equal(validDuelQuestion({ ...questions[0], options: ['A', ' A ', 'C', 'D'] }), false);
  assert.equal(validDuelQuestion({ ...questions[0], answerIndex: 4 }), false);
  assert.throws(() => createMatch('m', ['alice'], [questions[0], questions[0]], {}, 0));
});

test('grades option indexes exactly and reviews wrong/unanswered answers', () => {
  const { match } = fixture();
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  lockAnswer(match, 'alice', 'q1', 2, 2000);
  assert.deepEqual(reviewMatch(match, 'alice').map(q => q.status), ['correct', 'incorrect', 'unanswered']);
  assert.equal(reviewMatch(match, 'alice')[1].correctIndex, 1);
});

test('locks are immutable and identical network retries are idempotent', () => {
  const { match } = fixture();
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  assert.throws(() => lockAnswer(match, 'alice', 'q0', 1, 2000));
  assert.equal(Object.keys(match.answers.alice).length, 1);
});

test('rejects outsiders, foreign questions, string and out-of-range options', () => {
  const { match } = fixture();
  for (const args of [['eve', 'q0', 0], ['alice', 'other', 0], ['alice', 'q0', '0'], ['alice', 'q0', -1], ['alice', 'q0', 4]]) {
    assert.throws(() => lockAnswer(match, ...args, 2000));
  }
});

test('deadline and early finish both prevent new answers', () => {
  const { match } = fixture();
  assert.throws(() => lockAnswer(match, 'alice', 'q0', 0, match.expiresAt));
  match.finished.alice = true;
  assert.throws(() => lockAnswer(match, 'alice', 'q0', 0, 2000));
});

test('waits for actual opponent then updates both ratings exactly once', () => {
  const { match, users } = fixture();
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  lockAnswer(match, 'bob', 'q0', 1, 2000);
  match.finished.alice = true;
  assert.equal(settleMatch(match, users, 3000), false);
  assert.equal(matchProgress(match, 'alice', 3000).result, null);
  match.finished.bob = true;
  assert.equal(settleMatch(match, users, 4000), true);
  assert.equal(match.results.alice.verdict, 'win');
  assert.equal(match.results.bob.verdict, 'loss');
  assert.deepEqual(users.map(u => u.rating), [1496, 1464]);
  assert.equal(settleMatch(match, users, 5000), false);
  assert.equal(users[0].correctAnswers, 1);
  assert.equal(users[1].attemptedQuestions, 1);
});

test('disconnected opponent settles at the shared deadline', () => {
  const { match, users } = fixture();
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  assert.equal(settleMatch(match, users, match.expiresAt), true);
  assert.equal(match.results.bob.review.every(q => q.status === 'unanswered'), true);
});

test('forfeit overrides scores without fabricating opponent answers', () => {
  const { match, users } = fixture();
  lockAnswer(match, 'alice', 'q0', 0, 2000);
  match.forfeits.alice = true;
  settleMatch(match, users, 3000);
  assert.equal(match.results.alice.verdict, 'loss');
  assert.equal(match.results.bob.verdict, 'win');
  assert.equal(match.results.alice.opponentScore, 0);
});

test('match snapshot survives question-bank changes and serialization', () => {
  const { match, users } = fixture();
  const restored = JSON.parse(JSON.stringify(match));
  restored.finished.alice = restored.finished.bob = true;
  settleMatch(restored, users, 3000);
  assert.deepEqual(restored.results.alice.review.map(q => q.correctIndex), [0, 1, 2]);
  assert.notEqual(match.questions[0], questions[0]);
});

test('live progress never exposes answer keys, opponent answers or explanations', () => {
  const { match } = fixture();
  lockAnswer(match, 'bob', 'q0', 0, 2000);
  const progress = matchProgress(match, 'alice', 3000);
  assert.equal(progress.opponentAnswered, 1);
  assert.deepEqual(progress.answers, {});
  assert.doesNotMatch(JSON.stringify(progress), /answerIndex|explanation|correctIndex/);
});

test('bot score is server-owned and never changes the player rating', () => {
  const { match, users } = fixture('bot');
  match.botTimeline = [{ at: 2000, correct: true }, { at: 9000, correct: true }];
  match.finished.alice = true;
  settleMatch(match, users, 3000);
  assert.equal(match.results.alice.opponentScore, 1);
  assert.equal(match.results.alice.delta, 0);
  assert.equal(users[0].rating, 1480);
});
