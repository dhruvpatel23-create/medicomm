import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { Readable } from 'node:stream';
import { createPaymentHandler, hasPracticeAccess, paymentQuote } from './payments.mjs';

function fixture() {
  let database = { users: [{ id: 'one' }, { id: 'two' }], paymentOrders: [] };
  let account = 'one';
  let failure;
  let paymentStatus = 'captured';
  let paymentAmount = 79900;
  let creates = 0;
  let gatewayOrder;
  let queued = 0;
  const keySecret = 'isolated-test-secret';
  const handler = createPaymentHandler({
    keyId: 'rzp_test_fixture', keySecret,
    webhookSecret: 'test-webhook-secret',
    enqueueThankYou: order => { if (!order.thankYouEmail) { queued++; order.thankYouEmail = { status: 'pending' }; } },
    readDatabase: () => structuredClone(database), writeDatabase: async value => { database = structuredClone(value); },
    requireSessionUser: () => { if (!account) { const error = new Error('Sign in'); error.status = 401; throw error; } return { id: account }; },
    parseRequestBody: async request => request.body,
    sendJson: (response, status, body) => ({ status, body }),
    client: { orders: { create: async input => { if (failure) throw failure; creates++; gatewayOrder = input; assert(input.receipt.length <= 40); return { ...input, id: 'order_test123' }; } },
      payments: { fetch: async () => { if (failure) throw failure; return { order_id: 'order_test123', amount: paymentAmount, currency: 'INR', status: paymentStatus }; } } },
  });
  return {
    call: (route, body) => handler({ body }, {}, { pathname: route }),
    signed: (signature) => ({ razorpay_order_id: 'order_test123', razorpay_payment_id: 'pay_test123', razorpay_signature: signature ?? createHmac('sha256', keySecret).update('order_test123|pay_test123').digest('hex') }),
    state: () => database, creates: () => creates, gatewayOrder: () => gatewayOrder,
    account: value => account = value, failure: value => failure = value,
    status: value => paymentStatus = value, amount: value => paymentAmount = value,
    queued: () => queued,
    webhook: (event, signature) => {
      const raw = Buffer.from(JSON.stringify(event));
      const request = Readable.from([raw]);
      request.headers = { 'x-razorpay-signature': signature ?? createHmac('sha256', 'test-webhook-secret').update(raw).digest('hex') };
      return handler(request, {}, { pathname: '/api/payments/webhook' });
    },
  };
}
const order = { planId: 'lite', amount: 79900, currency: 'INR' };
const rejects = (promise, status) => assert.rejects(promise, error => error.status === status);

test('launch coupons charge the correct discounted amount for every plan and reject tampering', async () => {
  for (const [coupon, prices] of [['FIRST50', [51935, 77935, 103935]], ['LAUNCH25', [59925, 89925, 119925]]]) {
    for (const [index, planId] of ['lite', 'ultra', 'premium'].entries()) {
      const f = fixture();
      const originalAmount = paymentQuote({ planId }).amount;
      const amount = prices[index];
      const quote = await f.call('/api/payment-quote', { planId, coupon: ` ${coupon.toLowerCase()} ` });
      assert.deepEqual(quote.body, { planId, originalAmount, amount, currency: 'INR', coupon });
      const payload = { planId, coupon, amount, currency: 'INR' };
      await rejects(f.call('/api/create-order', { ...payload, amount: 100 }), 400);
      await rejects(f.call('/api/create-order', { ...payload, amount: originalAmount }), 400);
      await rejects(f.call('/api/create-order', { ...payload, coupon: '' }), 400);
      await rejects(f.call('/api/create-order', { ...payload, coupon: 'FIRST50,LAUNCH25' }), 400);
      assert.equal(f.creates(), 0);
      assert.equal((await f.call('/api/create-order', payload)).body.amount, amount);
      assert.equal(f.gatewayOrder().amount, amount);
      assert.equal(f.state().paymentOrders[0].coupon, coupon);
      assert.equal(f.state().paymentOrders[0].originalAmount, originalAmount);
      f.amount(originalAmount);
      await rejects(f.call('/api/verify-payment', f.signed()), 400);
      f.amount(amount);
      assert.equal((await f.call('/api/verify-payment', f.signed())).body.hasPracticeAccess, true);
    }
  }
});

test('orders validate server prices, minimum, authentication and provider errors', async () => {
  const f = fixture();
  for (const amount of [99, 100.5, '79900', 100, -1]) await rejects(f.call('/api/create-order', { ...order, amount }), 400);
  await rejects(f.call('/api/create-order', { ...order, currency: 'USD' }), 400);
  assert.equal(f.creates(), 0);
  f.account(null); await rejects(f.call('/api/create-order', order), 401); f.account('one');
  f.failure({ statusCode: 401 }); await rejects(f.call('/api/create-order', order), 401);
  f.failure({ statusCode: 500, secret: 'must-not-leak' }); await rejects(f.call('/api/create-order', order), 500);
  f.failure(null);
  const result = await f.call('/api/create-order', order);
  assert.equal(result.body.order_id, 'order_test123'); assert.equal(result.body.amount, 79900);
  assert.equal(result.body.key_id, 'rzp_test_fixture'); assert.equal(result.body.test_mode, true);
  assert.equal(JSON.stringify(result).includes('isolated-test-secret'), false);
  assert.equal(f.state().paymentOrders[0].status, 'created');
});

