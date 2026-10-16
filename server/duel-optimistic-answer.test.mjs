import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../src/App.jsx', import.meta.url), 'utf8');
const handler = source.slice(source.indexOf('  function submitDuelAnswer('), source.indexOf('  function forfeitDuel('));
function fixture(save) {
  const queue = { sessionId: 'match', tail: Promise.resolve(), locked: new Set(), confirmed: new Set(), failed: new Set(), pending: 0 };
  const state = { selections: {}, submitted: {}, busy: false, index: 0, message: '', status: 'live' };
  const setter = key => value => { state[key] = typeof value === 'function' ? value(state[key]) : value; };
  const context = vm.createContext({
    duelAnswerPendingRef: { current: queue }, currentDuelSubmitted: false,
    currentDuelQuestion: { id: 'q1', options: ['A', 'B'] }, user: { id: 'user' },
    duelSessionId: 'match', duelIndex: 0, duelQuestions: [{ id: 'q1' }], apiRequest: save,
    setDuelSelections: setter('selections'), setDuelSubmitted: setter('submitted'),
    setDuelAnswerBusy: setter('busy'), setDuelMessage: setter('message'),
    setDuelIndex: setter('index'), setDuelStatus: setter('status'),
  });
  vm.runInContext(handler, context);
  return { context, state, queue };
}

test('locks immediately, suppresses duplicate clicks, and waits for saving before finishing', async () => {
  let release;
  let calls = 0;
  const pending = new Promise(resolve => { release = resolve; });
  const f = fixture(() => { calls++; return pending; });
  f.context.submitDuelAnswer('A');
  f.context.submitDuelAnswer('B');
  assert.equal(f.state.submitted[0], true);
  assert.equal(f.state.selections[0], 'A');
  f.context.currentDuelSubmitted = true;
  const finish = f.context.nextDuelQuestion();
  await Promise.resolve();
  assert.equal(calls, 1);
  assert.equal(f.state.status, 'live');
  release();
  await finish;
  assert.equal(f.state.status, 'finished');
});

test('failed save unlocks the question for retry and prevents finishing', async () => {
  let fail = true;
  const f = fixture(async () => { if (fail) throw new Error('Offline'); });
  f.context.submitDuelAnswer('A');
  f.context.currentDuelSubmitted = true;
  await f.context.nextDuelQuestion();
  assert.equal(f.state.submitted[0], false);
  assert.equal(f.state.status, 'live');
  assert.match(f.state.message, /retry/);
  fail = false;
  f.context.currentDuelSubmitted = false;
  f.context.submitDuelAnswer('A');
  await f.queue.tail;
  assert.equal(f.state.submitted[0], true);
  assert.equal(f.queue.failed.size, 0);
});

test('server-confirmed answers survive a lost response; old saves cannot change a new match', async () => {
  let reject;
  const f = fixture(() => new Promise((_, rejectSave) => { reject = rejectSave; }));
  f.context.submitDuelAnswer('A');
  await Promise.resolve();
  f.queue.confirmed.add('q1');
  reject(new Error('Response lost'));
  await f.queue.tail;
  assert.equal(f.state.submitted[0], true);
  assert.equal(f.queue.failed.size, 0);

  const stale = fixture(async () => { throw new Error('Old match failed'); });
  stale.context.submitDuelAnswer('A');
  stale.context.duelAnswerPendingRef.current = null;
  await stale.queue.tail;
  assert.equal(stale.state.message, '');
  assert.equal(stale.state.submitted[0], true);
});
