import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtemp, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { once } from 'node:events';
import { createServer } from 'node:http';

test('real HTTP: auth, persistence, origins, limits, uploads and logout', { timeout: 30000 }, async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medicomm-test-'));
  await writeFile(path.join(directory, 'users.json'), JSON.stringify({ users: [], sessions: {} }));
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: new URL('..', import.meta.url),
    env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', RUNTIME_DATA_DIR: directory, PORT: '0', HOST: '127.0.0.1', SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '', APP_ORIGINS: 'http://localhost:5173', TRUST_PROXY: 'false' },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  t.after(async () => { if (child.exitCode === null) { child.kill(); await once(child, 'exit'); } await rm(directory, { recursive: true, force: true }); });
  let output = '';
  const address = await new Promise((resolve, reject) => {
    child.on('error', reject);
    child.once('exit', code => reject(new Error(`Server exited: ${code}: ${output}`)));
    child.stderr.on('data', chunk => { output += chunk; });
    child.stdout.on('data', chunk => { output += chunk; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) resolve(`http://127.0.0.1:${match[1]}`); });
  });
  let cookie = '';
  const call = (route, method = 'GET', payload, extra = {}) => fetch(address + route, { method, headers: { 'Content-Type': 'application/json', Origin: 'http://localhost:5173', ...(cookie ? { Cookie: cookie } : {}), ...extra }, body: payload === undefined ? undefined : JSON.stringify(payload) });
  assert.equal((await call('/health/ready')).status, 200);
  assert.equal((await call('/api/auth/session')).status, 401);
  assert.equal((await call('/api/dashboard')).status, 401);
  assert.equal((await call('/api/auth/login', 'POST', {}, { Origin: 'https://evil.example' })).status, 403);
  assert.equal((await call('/api/auth/login', 'POST', null)).status, 400);
  assert.equal((await call('/api/auth/login', 'POST', { password: 'x'.repeat(300000) })).status, 413);
  const payload = { name: 'Test Learner', email: 'test@example.test', medicalCollege: 'Test College', contactNumber: '9000000001', password: 'A-long-test-password' };
  const signup = await call('/api/auth/signup', 'POST', payload);
  assert.equal(signup.status, 201);
  const result = await signup.json();
  assert.equal(result.token, undefined);
  assert.equal(result.user.passwordHash, undefined);
  cookie = signup.headers.get('set-cookie').split(';')[0];
  assert.match(signup.headers.get('set-cookie'), /HttpOnly/);
  assert.equal((await call('/api/auth/session')).status, 200);
  const emptyDashboard = await (await call('/api/dashboard')).json();
  assert.equal(emptyDashboard.stats.attempted, 0);
  assert.equal(emptyDashboard.stats.streak, 0);
  assert.equal((await call('/api/dashboard/goal', 'PATCH', { exam: 'Test exam', date: '2027-03-01', weeklyTarget: 150 })).status, 200);
  assert.equal((await call('/api/dashboard/goal', 'PATCH', { exam: 'Test exam', date: '2027-02-30', weeklyTarget: 150 })).status, 400);
  const bank = await (await call('/api/practice')).json();
  const subject = bank.subjects.find(subject => subject.questions.length);
  const question = subject.questions[0];
  const attempt = { id: 'http-attempt-001', subjectId: subject.id, questionId: question.id, mode: 'pyq', selectedAnswer: question.answer, durationSeconds: 90 };
  assert.equal((await call('/api/practice/attempts', 'POST', attempt)).status, 200);
  assert.equal((await call('/api/practice/attempts', 'POST', attempt)).status, 200);
  const dashboard = await (await call('/api/dashboard')).json();
  assert.equal(dashboard.stats.attempted, 1); assert.equal(dashboard.stats.correct, 1);
  assert.equal(dashboard.today.seconds, 90); assert.equal(dashboard.goal.exam, 'Test exam');
  assert.equal(dashboard.recent[0].questionId, question.id);
  const saved = JSON.parse(await readFile(path.join(directory, 'users.json'), 'utf8'));
  assert.equal(saved.users.length, 1);
  assert.equal(saved.users[0].passwordIterations, 220000);
  assert.equal(JSON.stringify(saved).includes(cookie.split('=')[1]), false);
  const image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=';
  const profile = await call('/api/profile', 'PATCH', { ...payload, profileImageDataUrl: image });
  assert.equal(profile.status, 200);
  const imageUrl = (await profile.json()).user.profileImageUrl;
  assert.equal((await call(imageUrl)).status, 200);
  assert.equal((await fetch(address + imageUrl)).status, 401);
  assert.deepEqual(await (await call('/api/storage/status')).json(), { status: 'ready' });
  assert.equal((await call('/api/auth/logout', 'POST', {})).status, 200);
  assert.equal((await call('/api/auth/session')).status, 401);
  assert.equal((await call('/api/auth/login', 'POST', { email: payload.email, password: payload.password })).status, 200);
  for (let i = 0; i < 20; i++) await call('/api/auth/login', 'POST', {});
  assert.equal((await call('/api/auth/login', 'POST', {})).status, 429);
});

