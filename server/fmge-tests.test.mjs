import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readdirSync, statSync, readFileSync } from 'node:fs';
import { rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createMassTestStore, massAttemptId } from './massTestStore.mjs';
import { createFmgeTestsHandler, readFmgeTests, PART_MS, changeFmgeAttempt } from './fmgeTests.mjs';
import { createStateStore } from './stateStore.mjs';
const directories = [];

test('answer batches commit once, retry idempotently and reject invalid batches atomically', () => {
  const attempt = { id: 'batch', testId: 'test', status: 'active', part: 1, startedAt: 0, deadline: PART_MS,
    questions: Array.from({ length: 300 }, (_, i) => ({ id: `q-${i}`, prompt: 'Question', options: ['A','B','C','D'] })), answers: {}, marked: {}, revision: 0 };
  const body = { revision: 0, mutationId: 'batch-save-0001', changes: [{ questionId: 'q-0', optionIndex: 2 }, { questionId: 'q-1', marked: true, currentIndex: 1 }] };
  assert.equal(changeFmgeAttempt(attempt, 'PATCH', null, body, 100).changed, true);
  assert.equal(attempt.revision, 1);
  assert.equal(attempt.answers['q-0'], 2);
  assert.equal(attempt.marked['q-1'], true);
  assert.equal(changeFmgeAttempt(attempt, 'PATCH', null, body, 101).changed, false);
  assert.equal(attempt.revision, 1);
  const before = structuredClone(attempt);
  assert.throws(() => changeFmgeAttempt(attempt, 'PATCH', null, { revision: 1, mutationId: 'batch-save-0002', changes: [{ questionId: 'q-0', optionIndex: 1 }, { questionId: 'q-299', optionIndex: 3 }] }, 102), { status: 400 });
  assert.deepEqual(attempt, before);
  assert.throws(() => changeFmgeAttempt(attempt, 'PATCH', null, { revision: 1, changes: Array(151).fill({}) }, 102), { status: 400 });
});
after(async () => { for (const directory of directories) await rm(directory, { recursive: true, force: true }); });

function fixture() {
  let clock = 100000;
  const directory = mkdtempSync(path.join(tmpdir(), 'medulla-mass-test-'));
  directories.push(directory);
  const massStore = createMassTestStore({ directory });
  const store = createStateStore({ initial: { users: [{ id: 'alice', plan: 'premium' }, { id: 'bob' }] }, persist: async () => {} });
  const handler = createFmgeTestsHandler({ readDatabase: () => store.read(), writeDatabase: d => store.write(d),
    getSessionUser: (r,d) => d.users.find(u => u.id === r.user),
    parseRequestBody: async r => r.body ?? {}, sendJson: (_,status,body,headers) => ({ status, body, headers }), now: () => clock, massStore });
  const call = (suffix = '', method = 'GET', body = {}, user = 'alice') => handler({ method, body, user }, {}, new URL(`http://localhost/api/practice/fmge-tests${suffix}`));
  const start = async (key='start-key-123') => (await call('/fmge-practice-1/start','POST',{startKey:key})).body.attempt;
  return { store, massStore, directory, call, start, setTime: t => { clock=t; }, time: () => clock };
}

test('300-question tests match every subject quota and retain exam provenance', () => {
  const definitions = readFmgeTests();
  assert.ok(definitions.tests.length >= 3);
  assert.equal(definitions.blueprint.reduce((sum,s) => sum+s.count,0),300);
  for (const t of definitions.tests) {
    assert.equal(t.questions.length, 300);
    assert.equal(new Set(t.questions.map(q=>q.id)).size,300);
    assert.equal(new Set(t.questions.map(q=>q.prompt.toLowerCase().replace(/\W/g,''))).size,300);
    for (const s of definitions.blueprint) assert.equal(t.questions.filter(q=>q.subjectId===s.id).length,s.count,`${t.id}/${s.id}`);
    for (const q of t.questions) {
      assert.equal(q.options.length,4); assert.equal(new Set(q.options).size,4);
      assert.ok(Number.isInteger(q.answerIndex) && q.answerIndex>=0 && q.answerIndex<4);
      assert.ok(q.explanation.length>=100 && q.sourcePdf && q.sourceExam);
      assert.ok(['fmge','official'].includes(q.source));
    }
  }
});

