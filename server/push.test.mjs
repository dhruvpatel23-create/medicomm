import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
import webpush from 'web-push';
import vm from 'node:vm';
import { createStateStore } from './stateStore.mjs';
import { createPushService, queuePush, queueDailyReminders, validateSubscription } from './push.mjs';
import { dailyQuestionGoal } from '../src/lib/studyGoal.js';
import { isPublicPushAddress, publicPushLookup } from './pushNetwork.mjs';

const keys = webpush.generateVAPIDKeys();
const env = { VAPID_PUBLIC_KEY: keys.publicKey, VAPID_PRIVATE_KEY: keys.privateKey, VAPID_SUBJECT: 'https://medullaprep.com' };
const now = Date.parse('2026-10-26T12:30:00Z'); // 18:00 IST
const subscription = suffix => ({ endpoint: `https://fcm.googleapis.com/fcm/send/${suffix}`, keys: {
  p256dh: Buffer.concat([Buffer.from([4]), Buffer.alloc(64, 1)]).toString('base64url'), auth: Buffer.alloc(16, 2).toString('base64url'),
} });
function fixture({ send = async () => {}, configured = true } = {}) {
  const store = createStateStore({ initial: { users: [{ id: 'a', name: 'Alice', dailyQuestionGoal: 30 }, { id: 'b', name: 'Bob', dailyQuestionGoal: 30 }], sessions: {}, pushSubscriptions: [], pushQueue: [] }, persist: async () => {} });
  const dependencies = { read: () => store.read(), write: data => store.write(data),
    getUser: (req, res, db) => { const user = db.users.find(user => user.id === req.user); if (!user) res.status = 401; return user; },
    parseBody: async req => req.body, sendJson: (res, status, body) => ({ status, body }), env: configured ? env : {}, transport: send };
  const service = createPushService(dependencies);
  return { store, dependencies, service, call: (method, body = {}, user = 'b') => service.handle({ method, body, user }, {}),
    async update(fn) { const data = store.read(); fn(data); await store.write(data); } };
}

test('browser HTTPS providers and long tokens are accepted while unsafe URLs and keys are rejected', () => {
  assert.deepEqual(validateSubscription(subscription('valid')), subscription('valid'));
  for (const endpoint of ['https://wns2.example-push-provider.com/w/?token=example', 'https://updates.push.services.mozilla.com/wpush/v2/token',
    `https://fcm.googleapis.com/wp/${'a'.repeat(4096)}`]) {
    assert.equal(validateSubscription({ ...subscription('x'), endpoint }).endpoint, endpoint);
  }
  for (const endpoint of ['http://fcm.googleapis.com/test', 'https://127.0.0.1/a', 'https://169.254.169.254/token', 'https://10.0.0.1/a',
    'https://localhost/a', 'https://app.local/a', 'https://[::1]/a', 'https://[::ffff:127.0.0.1]/a',
    'https://fcm.googleapis.com:8443/a', 'https://user@fcm.googleapis.com/a']) {
    assert.throws(() => validateSubscription({ ...subscription('x'), endpoint }), { status: 400 });
  }
  assert.throws(() => validateSubscription({ ...subscription('x'), keys: { auth: 'secret', p256dh: 'bad' } }), { status: 400 });
});

test('authenticated subscriptions rebind to one account, remain private, and respect device limits', async () => {
  const f = fixture();
  await f.call('POST', { subscription: subscription('phone') });
  await f.call('POST', { subscription: subscription('phone') });
  assert.equal(f.store.read().pushSubscriptions.length, 1);
  await f.call('POST', { subscription: subscription('phone') }, 'a');
  assert.equal(f.store.read().pushSubscriptions[0].userId, 'a');
  assert.doesNotMatch(JSON.stringify(await f.call('GET')), /endpoint|p256dh|privateKey/);
  await f.call('DELETE', { endpoint: subscription('phone').endpoint });
  assert.equal(f.store.read().pushSubscriptions.length, 1, 'another account cannot unsubscribe this device');
  await f.call('DELETE', { endpoint: subscription('phone').endpoint }, 'a');
  assert.equal(f.store.read().pushSubscriptions.length, 0);
  const response = {};
  await f.service.handle({ method: 'GET', user: 'unknown' }, response);
  assert.equal(response.status, 401);
  for (let i = 0; i < 10; i++) await f.call('POST', { subscription: subscription(`device-${i}`) });
  await assert.rejects(f.call('POST', { subscription: subscription('too-many') }), { status: 400 });
});

