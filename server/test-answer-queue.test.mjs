import test from 'node:test';
import assert from 'node:assert/strict';
import { createTestAnswerQueue, applyTestChange } from '../src/lib/testAnswerQueue.js';

const initial = () => ({ id: 'attempt', status: 'active', revision: 0, answers: {}, marked: {}, currentIndex: 0 });
test('rapid choices stay immediate and never roll back while sequential saves use fresh revisions', async () => {
  let visible, release;
  const calls = [];
  const q = createTestAnswerQueue({ onChange: s => { visible = s; }, onSaving: () => {}, onError: assert.fail,
    send: async (base, change) => {
      calls.push({ revision: base.revision, change });
      await new Promise(resolve => { release = resolve; });
      return { ...applyTestChange(base, change), revision: base.revision + 1 };
    } });
  q.reset(initial());
  q.enqueue({ questionId: 'q1', optionIndex: 0 });
  await Promise.resolve();
  q.enqueue({ questionId: 'q1', optionIndex: 1 });
  q.enqueue({ questionId: 'q1', optionIndex: 3 });
  q.enqueue({ currentIndex: 1 });
  assert.equal(visible.answers.q1, 3);
  assert.equal(visible.currentIndex, 1);
  assert.equal(calls.length, 1);
  release(); await new Promise(resolve => setImmediate(resolve));
  assert.equal(visible.answers.q1, 3);
  assert.equal(calls[1].revision, 1);
  assert.equal(calls[1].change.optionIndex, 3);
  release(); await new Promise(resolve => setImmediate(resolve));
  assert.equal(calls[2].revision, 2);
  release(); await q.flush();
  assert.equal(visible.answers.q1, 3);
  assert.equal(q.pending, false);
});
test('failed saves block submission flush until an explicit server reload', async () => {
  let failed = false;
  const q = createTestAnswerQueue({ onChange: () => {}, onSaving: () => {}, onError: () => { failed = true; },
    send: async () => { throw new Error('offline'); } });
  q.reset(initial()); q.enqueue({ questionId: 'q1', optionIndex: 1 });
  await assert.rejects(q.flush(), /offline/);
  assert.equal(failed, true);
  q.reset(initial()); await q.flush(); assert.equal(q.pending, false);
});
test('part expiry discards queued changes and never sends them to the next part', async () => {
  let count = 0;
  const q = createTestAnswerQueue({ onChange: () => {}, onSaving: () => {}, onError: assert.fail,
    send: async base => { count++; return { ...base, status: 'break' }; } });
  q.reset(initial()); q.enqueue({ questionId: 'q1', optionIndex: 1 });
  q.enqueue({ questionId: 'q2', optionIndex: 2 }); await q.flush();
  assert.equal(count, 1);
});