test('authentication, payment, and ownership enforced; live APIs never expose answer keys', async () => {
  const f=fixture();
  await assert.rejects(f.call('','GET',{},'guest'), e=>e.status===401);
  assert.equal((await f.call('', 'GET', {}, 'bob')).status, 200);
  await assert.rejects(f.call('/fmge-practice-1/start', 'POST', { startKey: 'unpaid-start-123' }, 'bob'), e => e.status === 403);
  const a=await f.start();
  assert.equal(a.questions.length,150);
  assert.doesNotMatch(JSON.stringify(a), /answerIndex|explanation|sourcePdf|subjectTitle/);
  const d=f.store.read(); d.users.push({id:'eve'});await f.store.write(d);
  await assert.rejects(f.call(`/attempts/${a.id}`,'GET',{},'eve'),e=>e.status===404);
  await assert.rejects(f.call(`/attempts/${a.id}`,'PATCH',{revision:0,questionId:a.questions[0].id,optionIndex:4}),e=>e.status===400);
  const foreign=f.store.read().fmgeTestAttempts[0].questions[150].id;
  await assert.rejects(f.call(`/attempts/${a.id}`,'PATCH',{revision:0,questionId:foreign,optionIndex:0}),e=>e.status===400);
  assert.equal(f.store.read().fmgeTestAttempts[0].revision,0);
});

test('reviewed grand test has its own category and retains existing attempts', async () => {
  const f = fixture();
  const original = readFmgeTests().tests.find(t => t.id === 'fmge-grand-test-1');
  f.setTime(Date.parse(original.startsAt));
  const started = (await f.call('/fmge-grand-test-1/start', 'POST', { startKey: 'grand-start-123' })).body.attempt;
  const catalog = (await f.call()).body.tests;
  assert.deepEqual(catalog.filter(t => t.category === 'practice').map(t => t.id),
    ['fmge-practice-1', 'fmge-practice-2', 'fmge-practice-3']);
  const grand = catalog.filter(t => t.category === 'grand');
  assert.equal(grand.length, 1);
  assert.equal(grand[0].title, 'GRAND TEST 1');
  assert.equal(grand[0].startsAt, '2026-10-27T14:00:00+05:30');
  assert.equal(grand[0].attempts[0].id, started.id);
  assert.deepEqual((await f.massStore.get(original, 'alice')).attempt.questions, original.questions);
  assert.equal(original.questions.filter(q => q.imageUrls?.length).length, 39);
});

test('free, lower-plan and expired members can take the grand test but cannot bypass Premium practice locks', async () => {
  const f = fixture();
  const test = readFmgeTests().tests.find(t => t.eventId);
  const db = f.store.read();
  db.users.push({ id: 'lite', plan: 'lite' }, { id: 'ultra', plan: 'ultra' }, {
    id: 'expired', plan: 'premium', subscriptionPurchasedAt: '2020-01-01T00:00:00Z', subscriptionOrderId: 'expired-order',
  });
  await f.store.write(db);
  f.setTime(Date.parse(test.waitingRoomOpensAt));
  for (const user of ['bob', 'lite', 'ultra', 'expired']) {
    const catalog = (await f.call('', 'GET', {}, user)).body.tests;
    assert.ok(catalog.filter(t => t.category === 'practice').every(t => t.locked && t.access === 'premium'));
    const grand = catalog.find(t => t.id === test.id);
    assert.equal(grand.locked, false);
    assert.equal(grand.access, 'free');
    assert.equal((await f.call(`/${test.id}/waiting-room`, 'POST', {}, user)).status, 200);
    await assert.rejects(f.call(`/${test.id}/start`, 'POST', { startKey: 'free-start-123' }, user), e => e.status === 403 && /2:00 pm/.test(e.message));
    await assert.rejects(f.call('/fmge-practice-1/start', 'POST', { startKey: 'paid-start-123', access: 'free', hasPracticeAccess: true }, user), e => e.status === 403 && /Premium/.test(e.message));
  }
  f.setTime(Date.parse(test.startsAt));
  const attempt = (await f.call(`/${test.id}/start`, 'POST', { startKey: 'free-start-123' }, 'bob')).body.attempt;
  assert.equal(attempt.questions.length, 150);
  await f.call(`/attempts/${attempt.id}`, 'PATCH', { revision: 0, questionId: attempt.questions[0].id, optionIndex: test.questions[0].answerIndex }, 'bob');
  await f.call(`/attempts/${attempt.id}/finish-part`, 'POST', { part: 1 }, 'bob');
  await f.call(`/attempts/${attempt.id}/next-part`, 'POST', {}, 'bob');
  const result = (await f.call(`/attempts/${attempt.id}/finish-part`, 'POST', { part: 2 }, 'bob')).body.attempt;
  assert.equal(result.result.score, 1);
  assert.equal((await f.call(`/${test.id}/leaderboard`, 'GET', {}, 'bob')).body.leaderboard.released, false);
  f.setTime(Date.parse(test.rankReleaseAt));
  assert.equal((await f.call(`/${test.id}/leaderboard`, 'GET', {}, 'bob')).body.leaderboard.yourRank.rank, 1);
  // A previously Premium member still cannot open or modify their own paid
  // attempt after their plan expires or is removed.
  const paid = await f.start();
  const state = f.store.read();
  const own = state.fmgeTestAttempts.find(a => a.id === paid.id);
  own.userId = 'bob';
  await f.store.write(state);
  for (const [suffix, method, body] of [[`/attempts/${paid.id}`, 'GET'],
    [`/attempts/${paid.id}`, 'PATCH', { revision: 0, questionId: paid.questions[0].id, optionIndex: 0 }],
    [`/attempts/${paid.id}/finish-part`, 'POST', { part: 1 }], [`/attempts/${paid.id}/next-part`, 'POST']]) {
    await assert.rejects(f.call(suffix, method, body, 'bob'), e => e.status === 403 && /Premium/.test(e.message));
  }
});

