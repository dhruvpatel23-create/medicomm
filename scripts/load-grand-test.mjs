// Local-only HTTP capacity smoke test. Never connects to a deployment or real data.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { pbkdf2Sync, randomUUID } from 'node:crypto';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { once } from 'node:events';
import { performance } from 'node:perf_hooks';

const root = new URL('../', import.meta.url);
const directory = await mkdtemp(path.join(tmpdir(), 'medulla-load-'));
const sizes = [20, 50, 100];
const password = 'Synthetic-load-test1!';
const salt = randomUUID(), hash = pbkdf2Sync(password, salt, 220000, 64, 'sha512').toString('hex');
const users = sizes.flatMap(size => Array.from({ length: size }, (_, index) => ({
  id: `load-${size}-${index}`, name: `Load ${size} ${index}`, username: `load_${size}_${index}`,
  email: `load-${size}-${index}@example.test`, emailVerifiedAt: new Date().toISOString(),
  passwordHash: hash, passwordSalt: salt, passwordIterations: 220000,
})));
await writeFile(path.join(directory, 'users.json'), JSON.stringify({ users, sessions: {} }));
const child = spawn(process.execPath, ['server.mjs'], { cwd: root,
  env: { ...process.env, NODE_ENV: 'test', DATABASE_PROVIDER: 'local', LOAD_ENV_FILES: 'false',
    RUNTIME_DATA_DIR: directory, HOST: '127.0.0.1', PORT: '0', APP_ORIGINS: 'http://localhost:5173',
    SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '',
    SUPABASE_UPLOAD_BUCKET: '', TRUST_PROXY: 'false', RESEND_API_KEY: '', VAPID_PUBLIC_KEY: '', VAPID_PRIVATE_KEY: '' },
  stdio: ['ignore', 'pipe', 'pipe'] });
const report = { scope: 'isolated local HTTP; synthetic accounts; local filesystem storage; not production certification', node: process.version, phases: [] };
try {
  const address = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Local server startup timed out')), 30000);
    let output = '';
    child.once('error', error => { clearTimeout(timer); reject(error); });
    child.once('exit', code => { clearTimeout(timer); reject(new Error(`Local server exited ${code}: ${output.slice(-2000)}`)); });
    child.stdout.on('data', chunk => {
      output = (output + chunk).slice(-8000);
      const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/);
      if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); }
    });
    child.stderr.on('data', () => {});
  });
  async function call(candidate, route, body, method = 'POST') {
    const response = await fetch(address + route, { method, signal: AbortSignal.timeout(20000),
      headers: { 'Content-Type': 'application/json', Origin: 'http://localhost:5173', ...(candidate.cookie ? { Cookie: candidate.cookie } : {}) },
      body: body === undefined ? undefined : JSON.stringify(body) });
    const data = await response.json();
    if (!response.ok) throw new Error(`${response.status}: ${data.message}`);
    if (response.headers.get('set-cookie')) candidate.cookie = response.headers.get('set-cookie').split(';')[0];
    if (data.attempt) candidate.attempt = data.attempt;
    return data;
  }
  async function phase(size, name, candidates, operation) {
    const latencies = [], errors = [];
    const started = performance.now();
    await Promise.all(candidates.map(async candidate => {
      const start = performance.now();
      try { await operation(candidate); } catch (error) { errors.push(error.message); }
      latencies.push(performance.now() - start);
    }));
    latencies.sort((a, b) => a - b);
    const row = { users: size, phase: name, requests: candidates.length, failures: errors.length,
      wallMs: Math.round(performance.now() - started), p95Ms: Math.round(latencies[Math.ceil(latencies.length * .95) - 1]), maxMs: Math.round(latencies.at(-1)),
      ...(errors.length ? { errors: [...new Set(errors)] } : {}) };
    report.phases.push(row); console.log(JSON.stringify(row));
    assert.equal(errors.length, 0, `${name}: ${errors[0]}`);
  }
  for (const size of sizes) {
    const candidates = users.filter(user => user.id.startsWith(`load-${size}-`)).map(user => ({ user }));
    await phase(size, 'simultaneous login behind one IP', candidates, candidate => call(candidate, '/api/auth/login', { email: candidate.user.email, password }));
    await phase(size, 'start grand test', candidates, candidate => call(candidate, '/api/practice/fmge-tests/fmge-grand-test-1/start', { startKey: randomUUID() }));
    for (const part of [1, 2]) {
      if (part === 2) await phase(size, 'start part 2', candidates, candidate => call(candidate, `/api/practice/fmge-tests/attempts/${candidate.attempt.id}/next-part`, {}));
      for (let offset = 0; offset < 150; offset += 50) {
        await phase(size, `part ${part} batch ${offset / 50 + 1}`, candidates, async candidate => {
          const attempt = candidate.attempt;
          const body = { revision: attempt.revision, mutationId: randomUUID(), changes: attempt.questions.slice(offset, offset + 50).map(question => ({ questionId: question.id, optionIndex: 0 })) };
          await call(candidate, `/api/practice/fmge-tests/attempts/${attempt.id}`, body, 'PATCH');
        });
      }
      await phase(size, `submit part ${part}`, candidates, async candidate => {
        assert.equal(Object.keys(candidate.attempt.answers).length, part * 150);
        await call(candidate, `/api/practice/fmge-tests/attempts/${candidate.attempt.id}/finish-part`, { part });
        assert.equal(candidate.attempt.status, part === 1 ? 'break' : 'completed');
      });
    }
  }
} finally {
  if (child.exitCode === null) { child.kill(); await once(child, 'exit'); }
  // Only remove the verified directory allocated by mkdtemp above.
  assert.ok(path.resolve(directory).startsWith(path.resolve(tmpdir()) + path.sep));
  await rm(directory, { recursive: true, force: true });
  await mkdir(new URL('../output/', import.meta.url), { recursive: true });
  await writeFile(new URL('../output/server-reliability-load.json', import.meta.url), JSON.stringify(report, null, 2));
}
