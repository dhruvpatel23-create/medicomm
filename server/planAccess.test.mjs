import test from 'node:test';
import assert from 'node:assert/strict';
import { canAccessFeature, canOpenFeature, filterLibraryByPlan, practiceFeature } from '../src/data/planAccess.js';
import { requireFeature, routeFeature, isTrialPracticeRoute } from './planAccess.mjs';

test('plan access matches pricing, including free and expired memberships', () => {
  const features = ['practice', 'community', 'inbox', 'theory', 'usmle', 'tests'];
  for (const [plan, expected] of [
    ['free', [false, false, false, false, false, false]],
    ['lite', [true, true, true, false, false, false]],
    ['ultra', [true, true, true, true, false, false]],
    ['premium', [true, true, true, true, true, true]],
  ]) {
    const membership = { plan, hasPracticeAccess: plan !== 'free' };
    assert.deepEqual(features.map(feature => canAccessFeature(membership, feature)), expected, plan);
    assert.ok(features.every(feature => !canAccessFeature({ ...membership, subscriptionStatus: 'expired' }, feature)));
  }
  assert.equal(canAccessFeature(null, 'practice'), false);
  assert.equal(canAccessFeature({ hasPracticeAccess: true }, 'practice'), true);
  assert.equal(canAccessFeature({ hasPracticeAccess: true }, 'usmle'), false);
});

test('server rejects restricted features and allows subscribed features', () => {
  const database = { users: [{ id: 'lite', plan: 'lite' }, { id: 'ultra', plan: 'ultra' }, { id: 'premium', plan: 'premium' }, { id: 'free' }], paymentOrders: [] };
  assert.throws(() => requireFeature(database, 'free', 'inbox'), { status: 403 });
  assert.throws(() => requireFeature(database, 'lite', 'theory'), { status: 403 });
  assert.throws(() => requireFeature(database, 'ultra', 'tests'), { status: 403 });
  assert.doesNotThrow(() => requireFeature(database, 'ultra', 'theory'));
  assert.doesNotThrow(() => requireFeature(database, 'premium', 'tests'));
});

test('API and static paths require the correct package; directories remain browsable', () => {
  for (const path of ['/api/viva/sessions', '/api/clinical-cases/sessions', '/api/short-notes/reviews', '/short-notes.json']) assert.equal(routeFeature(path, 'GET'), 'theory');
  assert.equal(routeFeature('/api/practice/fmge-tests/attempts/123', 'PATCH'), null);
  assert.equal(routeFeature('/api/practice/neetpg-tests/attempts/123', 'PATCH'), 'tests');
  assert.equal(routeFeature('/practice-question-bank.json', 'GET'), 'usmle');
  assert.equal(routeFeature('/api/practice', 'GET', new URLSearchParams('source=usmle')), null);
  assert.equal(routeFeature('/api/communities', 'GET'), null);
  assert.equal(routeFeature('/api/communities/room/messages', 'POST'), 'community');
  assert.equal(routeFeature('/api/direct-messages/open', 'POST'), 'inbox');
  assert.equal(practiceFeature('fmge'), 'fullPractice');
  assert.equal(practiceFeature('fmge-tests'), 'fmgeTests');
});

test('lower packages cannot receive USMLE content through the shared library or cache', () => {
  const library = { subjects: [{ id: 'neet' }], fmgeSessions: [{ id: 'fmge' }], aiSubjects: [{ id: 'topic' }], usmleSubjects: [{ questions: ['restricted'] }], usmleModules: [{ questions: ['restricted'] }] };
  for (const plan of ['lite', 'ultra']) {
    const result = filterLibraryByPlan(library, { hasPracticeAccess: true, plan });
    assert.ok(result.usmleSubjects.every(subject => subject.questions.every(q => q.locked)));
    assert.ok(result.usmleModules.every(module => module.locked && module.questions.every(q => q.locked)));
    assert.deepEqual(result.subjects, library.subjects);
    assert.deepEqual(result.fmgeSessions, library.fmgeSessions);
    assert.deepEqual(result.aiSubjects, library.aiSubjects);
  }
  assert.equal(filterLibraryByPlan(library, { hasPracticeAccess: true, plan: 'premium' }), library);
  assert.equal(library.usmleModules.length, 1);
});