test('waiting room and all question routes enforce exact IST boundaries with server time', async () => {
  const f = fixture();
  const test = readFmgeTests().tests.find(t => t.eventId);
  const start = () => f.call(`/${test.id}/start`, 'POST', { startKey: 'grand-start-123', serverNow: Date.parse(test.startsAt) });
  const waiting = method => f.call(`/${test.id}/waiting-room`, method);
  f.setTime(Date.parse(test.waitingRoomOpensAt) - 1);
  assert.equal((await f.call()).body.tests.find(t => t.id === test.id).stage, 'locked');
  await assert.rejects(waiting('GET'), e => e.status === 403);
  await assert.rejects(waiting('POST'), e => e.status === 403);
  await assert.rejects(start(), e => e.status === 403);
  f.setTime(Date.parse(test.waitingRoomOpensAt));
  const joined = await waiting('POST');
  assert.equal(joined.body.waitingRoom.stage, 'waiting');
  assert.equal(joined.headers['Cache-Control'], 'private, no-store');
  assert.equal((await waiting('POST')).body.waitingRoom.joinedAt, joined.body.waitingRoom.joinedAt);
  assert.doesNotMatch(JSON.stringify(joined.body), /questions|answerIndex|explanation|imageUrls/);
  const id = massAttemptId(test, 'alice');
  for (const [suffix, method, body] of [[`/attempts/${id}`, 'GET'], [`/attempts/${id}`, 'PATCH', { revision: 0 }],
    [`/attempts/${id}/finish-part`, 'POST', { part: 1 }], [`/attempts/${id}/next-part`, 'POST']]) {
    await assert.rejects(f.call(suffix, method, body), e => e.status === 403);
  }
  f.setTime(Date.parse(test.startsAt) - 1);
  await assert.rejects(start(), e => e.status === 403);
  assert.equal((await f.massStore.get(test, 'alice')).attempt, null);
  f.setTime(Date.parse(test.startsAt));
  assert.equal((await waiting('GET')).body.waitingRoom.stage, 'open');
  const attempt = (await start()).body.attempt;
  assert.equal(attempt.questions.length, 150);
  assert.equal(attempt.startedAt, f.time());
  assert.equal(attempt.deadline, f.time() + PART_MS);
  assert.doesNotMatch(JSON.stringify(attempt), /answerIndex|explanation/);
});

