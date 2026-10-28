import test from 'node:test';
import assert from 'node:assert/strict';
import { createPromotionsHandler, HOME_PROMOTION } from './promotions.mjs';
import { createStateStore } from './stateStore.mjs';

function fixture() {
  let clock = Date.parse('2026-10-28T10:00:00+05:30');
  const store = createStateStore({ initial: { users: [
    { id: 'alice', name: 'Alice', email: 'alice@example.com', contactNumber: '9876543210', medicalCollege: 'Example College', passwordHash: 'private' },
    { id: 'bob', name: 'Bob', email: 'bob@example.com' },
  ] }, persist: async () => {} });
  const handler = createPromotionsHandler({ readDatabase: () => store.read(), writeDatabase: data => store.write(data),
    getSessionUser: (request, data) => data.users.find(user => user.id === request.user),
    sendJson: (_, status, body, headers) => ({ status, body, headers }), now: () => clock });
  const call = (method = 'GET', user = 'alice', body = {}) => handler({ method, user, body }, {},
    new URL(`http://localhost/api/promotions/${method === 'GET' ? 'current' : `${HOME_PROMOTION.id}/register`}`));
  return { store, call, setTime: time => { clock = Date.parse(time); } };
}

test('promotion dates use IST and public status never exposes learner details', async () => {
  const f = fixture();
  const response = await f.call('GET', 'visitor');
  assert.equal(response.status, 200);
  assert.equal(response.body.promotion.startsAt, '2026-11-15T14:00:00+05:30');
  assert.equal(response.body.promotion.title, 'NEET-PG Grand Test');
  assert.equal(response.body.promotion.id, 'neet-pg-grand-test-2026-11-15');
  assert.equal(response.body.registrationOpen, true);
  assert.equal(response.body.registered, false);
  assert.equal(response.headers['Cache-Control'], 'private, no-store');
  assert.doesNotMatch(JSON.stringify(response.body), /alice@example|passwordHash|9876543210/);
  await assert.rejects(f.call('POST', 'visitor'), error => error.status === 401);
  assert.equal(f.store.read().promotionRegistrations, undefined);
});

test('registration saves authenticated account details, survives handler recreation, and rejects impersonation', async () => {
  const f = fixture();
  const result = await f.call('POST', 'alice', { userId: 'bob', email: 'fake@example.com' });
  assert.equal(result.status, 201);
  assert.equal(result.body.message, 'Thank you for registration!');
  const saved = f.store.read().promotionRegistrations[0];
  assert.equal(saved.userId, 'alice');
  assert.equal(saved.email, 'alice@example.com');
  assert.equal(saved.contactNumber, '9876543210');
  assert.equal(saved.medicalCollege, 'Example College');
  assert.equal(saved.passwordHash, undefined);
  assert.equal((await f.call()).body.registered, true);
  assert.equal((await f.call('GET', 'bob')).body.registered, false);
  const restored = createStateStore({ initial: f.store.read(), persist: async () => {} });
  const handler = createPromotionsHandler({ readDatabase: () => restored.read(), writeDatabase: d => restored.write(d),
    getSessionUser: (_, d) => d.users[0], sendJson: (_, status, body) => ({ status, body }) });
  assert.equal((await handler({ method: 'GET' }, {}, new URL('http://localhost/api/promotions/current'))).body.registered, true);
});

test('double clicks, concurrent requests and retries create only one record per account and event', async () => {
  const f = fixture();
  const responses = await Promise.all([f.call('POST'), f.call('POST'), f.call('POST', 'bob')]);
  assert.deepEqual(responses.map(r => r.status).sort(), [200, 201, 201]);
  assert.equal(f.store.read().promotionRegistrations.length, 2);
  assert.equal((await f.call('POST')).body.alreadyRegistered, true);
  assert.equal(f.store.read().promotionRegistrations.length, 2);
});

test('previous FMGE registrations are preserved and do not register users for the new NEET-PG event', async () => {
  const f = fixture();
  const database = f.store.read();
  const previous = { promotionId: 'fmge-grand-test-2026-10-27', userId: 'alice', eventTitle: 'FMGE Grand Test', registeredAt: '2026-10-26T10:00:00+05:30' };
  database.promotionRegistrations = [previous];
  await f.store.write(database);
  assert.equal((await f.call()).body.registered, false);
  assert.equal((await f.call('POST')).status, 201);
  const saved = f.store.read().promotionRegistrations;
  assert.equal(saved.length, 2);
  assert.deepEqual(saved[0], previous);
  assert.equal(saved[1].promotionId, HOME_PROMOTION.id);
});

test('registration closes at the scheduled start, while existing confirmation is retained', async () => {
  const f = fixture();
  await f.call('POST');
  f.setTime(HOME_PROMOTION.startsAt);
  assert.equal((await f.call()).body.registrationOpen, false);
  assert.equal((await f.call('POST')).body.registered, true);
  await assert.rejects(f.call('POST', 'bob'), error => error.status === 409);
  assert.equal(f.store.read().promotionRegistrations.length, 1);
});

test('a failed database write never returns a successful confirmation', async () => {
  const handler = createPromotionsHandler({ readDatabase: () => ({ users: [{ id: 'alice' }] }),
    writeDatabase: async () => { throw new Error('Database unavailable'); },
    getSessionUser: (_, d) => d.users[0], sendJson: () => assert.fail('Must not confirm a failed write'),
    now: () => Date.parse('2026-10-26T10:00:00+05:30') });
  await assert.rejects(handler({ method: 'POST' }, {}, new URL(`http://localhost/api/promotions/${HOME_PROMOTION.id}/register`)), /Database unavailable/);
});
