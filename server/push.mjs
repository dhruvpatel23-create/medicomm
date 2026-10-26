import webpush from 'web-push';
import { createHash, randomUUID } from 'node:crypto';
import { HttpError } from './security.mjs';
import { dashboardData } from './dashboard.mjs';
import { dailyQuestionGoal } from '../src/lib/studyGoal.js';
import { isIP } from 'node:net';
import { isPublicPushAddress, pushAgent } from './pushNetwork.mjs';

const day = now => new Date(now + 330 * 60000).toISOString().slice(0, 10);
const defaults = { messages: true, challenges: true, daily: true };
const idFor = endpoint => createHash('sha256').update(endpoint).digest('hex');

export function validateSubscription(value) {
  let url;
  try {
    if (typeof value?.endpoint !== 'string' || value.endpoint.length > 16384) throw new Error();
    url = new URL(value.endpoint);
  } catch { throw new HttpError(400, 'Invalid push subscription.'); }
  const hostname = url.hostname.replace(/^\[|\]$/g, '');
  // Vendor-neutral HTTPS endpoints; DNS/IP checks on the sending agent prevent SSRF.
  if (url.protocol !== 'https:' || url.port || url.username || url.password || url.hash ||
      hostname === 'localhost' || hostname.endsWith('.localhost') || hostname.endsWith('.local') || !hostname.includes('.') ||
      (isIP(hostname) && !isPublicPushAddress(hostname))) throw new HttpError(400, 'Push notifications require a public HTTPS provider.');
  const keys = value.keys;
  if (!keys || !/^[A-Za-z0-9_-]{87}$/.test(keys.p256dh) || !/^[A-Za-z0-9_-]{22}$/.test(keys.auth) ||
      Buffer.from(keys.p256dh, 'base64url').length !== 65 || Buffer.from(keys.p256dh, 'base64url')[0] !== 4) throw new HttpError(400, 'Invalid push keys.');
  return { endpoint: url.href, keys: { p256dh: keys.p256dh, auth: keys.auth } };
}

export function queuePush(database, { userId, kind, key, title, body, url, group = key, ttl = 600 }, now = Date.now()) {
  const user = database.users.find(user => user.id === userId);
  const devices = (database.pushSubscriptions ?? []).filter(device => device.userId === userId);
  if (!user || user.notificationPreferences?.[kind] === false || !devices.length) return false;
  const queue = database.pushQueue ??= [];
  if (queue.some(job => job.key === key || (kind === 'messages' && job.userId === userId && job.group === group && now - job.createdAt < 60000))) return false;
  if (kind === 'challenges') {
    // A new invitation cancels the sender's previous room. Keep the latest
    // actionable invitation instead of suppressing it behind a cancelled one.
    // The stable OS notification tag and renotify:false replace earlier alerts.
    for (const job of queue) {
      if (job.kind === kind && job.userId === userId && job.group === group && !job.claimedAt) {
        job.claimedAt = now;
        job.deliveryStatus = 'superseded';
      }
    }
  }
  queue.push({ id: randomUUID(), userId, kind, key, group, title, body, url, createdAt: now, expiresAt: now + ttl * 1000 });
  return true;
}

export function queueDailyReminders(database, now = Date.now(), hour = 18) {
  if (new Date(now + 330 * 60000).getUTCHours() < hour) return false;
  let changed = false;
  const eligible = new Set((database.pushSubscriptions ?? []).map(device => device.userId));
  for (const user of database.users) {
    if (!eligible.has(user.id) || user.notificationPreferences?.daily === false || user.lastPushReminderDate === day(now)) continue;
    const goal = dailyQuestionGoal(user);
    const remaining = Math.max(0, goal - dashboardData(database, user, () => '', now).today.attempts);
    user.lastPushReminderDate = day(now);
    changed = true;
    if (remaining) queuePush(database, { userId: user.id, kind: 'daily', key: `daily:${user.id}:${day(now)}`,
      title: `Your daily ${goal} questions`, body: `${remaining} of your ${goal} questions today are still to be done. Keep your streak going!`,
      url: '/?notification=practice', ttl: Math.min(3600, Math.floor((Date.parse(`${day(now)}T18:30:00Z`) - now) / 1000)) }, now);
  }
  return changed;
}