test('mass starts are isolated per participant, duplicate clicks reuse the official attempt, and progress survives restart', async () => {
  const f = fixture();
  const test = readFmgeTests().tests.find(t => t.eventId);
  f.setTime(Date.parse(test.startsAt));
  const db = f.store.read();
  for (let i = 0; i < 100; i++) db.users.push({ id: `candidate-${i}` });
  await f.store.write(db);
  const results = await Promise.all(Array.from({ length: 100 }, (_, i) =>
    f.call(`/${test.id}/start`, 'POST', { startKey: `start-key-${i}` }, `candidate-${i}`)));
  assert.equal(new Set(results.map(r => r.body.attempt.id)).size, 100);
  const repeats = await Promise.all(Array.from({ length: 12 }, (_, i) =>
    f.call(`/${test.id}/start`, 'POST', { startKey: `retry-key-${i}` }, 'candidate-0')));
  assert.ok(repeats.every(r => r.body.attempt.id === results[0].body.attempt.id));
  const attempt = results[0].body.attempt;
  const own = (suffix, method, body) => f.call(suffix, method, body, 'candidate-0');
  await assert.rejects(f.call(`/attempts/${attempt.id}`, 'GET', {}, 'alice'), e => e.status === 404);
  await own(`/attempts/${attempt.id}`, 'PATCH', { revision: 0, questionId: attempt.questions[0].id, optionIndex: 2 });
  await assert.rejects(own(`/attempts/${attempt.id}`, 'PATCH', { revision: 0, questionId: attempt.questions[0].id, optionIndex: 1 }), e => e.status === 409);
  const restarted = createMassTestStore({ directory: f.directory });
  const saved = (await restarted.get(test, 'candidate-0')).attempt;
  assert.equal(saved.answers[attempt.questions[0].id], 2);
  assert.equal(saved.revision, 1);
  assert.deepEqual(saved.questions, test.questions);
  const files = readdirSync(f.directory);
  assert.equal(files.filter(name => name.startsWith('questions-')).length, 1, 'one immutable question set for the whole crowd');
  for (const file of files.filter(name => !name.startsWith('questions-'))) {
    assert.ok(statSync(path.join(f.directory, file)).size < 10000, 'answer saves must not duplicate questions');
    assert.doesNotMatch(readFileSync(path.join(f.directory, file), 'utf8'), /"questions"|"explanation"/);
  }
  await own(`/attempts/${attempt.id}/finish-part`, 'POST', { part: 1 });
  await own(`/attempts/${attempt.id}/next-part`, 'POST');
  await own(`/attempts/${attempt.id}/finish-part`, 'POST', { part: 2 });
  const again = (await own(`/${test.id}/start`, 'POST', { startKey: 'another-start-key' })).body.attempt;
  assert.equal(again.id, attempt.id);
  assert.equal(again.status, 'completed', 'a different key must not create a retake');
});

test('old preview IDs cannot expose questions and mass deadlines reject late answers durably', async () => {
  const f = fixture();
  const test = readFmgeTests().tests.find(t => t.eventId);
  const previewId = '00000000-0000-0000-0000-000000000001';
  const db = f.store.read();
  db.fmgeTestAttempts = [{ id: previewId, testId: test.id, userId: 'alice', questions: test.questions }];
  await f.store.write(db);
  f.setTime(Date.parse(test.waitingRoomOpensAt));
  assert.deepEqual((await f.call()).body.tests.find(t => t.id === test.id).attempts, []);
  await assert.rejects(f.call(`/attempts/${previewId}`), e => e.status === 410);
  f.setTime(Date.parse(test.startsAt));
  const a = (await f.call(`/${test.id}/start`, 'POST', { startKey: 'mass-expiry-123' })).body.attempt;
  f.setTime(a.deadline);
  const late = (await f.call(`/attempts/${a.id}`, 'PATCH', {
    revision: 0, questionId: a.questions[0].id, optionIndex: 0,
  })).body;
  assert.equal(late.attempt.status, 'break');
  assert.equal(late.attempt.answers[a.questions[0].id], undefined);
  assert.ok(late.message);
  const restarted = createMassTestStore({ directory: f.directory });
  assert.equal((await restarted.get(test, 'alice')).attempt.status, 'break');
});

