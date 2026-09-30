import { createHash, randomBytes } from 'node:crypto';

export class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

export async function readJson(request, limit = 256 * 1024) {
  if (request.parsedBody !== undefined) return request.parsedBody;
  if (request.headers['content-encoding'] && request.headers['content-encoding'] !== 'identity') {
    throw new HttpError(415, 'Compressed request bodies are not supported.');
  }
  if (Number(request.headers['content-length']) > limit) throw new HttpError(413, 'Request body is too large.');
  const chunks = [];
  let size = 0;
  // Do not destroy the socket before the caller can send the error response.
  for await (const chunk of request.iterator({ destroyOnReturn: false })) {
    size += chunk.length;
    if (size > limit) throw new HttpError(413, 'Request body is too large.');
    chunks.push(chunk);
  }
  if (!size) return {};
  if (request.headers['content-type']?.split(';')[0].trim().toLowerCase() !== 'application/json') {
    throw new HttpError(415, 'Use application/json.');
  }
  let value;
  try { value = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch { throw new HttpError(400, 'Invalid JSON body.'); }
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new HttpError(400, 'Send a JSON object.');
  return value;
}

export function createLimiter({ now = Date.now, maxKeys = 10000 } = {}) {
  const entries = new Map();
  return (key, limit, windowMs) => {
    const time = now();
    let entry = entries.get(key);
    if (!entry || entry.until <= time) {
      if (entries.size >= maxKeys) {
        for (const [id, item] of entries) if (item.until <= time) entries.delete(id);
        if (entries.size >= maxKeys) throw new HttpError(429, 'Server is busy. Please try again later.');
      }
      entry = { count: 0, until: time + windowMs };
      entries.set(key, entry);
    }
    if (++entry.count > limit) {
      const error = new HttpError(429, 'Too many requests. Please try again later.');
      error.retryAfter = Math.ceil((entry.until - time) / 1000);
      throw error;
    }
  };
}

export const sessionHash = token => createHash('sha256').update(token).digest('hex');
export const SESSION_SECONDS = 7 * 24 * 60 * 60;
export function issueSession(database, userId, now = Date.now()) {
  // Retire indefinite legacy sessions and expired entries on authentication.
  for (const [key, session] of Object.entries(database.sessions)) {
    if (!session || typeof session !== 'object' || session.expiresAt <= now) delete database.sessions[key];
  }
  const own = Object.entries(database.sessions).filter(([, s]) => s.userId === userId).sort((a, b) => a[1].expiresAt - b[1].expiresAt);
  for (const [key] of own.slice(0, Math.max(0, own.length - 4))) delete database.sessions[key];
  const token = randomBytes(32).toString('hex');
  database.sessions[sessionHash(token)] = { userId, expiresAt: now + SESSION_SECONDS * 1000 };
  return token;
}
export function sessionToken(request) {
  const cookie = (request.headers.cookie ?? '').split(';').map(part => part.trim()).find(part => part.startsWith('medicomm_session='));
  const token = cookie?.slice('medicomm_session='.length) ?? request.headers.authorization?.match(/^Bearer ([a-f0-9]{64})$/)?.[1];
  return /^[a-f0-9]{64}$/.test(token ?? '') ? token : null;
}
export function sessionUser(request, database, now = Date.now()) {
  const token = sessionToken(request);
  const session = token && database.sessions[sessionHash(token)];
  if (!session || typeof session !== 'object' || !Number.isFinite(session.expiresAt) || session.expiresAt <= now) return null;
  return database.users.find(user => user.id === session.userId) ?? null;
}
export function sessionCookie(token, production, clear = false) {
  return `medicomm_session=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${clear ? 0 : SESSION_SECONDS}${production ? '; Secure' : ''}`;
}

export function checkOrigin(request, response, origins) {
  const origin = request.headers.origin;
  if (origin && !origins.has(origin)) throw new HttpError(403, 'Origin is not allowed.');
  if (origin) {
    response.setHeader('Access-Control-Allow-Origin', origin);
    response.setHeader('Access-Control-Allow-Credentials', 'true');
    response.setHeader('Vary', 'Origin');
  }
  if (request.headers['sec-fetch-site'] === 'cross-site' && (!['GET', 'HEAD', 'OPTIONS'].includes(request.method) || request.headers.cookie?.includes('medicomm_session='))) {
    throw new HttpError(403, 'Cross-site requests are not allowed.');
  }
  // Cookie mutations need an Origin; API clients can use bearer authentication.
  if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method) && request.headers.cookie?.includes('medicomm_session=') && !origin) {
    throw new HttpError(403, 'An Origin header is required.');
  }
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
}