test('trial access opens practice directories without granting paid features', () => {
  assert.equal(isTrialPracticeRoute('/api/practice', 'GET'), true);
  assert.equal(isTrialPracticeRoute('/api/practice/attempts', 'POST'), true);
  for (const path of ['/practice-question-bank.json', '/topic-wise-question-bank.json', '/api/generate-question', '/api/practice/fmge-tests']) {
    assert.equal(isTrialPracticeRoute(path, 'GET'), false);
    assert.equal(isTrialPracticeRoute(path, 'POST'), false);
  }
  const free = { plan: 'free', hasPracticeAccess: false };
  assert.equal(canOpenFeature(free, 'practice'), true);
  assert.equal(canOpenFeature(free, 'usmle'), true);
  assert.equal(canOpenFeature(free, 'fmgeTests'), true);
  assert.equal(canOpenFeature({ ...free, subscriptionStatus: 'expired' }, 'fmgeTests'), true);
  for (const feature of ['theory', 'tests', 'community', 'inbox', 'fullPractice']) {
    assert.equal(canOpenFeature(free, feature), false);
  }
  assert.equal(canOpenFeature(null, 'practice'), false);
});

test('free and expired libraries only expose the requested trial; cache filtering is idempotent', () => {
  const question = (id, examId, year = 2020) => ({ id, examId, year, source: 'official' });
  const library = {
    years: [{ id: 'first-year', subjectIds: ['anatomy'] }, { id: 'second-year', subjectIds: ['pathology'] }],
    subjects: ['anatomy', 'pathology', 'ent'].map(id => ({ id, questions: [
      question('trial', 'neet-pg-2020'), question('other-year', 'neet-pg-2021', 2021),
      question('other-exam', 'aiims-2020'), question('inicet', 'ini-cet-2020'),
    ] })),
    aiSubjects: ['anatomy', 'ent', 'general-medicine'].map(id => ({ id, questions: [
      { id: 'later', chapterTitle: 'Later chapter', chapterOrder: 2 },
      { id: 'first-a', chapterTitle: 'First chapter', chapterOrder: 1, topic: 'One' },
      { id: 'first-b', chapterTitle: 'First chapter', chapterOrder: 1, topic: 'Two' },
    ] })),
    usmleSubjects: [{ questions: [question('restricted-subject')] }],
    usmleModules: [2, 1, 3].map(moduleNumber => ({ moduleNumber, questions: [question(`module-${moduleNumber}`)] })),
    fmgeSessions: [{ questions: [question('restricted-fmge')] }],
    questions: [question('unfiltered-flat-list')],
  };
  const before = structuredClone(library);
  for (const membership of [
    { hasPracticeAccess: false, plan: 'free' },
    { hasPracticeAccess: true, plan: 'premium', subscriptionStatus: 'expired' },
  ]) {
    const trial = filterLibraryByPlan(library, membership);
    assert.deepEqual(trial.subjects.map(s => s.questions.filter(q => !q.locked).map(q => q.id)), [['trial'], ['trial'], []]);
    assert.ok(trial.aiSubjects.every(s => s.questions.filter(q => !q.locked).map(q => q.id).join(',') === 'first-a,first-b'));
    assert.deepEqual(trial.usmleModules.flatMap(m => m.questions.filter(q => !q.locked).map(q => q.id)), ['module-1']);
    assert.ok(trial.usmleSubjects.every(s => s.questions.every(q => q.locked)));
    assert.ok(trial.fmgeSessions.every(s => s.questions.every(q => q.locked)));
    assert.deepEqual(trial.questions, []);
    assert.deepEqual(filterLibraryByPlan(trial, membership), trial);
  }
  for (const plan of ['lite', 'ultra']) {
    const filtered = filterLibraryByPlan(library, { plan, hasPracticeAccess: true });
    assert.equal(filtered.subjects, library.subjects);
    assert.deepEqual(filtered.usmleModules.flatMap(m => m.questions.filter(q => !q.locked).map(q => q.id)), ['module-1']);
  }
  assert.deepEqual(library, before);
});