test('individual scores are immediate; ranks are private until exactly 8 pm IST and equal scores share ranks', async () => {
  const f = fixture();
  const test = readFmgeTests().tests.find(t => t.eventId);
  const db = f.store.read();
  db.users[0].name = 'Alice'; db.users[0].email = 'private@example.test';
  db.users.push({ id: 'charlie', name: 'Charlie' }, { id: 'eve', name: 'Eve' }, { id: 'unfinished', name: 'Unfinished' });
  await f.store.write(db);
  f.setTime(Date.parse(test.startsAt));
  const endpoint = `/${test.id}/leaderboard`;
  const finish = async (user, correct) => {
    const a = (await f.call(`/${test.id}/start`, 'POST', { startKey: `ranking-${user}-123` }, user)).body.attempt;
    if (correct) await f.call(`/attempts/${a.id}`, 'PATCH', { revision: 0,
      questionId: a.questions[0].id, optionIndex: test.questions[0].answerIndex, score: 300 }, user);
    await f.call(`/attempts/${a.id}/finish-part`, 'POST', { part: 1 }, user);
    await f.call(`/attempts/${a.id}/next-part`, 'POST', {}, user);
    return (await f.call(`/attempts/${a.id}/finish-part`, 'POST', { part: 2 }, user)).body.attempt;
  };
  const personal = await finish('alice', true);
  assert.equal(personal.result.score, 1, 'the individual score is available before rank publication');
  assert.equal(personal.rankReleaseAt, '2026-10-27T20:00:00+05:30');
  assert.equal(personal.result.rank, undefined);
  await finish('charlie', true);
  await finish('eve', false);
  await f.call(`/${test.id}/start`, 'POST', { startKey: 'ranking-unfinished-123' }, 'unfinished');
  let scoreQueries = 0;
  const completed = f.massStore.completedRows.bind(f.massStore);
  f.massStore.completedRows = async (...args) => { scoreQueries++; return completed(...args); };
  f.setTime(Date.parse(test.rankReleaseAt) - 1);
  const hidden = await f.call(`${endpoint}?serverNow=${Date.parse(test.rankReleaseAt) + 99999}`);
  assert.equal(hidden.body.leaderboard.released, false);
  assert.equal(hidden.headers['Cache-Control'], 'private, no-store');
  assert.doesNotMatch(JSON.stringify(hidden.body), /"rank"|"score"|"entries"|"yourRank"|Alice|Charlie/);
  assert.equal(scoreQueries, 0, 'scores must not even be read before publication');
  await assert.rejects(f.call(endpoint, 'GET', {}, 'guest'), e => e.status === 401);
  assert.equal((await f.call(endpoint, 'GET', {}, 'bob')).body.leaderboard.released, false);
  f.setTime(Date.parse(test.rankReleaseAt));
  const pages = await Promise.all(Array.from({ length: 10 }, () => f.call(`${endpoint}?limit=2`)));
  const board = pages[0].body.leaderboard;
  assert.equal(scoreQueries, 1, 'the release crowd shares one ranking read');
  assert.equal(board.released, true);
  assert.equal(board.completedCount, 3, 'unfinished attempts are excluded');
  assert.deepEqual(board.entries.map(row => row.rank), [1, 1]);
  assert.equal(board.yourRank.rank, 1);
  assert.equal(board.yourRank.score, 1);
  assert.equal(board.hasMore, true);
  const last = (await f.call(`${endpoint}?offset=2&limit=2`)).body.leaderboard;
  assert.deepEqual(last.entries.map(row => row.rank), [3]);
  assert.equal(last.hasMore, false);
  assert.doesNotMatch(JSON.stringify(board), /private@example|userId|attemptId|answers|password/);
  await assert.rejects(f.call(`${endpoint}?limit=100000`), e => e.status === 400);
  const restarted = createMassTestStore({ directory: f.directory });
  assert.deepEqual((await restarted.completedRows(test)).map(row => row.score).sort(), [0, 1, 1]);
  const otherEvent = { ...test, eventId: 'another-sitting' };
  assert.deepEqual(await restarted.completedRows(otherEvent), [], 'rankings cannot cross event boundaries');
  await finish('unfinished', false);
  assert.equal((await f.call(endpoint)).body.leaderboard.completedCount, 4, 'post-release submissions update the leaderboard');
});

test('save, clear, review flags and navigation survive reload; stale edits rejected', async () => {
  const f=fixture();const a=await f.start();const q=a.questions[0];
  const saved=(await f.call(`/attempts/${a.id}`,'PATCH',{revision:0,questionId:q.id,optionIndex:2,marked:true,currentIndex:8})).body.attempt;
  assert.equal(saved.answers[q.id],2);assert.equal(saved.currentIndex,8);assert.equal(saved.marked[q.id],true);
  assert.deepEqual((await f.call(`/attempts/${a.id}`)).body.attempt,saved);
  await assert.rejects(f.call(`/attempts/${a.id}`,'PATCH',{revision:0,questionId:q.id,optionIndex:1}),e=>e.status===409);
  const cleared=(await f.call(`/attempts/${a.id}`,'PATCH',{revision:1,questionId:q.id,optionIndex:null,marked:false})).body.attempt;
  assert.equal(cleared.answers[q.id],undefined);assert.equal(cleared.marked[q.id],undefined);
});

