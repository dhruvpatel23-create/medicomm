import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { once } from 'node:events';

test('HTTP signup waits for OTP, persists verification, and sets a session only after verification', { timeout: 45000 }, async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medulla-email-'));
  const mailFile = path.join(directory, 'mail.json'), preload = path.join(directory, 'mock-email.mjs');
  await writeFile(path.join(directory, 'users.json'), JSON.stringify({ users: [], sessions: {} }));
  await writeFile(preload, `import { writeFile } from 'node:fs/promises';
const original = globalThis.fetch;
globalThis.fetch = async (url, options) => {
  if (url !== 'https://api.resend.com/emails') return original(url, options);
  await writeFile(${JSON.stringify(mailFile)}, options.body, { mode: 0o600 });
  return new Response(JSON.stringify({ id: 'mock-delivery' }), { status: 200 });
};`);
  const child = spawn(process.execPath, ['--import', pathToFileURL(preload).href, 'server.mjs'], {
    cwd: new URL('..', import.meta.url),
    env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', RUNTIME_DATA_DIR: directory, PORT: '0', HOST: '127.0.0.1',
      SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '',
      APP_ORIGINS: 'http://localhost:5173', EMAIL_VERIFICATION_REQUIRED: 'true', RESEND_API_KEY: 'mock-key', EMAIL_FROM: 'Medulla <noreply@example.test>', EMAIL_OTP_SECRET: 'test-otp-secret-with-at-least-32-characters' },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  t.after(async () => { if (child.exitCode === null) { child.kill(); await once(child, 'exit'); } await rm(directory, { recursive: true, force: true }); });
  let output = '';
  const base = await new Promise((resolve, reject) => {
    child.on('error', reject); child.once('exit', code => reject(new Error(`Server exited ${code}: ${output}`)));
    child.stderr.on('data', data => { output += data; });
    child.stdout.on('data', data => { output += data; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) resolve(`http://127.0.0.1:${match[1]}`); });
  });
  const call = (route, body) => fetch(base + route, { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'http://localhost:5173' }, body: JSON.stringify(body) });
  const signup = await call('/api/auth/signup', { name: 'Email Learner', email: 'learner@example.test', password: 'Strong1!pass', contactNumber: '9000000001', medicalCollege: 'College', mbbsBatch: 2023 });
  assert.equal(signup.status, 202); assert.equal(signup.headers.get('set-cookie'), null);
  const challenge = await signup.json();
  assert.equal(JSON.parse(await readFile(path.join(directory, 'users.json'))).users.length, 0);
  const email = JSON.parse(await readFile(mailFile));
  const code = email.text.match(/code is: (\d{6})/)[1];
  assert(!output.includes(code)); assert(!JSON.stringify(challenge).includes('password'));
  const verified = await call('/api/auth/verify-email', { challengeId: challenge.challengeId, code });
  assert.equal(verified.status, 200); assert.match(verified.headers.get('set-cookie'), /medicomm_session=.*HttpOnly/);
  assert.equal((await verified.json()).user.email, 'learner@example.test');
  const saved = JSON.parse(await readFile(path.join(directory, 'users.json')));
  assert(saved.users[0].emailVerifiedAt); assert.equal(saved.emailChallenges.length, 0);
  assert.equal((await call('/api/auth/verify-email', { challengeId: challenge.challengeId, code })).status, 400);
  assert.equal((await call('/api/auth/login', { email: 'learner@example.test', password: 'Strong1!pass' })).status, 200);
});
