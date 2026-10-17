import test from 'node:test';
import assert from 'node:assert/strict';
import { createFmgeTestsHandler, readFmgeTests, PART_MS } from './fmgeTests.mjs';
import { createStateStore } from './stateStore.mjs';

function fixture() {
  let clock = 100000;
  const store = createStateStore({ initial: { users: [{ id: 'alice' }, { id: 'bob' }] }, persist: async () => {} });
  const handler = createFmgeTestsHandler({ readDatabase: () => store.read(), writeDatabase: d => store.write(d),
    getSessionUser: (r,d) => d.users.find(u => u.id === r.user), hasPracticeAccess: (_,id) => id !== 'bob',
    parseRequestBody: async r => r.body ?? {}, sendJson: (_,status,body) => ({ status, body }), now: () => clock });
  const call = (suffix = '', method = 'GET', body = {}, user = 'alice') => handler({ method, body, user }, {}, new URL(`http://localhost/api/practice/fmge-tests${suffix}`));
  const start = async (key='start-key-123') => (await call('/fmge-practice-1/start','POST',{startKey:key})).body.attempt;
  return { store, call, start, setTime: t => { clock=t; }, time: () => clock };
}

test('three 300-question tests exactly match every subject quota and retain exam provenance', () => {
  const definitions = readFmgeTests();
  assert.equal(definitions.tests.length, 3);
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
  await assert.rejects(f.call('','GET',{},'bob'), e=>e.status===403);
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
