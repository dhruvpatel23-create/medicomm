import test from 'node:test';
import assert from 'node:assert/strict';
import { dashboardData, recordPracticeAttempt, validateStudyGoal } from './dashboard.mjs';

const now = Date.parse('2026-10-08T03:00:00Z');
const learner = () => ({ id: 'one', name: 'Learner', medicalCollege: 'Kerala', rating: 1500, attemptedQuestions: 0, correctAnswers: 0 });
const subject = { id: 'anatomy', title: 'Anatomy' };
const question = { id: 'q1', options: ['A', 'B'], answer: 'A', topic: 'Neck', year: 2024 };
const payload = { id: 'attempt-0001', mode: 'pyq', selectedAnswer: 'A', durationSeconds: 70 };

test('verified attempts are idempotent and retain prior totals', () => {
  const user = { ...learner(), attemptedQuestions: 41, correctAnswers: 18 };
  const db = { users: [user], practiceResults: [] };
  recordPracticeAttempt(db, user.id, { ...payload, correct: false }, subject, question, now);
  recordPracticeAttempt(db, user.id, payload, subject, question, now);
  assert.equal(user.attemptedQuestions, 42); assert.equal(user.correctAnswers, 19);
  assert.equal(db.practiceResults.length, 1); assert.equal(db.practiceResults[0].correct, true);
  assert.throws(() => recordPracticeAttempt(db, user.id, { ...payload, id: 'attempt-0002', selectedAnswer: 'not an option' }, subject, question, now));
});

test('overview uses India dates, actual streaks, owned records and completed battles', () => {
  const user = learner(), db = { users: [user, { ...learner(), id: 'two', rating: 1700 }], practiceResults: [], duels: [] };
  recordPracticeAttempt(db, 'one', payload, subject, question, now - 86400000);
  recordPracticeAttempt(db, 'one', { ...payload, id: 'attempt-0002', selectedAnswer: 'B' }, subject, question, now);
  recordPracticeAttempt(db, 'two', { ...payload, id: 'attempt-0003' }, subject, question, now);
  db.duels.push({ results: { one: { duelId: 'battle', mode: 'rated', completedAt: new Date(now).toISOString(), verdict: 'win', delta: 12, userScore: 1, opponentScore: 0, review: [{ selectedIndex: 0, status: 'correct' }] } } });
  const result = dashboardData(db, user, value => value, now);
  assert.equal(result.stats.streak, 2); assert.equal(result.stats.nationalRank, 2); assert.equal(result.stats.stateRank, 2);
  assert.equal(result.today.attempts, 2); assert.equal(result.today.seconds, 70);
  assert.equal(result.recent.length, 2); assert.equal(result.battles[0].ratingChange, 12);
  assert.equal(result.recommendations[0].accuracy, 50); assert.equal(result.activity.length, 56);
  assert.equal(dashboardData(db, user, value => value, now + 3 * 86400000).stats.streak, 0);
});

test('empty accounts have no made-up activity or accuracy; goals validate dates', () => {
  const user = learner(), data = dashboardData({ users: [user] }, user, value => value, now);
  assert.equal(data.stats.streak, 0); assert.equal(data.stats.accuracy, null); assert.equal(data.resume, null);
  assert(data.activity.every(day => day.attempts === 0)); assert.equal(data.goal, null);
  assert.deepEqual(validateStudyGoal({ exam: 'My exam', date: '2027-03-01', weeklyTarget: '150' }), { exam: 'My exam', date: '2027-03-01', weeklyTarget: 150 });
  for (const date of ['2027-02-30', 'invalid']) assert.throws(() => validateStudyGoal({ exam: 'Test', date, weeklyTarget: 150 }));
});