test('daily reminder respects IST, progress, preferences and persisted per-user date', async () => {
  const f = fixture();
  await f.call('POST', { subscription: subscription('phone') });
  await f.call('POST', { subscription: subscription('laptop') });
  const data = f.store.read();
  assert.equal(queueDailyReminders(data, now - 1), false);
  data.practiceResults = Array.from({ length: 12 }, () => ({ userId: 'b', answeredAt: new Date(now).toISOString() }));
  assert.equal(queueDailyReminders(data, now), true);
  assert.equal(data.pushQueue.length, 1);
  assert.match(data.pushQueue[0].body, /18 of your 30/);
  assert.equal(queueDailyReminders(data, now + 3600000), false);
  const restarted = structuredClone(data);
  assert.equal(queueDailyReminders(restarted, now + 7200000), false);
  restarted.pushQueue = [];
  restarted.practiceResults = Array.from({ length: 30 }, () => ({ userId: 'b', answeredAt: new Date(now + 86400000).toISOString() }));
  queueDailyReminders(restarted, now + 86400000);
  assert.equal(restarted.pushQueue.length, 0, 'completed goal is skipped');
  restarted.users[1].notificationPreferences = { daily: false };
  assert.equal(queueDailyReminders(restarted, now + 2 * 86400000), false);
});

test('daily progress includes answered duel questions, and reminders never cross midnight IST', () => {
  const data = { users: [{ id: 'b', name: 'Bob', dailyQuestionGoal: 30 }], pushSubscriptions: [{ userId: 'b' }], duels: [{ results: { b: {
    completedAt: new Date(now).toISOString(), review: Array.from({ length: 30 }, () => ({ selectedIndex: 0, status: 'correct' })),
  } } }] };
  queueDailyReminders(data, now);
  assert.equal((data.pushQueue ?? []).length, 0);
  data.duels = []; delete data.users[0].lastPushReminderDate;
  queueDailyReminders(data, now + 5.5 * 3600000);
  assert.equal(data.pushQueue[0].expiresAt, Date.parse('2026-10-26T18:30:00Z'));
});

test('public push DNS lookup rejects private records and pins the exact validated address', async () => {
  for (const address of ['127.0.0.1', '10.0.0.1', '172.16.1.1', '192.168.1.1', '100.64.0.1', '169.254.169.254', '0.0.0.0', '224.0.0.1', '::1', 'fc00::1', 'fe80::1', '::ffff:127.0.0.1', '2001:db8::1']) assert.equal(isPublicPushAddress(address), false, address);
  for (const address of ['8.8.8.8', '1.1.1.1', '2606:4700:4700::1111']) assert.equal(isPublicPushAddress(address), true, address);
  const invoke = (records, options = {}) => new Promise((resolve, reject) => {
    publicPushLookup((host, opts, callback) => callback(null, records))('push.example.com', options, (error, address, family) => error ? reject(error) : resolve({ address, family }));
  });
  assert.deepEqual(await invoke([{ address: '8.8.8.8', family: 4 }]), { address: '8.8.8.8', family: 4 });
  await assert.rejects(invoke([{ address: '8.8.8.8', family: 4 }, { address: '192.168.1.1', family: 4 }]), { code: 'EPUSHADDRESS' });
  assert.deepEqual((await invoke([{ address: '8.8.8.8', family: 4 }], { all: true })).address, [{ address: '8.8.8.8', family: 4 }]);
});

test('daily goal is saved per account and validated independently of notification preferences', async () => {
  const f = fixture();
  assert.equal((await f.call('GET')).body.dailyQuestionGoal, 30);
  assert.equal((await f.call('PATCH', { dailyQuestionGoal: 60 })).body.dailyQuestionGoal, 60);
  assert.equal((await f.call('GET')).body.dailyQuestionGoal, 60);
  assert.equal((await f.call('GET', {}, 'a')).body.dailyQuestionGoal, 30);
  for (const value of [0, -1, 5001, 10.5, '40', null]) await assert.rejects(f.call('PATCH', { dailyQuestionGoal: value }), { status: 400 });
  assert.equal(dailyQuestionGoal({}), 40);
  assert.equal(dailyQuestionGoal({ studyGoal: { weeklyTarget: 140 } }), 20);
  assert.equal(dailyQuestionGoal({ studyGoal: { weeklyTarget: 150 } }), 22);
  assert.equal(dailyQuestionGoal({ dailyQuestionGoal: 70, studyGoal: { weeklyTarget: 140 } }), 70);
});

