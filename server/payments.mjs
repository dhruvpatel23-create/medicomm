import { updateTokenState } from './tokens.mjs';
import Razorpay from 'razorpay';
import { createHmac, timingSafeEqual, randomUUID } from 'node:crypto';
import { HttpError } from './security.mjs';
import { PAYMENT_PLANS } from '../src/data/paymentPlans.js';
import { annualExpiry, reconcileSubscriptions, subscriptionDetails } from './subscriptions.mjs';

export function hasPracticeAccess(database, userId) {
  return subscriptionDetails(database, userId).hasPracticeAccess;
}

export function paymentQuote(payload) {
  const plan = PAYMENT_PLANS.find(item => item.id === payload.planId);
  if (!plan) throw new HttpError(400, 'Choose a valid plan.');
  const coupon = String(payload.coupon ?? '').trim().toUpperCase();
  const discountPercent = new Map([['FIRST50', 35], ['LAUNCH25', 25]]).get(coupon);
  if (coupon && coupon !== 'TEST1' && discountPercent === undefined) throw new HttpError(400, 'That coupon code is not valid.');
  const amount = coupon === 'TEST1' ? plan.discountedAmount
    : discountPercent === undefined ? plan.amount : Math.round(plan.amount * (100 - discountPercent) / 100);
  return { planId: plan.id, originalAmount: plan.amount, amount, currency: plan.currency, coupon };
}

export function validPaymentSignature(orderId, paymentId, signature, secret) {
  if (typeof signature !== 'string' || !/^[a-f0-9]{64}$/i.test(signature)) return false;
  const expected = createHmac('sha256', secret).update(`${orderId}|${paymentId}`).digest();
  return timingSafeEqual(expected, Buffer.from(signature, 'hex'));
}

