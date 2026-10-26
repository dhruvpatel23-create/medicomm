import test from 'node:test';
import assert from 'node:assert/strict';
import { validateSupabaseState, createStateStore } from './stateStore.mjs';

const validate = rows => validateSupabaseState(rows, 'app_state', 'medicomm');

test('startup distinguishes missing state, migration, and invalid revision', () => {
  assert.throws(() => validate([]), /No readable database row.*SUPABASE_STATE_KEY/);
  assert.throws(() => validate([{ data: {} }]), /Missing revision column/);
  for (const revision of [null, '0', -1, 0.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => validate([{ data: {}, revision }]), /Invalid revision/);
  }
});

test('invalid responses and data cannot silently become empty user databases', () => {
  assert.throws(() => validate({}), /Invalid Supabase response/);
  for (const data of [null, [], 'invalid']) {
    assert.throws(() => validate([{ data, revision: 0 }]), /Invalid database data/);
  }
  assert.throws(() => validate([{ data: {}, revision: 0 }, { data: {}, revision: 1 }]), /Expected one database row/);
});

test('valid state retains existing data and revision', () => {
  const row = { data: { users: [{ id: 'existing-user' }] }, revision: 4 };
  assert.equal(validate([row]), row);
});

test('test access snapshots isolate the session owner and cannot mutate stored accounts', () => {
  const store = createStateStore({ initial: {
    users: [{ id: 'alice', plan: 'premium' }, { id: 'bob' }],
    sessions: { aliceKey: { userId: 'alice', expiresAt: 9999999999999 }, bobKey: { userId: 'bob' } },
    paymentOrders: [{ userId: 'alice', orderId: 'own' }, { userId: 'bob', orderId: 'other' }],
    questions: [{ private: 'large question bank' }], fmgeTestAttempts: [{ private: 'other attempts' }],
  }, persist: async () => {} });
  const access = store.accessSnapshot('aliceKey');
  assert.deepEqual(access.users.map(user => user.id), ['alice']);
  assert.deepEqual(Object.keys(access.sessions), ['aliceKey']);
  assert.deepEqual(access.paymentOrders.map(order => order.orderId), ['own']);
  assert.equal(access.questions, undefined);
  assert.equal(access.fmgeTestAttempts, undefined);
  access.users[0].plan = 'changed';
  assert.equal(store.accessSnapshot('aliceKey').users[0].plan, 'premium');
  assert.deepEqual(store.accessSnapshot(null), { users: [], sessions: {}, paymentOrders: [] });
});