test('production refuses startup without required configuration', { timeout: 10000 }, async () => {
  const child = spawn(process.execPath, ['server.mjs'], { cwd: new URL('..', import.meta.url), env: { ...process.env, NODE_ENV: 'production', SUPABASE_URL: '', APP_ORIGINS: '', SUPABASE_UPLOAD_BUCKET: '' }, stdio: 'ignore' });
  const [code] = await once(child, 'exit');
  assert.notEqual(code, 0);
});

test('remote storage outages fail readiness and never acknowledge failed writes', { timeout: 30000 }, async t => {
  let outage = false;
  const remote = createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (outage) { res.writeHead(503); res.end('{}'); return; }
    if (req.url.startsWith('/storage/')) { res.end('{"public":false}'); return; }
    res.end(JSON.stringify([{ data: { users: [], sessions: {} }, revision: 0 }]));
  });
  remote.listen(0, '127.0.0.1'); await once(remote, 'listening');
  const directory = await mkdtemp(path.join(tmpdir(), 'medicomm-outage-'));
  const local = JSON.stringify({ users: [], sessions: {} });
  await writeFile(path.join(directory, 'users.json'), local);
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: new URL('..', import.meta.url),
    env: { ...process.env, NODE_ENV: 'production', RUNTIME_DATA_DIR: directory, PORT: '0', HOST: '127.0.0.1', SUPABASE_URL: `http://127.0.0.1:${remote.address().port}`, SUPABASE_SECRET_KEY: 'fake-test-key', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '', APP_ORIGINS: '', RENDER_EXTERNAL_URL: 'https://app.example' },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  t.after(async () => {
    if (child.exitCode === null) { child.kill(); await once(child, 'exit'); }
    remote.closeAllConnections(); await new Promise(resolve => remote.close(resolve));
    await rm(directory, { recursive: true, force: true });
  });
  const address = await new Promise((resolve, reject) => {
    let output = '';
    child.once('error', reject);
    child.once('exit', code => reject(new Error(`Server exited ${code}: ${output}`)));
    child.stderr.on('data', chunk => { output += chunk; });
    child.stdout.on('data', chunk => { output += chunk; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) resolve(`http://127.0.0.1:${match[1]}`); });
  });
  assert.equal((await fetch(address + '/health/ready')).status, 200);
  // Module scripts send Origin even on the same site. Public custom domains
  // must load the HTML's actual script, not receive a JSON origin rejection.
  const html = await (await fetch(address + '/')).text();
  const script = html.match(/<script[^>]+src="([^"]+)"/);
  assert.ok(script, 'built HTML includes a module script');
  for (const origin of ['https://medullaprep.com', 'https://www.medullaprep.com']) {
    const asset = await fetch(address + script[1], { headers: { Origin: origin } });
    assert.equal(asset.status, 200);
    assert.match(asset.headers.get('content-type'), /javascript/);
    assert.equal((await fetch(address + '/api/auth/session', { headers: { Origin: origin } })).status, 401);
  }
  assert.equal((await fetch(address + script[1], { headers: { Origin: 'https://untrusted.example' } })).status, 403);
  outage = true;
  assert.equal((await fetch(address + '/health/live')).status, 200);
  assert.equal((await fetch(address + '/health/ready')).status, 503);
  const signup = await fetch(address + '/api/auth/signup', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://app.example' }, body: JSON.stringify({ name: 'Test', email: 'test@example.test', password: 'long-test-password', medicalCollege: 'College', contactNumber: '9000000001' }) });
  assert.equal(signup.status, 503);
  assert.equal(signup.headers.get('set-cookie'), null);
  assert.equal(await readFile(path.join(directory, 'users.json'), 'utf8'), local);
});
