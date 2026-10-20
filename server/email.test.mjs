import test from 'node:test';
import assert from 'node:assert/strict';
import { createMailer, emailMessage, queueThankYou, createEmailWorker } from './email.mjs';
import { createEmailVerification } from './emailVerification.mjs';
import { createStateStore } from './stateStore.mjs';

function fixture() {
  let time = 1800000000000, deliveries = [], fail = false;
  const state = createStateStore({ initial: { users: [], sessions: {}, paymentOrders: [] }, persist: async () => {} });
  const readDatabase = () => state.read(), writeDatabase = value => state.write(value);
  const mailer = { configured: true, from: 'Medulla <noreply@example.test>', send: async (body, key) => {
    if (fail) throw new Error('Mail provider unavailable'); deliveries.push({ body, key }); return `mail-${deliveries.length}`;
  } };
  const options = { enabled: true, secret: 'test-only-secret-with-more-than-32-characters', readDatabase, writeDatabase, mailer, now: () => time,
    validateNewUser(db, user) { if (db.users.some(u => u.email === user.email)) throw Object.assign(new Error('Duplicate account'), { status: 409 }); } };
  return { options, mailer, readDatabase, writeDatabase, deliveries, service: createEmailVerification(options),
    advance: ms => { time += ms; }, fail: value => { fail = value; }, now: () => time,
    code: () => deliveries.at(-1).body.text.match(/code is: (\d{6})/)[1] };
}
const user = { id: 'learner', name: 'Learner', email: 'learner@example.test', passwordHash: 'hashed-password' };

test('signup creates no account or session until correct single-use email code', async () => {
  const f = fixture(); const pending = await f.service.start({ user, signup: true }); const code = f.code();
  assert.equal(f.readDatabase().users.length, 0); assert.deepEqual(f.readDatabase().sessions, {});
  assert(!JSON.stringify(f.readDatabase()).includes(code));
  assert(!JSON.stringify(pending).includes('hashed-password'));
  const result = await f.service.verify(pending.challengeId, code);
  assert.equal(result.user.email, user.email); assert(result.user.emailVerifiedAt); assert.equal(result.token.length, 64);
  assert.equal(f.readDatabase().users.length, 1); assert.equal(f.readDatabase().emailChallenges.length, 0);
  await assert.rejects(f.service.verify(pending.challengeId, code), { status: 400 });
});
test('wrong attempts persist, stop after five, and cannot issue a session', async () => {
  const f = fixture(); const pending = await f.service.start({ user, signup: true }); const right = f.code();
  const wrong = right === '000000' ? '000001' : '000000';
  for (let i = 0; i < 5; i++) await assert.rejects(f.service.verify(pending.challengeId, wrong), { status: 400 });
  assert.equal(f.readDatabase().emailChallenges[0].attempts, 5);
  await assert.rejects(f.service.verify(pending.challengeId, right), { status: 400 });
  assert.equal(f.readDatabase().users.length, 0);
});
test('expired codes fail; resend has cooldown and replaces previous code', async () => {
  const f = fixture(); const pending = await f.service.start({ user, signup: true }); const oldHash = f.readDatabase().emailChallenges[0].hash;
  await assert.rejects(f.service.resend(pending.challengeId), { status: 429 });
  f.advance(10 * 60000 + 1); await assert.rejects(f.service.verify(pending.challengeId, f.code()), { status: 400 });
  await f.service.resend(pending.challengeId);
  assert.equal(f.readDatabase().emailChallenges[0].generation, 2);
  // Random codes can repeat, but the latest generation is the only active record.
  assert.equal(typeof oldHash, 'string'); assert.equal(f.readDatabase().emailChallenges.length, 1);
  assert.equal((await f.service.verify(pending.challengeId, f.code())).user.id, user.id);
});
test('hourly limit and restarts preserve challenge security', async () => {
  const f = fixture(); const pending = await f.service.start({ user, signup: true });
  for (let i = 0; i < 4; i++) { f.advance(60001); await f.service.resend(pending.challengeId); }
  f.advance(60001); await assert.rejects(f.service.resend(pending.challengeId), { status: 429 });
  const restarted = createEmailVerification(f.options);
  assert.equal((await restarted.verify(pending.challengeId, f.code())).user.id, user.id);
});
test('simultaneous verification cannot create duplicate accounts or sessions', async () => {
  const f = fixture(); const pending = await f.service.start({ user, signup: true }); const code = f.code();
  const result = await Promise.allSettled([f.service.verify(pending.challengeId, code), f.service.verify(pending.challengeId, code)]);
  assert.equal(result.filter(item => item.status === 'fulfilled').length, 1);
  assert.equal(Object.keys(f.readDatabase().sessions).length, 1);
});
test('existing account verifies without duplicate user; email change invalidates challenge', async () => {
  const f = fixture(); let db = f.readDatabase(); db.users.push({ ...user }); await f.writeDatabase(db);
  const pending = await f.service.start({ user });
  await f.service.verify(pending.challengeId, f.code()); assert.equal(f.readDatabase().users.length, 1);
  f.advance(60001); const next = await f.service.start({ user });
  db = f.readDatabase(); db.users[0].email = 'changed@example.test'; await f.writeDatabase(db);
  await assert.rejects(f.service.verify(next.challengeId, f.code()), { status: 400 });
});
test('mail failure cannot create an account; incomplete configuration fails closed', async () => {
  const f = fixture(); f.fail(true);
  await assert.rejects(f.service.start({ user, signup: true })); assert.equal(f.readDatabase().users.length, 0);
  assert.throws(() => createEmailVerification({ ...f.options, secret: 'short' }));
  assert.throws(() => createEmailVerification({ ...f.options, mailer: { configured: false } }));
});
test('provider request uses stable idempotency, escapes HTML, and hides provider errors', async () => {
  let sent;
  const mailer = createMailer({ apiKey: 'private-key', from: 'Medulla <noreply@example.test>', fetchImpl: async (url, opts) => {
    sent = { url, opts }; return { ok: true, json: async () => ({ id: 'provider-id' }) };
  } });
  const message = { to: 'learner@example.test', ...emailMessage('Hello', ['<script>evil</script>']) };
  assert.equal(await mailer.send(message, 'stable-key'), 'provider-id');
  assert.equal(sent.opts.headers['Idempotency-Key'], 'stable-key');
  assert(!JSON.parse(sent.opts.body).html.includes('<script>'));
  const broken = createMailer({ apiKey: 'private-key', from: 'sender', fetchImpl: async () => { throw new Error('secret credentials'); } });
  await assert.rejects(broken.send(message, 'key'), error => error.status === 503 && !error.message.includes('secret'));
});

