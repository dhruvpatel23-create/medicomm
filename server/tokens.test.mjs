import test from 'node:test';
import assert from 'node:assert/strict';
import { tokenStatus, chargeTokens, refundTokens, TOKEN_WINDOW_MS, updateTokenState } from './tokens.mjs';
import { createStateStore } from './stateStore.mjs';

const database = plan => ({ users: [{ id: 'u', plan }], paymentOrders: [] });
test('plan allowances and expired subscriptions', () => {
  for (const [plan, count] of [[null, 20], ['lite', 100], ['ultra', 200], ['premium', 300]]) {
    assert.equal(tokenStatus(database(plan), 'u').remaining, count);
  }
  const db = database('premium');
  Object.assign(db.users[0], { subscriptionPurchasedAt: '2020-01-01', subscriptionOrderId: 'old' });
  assert.equal(tokenStatus(db, 'u').remaining, 20);
});
test('window begins on first use; exact 24-hour reset; no rollover', () => {
  const db = database();
  assert.equal(tokenStatus(db, 'u', 100).resetsAt, null);
  chargeTokens(db, 'u', 5, 'battle:a', 1000);
  chargeTokens(db, 'u', 10, 'review:b', 2000);
  assert.equal(tokenStatus(db, 'u', TOKEN_WINDOW_MS + 999).remaining, 5);
  assert.deepEqual(tokenStatus(db, 'u', TOKEN_WINDOW_MS + 1000), { allowance: 20, remaining: 20, resetsAt: null });
  chargeTokens(db, 'u', 10, 'review:c', TOKEN_WINDOW_MS + 2000);
  assert.equal(db.users[0].tokens.startedAt, TOKEN_WINDOW_MS + 2000);
});
test('duplicate charges and refunds are idempotent; insufficient balance rejected', () => {
  const db = database();
  chargeTokens(db, 'u', 10, 'review:a');
  chargeTokens(db, 'u', 10, 'review:a');
  assert.equal(tokenStatus(db, 'u').remaining, 10);
  assert.throws(() => chargeTokens(db, 'u', 30, 'clinical:b'), error => error.status === 402);
  refundTokens(db, 'u', 'review:a'); refundTokens(db, 'u', 'review:a');
  assert.equal(tokenStatus(db, 'u').remaining, 20);
});
test('concurrent spends cannot overdraw balance', async () => {
  const store = createStateStore({ initial: database(), persist: async () => {} });
  const results = await Promise.allSettled([1, 2, 3].map(id => updateTokenState(store.read, store.write, db => chargeTokens(db, 'u', 10, `review:${id}`))));
  assert.equal(results.filter(result => result.status === 'fulfilled').length, 2);
  assert.equal(tokenStatus(store.read(), 'u').remaining, 0);
});
test('a battle charges both players atomically and retries do not charge again', async () => {
  const initial = { users: [{ id: 'u' }, { id: 'v' }] };
  const store = createStateStore({ initial, persist: async () => {} });
  const match = db => {
    chargeTokens(db, 'u', 5, 'battle:one');
    chargeTokens(db, 'v', 5, 'battle:one');
  };
  await updateTokenState(store.read, store.write, match);
  await updateTokenState(store.read, store.write, match);
  assert.equal(tokenStatus(store.read(), 'u').remaining, 15);
  assert.equal(tokenStatus(store.read(), 'v').remaining, 15);
  await updateTokenState(store.read, store.write, db => chargeTokens(db, 'v', 15, 'other'));
  await assert.rejects(updateTokenState(store.read, store.write, db => {
    chargeTokens(db, 'u', 5, 'battle:two');
    chargeTokens(db, 'v', 5, 'battle:two');
  }), error => error.status === 402);
  assert.equal(tokenStatus(store.read(), 'u').remaining, 15);
});
