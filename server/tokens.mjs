import { subscriptionDetails } from './subscriptions.mjs';
import { HttpError } from './security.mjs';

export const TOKEN_WINDOW_MS = 24 * 60 * 60 * 1000;
export const TOKEN_ALLOWANCES = { free: 20, lite: 100, ultra: 200, premium: 300 };

export function tokenStatus(database, userId, now = Date.now()) {
  const membership = subscriptionDetails(database, userId, now);
  const plan = membership.hasPracticeAccess ? String(membership.plan || '').toLowerCase() : 'free';
  const allowance = TOKEN_ALLOWANCES[plan] ?? TOKEN_ALLOWANCES.free;
  const state = database.users.find(user => user.id === userId)?.tokens;
  const active = Number.isFinite(state?.startedAt) && now < state.startedAt + TOKEN_WINDOW_MS;
  const spent = active ? Object.values(state.charges || {}).reduce((sum, charge) => sum + charge, 0) : 0;
  return { allowance, remaining: Math.max(0, allowance - spent), resetsAt: active ? new Date(state.startedAt + TOKEN_WINDOW_MS).toISOString() : null };
}

export function requireTokens(database, userId, cost, now = Date.now()) {
  const status = tokenStatus(database, userId, now);
  if (status.remaining < cost) throw new HttpError(402, `You need ${cost} tokens but have ${status.remaining}. Your tokens reset ${status.resetsAt ? new Date(status.resetsAt).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) + ' IST' : '24 hours after first use'}.`);
}

// Mutate the same database snapshot as the purchased action, then persist once.
export function chargeTokens(database, userId, cost, key, now = Date.now()) {
  const user = database.users.find(user => user.id === userId);
  if (!user) throw new HttpError(401, 'Sign in to use tokens.');
  const status = tokenStatus(database, userId, now);
  if (status.resetsAt && Object.hasOwn(user.tokens.charges, key)) return;
  requireTokens(database, userId, cost, now);
  if (!status.resetsAt) user.tokens = { startedAt: now, charges: {} };
  user.tokens.charges[key] = cost;
}

export function refundTokens(database, userId, key) {
  const state = database.users.find(user => user.id === userId)?.tokens;
  if (state?.charges) delete state.charges[key];
}

export async function updateTokenState(readDatabase, writeDatabase, update) {
  for (let attempt = 0; ; attempt++) {
    const database = readDatabase();
    await update(database);
    try { await writeDatabase(database); return; }
    catch (error) { if (error.status !== 409 || attempt >= 3) throw error; }
  }
}
