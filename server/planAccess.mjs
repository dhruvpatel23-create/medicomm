import { canAccessFeature, requiredPlans, FEATURE_NAMES } from '../src/data/planAccess.js';
import { subscriptionDetails } from './subscriptions.mjs';
import { HttpError } from './security.mjs';

export function isTrialPracticeRoute(pathname, method) {
  return (pathname === '/api/practice' && method === 'GET')
    || (pathname === '/api/practice/attempts' && method === 'POST');
}

export function requireFeature(database, userId, feature) {
  if (!canAccessFeature(subscriptionDetails(database, userId), feature)) {
    throw new HttpError(403, `${FEATURE_NAMES[feature]} requires ${requiredPlans(feature)}.`);
  }
}

export function routeFeature(pathname, method, searchParams = new URLSearchParams()) {
  if (/^\/api\/(?:viva|clinical-cases|short-notes)\//.test(pathname) || /\/short-notes\.json$/i.test(pathname)) return 'theory';
  // FMGE mixes free scheduled tests with premium practice attempts. Its handler
  // enforces access per test rather than locking the entire directory.
  if (/^\/api\/practice\/neetpg-tests(?:\/|$)/.test(pathname)) return 'tests';
  if (/\/practice-question-bank\.json$/i.test(pathname)) return 'usmle';
  if (method !== 'GET' && method !== 'HEAD') {
    if (/^\/api\/communities(?:\/|$)/.test(pathname)) return 'community';
    if (/^\/api\/direct-messages(?:\/|$)/.test(pathname)) return 'inbox';
  }
  return null;
}