export function createPushService({ read, write, getUser, parseBody, sendJson, env = process.env, transport = webpush.sendNotification }) {
  const publicKey = env.VAPID_PUBLIC_KEY || '', privateKey = env.VAPID_PRIVATE_KEY || '', subject = env.VAPID_SUBJECT || '';
  const configured = Boolean(publicKey && privateKey && subject);
  const hour = Number(env.PUSH_REMINDER_HOUR_IST ?? 18);
  if (!Number.isInteger(hour) || hour < 0 || hour > 23) throw new Error('PUSH_REMINDER_HOUR_IST must be 0–23.');
  if (configured) webpush.setVapidDetails(subject, publicKey, privateKey);
  async function change(update) {
    for (let retry = 0; retry < 4; retry++) {
      const data = read();
      const result = update(data);
      if (result === false) return result;
      try { await write(data); return result; } catch (error) { if (error.status !== 409 || retry === 3) throw error; }
    }
  }
  async function handle(request, response) {
    const data = read(), user = getUser(request, response, data);
    if (!user) return;
    if (request.method === 'GET') return sendJson(response, 200, { configured, publicKey: configured ? publicKey : null,
      preferences: { ...defaults, ...user.notificationPreferences }, reminderHourIST: hour, dailyQuestionGoal: dailyQuestionGoal(user) });
    const payload = await parseBody(request);
    if (request.method === 'POST') {
      if (!configured) throw new HttpError(503, 'Device notifications are not configured yet.');
      const subscription = validateSubscription(payload.subscription);
      const id = idFor(subscription.endpoint);
      data.pushSubscriptions = (data.pushSubscriptions ?? []).filter(device => device.id !== id);
      if (data.pushSubscriptions.filter(device => device.userId === user.id).length >= 10) throw new HttpError(400, 'Disable notifications on another device first.');
      data.pushSubscriptions.push({ id, userId: user.id, subscription, createdAt: Date.now() });
    } else if (request.method === 'DELETE') {
      data.pushSubscriptions = (data.pushSubscriptions ?? []).filter(device => device.userId !== user.id || device.id !== idFor(String(payload.endpoint)));
    } else if (request.method === 'PATCH') {
      if (!payload.preferences && payload.dailyQuestionGoal === undefined) throw new HttpError(400, 'Choose a notification preference or daily question goal.');
      if (payload.preferences) {
        if (typeof payload.preferences !== 'object' || Array.isArray(payload.preferences) || Object.keys(payload.preferences).some(key => !Object.hasOwn(defaults, key) || typeof payload.preferences[key] !== 'boolean')) throw new HttpError(400, 'Invalid notification preferences.');
        user.notificationPreferences = { ...defaults, ...user.notificationPreferences, ...payload.preferences };
      }
      if (payload.dailyQuestionGoal !== undefined) {
        if (!Number.isInteger(payload.dailyQuestionGoal) || payload.dailyQuestionGoal < 1 || payload.dailyQuestionGoal > 5000) throw new HttpError(400, 'Daily question goal must be a whole number from 1 to 5,000.');
        user.dailyQuestionGoal = payload.dailyQuestionGoal;
      }
    } else throw new HttpError(405, 'Method not allowed.');
    await write(data);
    return sendJson(response, 200, { ok: true, preferences: { ...defaults, ...user.notificationPreferences }, dailyQuestionGoal: dailyQuestionGoal(user) });
  }
  let running = false;
  async function tick() {
    if (!configured || running) return;
    running = true;
    try {
      await change(data => {
        const now = Date.now(), old = data.pushQueue ?? [];
        data.pushQueue = old.filter(job => job.expiresAt > now || job.createdAt > now - 86400000);
        return queueDailyReminders(data, now, hour) || data.pushQueue.length !== old.length;
      });
      for (let batch = 0; batch < 50; batch++) {
        const delivery = await change(data => {
          const job = (data.pushQueue ?? []).find(job => !job.claimedAt && job.expiresAt > Date.now());
          if (!job) return false;
          // Persist the claim before contacting the provider. Restarts and competing
          // workers cannot resend it; an interrupted delivery may be missed.
          job.claimedAt = Date.now();
          const user = data.users.find(user => user.id === job.userId);
          const active = user && user.notificationPreferences?.[job.kind] !== false;
          const validChallenge = job.kind !== 'challenges' || (data.challengeRooms ?? []).some(room => {
            const createdAt = Number(room.createdAtMs) || Date.parse(room.createdAt);
            return job.key === `challenge:${room.id}` && room.challengedId === job.userId && room.status === 'waiting' &&
              Number.isFinite(createdAt) && Date.now() - createdAt < 600000;
          });
          let incomplete = true;
          if (job.kind === 'daily' && user) {
            const goal = dailyQuestionGoal(user), remaining = Math.max(0, goal - dashboardData(data, user, () => '').today.attempts);
            incomplete = remaining > 0;
            job.title = `Your daily ${goal} questions`;
            job.body = `${remaining} of your ${goal} questions today are still to be done. Keep your streak going!`;
          }
          const devices = active && validChallenge && incomplete ? (data.pushSubscriptions ?? []).filter(device => device.userId === job.userId) : [];
          job.deliveryStatus = devices.length ? 'sending' : 'skipped';
          if (!devices.length) job.skipReason = !active ? 'preference-disabled' : !validChallenge ? 'invitation-unavailable' : !incomplete ? 'goal-completed' : 'no-devices';
          return { job, devices };
        });
        if (!delivery) break;
        const { job, devices } = delivery;
        if (!devices.length) {
          if (job.kind === 'challenges') console.info('Challenge push skipped', { reason: job.skipReason });
          continue;
        }
        const expired = [];
        let accepted = 0;
        await Promise.all(devices.map(async device => {
          try {
            await transport(validateSubscription(device.subscription), JSON.stringify({ title: job.title, body: job.body, url: job.url, tag: job.group }), {
              TTL: Math.max(0, Math.floor((job.expiresAt - Date.now()) / 1000)), timeout: 10000,
              agent: pushAgent,
              urgency: job.kind === 'daily' ? 'normal' : 'high',
            });
            accepted++;
          } catch (error) {
            if ([404, 410].includes(error.statusCode)) expired.push(device.id);
            else console.warn('Push delivery failed', { kind: job.kind, status: error.statusCode || 'network' });
          }
        }));
        await change(data => {
          const savedJob = (data.pushQueue ?? []).find(item => item.id === job.id);
          if (savedJob) Object.assign(savedJob, { deliveryStatus: accepted === devices.length ? 'accepted' : accepted ? 'partial' : 'failed',
            acceptedDevices: accepted, attemptedDevices: devices.length, processedAt: Date.now() });
          if (expired.length) data.pushSubscriptions = (data.pushSubscriptions ?? []).filter(device => !expired.includes(device.id));
        });
      }
    } catch (error) { console.warn('Push worker paused', { status: error.status || 'storage' }); }
    finally { running = false; }
  }
  return { configured, handle, tick };
}
