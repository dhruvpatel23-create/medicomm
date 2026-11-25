import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { issueSession } from './security.mjs';
import { UNIVERSITY_PREP_SAMPLE_LIMIT, UNIVERSITY_PREP_SUBJECTS } from '../src/data/universityPrep.js';

test('theory routes serve the source library with University Prep access enforced on notes and assets', { timeout: 180000 }, async t => {
  const directory = await mkdtemp(path.join(tmpdir(), 'medulla-theory-publication-'));
  const seed = {
    users: [
      { id: 'subscriber', name: 'Subscriber', plan: 'lite' },
      { id: 'free', name: 'Trial Learner', plan: 'free' },
      { id: 'expired', name: 'Expired Subscriber', plan: 'premium', subscriptionPurchasedAt: '2020-01-01', subscriptionOrderId: 'test-order' },
    ],
    sessions: {},
  };
  const subscriberToken = issueSession(seed, 'subscriber');
  const freeToken = issueSession(seed, 'free');
  const expiredToken = issueSession(seed, 'expired');
  const origin = 'http://127.0.0.1:4173';
  await writeFile(path.join(directory, 'users.json'), JSON.stringify(seed));
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: new URL('..', import.meta.url),
    env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', DATABASE_PROVIDER: 'local', UPLOAD_STORAGE: 'local', RUNTIME_DATA_DIR: directory, HOST: '127.0.0.1', PORT: '0', APP_ORIGINS: origin },
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
  assert.equal((await get('/short-notes.json?subjectId=pathology')).status, 401);
  const source = JSON.parse((await readFile(new URL('../public/short-notes.json', import.meta.url), 'utf8')).replace(/^\uFEFF/, ''));
  const fullResponse = await get('/short-notes.json', subscriberToken);
  assert.equal(fullResponse.status, 200);
  assert.equal(fullResponse.headers.get('cache-control'), 'private, no-store');
  assert.deepEqual(await fullResponse.json(), source);

  const freeCatalog = await (await get('/short-notes.json', freeToken)).json();
  const expiredCatalog = await (await get('/short-notes.json', expiredToken)).json();
  assert.deepEqual(expiredCatalog, freeCatalog);
  for (const { id } of UNIVERSITY_PREP_SUBJECTS) {
    const response = await get(`/short-notes.json?subjectId=${id}`);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('cache-control'), 'private, no-store');
    const guest = await response.json();
    assert.deepEqual(guest.subjects, [freeCatalog.subjects.find(subject => subject.id === id)]);
    const questions = guest.subjects[0].topics.flatMap(topic => topic.questions);
    const samples = questions.filter(question => question.isSample);
    assert.equal(samples.length, UNIVERSITY_PREP_SAMPLE_LIMIT, id);
    assert.ok(samples.every(question => !question.locked && question.answerDocument?.pages?.length));
    assert.ok(questions.filter(question => !question.isSample).every(question => question.locked && !question.answerDocument));
    const samplePage = await get(samples[0].answerDocument.pages[0]);
    assert.equal(samplePage.status, 200, id);
    await samplePage.body.cancel();
  }
  assert.deepEqual(freeCatalog.subjects.find(subject => subject.id === 'pathology'), source.subjects.find(subject => subject.id === 'pathology'));

  const medicineQuestions = source.subjects.find(subject => subject.id === 'general-medicine').topics.flatMap(topic => topic.questions);
  const trialMedicine = freeCatalog.subjects.find(subject => subject.id === 'general-medicine').topics.flatMap(topic => topic.questions);
  const locked = medicineQuestions.find(question => question.answerDocument?.pdf && trialMedicine.find(item => item.id === question.id)?.locked);
  for (const asset of [locked.answerDocument.pdf, locked.answerDocument.pages[0]]) {
    for (const token of [undefined, freeToken, expiredToken]) {
      const response = await get(asset, token);
      assert.equal(response.status, 403, asset);
      assert.match((await response.json()).message, /buy a subscription/i);
    }
    const response = await get(asset, subscriberToken);
    assert.equal(response.status, 200, asset);
    assert.equal(response.headers.get('cache-control'), 'private, no-store');
    await response.body.cancel();
  }
  const review = await fetch(base + '/api/short-notes/reviews', {
    method: 'POST',
    headers: { Cookie: `medicomm_session=${freeToken}`, 'Content-Type': 'application/json', Origin: origin },
    body: JSON.stringify({ questionId: locked.id }),
  });
  assert.equal(review.status, 403);
  assert.match((await review.json()).message, /buy a subscription/i);

  for (const [asset, type] of [
    ['/%74heory-answers/medicine/anaphylactic-shock/page-1.webp', 'image/webp'],
    ['/theory-answers/general-surgery/wounds-and-wound-healing/factors-delaying-wound-healing/factors-delaying-wound-healing.pdf', 'application/pdf'],
  ]) {
    const file = await get(asset, subscriberToken);
    assert.equal(file.status, 200, asset);
    assert.equal(file.headers.get('content-type'), type, asset);
    assert.deepEqual(Buffer.from(await file.arrayBuffer()), await readFile(new URL(`../public${asset}`, import.meta.url)));
  }
  assert.equal((await get('/theory-answers/medicine/missing.webp')).status, 404);
});