test('concurrent starts and network retries create only one active attempt', async () => {
  const f=fixture();const [a,b]=await Promise.all([f.start('first-key-123'),f.start('second-key-456')]);
  assert.equal(a.id,b.id);assert.equal(f.store.read().fmgeTestAttempts.length,1);
  assert.equal((await f.start()).id,a.id);
});

test('parts are server-timed; late changes rejected and break does not consume Part 2 time', async () => {
  const f=fixture();const a=await f.start();
  await assert.rejects(f.call(`/attempts/${a.id}/next-part`,'POST'),e=>e.status===409);
  f.setTime(a.deadline);
  const expired=(await f.call(`/attempts/${a.id}`,'PATCH',{revision:0,questionId:a.questions[0].id,optionIndex:0})).body;
  assert.equal(expired.attempt.status,'break');assert.equal(expired.attempt.answers[a.questions[0].id],undefined);
  assert.equal(expired.attempt.questions.length,0);assert.ok(expired.message);
  f.setTime(f.time()+86400000);
  const next=(await f.call(`/attempts/${a.id}/next-part`,'POST')).body.attempt;
  assert.equal(next.part,2);assert.equal(next.deadline,f.time()+PART_MS);assert.equal(next.questions[0].number,151);
  const retry=(await f.call(`/attempts/${a.id}/next-part`,'POST')).body.attempt;
  assert.equal(retry.deadline,next.deadline);
  f.setTime(next.deadline+1);
  const done=(await f.call(`/attempts/${a.id}`)).body.attempt;
  assert.equal(done.status,'completed');assert.equal(done.result.score,0);assert.equal(done.result.unanswered,300);
  assert.equal(done.questions.length,300);assert.ok(done.questions.every(q=>Number.isInteger(q.answerIndex)));
});

test('grading is server-owned; marked answers count, no negative marks; completed attempts immutable', async () => {
  const f=fixture();let a=await f.start();
  const key=f.store.read().fmgeTestAttempts[0].questions[0].answerIndex;
  a=(await f.call(`/attempts/${a.id}`,'PATCH',{revision:a.revision,questionId:a.questions[0].id,optionIndex:key,marked:true,score:300})).body.attempt;
  a=(await f.call(`/attempts/${a.id}/finish-part`,'POST',{part:1})).body.attempt;
  assert.equal(a.status,'break');
  a=(await f.call(`/attempts/${a.id}/next-part`,'POST')).body.attempt;
  const secondKey=f.store.read().fmgeTestAttempts[0].questions[150].answerIndex;
  a=(await f.call(`/attempts/${a.id}`,'PATCH',{revision:a.revision,questionId:a.questions[0].id,optionIndex:(secondKey+1)%4})).body.attempt;
  // Retried Part 1 submit must never end Part 2.
  assert.equal((await f.call(`/attempts/${a.id}/finish-part`,'POST',{part:1})).body.attempt.status,'active');
  a=(await f.call(`/attempts/${a.id}/finish-part`,'POST',{part:2,score:300})).body.attempt;
  assert.equal(a.result.score,1);assert.equal(a.result.incorrect,1);assert.equal(a.result.unanswered,298);
  assert.equal(a.result.subjects.reduce((sum,s)=>sum+s.correct,0),1);
  await assert.rejects(f.call(`/attempts/${a.id}`,'PATCH',{revision:a.revision,questionId:a.questions[0].id,optionIndex:0}),e=>e.status===409);
  assert.equal((await f.call(`/attempts/${a.id}/finish-part`,'POST',{part:2})).body.attempt.result.score,1);
  assert.equal((await f.start()).id,a.id,'same start key returns completed original');
  assert.notEqual((await f.start('new-retake-123')).id,a.id);
});

test('attempt snapshots and saved progress survive serialization and question-bank changes', async () => {
  const f=fixture();const a=await f.start();const database=JSON.parse(JSON.stringify(f.store.read()));
  assert.equal(database.fmgeTestAttempts[0].questions.length,300);
  const definitions=readFmgeTests();const old=definitions.tests[0].questions[0].prompt;
  try { definitions.tests[0].questions[0].prompt='Changed after starting';assert.equal((await f.call(`/attempts/${a.id}`)).body.attempt.questions[0].prompt,old); }
  finally { definitions.tests[0].questions[0].prompt=old; }
});