export function createPaymentHandler({ readDatabase, writeDatabase, requireSessionUser, parseRequestBody, sendJson,
  enqueueThankYou = () => {}, afterPayment = () => {}, requireVerifiedEmail = false,
  webhookSecret = process.env.RAZORPAY_WEBHOOK_SECRET,
  keyId = process.env.RAZORPAY_KEY_ID, keySecret = process.env.RAZORPAY_KEY_SECRET, client }) {
  const gateway = client || (keyId && keySecret ? new Razorpay({ key_id: keyId, key_secret: keySecret }) : null);
  if (!client && gateway) gateway.api.rq.defaults.timeout = 20000;
  async function provider(operation) {
    try { return await operation(); }
    catch (error) {
      // Do not expose provider request objects, authorization headers or secrets.
      throw new HttpError(error.statusCode === 401 ? 401 : 500,
        error.statusCode === 401 ? 'Payment provider authentication failed. Please contact support.' : 'Razorpay could not process this request. Please try again.');
    }
  }
  async function completePayment(stored, payment, paymentId, signature) {
    if (payment.order_id !== stored.orderId || payment.amount !== stored.amount || payment.currency !== stored.currency) throw new HttpError(400, 'Payment details do not match the saved order.');
    if (!['captured', 'authorized'].includes(payment.status)) throw new HttpError(400, 'Payment is not completed.');
    let result;
    await updateTokenState(readDatabase, writeDatabase, database => {
      const order = database.paymentOrders.find(item => item.orderId === stored.orderId && item.userId === stored.userId);
      if (!order) throw new HttpError(400, 'Payment order was not found.');
      if (order.paymentId && order.paymentId !== paymentId) throw new HttpError(400, 'This order already has a verified payment.');
      order.paymentId = paymentId;
      if (signature) order.signature = signature;
      order.status = order.status === 'paid' || payment.status === 'captured' ? 'paid' : 'authorized';
      order.verifiedAt ||= new Date().toISOString();
      if (order.status === 'paid' && !order.purchasedAt) {
        const providerTime = Number.isFinite(payment.created_at) && payment.created_at > 0 ? payment.created_at * 1000 : null;
        order.purchasedAt = providerTime ? new Date(providerTime).toISOString() : order.verifiedAt;
        order.purchaseDateSource = providerTime ? 'razorpay_payment' : 'saved_verification';
        order.expiresAt = annualExpiry(order.purchasedAt);
      }
      reconcileSubscriptions(database);
      if (order.status === 'paid') enqueueThankYou(order, database.users.find(entry => entry.id === stored.userId));
      result = { success: true, paid: order.status === 'paid', status: order.status,
        ...subscriptionDetails(database, stored.userId),
        order_id: order.orderId, payment_id: paymentId, planId: order.planId, test_mode: order.testMode };
    });
    try { afterPayment(); } catch { /* Email delivery must never change payment success. */ }
    return result;
  }
  return async function handlePayment(request, response, url) {
    if (url.pathname === '/api/payments/webhook') {
      if (!gateway || !webhookSecret) throw new HttpError(503, 'Payment webhook is not configured.');
      const signature = request.headers['x-razorpay-signature'];
      if (typeof signature !== 'string' || !/^[a-f0-9]{64}$/i.test(signature)) throw new HttpError(400, 'Invalid webhook signature.');
      if (request.headers['content-encoding'] && request.headers['content-encoding'] !== 'identity') throw new HttpError(415, 'Unsupported encoding.');
      const chunks = []; let bytes = 0;
      for await (const chunk of request.iterator({ destroyOnReturn: false })) {
        bytes += chunk.length; if (bytes > 256 * 1024) throw new HttpError(413, 'Webhook is too large.'); chunks.push(chunk);
      }
      const raw = Buffer.concat(chunks);
      const expected = createHmac('sha256', webhookSecret).update(raw).digest();
      if (!timingSafeEqual(expected, Buffer.from(signature, 'hex'))) throw new HttpError(400, 'Invalid webhook signature.');
      let event;
      try { event = JSON.parse(raw); } catch { throw new HttpError(400, 'Invalid webhook payload.'); }
      if (event?.event !== 'payment.captured') return sendJson(response, 200, { received: true });
      const entity = event.payload?.payment?.entity;
      if (!/^pay_[a-zA-Z0-9]+$/.test(entity?.id || '') || !/^order_[a-zA-Z0-9]+$/.test(entity?.order_id || '')) throw new HttpError(400, 'Invalid webhook payment.');
      const stored = (readDatabase().paymentOrders || []).find(item => item.orderId === entity.order_id);
      if (!stored) return sendJson(response, 200, { received: true });
      const payment = await provider(() => gateway.payments.fetch(entity.id));
      if (payment.status !== 'captured') throw new HttpError(409, 'Payment capture is not yet confirmed.');
      await completePayment(stored, payment, entity.id);
      return sendJson(response, 200, { received: true });
    }
    if (url.pathname === '/api/payment-quote') return sendJson(response, 200, paymentQuote(await parseRequestBody(request)));
    const user = requireSessionUser(request, response, readDatabase());
    if (!user) return;
    if (!gateway) throw new HttpError(503, 'Checkout is not configured yet. Please try again later.');
    const payload = await parseRequestBody(request);
    if (url.pathname === '/api/create-order') {
      if (requireVerifiedEmail && !readDatabase().users.find(entry => entry.id === user.id)?.emailVerifiedAt) {
        throw new HttpError(403, 'Please sign out and sign in again to verify your email before buying a subscription.');
      }
      const plan = paymentQuote(payload);
      if (!Number.isSafeInteger(payload.amount) || payload.amount < 100) throw new HttpError(400, 'Amount must be an integer of at least 100 paise.');
      if (!plan || payload.amount !== plan.amount || payload.currency !== plan.currency) throw new HttpError(400, 'The selected plan or price is invalid. Please refresh and try again.');
      const receipt = `med_${randomUUID().replaceAll('-', '')}`;
      const order = await provider(() => gateway.orders.create({ amount: plan.amount, currency: plan.currency, receipt }));
      if (!order.id || order.amount !== plan.amount || order.currency !== plan.currency) throw new HttpError(500, 'Razorpay returned an invalid order.');
      const database = readDatabase();
      database.paymentOrders ??= [];
      database.paymentOrders.push({ orderId: order.id, userId: user.id, planId: plan.planId, amount: plan.amount, coupon: plan.coupon, originalAmount: plan.originalAmount,
        currency: plan.currency, receipt, status: 'created', testMode: keyId.startsWith('rzp_test_'), createdAt: new Date().toISOString() });
      await writeDatabase(database);
      return sendJson(response, 200, { order_id: order.id, amount: plan.amount, currency: plan.currency, key_id: keyId, test_mode: keyId.startsWith('rzp_test_') });
    }
    const { razorpay_payment_id: paymentId, razorpay_order_id: orderId, razorpay_signature: signature } = payload;
    if (typeof orderId !== 'string' || !/^order_[a-zA-Z0-9]+$/.test(orderId) || typeof paymentId !== 'string' || !/^pay_[a-zA-Z0-9]+$/.test(paymentId) || typeof signature !== 'string' || !signature) {
      throw new HttpError(400, 'Payment ID, order ID and signature are required.');
    }
    const stored = (readDatabase().paymentOrders ?? []).find(item => item.orderId === orderId && item.userId === user.id);
    if (!stored) throw new HttpError(400, 'Payment order was not found for this account.');
    if (!validPaymentSignature(stored.orderId, paymentId, signature, keySecret)) throw new HttpError(400, 'Payment signature does not match.');
    if (stored.paymentId && stored.paymentId !== paymentId) throw new HttpError(400, 'This order already has a verified payment.');
    const payment = await provider(() => gateway.payments.fetch(paymentId));
    return sendJson(response, 200, await completePayment(stored, payment, paymentId, signature));
  };
}
