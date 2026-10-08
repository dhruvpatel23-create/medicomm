import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { createPaymentHandler, hasPracticeAccess, paymentQuote } from './payments.mjs';

function fixture() {
  let database = { users: [{ id: 'one' }, { id: 'two' }], paymentOrders: [] };
  let account = 'one';
  let failure;
  let paymentStatus = 'captured';
  let paymentAmount = 49900;
  let creates = 0;
  const keySecret = 'isolated-test-secret';
  const handler = createPaymentHandler({
    keyId: 'rzp_test_fixture', keySecret,
    readDatabase: () => structuredClone(database), writeDatabase: async value => { database = structuredClone(value); },
    requireSessionUser: () => { if (!account) { const error = new Error('Sign in'); error.status = 401; throw error; } return { id: account }; },
    parseRequestBody: async request => request.body,
    sendJson: (response, status, body) => ({ status, body }),
    client: { orders: { create: async input => { if (failure) throw failure; creates++; assert(input.receipt.length <= 40); return { ...input, id: 'order_test123' }; } },
      payments: { fetch: async () => { if (failure) throw failure; return { order_id: 'order_test123', amount: paymentAmount, currency: 'INR', status: paymentStatus }; } } },
  });
  return {
    call: (route, body) => handler({ body }, {}, { pathname: route }),
    signed: (signature) => ({ razorpay_order_id: 'order_test123', razorpay_payment_id: 'pay_test123', razorpay_signature: signature ?? createHmac('sha256', keySecret).update('order_test123|pay_test123').digest('hex') }),
    state: () => database, creates: () => creates,
    account: value => account = value, failure: value => failure = value,
    status: value => paymentStatus = value, amount: value => paymentAmount = value,
  };
}
const order = { planId: 'lite', amount: 49900, currency: 'INR' };
const rejects = (promise, status) => assert.rejects(promise, error => error.status === status);

test('orders validate server prices, minimum, authentication and provider errors', async () => {
  const f = fixture();
  for (const amount of [99, 100.5, '49900', 100, -1]) await rejects(f.call('/api/create-order', { ...order, amount }), 400);
  await rejects(f.call('/api/create-order', { ...order, currency: 'USD' }), 400);
  assert.equal(f.creates(), 0);
  f.account(null); await rejects(f.call('/api/create-order', order), 401); f.account('one');
  f.failure({ statusCode: 401 }); await rejects(f.call('/api/create-order', order), 401);
  f.failure({ statusCode: 500, secret: 'must-not-leak' }); await rejects(f.call('/api/create-order', order), 500);
  f.failure(null);
  const result = await f.call('/api/create-order', order);
  assert.equal(result.body.order_id, 'order_test123'); assert.equal(result.body.amount, 49900);
  assert.equal(result.body.key_id, 'rzp_test_fixture'); assert.equal(result.body.test_mode, true);
  assert.equal(JSON.stringify(result).includes('isolated-test-secret'), false);
  assert.equal(f.state().paymentOrders[0].status, 'created');
});

test('verification rejects missing, forged, foreign and mismatched payments without marking paid', async () => {
  const f = fixture(); await f.call('/api/create-order', order);
  await rejects(f.call('/api/verify-payment', {}), 400);
  for (const signature of ['bad', '0'.repeat(64), 'g'.repeat(64)]) await rejects(f.call('/api/verify-payment', f.signed(signature)), 400);
  f.account('two'); await rejects(f.call('/api/verify-payment', f.signed()), 400); f.account('one');
  f.amount(100); await rejects(f.call('/api/verify-payment', f.signed()), 400); f.amount(49900);
  f.status('failed'); await rejects(f.call('/api/verify-payment', f.signed()), 400);
  assert.equal(f.state().paymentOrders[0].status, 'created');
});

test('authorized remains pending, captured is paid, repeated verification is safe', async () => {
  const f = fixture(); await f.call('/api/create-order', order);
  f.status('authorized');
  assert.equal((await f.call('/api/verify-payment', f.signed())).body.paid, false);
  assert.equal(f.state().paymentOrders[0].status, 'authorized');
  assert.equal(hasPracticeAccess(f.state(), 'one'), false);
  f.status('captured');
  assert.equal((await f.call('/api/verify-payment', f.signed())).body.paid, true);
  assert.equal((await f.call('/api/verify-payment', f.signed())).body.paid, true);
  assert.equal(f.state().paymentOrders.length, 1);
  assert.equal(f.state().paymentOrders[0].paymentId, 'pay_test123');
  assert.equal(hasPracticeAccess(f.state(), 'one'), true);
  assert.equal(hasPracticeAccess(f.state(), 'two'), false);
});

test('PRELAUNCH charges exactly 900 paise and cannot be forged by changing the amount', async () => {
  for (const planId of ['lite', 'ultra', 'premium']) assert.equal(paymentQuote({ planId, coupon: ' prelaunch ' }).amount, 900);
  const f = fixture();
  await rejects(f.call('/api/create-order', { ...order, amount: 900 }), 400);
  await rejects(f.call('/api/create-order', { ...order, amount: 900, coupon: 'FAKE' }), 400);
  await rejects(f.call('/api/create-order', { ...order, amount: 100, coupon: 'PRELAUNCH' }), 400);
  const created = await f.call('/api/create-order', { ...order, amount: 900, coupon: 'PRELAUNCH' });
  assert.equal(created.body.amount, 900);
  assert.equal(f.state().paymentOrders[0].coupon, 'PRELAUNCH');
  assert.equal(hasPracticeAccess(f.state(), 'one'), false);
  f.amount(900);
  const verified = await f.call('/api/verify-payment', f.signed());
  assert.equal(verified.body.hasPracticeAccess, true);
});
