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
  if (/^\/api\/practice\/(?:fmge-tests|neetpg-tests)(?:\/|$)/.test(pathname)) return 'tests';
  if (/\/practice-question-bank\.json$/i.test(pathname)) return 'usmle';
  if (method !== 'GET' && method !== 'HEAD') {
    if (/^\/api\/communities(?:\/|$)/.test(pathname)) return 'community';
    if (/^\/api\/direct-messages(?:\/|$)/.test(pathname)) return 'inbox';
  }
  return null;
}
