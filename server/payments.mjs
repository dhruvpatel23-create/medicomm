import Razorpay from 'razorpay';
import { createHmac, timingSafeEqual, randomUUID } from 'node:crypto';
import { HttpError } from './security.mjs';
import { PAYMENT_PLANS } from '../src/data/paymentPlans.js';

export function validPaymentSignature(orderId, paymentId, signature, secret) {
  if (typeof signature !== 'string' || !/^[a-f0-9]{64}$/i.test(signature)) return false;
  const expected = createHmac('sha256', secret).update(`${orderId}|${paymentId}`).digest();
  return timingSafeEqual(expected, Buffer.from(signature, 'hex'));
}

export function createPaymentHandler({ readDatabase, writeDatabase, requireSessionUser, parseRequestBody, sendJson,
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
  return async function handlePayment(request, response, url) {
    const user = requireSessionUser(request, response, readDatabase());
    if (!user) return;
    if (!gateway) throw new HttpError(503, 'Checkout is not configured yet. Please try again later.');
    const payload = await parseRequestBody(request);
    if (url.pathname === '/api/create-order') {
      const plan = PAYMENT_PLANS.find(item => item.id === payload.planId);
      if (!Number.isSafeInteger(payload.amount) || payload.amount < 100) throw new HttpError(400, 'Amount must be an integer of at least 100 paise.');
      if (!plan || payload.amount !== plan.amount || payload.currency !== plan.currency) throw new HttpError(400, 'The selected plan or price is invalid. Please refresh and try again.');
      const receipt = `med_${randomUUID().replaceAll('-', '')}`;
      const order = await provider(() => gateway.orders.create({ amount: plan.amount, currency: plan.currency, receipt }));
      if (!order.id || order.amount !== plan.amount || order.currency !== plan.currency) throw new HttpError(500, 'Razorpay returned an invalid order.');
      const database = readDatabase();
      database.paymentOrders ??= [];
      database.paymentOrders.push({ orderId: order.id, userId: user.id, planId: plan.id, amount: plan.amount,
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
    if (payment.order_id !== stored.orderId || payment.amount !== stored.amount || payment.currency !== stored.currency) throw new HttpError(400, 'Payment details do not match the saved order.');
    if (!['captured', 'authorized'].includes(payment.status)) throw new HttpError(400, 'Payment is not completed.');
    const database = readDatabase();
    const order = database.paymentOrders.find(item => item.orderId === stored.orderId && item.userId === user.id);
    if (order.paymentId && order.paymentId !== paymentId) throw new HttpError(400, 'This order already has a verified payment.');
    order.paymentId = paymentId;
    order.signature = signature;
    order.status = payment.status === 'captured' ? 'paid' : 'authorized';
    order.verifiedAt = new Date().toISOString();
    await writeDatabase(database);
    return sendJson(response, 200, { success: true, paid: order.status === 'paid', status: order.status,
      order_id: order.orderId, payment_id: paymentId, planId: order.planId, test_mode: order.testMode });
  };
}