async function paidFixture() {
  const f = fixture(), db = f.readDatabase();
  const verified = { ...user, emailVerifiedAt: new Date(f.now()).toISOString() };
  db.users.push(verified);
  const order = { orderId: 'order_123', paymentId: 'pay_123', userId: user.id, planId: 'lite', amount: 79900, currency: 'INR', status: 'paid', expiresAt: '2027-10-19T00:00:00Z' };
  queueThankYou(order, verified, f.mailer, f.now()); db.paymentOrders.push(order); await f.writeDatabase(db);
  return { ...f, order, worker: createEmailWorker(f.options) };
}
test('subscription email is queued once and retry uses the same payload and key', async () => {
  const f = await paidFixture();
  const original = structuredClone(f.order.thankYouEmail);
  queueThankYou(f.order, user, f.mailer); assert.deepEqual(f.order.thankYouEmail, original);
  f.fail(true); await f.worker();
  assert.equal(f.readDatabase().paymentOrders[0].status, 'paid');
  assert.equal(f.readDatabase().paymentOrders[0].thankYouEmail.attempts, 1);
  f.advance(60001); f.fail(false); await f.worker(); await f.worker();
  assert.equal(f.deliveries.length, 1); assert.equal(f.deliveries[0].key, 'subscription-order_123');
  assert.equal(f.readDatabase().paymentOrders[0].thankYouEmail.status, 'sent');
  assert(!f.readDatabase().paymentOrders[0].thankYouEmail.message);
});
test('authorized/unverified payments never trigger thank-you mail', () => {
  const f = fixture();
  for (const status of ['created', 'authorized', 'failed']) {
    const order = { status }; queueThankYou(order, { ...user, emailVerifiedAt: 'today' }, f.mailer); assert(!order.thankYouEmail);
  }
  const order = { status: 'paid' }; queueThankYou(order, user, f.mailer); assert(!order.thankYouEmail);
});
test('multiple workers claim once; old uncertain attempts require operator review', async () => {
  const f = await paidFixture();
  await Promise.all([f.worker(), createEmailWorker(f.options)()]); assert.equal(f.deliveries.length, 1);
  const db = f.readDatabase(); db.paymentOrders[0].thankYouEmail = { status: 'pending', attempts: 1, firstAttemptAt: f.now() - 24 * 3600000, nextAttemptAt: 0 };
  await f.writeDatabase(db); await f.worker();
  assert.equal(f.readDatabase().paymentOrders[0].thankYouEmail.status, 'needs_review'); assert.equal(f.deliveries.length, 1);
});