test('reminder uses each saved goal, skips completed goals and does not repeat when a goal changes', async () => {
  const f = fixture(); await f.call('POST', { subscription: subscription('phone') });
  await f.call('PATCH', { dailyQuestionGoal: 60 });
  const data = f.store.read();
  data.practiceResults = Array.from({ length: 35 }, () => ({ userId: 'b', answeredAt: new Date(now).toISOString() }));
  queueDailyReminders(data, now);
  assert.equal(data.pushQueue.length, 1);
  assert.equal(data.pushQueue[0].title, 'Your daily 60 questions');
  assert.match(data.pushQueue[0].body, /25 of your 60/);
  data.users[1].dailyQuestionGoal = 100;
  assert.equal(queueDailyReminders(data, now + 1000), false);
  assert.equal(data.pushQueue.length, 1);
  data.pushQueue = []; delete data.users[1].lastPushReminderDate;
  data.users[1].dailyQuestionGoal = 20;
  queueDailyReminders(data, now);
  assert.equal(data.pushQueue.length, 0);
});

test('queued reminders refresh a changed goal and progress immediately before delivery', async () => {
  for (const goal of [60, 20]) {
    const sent = [], f = fixture({ send: async (sub, payload) => sent.push(JSON.parse(payload)) });
    await f.call('POST', { subscription: subscription('phone') });
    await f.update(data => {
      const actualNow = Date.now();
      data.users[1].lastPushReminderDate = new Date(actualNow + 330 * 60000).toISOString().slice(0, 10);
      queuePush(data, { userId: 'b', kind: 'daily', key: 'daily-before-change', title: 'Your daily 30 questions', body: 'Old progress', url: '/' });
      data.users[1].dailyQuestionGoal = goal;
      data.practiceResults = Array.from({ length: 35 }, () => ({ userId: 'b', answeredAt: new Date(actualNow).toISOString() }));
    });
    await f.service.tick();
    assert.equal(sent.length, goal === 60 ? 1 : 0);
    if (sent.length) assert.match(sent[0].body, /25 of your 60/);
  }
});

test('message alerts deduplicate events, throttle bursts, and honor category opt-out', async () => {
  const f = fixture(); await f.call('POST', { subscription: subscription('phone') });
  const data = f.store.read();
  const job = { userId: 'b', kind: 'messages', key: 'message:1', group: 'conversation:1', title: 'Alice', body: 'New message', url: '/' };
  assert.equal(queuePush(data, job, now), true);
  assert.equal(queuePush(data, job, now + 61000), false);
  assert.equal(queuePush(data, { ...job, key: 'message:2' }, now + 1000), false);
  assert.equal(queuePush(data, { ...job, key: 'message:3' }, now + 60000), true);
  await f.call('PATCH', { preferences: { messages: false } });
  assert.equal(queuePush(f.store.read(), { ...job, key: 'message:4' }), false);
  await assert.rejects(f.call('PATCH', { preferences: { messages: 'true' } }), { status: 400 });
  await assert.rejects(f.call('PATCH', { preferences: { spam: true } }), { status: 400 });
});

test('two workers and a restart cannot redeliver a claimed job; all enabled devices receive a copy', async () => {
  const sent = [], f = fixture({ send: async (sub, payload) => { sent.push({ endpoint: sub.endpoint, payload: JSON.parse(payload) }); } });
  await f.call('POST', { subscription: subscription('phone') });
  await f.call('POST', { subscription: subscription('laptop') });
  await f.update(data => { data.users[1].notificationPreferences = { daily: false }; queuePush(data, { userId: 'b', kind: 'messages', key: 'm:1', title: 'Alice', body: 'New message', url: '/?notification=inbox' }); });
  const second = createPushService(f.dependencies);
  await Promise.all([f.service.tick(), second.tick(), f.service.tick()]);
  assert.equal(sent.length, 2);
  await createPushService(f.dependencies).tick();
  assert.equal(sent.length, 2);
  assert.ok(f.store.read().pushQueue[0].claimedAt);
});

test('expired endpoints are removed and delivery failures never retry uncertain sends', async () => {
  let calls = 0;
  const f = fixture({ send: async () => { calls++; throw Object.assign(new Error('gone'), { statusCode: 410 }); } });
  await f.call('POST', { subscription: subscription('gone') });
  await f.update(data => { data.users[1].notificationPreferences = { daily: false }; queuePush(data, { userId: 'b', kind: 'messages', key: 'm:1', title: 'Alice', body: 'New message', url: '/' }); });
  await f.service.tick(); await f.service.tick();
  assert.equal(calls, 1);
  assert.equal(f.store.read().pushSubscriptions.length, 0);
});

test('expired jobs, cancelled challenges, and opted-out queued categories are skipped', async () => {
  let calls = 0; const f = fixture({ send: async () => { calls++; } });
  await f.call('POST', { subscription: subscription('phone') });
  await f.update(data => {
    const base = { userId: 'b', title: 'Alice', body: 'New update', url: '/' };
    queuePush(data, { ...base, kind: 'messages', key: 'expired', ttl: 0 });
    queuePush(data, { ...base, kind: 'challenges', key: 'challenge:cancelled' });
    queuePush(data, { ...base, kind: 'messages', key: 'opt-out' });
    data.users[1].notificationPreferences = { messages: false, daily: false };
  });
  await f.service.tick(); assert.equal(calls, 0);
});

