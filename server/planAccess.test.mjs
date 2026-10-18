import test from 'node:test';
import assert from 'node:assert/strict';
import { canAccessFeature, filterLibraryByPlan, practiceFeature } from '../src/data/planAccess.js';
import { requireFeature, routeFeature } from './planAccess.mjs';

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
  assert.equal(routeFeature('/api/practice/fmge-tests/attempts/123', 'PATCH'), 'tests');
  assert.equal(routeFeature('/practice-question-bank.json', 'GET'), 'usmle');
  assert.equal(routeFeature('/api/practice', 'GET', new URLSearchParams('source=usmle')), 'usmle');
  assert.equal(routeFeature('/api/communities', 'GET'), null);
  assert.equal(routeFeature('/api/communities/room/messages', 'POST'), 'community');
  assert.equal(routeFeature('/api/direct-messages/open', 'POST'), 'inbox');
  assert.equal(practiceFeature('fmge'), 'practice');
  assert.equal(practiceFeature('fmge-tests'), 'tests');
});

test('lower packages cannot receive USMLE content through the shared library or cache', () => {
  const library = { subjects: [{ id: 'neet' }], fmgeSessions: [{ id: 'fmge' }], aiSubjects: [{ id: 'topic' }], usmleSubjects: [{ questions: ['restricted'] }], usmleModules: [{ questions: ['restricted'] }] };
  for (const plan of ['lite', 'ultra']) {
    const result = filterLibraryByPlan(library, { hasPracticeAccess: true, plan });
    assert.deepEqual(result.usmleSubjects, []);
    assert.deepEqual(result.usmleModules, []);
    assert.deepEqual(result.subjects, library.subjects);
    assert.deepEqual(result.fmgeSessions, library.fmgeSessions);
    assert.deepEqual(result.aiSubjects, library.aiSubjects);
  }
  assert.equal(filterLibraryByPlan(library, { hasPracticeAccess: true, plan: 'premium' }), library);
  assert.equal(library.usmleModules.length, 1);
});
