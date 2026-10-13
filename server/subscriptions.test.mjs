import test from 'node:test';
import assert from 'node:assert/strict';
import { annualExpiry, reconcileSubscriptions, subscriptionDetails } from './subscriptions.mjs';

test('annual term follows the Indian calendar, including leap-day evening purchases', () => {
  assert.equal(annualExpiry('2026-10-13T12:15:00Z'), '2027-10-13T12:15:00.000Z');
  assert.equal(annualExpiry('2024-02-28T22:00:00Z'), '2025-02-27T22:00:00.000Z');
  assert.equal(annualExpiry('2024-02-29T12:00:00Z'), '2025-02-28T12:00:00.000Z');
});

test('backfill is permanent and access survives missing flags but ends at the anniversary', () => {
  const database = { users: [{ id: 'u', hasPracticeAccess: true }], paymentOrders: [
    { userId: 'u', orderId: 'order_1', paymentId: 'pay_1', planId: 'lite', status: 'paid', verifiedAt: '2026-10-13T12:00:00Z' },
  ] };
  assert.equal(reconcileSubscriptions(database), true);
  assert.equal(reconcileSubscriptions(database), false);
  assert.equal(database.users[0].subscriptionExpiresAt, '2027-10-13T12:00:00.000Z');
  database.users[0].hasPracticeAccess = false;
  assert.equal(subscriptionDetails(database, 'u', Date.parse('2027-10-13T11:59:59Z')).hasPracticeAccess, true);
  database.users[0].hasPracticeAccess = true;
  assert.equal(subscriptionDetails(database, 'u', Date.parse('2027-10-13T12:00:00Z')).hasPracticeAccess, false);
  database.paymentOrders = [];
  assert.equal(subscriptionDetails(database, 'u', Date.parse('2027-01-01T00:00:00Z')).hasPracticeAccess, true);
});

test('undated legacy access is preserved and pending orders do not grant membership', () => {
  const db = { users: [{ id: 'legacy', plan: 'ultra' }, { id: 'free' }], paymentOrders: [
    { userId: 'free', orderId: 'pending', status: 'authorized', paymentId: 'p', verifiedAt: '2026-10-13T00:00:00Z' },
  ] };
  assert.equal(reconcileSubscriptions(db), false);
  assert.equal(subscriptionDetails(db, 'legacy').subscriptionStatus, 'purchase_date_required');
  assert.equal(subscriptionDetails(db, 'legacy').hasPracticeAccess, true);
  assert.equal(subscriptionDetails(db, 'free').hasPracticeAccess, false);
});
