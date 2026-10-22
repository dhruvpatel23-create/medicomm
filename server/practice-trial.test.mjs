import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { filterLibraryByPlan } from '../src/data/planAccess.js';
import { subscriptionDetails } from './subscriptions.mjs';
import { practiceProgressData, recordPracticeAttempt } from './dashboard.mjs';

const readJson = path => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8').replace(/^\uFEFF/, ''));
const bank = readJson('../data/practice-question-bank.json');
const library = {
  ...bank,
  subjects: bank.subjects.map(s => ({ ...s, questions: s.questions.filter(q => !q.source || q.source === 'official') })),
  aiSubjects: bank.subjects.map(s => ({ ...s, questions: s.questions.filter(q => q.source === 'ai') })),
  usmleModules: readJson('../data/usmle-module-bank.json').modules,
};
const free = { plan: 'free', hasPracticeAccess: false };

test('real bank supplies all six NEET 2020 subjects, each populated first chapter, and module one', () => {
  const trial = filterLibraryByPlan(library, free);
  for (const key of ['subjects', 'aiSubjects', 'usmleModules']) {
    assert.deepEqual(trial[key].map(s => s.questions.length), library[key].map(s => s.questions.length), `${key} catalog counts preserved`);
    for (const question of trial[key].flatMap(s => s.questions).filter(q => q.locked)) {
      for (const privateField of ['prompt', 'options', 'answer', 'answerIndex', 'explanation', 'imageUrls']) {
        assert.equal(question[privateField], undefined, `${question.id}: ${privateField} must stay private`);
      }
    }
  }
  assert.deepEqual(trial.subjects.filter(s => s.questions.some(q => !q.locked)).map(s => s.id).sort(),
    ['anatomy', 'biochemistry', 'microbiology', 'pathology', 'pharmacology', 'physiology']);
  for (const subject of trial.subjects) {
    assert.ok(subject.questions.filter(q => !q.locked).every(q => Number(q.year) === 2020 && q.examId === 'neet-pg-2020'));
  }
  for (const subject of library.aiSubjects.filter(s => s.questions.length)) {
    const questions = trial.aiSubjects.find(s => s.id === subject.id).questions.filter(q => !q.locked);
    assert.ok(questions.length > 0, subject.id);
    assert.equal(new Set(questions.map(q => q.chapterTitle)).size, 1, subject.id);
    assert.equal(Number(questions[0].chapterOrder), Math.min(...subject.questions.map(q => Number(q.chapterOrder))), subject.id);
  }
  assert.ok(trial.usmleModules.find(m => m.moduleNumber === 1).questions.length > 0);
  assert.ok(trial.usmleModules.filter(m => m.moduleNumber !== 1).every(m => m.questions.every(q => q.locked)));
  console.log('Trial PYQs:', trial.subjects.filter(s => s.questions.some(q => !q.locked)).map(s => `${s.id}: ${s.questions.filter(q => !q.locked).length}`).join(', '));
  console.log('Trial topic-wise questions:', trial.aiSubjects.reduce((sum, s) => sum + s.questions.filter(q => !q.locked).length, 0));
});

test('actual attempt handler saves free trial answers and rejects questions outside the trial', async () => {
  let database = { users: [{ id: 'trial-user' }], paymentOrders: [] };
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const handler = source.slice(source.indexOf('async function handleDashboard('), source.indexOf('async function handleQuestionBookmarkUpdate('));
  const dependencies = {
    readDatabase: () => structuredClone(database),
    requireSessionUser: (request, response, db) => db.users[0],
    parseRequestBody: async request => request.body,
    buildPracticeLibrary: () => library, readPracticeQuestionBank: () => library,
    filterLibraryByPlan, subscriptionDetails, recordPracticeAttempt, practiceProgressData,
    writeDatabase: async next => { database = next; },
    sanitizeUser: user => user,
    sendJson: (response, status, body) => ({ status, body }),
  };
  const handle = new Function(...Object.keys(dependencies), `${handler}; return handleDashboard;`)(...Object.values(dependencies));
  const trial = filterLibraryByPlan(library, free);
  for (const [mode, sets] of [['pyq', trial.subjects], ['ai', trial.aiSubjects], ['usmle', trial.usmleModules]]) {
    const subject = sets.find(s => s.questions.some(q => !q.locked));
    const question = subject.questions.find(q => !q.locked);
    const result = await handle({ method: 'POST', body: {
      id: `trial-attempt-${mode}`, mode, subjectId: subject.id, questionId: question.id,
      selectedAnswer: question.answer,
    } }, {}, new URL('http://localhost/api/practice/attempts'));
    assert.equal(result.status, 200, mode);
    assert.equal(result.body.attempt.correct, true, mode);
  }
  const subject = library.subjects.find(s => s.id === 'anatomy');
  const question = subject.questions.find(q => q.year !== 2020);
  const rejected = await handle({ method: 'POST', body: {
    id: 'restricted-attempt', mode: 'pyq', subjectId: subject.id, questionId: question.id,
    selectedAnswer: question.answer,
  } }, {}, new URL('http://localhost/api/practice/attempts'));
  assert.equal(rejected.status, 400);
  assert.equal(database.practiceResults.length, 3);
  const progress = await handle({ method: 'GET' }, {}, new URL('http://localhost/api/practice/progress'));
  assert.equal(progress.status, 200);
  assert.equal(Object.keys(progress.body.progress).length, 3);
  assert.ok(Object.values(progress.body.progress).every(item => item.firstAttemptCorrect));
});