test('signed captured webhook confirms payment without a browser and repeated events do not requeue email', async () => {
  const f = fixture(); await f.call('/api/create-order', order); f.account(null);
  const event = { event: 'payment.captured', payload: { payment: { entity: { id: 'pay_test123', order_id: 'order_test123' } } } };
  await rejects(f.webhook(event, '0'.repeat(64)), 400); assert.equal(f.queued(), 0);
  f.amount(1); await rejects(f.webhook(event), 400); f.amount(79900);
  assert.equal((await f.webhook(event)).status, 200);
  assert.equal(f.state().paymentOrders[0].status, 'paid');
  assert.equal((await f.webhook(event)).status, 200); assert.equal(f.queued(), 1);
  f.account('one'); await f.call('/api/verify-payment', f.signed()); assert.equal(f.queued(), 1);
});

test('verification rejects missing, forged, foreign and mismatched payments without marking paid', async () => {
  const f = fixture(); await f.call('/api/create-order', order);
  await rejects(f.call('/api/verify-payment', {}), 400);
  for (const signature of ['bad', '0'.repeat(64), 'g'.repeat(64)]) await rejects(f.call('/api/verify-payment', f.signed(signature)), 400);
  f.account('two'); await rejects(f.call('/api/verify-payment', f.signed()), 400); f.account('one');
  f.amount(100); await rejects(f.call('/api/verify-payment', f.signed()), 400); f.amount(79900);
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
  const firstPurchase = f.state().paymentOrders[0].purchasedAt;
  const firstExpiry = f.state().paymentOrders[0].expiresAt;
  assert.equal((await f.call('/api/verify-payment', f.signed())).body.paid, true);
  assert.equal(f.state().paymentOrders[0].purchasedAt, firstPurchase);
  assert.equal(f.state().paymentOrders[0].expiresAt, firstExpiry);
  assert.equal(f.state().users[0].subscriptionExpiresAt, firstExpiry);
  assert.equal(f.state().paymentOrders.length, 1);
  assert.equal(f.state().paymentOrders[0].paymentId, 'pay_test123');
  assert.equal(hasPracticeAccess(f.state(), 'one'), true);
  assert.equal(hasPracticeAccess(f.state(), 'two'), false);
});

test('TEST1 sends each discounted price to Razorpay and rejects forged or stale amounts', async () => {
  for (const [planId, originalAmount, amount] of [['lite', 79900, 6900], ['ultra', 119900, 9900], ['premium', 159900, 14900]]) {
    assert.equal(paymentQuote({ planId }).amount, originalAmount);
    const f = fixture();
    const quote = await f.call('/api/payment-quote', { planId, coupon: ' test1 ' });
    assert.deepEqual(quote.body, { planId, originalAmount, amount, currency: 'INR', coupon: 'TEST1' });
    const discounted = { planId, amount, currency: 'INR', coupon: 'TEST1' };
    await rejects(f.call('/api/create-order', { ...discounted, coupon: '' }), 400);
    await rejects(f.call('/api/create-order', { ...discounted, coupon: 'FAKE' }), 400);
    for (const expiredCode of ['PRELAUNCH', ' prelaunch ']) {
      await rejects(f.call('/api/payment-quote', { planId, coupon: expiredCode }), 400);
      await rejects(f.call('/api/create-order', { ...discounted, coupon: expiredCode }), 400);
    }
    for (const invalidAmount of [100, 900, originalAmount, ...[6900, 9900, 14900].filter(price => price !== amount)]) {
      await rejects(f.call('/api/create-order', { ...discounted, amount: invalidAmount }), 400);
    }
    assert.equal(f.creates(), 0);
    const created = await f.call('/api/create-order', discounted);
    assert.equal(created.body.amount, amount);
    assert.equal(f.gatewayOrder().amount, amount);
    assert.equal(f.gatewayOrder().currency, 'INR');
    assert.equal(f.state().paymentOrders[0].amount, amount);
    assert.equal(f.state().paymentOrders[0].originalAmount, originalAmount);
    assert.equal(f.state().paymentOrders[0].coupon, 'TEST1');
    assert.equal(hasPracticeAccess(f.state(), 'one'), false);
    f.amount(originalAmount);
    await rejects(f.call('/api/verify-payment', f.signed()), 400);
    f.amount(amount);
    const verified = await f.call('/api/verify-payment', f.signed());
    assert.equal(verified.body.hasPracticeAccess, true);
  }
});
