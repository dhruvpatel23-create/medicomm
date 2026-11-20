import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { issueSession } from './security.mjs';

test('theory routes serve the source catalog and answer assets even with a stale frontend build', { timeout: 180000 }, async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medulla-theory-publication-'));
  const seed = {
    users: [{ id: 'subscriber', name: 'Subscriber', plan: 'premium' }, { id: 'free', name: 'Trial Learner' }],
    sessions: {},
  };
  const subscriberToken = issueSession(seed, 'subscriber');
  const freeToken = issueSession(seed, 'free');
  await writeFile(path.join(directory, 'users.json'), JSON.stringify(seed));
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: new URL('..', import.meta.url),
    env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', DATABASE_PROVIDER: 'local', UPLOAD_STORAGE: 'local', RUNTIME_DATA_DIR: directory, HOST: '127.0.0.1', PORT: '0' },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  t.after(async () => {
    if (child.exitCode === null && child.signalCode === null && child.pid) {
      child.kill();
      await once(child, 'exit');
    }
    await rm(directory, { recursive: true, force: true });
  });
  let output = '';
  const base = await new Promise((resolve, reject) => {
    child.on('error', reject);
    child.once('exit', code => reject(new Error(`Server exited (${code}): ${output}`)));
    child.stderr.on('data', data => { output += data; });
    child.stdout.on('data', data => {
      output += data;
      const match = output.match(/listening on (http:\/\/127\.0\.0\.1:\d+)/);
      if (match) resolve(match[1]);
    });
  });
  const get = (route, token) => fetch(base + route, { headers: token ? { Cookie: `medicomm_session=${token}` } : {} });
  assert.equal((await get('/short-notes.json')).status, 401);
  const source = await readFile(new URL('../public/short-notes.json', import.meta.url), 'utf8');
  for (const token of [freeToken, subscriberToken]) {
    const response = await get('/short-notes.json', token);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('cache-control'), 'private, no-store');
    assert.equal(await response.text(), source.replace(/^\uFEFF/, ''));
  }

  for (const [asset, type] of [
    ['/theory-answers/medicine/anaphylactic-shock/page-1.webp', 'image/webp'],
    ['/theory-answers/general-surgery/wounds-and-wound-healing/factors-delaying-wound-healing/factors-delaying-wound-healing.pdf', 'application/pdf'],
    ['/theory-answers/general-anatomy-01-synovial-joint/01%20-%20Synovial%20joint.pdf', 'application/pdf'],
  ]) {
    const file = await get(asset);
    assert.equal(file.status, 200, asset);
    assert.equal(file.headers.get('content-type'), type, asset);
    assert.deepEqual(Buffer.from(await file.arrayBuffer()), await readFile(new URL(`../public${asset}`, import.meta.url)));
  }
  assert.equal((await get('/theory-answers/medicine/missing.webp')).status, 404);
});
