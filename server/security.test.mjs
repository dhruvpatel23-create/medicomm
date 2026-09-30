import test from 'node:test';
import assert from 'node:assert/strict';
import { Readable } from 'node:stream';
import { readJson, createLimiter, issueSession, sessionUser, sessionHash, sessionCookie, checkOrigin } from './security.mjs';
import { createStateStore } from './stateStore.mjs';
import { decodeImage, createUploads } from './uploads.mjs';

function body(text, headers = {}) {
  const request = Readable.from([Buffer.from(text)]);
  request.headers = { 'content-type': 'application/json', ...headers };
  return request;
}
test('JSON rejects oversized, malformed, non-object and wrong-type bodies', async () => {
  assert.deepEqual(await readJson(body('{"ok":true}')), { ok: true });
  await assert.rejects(readJson(body('x'.repeat(20)), 10), { status: 413 });
  await assert.rejects(readJson(body('{}', { 'content-length': '999' }), 10), { status: 413 });
  for (const text of ['null', '[]', 'true', '{']) await assert.rejects(readJson(body(text)), { status: 400 });
  await assert.rejects(readJson(body('{}', { 'content-type': 'text/plain' })), { status: 415 });
});
test('rate limits expire and stay bounded without evicting live limits', () => {
  let now = 0;
  const limit = createLimiter({ now: () => now, maxKeys: 1 });
  limit('a', 1, 1000);
  assert.throws(() => limit('a', 1, 1000), { status: 429 });
  assert.throws(() => limit('b', 1, 1000), { status: 429 });
  now = 1001; limit('b', 1, 1000);
});
test('sessions hash credentials, expire, revoke and reject legacy sessions', () => {
  const database = { users: [{ id: 'alice' }], sessions: { legacy: 'alice' } };
  const token = issueSession(database, 'alice', 100);
  assert.equal(database.sessions[token], undefined);
  assert.equal(database.sessions.legacy, undefined);
  const request = { headers: { cookie: `medicomm_session=${token}` } };
  assert.equal(sessionUser(request, database, 101).id, 'alice');
  assert.equal(sessionUser(request, database, 1e12), null);
  delete database.sessions[sessionHash(token)];
  assert.equal(sessionUser(request, database, 101), null);
  assert.match(sessionCookie(token, true), /HttpOnly; SameSite=Lax; Max-Age=604800; Secure/);
});
test('CORS rejects untrusted origins and cookie CSRF including missing Origin', () => {
  const response = { setHeader() {} };
  const origins = new Set(['https://app.example']);
  checkOrigin({ method: 'POST', headers: { origin: 'https://app.example' } }, response, origins);
  assert.throws(() => checkOrigin({ method: 'POST', headers: { origin: 'https://evil.example' } }, response, origins), { status: 403 });
  assert.throws(() => checkOrigin({ method: 'POST', headers: { cookie: 'medicomm_session=x' } }, response, origins), { status: 403 });
});
test('simultaneous snapshots cannot overwrite a committed update', async () => {
  let writes = 0;
  const store = createStateStore({ initial: { value: 0 }, persist: async () => { writes++; } });
  const first = store.read(), second = store.read();
  first.value = 1; second.value = 2;
  const results = await Promise.allSettled([store.write(first), store.write(second)]);
  assert.equal(results[0].status, 'fulfilled');
  assert.equal(results[1].reason.status, 409);
  assert.equal(store.read().value, 1);
  assert.equal(writes, 1);
});
test('uncommitted writes stay invisible and persistence failures close the store', async () => {
  let release;
  const store = createStateStore({ initial: { value: 0 }, persist: () => new Promise((resolve, reject) => { release = reject; }) });
  const snapshot = store.read(); snapshot.value = 1;
  const write = store.write(snapshot);
  await Promise.resolve();
  assert.equal(store.read().value, 0);
  release(new Error('disk failure'));
  await assert.rejects(write, { status: 503 });
  assert.equal(store.healthy, false);
  assert.throws(() => store.read(), { status: 503 });
});
test('uncertain remote writes reload committed data before accepting another write', async () => {
  const store = createStateStore({ initial: { value: 0 }, persist: async () => { throw new Error('response lost'); }, reload: async () => ({ data: { value: 1 }, revision: 1 }) });
  await assert.rejects(store.write(store.read()), { status: 503 });
  assert.equal(store.healthy, true);
  assert.equal(store.read().value, 1);
});
test('uploads reject MIME spoofing, SVG and excessive size; storage failures propagate', async () => {
  assert.throws(() => decodeImage('data:image/png;base64,aGVsbG8='), { status: 400 });
  assert.throws(() => decodeImage('data:image/svg+xml;base64,PHN2Zz4='), { status: 400 });
  assert.throws(() => decodeImage('data:image/png;base64,' + 'A'.repeat(8 * 1024 * 1024)), { status: 400 });
  const png = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=';
  assert.equal(decodeImage(png).extension, 'png');
  const uploads = createUploads({ url: 'https://storage.example', key: 'test', bucket: 'private', fetchImpl: async () => new Response('', { status: 500 }) });
  await assert.rejects(uploads.save(png), { status: 503 });
});