test('message handler queues only for the other participant and never exposes message contents', async () => {
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const handler = source.slice(source.indexOf('async function handleSendDirectMessage('), source.indexOf('function handleLeaderboard('));
  let data = { users: [{ id: 'a', name: 'Alice' }, { id: 'b', name: 'Bob' }], directConversations: [{ id: 'chat', participantIds: ['a', 'b'], messages: [] }],
    pushSubscriptions: [{ userId: 'a' }, { userId: 'b' }] };
  const deps = { readDatabase: () => structuredClone(data), writeDatabase: async db => { data = db; },
    requireSessionUser: (req, res, db) => db.users[0], parseRequestBody: async req => req.body,
    sendJson: (res, status, body) => ({ status, body }), randomBytes, queuePush, pushService: { tick: async () => {} }, sanitizeDirectConversation: c => c };
  const api = new Function(...Object.keys(deps), `${handler}; return handleSendDirectMessage;`)(...Object.values(deps));
  assert.equal((await api({ body: { text: 'private medical conversation' } }, {}, 'chat')).status, 200);
  assert.equal(data.pushQueue.length, 1); assert.equal(data.pushQueue[0].userId, 'b');
  assert.doesNotMatch(JSON.stringify(data.pushQueue), /private medical conversation/);
});

test('unconfigured server has no scheduler deliveries and reports availability honestly', async () => {
  const f = fixture({ configured: false });
  assert.equal((await f.call('GET')).body.configured, false);
  await assert.rejects(f.call('POST', { subscription: subscription('phone') }), { status: 503 });
  await f.service.tick(); assert.equal(f.store.read().pushQueue.length, 0);
});

test('background push displays an OS notification and clicks focus the linked inbox safely', async () => {
  const handlers = {}, displayed = [], opened = [], navigated = [];
  let focused = 0;
  const self = { location: { origin: 'https://medullaprep.com' },
    addEventListener: (name, handler) => { handlers[name] = handler; },
    registration: { showNotification: async (title, options) => displayed.push({ title, options }) },
    clients: { matchAll: async () => [{ url: 'https://medullaprep.com/', navigate: async url => navigated.push(url), focus: async () => focused++ }], openWindow: async url => opened.push(url) } };
  vm.runInNewContext(readFileSync(new URL('../public/push-sw.js', import.meta.url), 'utf8'), { self, URL });
  let pending;
  handlers.push({ data: { json: () => ({ title: 'Alice', body: 'New message', url: '/?notification=inbox&conversation=chat' }) }, waitUntil: promise => { pending = promise; } });
  await pending;
  assert.equal(displayed[0].title, 'Alice');
  assert.equal(displayed[0].options.renotify, false);
  handlers.notificationclick({ notification: { close() {}, data: displayed[0].options.data }, waitUntil: promise => { pending = promise; } });
  await pending;
  assert.equal(navigated[0], 'https://medullaprep.com/?notification=inbox&conversation=chat');
  assert.equal(focused, 1); assert.equal(opened.length, 0);
  handlers.notificationclick({ notification: { close() {}, data: { url: 'https://evil.test' } }, waitUntil: promise => { pending = promise; } });
  await pending;
  assert.equal(navigated[1], 'https://medullaprep.com/');
});

test('logout removes only the signed-in account device and clears the session together', async () => {
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const handler = source.slice(source.indexOf('async function handleLogout('), source.indexOf('async function handleProfileUpdate('));
  let data = { users: [{ id: 'a' }, { id: 'b' }], sessions: { hashed: { userId: 'a' } },
    pushSubscriptions: [{ userId: 'a', subscription: subscription('phone') }, { userId: 'a', subscription: subscription('laptop') }, { userId: 'b', subscription: subscription('other') }] };
  const deps = { readDatabase: () => structuredClone(data), getTokenFromRequest: () => 'token', getSessionUser: (req, db) => db.users[0],
    parseRequestBody: async req => req.body, sessionHash: () => 'hashed', writeDatabase: async db => { data = db; },
    sendJson: (res, status, body) => ({ status, body }), sessionCookie: () => 'cleared', production: false };
  const logout = new Function(...Object.keys(deps), `${handler}; return handleLogout;`)(...Object.values(deps));
  await logout({ body: { pushEndpoint: subscription('phone').endpoint } }, {});
  assert.equal(data.pushSubscriptions.length, 2);
  assert.deepEqual(data.sessions, {});
  assert.equal(data.pushSubscriptions[0].subscription.endpoint, subscription('laptop').endpoint);
});
