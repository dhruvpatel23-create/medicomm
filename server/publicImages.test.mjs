import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { servePublicImage } from './publicImages.mjs';
import { createStateStore } from './stateStore.mjs';

test('public images stream, cache, revalidate, and retain source precedence', async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medulla-images-'));
  const primary = path.join(directory, 'primary.png');
  const fallback = path.join(directory, 'fallback.png');
  await writeFile(primary, 'current image');
  await writeFile(fallback, 'old image');
  const server = createServer((req, res) => {
    const candidates = req.url === '/missing' ? [path.join(directory, 'missing.png')] : [primary, fallback];
    servePublicImage(req, res, candidates, () => 'image/png').catch(error => res.destroy(error));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(async () => {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
    await rm(directory, { recursive: true, force: true });
  });
  const url = `http://127.0.0.1:${server.address().port}`;
  const first = await fetch(url);
  assert.equal(await first.text(), 'current image');
  assert.equal(first.headers.get('content-type'), 'image/png');
  assert.match(first.headers.get('cache-control'), /public, max-age=3600/);
  const etag = first.headers.get('etag');
  const cached = await fetch(url, { headers: { 'If-None-Match': etag } });
  assert.equal(cached.status, 304);
  assert.equal(await cached.text(), '');
  const head = await fetch(url, { method: 'HEAD' });
  assert.equal(head.headers.get('content-length'), '13');
  assert.equal(await head.text(), '');
  await writeFile(primary, 'corrected illustration');
  const changed = await fetch(url, { headers: { 'If-None-Match': etag } });
  assert.equal(changed.status, 200);
  assert.equal(await changed.text(), 'corrected illustration');
  await rm(primary);
  assert.equal(await (await fetch(url)).text(), 'old image');
  assert.equal((await fetch(`${url}/missing`)).status, 404);
});

test('private image index follows committed state and recovered writes', async () => {
  const initial = { users: [{ profileImagePath: 'legacy.png' }], communities: [{ messages: [{ imagePath: 'attachment.png' }] }] };
  const store = createStateStore({ initial, persist: async () => {} });
  assert.equal(store.isPrivateImage('user-new.png'), true);
  assert.equal(store.isPrivateImage('legacy.png'), true);
  assert.equal(store.isPrivateImage('attachment.png'), true);
  assert.equal(store.isPrivateImage('atlas.png'), false);
  const snapshot = store.read();
  snapshot.users[0].profileImagePath = 'updated.png';
  assert.equal(store.isPrivateImage('updated.png'), false);
  await store.write(snapshot);
  assert.equal(store.isPrivateImage('updated.png'), true);
  assert.equal(store.isPrivateImage('legacy.png'), false);
  const recovered = createStateStore({ initial, persist: async () => { throw new Error('lost response'); }, reload: async () => ({ data: snapshot, revision: 1 }) });
  await assert.rejects(recovered.write(recovered.read()));
  assert.equal(recovered.isPrivateImage('updated.png'), true);
  const unhealthy = createStateStore({ initial, persist: async () => { throw new Error('offline'); } });
  await assert.rejects(unhealthy.write(unhealthy.read()));
  assert.throws(() => unhealthy.isPrivateImage('atlas.png'), /Storage is unavailable/);
});
