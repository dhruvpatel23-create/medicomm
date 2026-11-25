import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { randomBytes } from 'node:crypto';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { issueSession } from './security.mjs';

test('a scoped invite lets one guest play the selected subjects without an account', { timeout: 300000 }, async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medulla-link-duel-'));
  const databaseFile = path.join(directory, 'users.json');
  const seed = {
    users: [
      { id: 'host', name: 'Room Host', email: 'host@example.test', rating: 1530, attemptedQuestions: 17 },
      { id: 'visitor', name: 'Registered Visitor', email: 'visitor@example.test', rating: 1600 },
    ],
    sessions: {},
  };
  const host = issueSession(seed, 'host');
  const visitor = issueSession(seed, 'visitor');
  await writeFile(databaseFile, JSON.stringify(seed));
  const origin = 'http://127.0.0.1:4173';
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: new URL('..', import.meta.url), windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', DATABASE_PROVIDER: 'local',
      UPLOAD_STORAGE: 'local', RUNTIME_DATA_DIR: directory, HOST: '127.0.0.1', PORT: '0', APP_ORIGINS: origin },
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
  async function call(route, { user, guestKey, body } = {}) {
    const response = await fetch(base + route, {
      method: body ? 'POST' : 'GET',
      headers: { Origin: origin, ...(user && { Cookie: `medicomm_session=${user}` }),
        ...(guestKey && { 'X-Duel-Guest': guestKey }), ...(body && { 'Content-Type': 'application/json' }) },
      body: body ? JSON.stringify(body) : undefined,
    });
    return { status: response.status, body: await response.json() };
  }
  const options = await call('/api/duels/challenge/options', { user: host });
  assert.equal(options.status, 200);
  const subject = options.body.subjects.find(item => item.questionCount >= 10);
  assert.ok(subject);
  const settings = { subjectIds: [subject.id], questionCount: 10 };
  const create = (body = settings) => call('/api/duels/link/create', { user: host, body });
  assert.equal((await call('/api/duels/link/create', { body: settings })).status, 401);
  assert.equal((await create({ ...settings, subjectIds: ['invalid'] })).status, 400);
  const created = await create();
  assert.equal(created.status, 201, created.body.message);
  const { id, invite } = created.body;
  const waitingPath = `/api/duels/challenge/status?id=${id}`;
  assert.equal((await call(waitingPath, { user: host })).body.status, 'waiting');
  assert.equal((await call(waitingPath, { user: visitor })).status, 403);
  assert.equal((await call('/api/tokens', { user: host })).body.tokens.remaining, 20);

  const guestA = randomBytes(32).toString('hex');
  const guestB = randomBytes(32).toString('hex');
  const join = (guestKey, user, link = invite) => call('/api/duels/link/join', { user, body: { invite: link, guestKey } });
  assert.equal((await join(guestA, host)).status, 409);
  const joins = await Promise.all([join(guestA, visitor), join(guestB)]);
  assert.deepEqual(joins.map(result => result.status).sort(), [200, 409]);
  const joinedIndex = joins.findIndex(result => result.status === 200);
  const guestKey = [guestA, guestB][joinedIndex];
  const otherKey = [guestB, guestA][joinedIndex];
  const { sessionId } = joins[joinedIndex].body;
  assert.equal((await join(guestKey)).body.sessionId, sessionId);
  assert.equal((await join(otherKey)).status, 409);
  const room = await call(waitingPath, { user: host });
  assert.equal(room.body.duelId, sessionId);
  assert.equal(room.body.opponent.name, 'Guest');
  assert.equal((await call('/api/duels/link/cancel', { user: host, body: { challengeId: id } })).status, 409);
  assert.equal((await call('/api/tokens', { user: host })).body.tokens.remaining, 15);

  const questionsPath = `/api/duels/questions?session=${sessionId}`;
  const questions = await call(questionsPath, { user: host });
  const guestQuestions = await call(questionsPath, { guestKey });
  assert.equal(guestQuestions.status, 200);
  assert.equal(guestQuestions.body.opponent.name, 'Room Host');
  assert.equal(questions.body.opponent.name, 'Guest');
  assert.equal(questions.body.mode, 'link');
  assert.equal(questions.body.expiresAt, guestQuestions.body.expiresAt);
  assert.deepEqual(questions.body.questions, guestQuestions.body.questions);
  assert.equal(questions.body.questions.length, 10);
  assert.ok(questions.body.questions.every(q => q.subjectId === subject.id && !Object.hasOwn(q, 'answerIndex')));
  assert.equal((await call(questionsPath, { user: visitor })).status, 403);
  assert.equal((await call(questionsPath, { guestKey: otherKey })).status, 401);
  assert.equal((await call('/api/auth/session', { guestKey })).status, 401);

  const questionId = questions.body.questions[0].id;
  const answer = { sessionId, questionId, optionIndex: 0 };
  const replies = await Promise.all([
    call('/api/duels/answer', { user: host, body: answer }),
    call('/api/duels/answer', { guestKey, body: answer }),
  ]);
  assert.deepEqual(replies.map(result => result.status), [200, 200]);
  assert.equal((await call('/api/duels/complete', { guestKey, body: { sessionId } })).body.result, null);
  const finished = await call('/api/duels/complete', { user: host, body: { sessionId } });
  assert.equal(finished.body.result.ratingAffected, false);
  assert.equal(finished.body.result.delta, 0);
  const guestResult = await call(`/api/duels/status?session=${sessionId}`, { guestKey });
  assert.equal(guestResult.body.result.attemptedQuestions, 1);
  assert.equal(guestResult.body.user, null);
  const stored = JSON.parse(await readFile(databaseFile, 'utf8'));
  assert.equal(stored.users.length, 2);
  assert.equal(stored.users.find(user => user.id === 'host').attemptedQuestions, 17);
  assert.equal(stored.users.find(user => user.id === 'host').rating, 1530);
  assert.ok(!JSON.stringify(stored).includes(guestKey) && !JSON.stringify(stored).includes(invite));

  const cancellation = await create();
  assert.equal((await call('/api/duels/link/cancel', { user: visitor, body: { challengeId: cancellation.body.id } })).status, 404);
  assert.equal((await call('/api/duels/link/cancel', { user: host, body: { challengeId: cancellation.body.id } })).status, 200);
  assert.equal((await join(otherKey, undefined, cancellation.body.invite)).status, 410);
});
