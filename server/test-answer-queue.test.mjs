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

function memoryStorage() {
  const values = new Map();
  return { getItem: key => values.get(key), setItem: (key, value) => values.set(key, value), removeItem: key => values.delete(key) };
}
const callbacks = { onChange() {}, onSaving() {}, onError() {} };

test('rapid answer changes batch into one write while navigation creates no writes', async () => {
  let visible;
  const calls = [];
  const q = createTestAnswerQueue({ ...callbacks, onChange: value => { visible = value; }, batchSize: 150, debounceMs: 10000,
    send: async (base, changes) => { calls.push(changes); return { ...changes.reduce(applyTestChange, base), revision: base.revision + 1 }; } });
  q.reset({ ...initial(), part: 1 });
  q.navigate(8); await q.flush(); assert.equal(calls.length, 0); assert.equal(visible.currentIndex, 8);
  q.enqueue({ questionId: 'q1', optionIndex: 0 }); q.enqueue({ questionId: 'q1', optionIndex: 2 }); q.enqueue({ questionId: 'q2', marked: true });
  await q.flush();
  assert.equal(calls.length, 1); assert.equal(calls[0].length, 2); assert.equal(visible.answers.q1, 2);
});

test('lost save response reconciles a committed batch without replaying it', async () => {
  let server = { ...initial(), part: 1 }, writes = 0, sends = 0;
  const q = createTestAnswerQueue({ ...callbacks, batchSize: 150,
    recover: async () => server,
    send: async (base, changes, mutationId) => {
      sends++; server = { ...changes.reduce(applyTestChange, base), revision: base.revision + 1, lastMutationId: mutationId }; writes++;
      throw new Error('response lost');
    } });
  q.reset(server); q.enqueue({ questionId: 'q1', optionIndex: 3 }); await q.flush();
  assert.equal(writes, 1); assert.equal(sends, 1); assert.equal(q.pending, false);
});

test('uncommitted timeout retries the same save ID and revision after reading the server', async () => {
  const server = { ...initial(), part: 1 }, ids = [];
  const q = createTestAnswerQueue({ ...callbacks, batchSize: 150, recover: async () => server,
    send: async (base, changes, id) => { ids.push(id); if (ids.length === 1) throw new Error('offline'); return { ...changes.reduce(applyTestChange, base), revision: 1, lastMutationId: id }; } });
  q.reset(server); q.enqueue({ questionId: 'q1', optionIndex: 2 }); await q.flush();
  assert.equal(ids.length, 2); assert.equal(ids[0], ids[1]);
});

test('tab reload restores pending answers and never rebases over another tab', async () => {
  const storage = memoryStorage();
  const server = { ...initial(), part: 1 };
  const offline = createTestAnswerQueue({ ...callbacks, storage, send: async () => { throw new Error('offline'); } });
  offline.reset(server); offline.enqueue({ questionId: 'q1', optionIndex: 2 }); await assert.rejects(offline.flush());
  let visible;
  const restored = createTestAnswerQueue({ ...callbacks, storage, onChange: value => { visible = value; },
    send: async (base, change, mutationId) => ({ ...applyTestChange(base, change), revision: 1, lastMutationId: mutationId }) });
  restored.reset(server); await restored.flush(); assert.equal(visible.answers.q1, 2);
  assert.equal(JSON.parse(storage.getItem('medulla-test-pending:attempt')).queue.length, 0);
  storage.setItem('medulla-test-pending:attempt', JSON.stringify({ part: 1, revision: 0, queue: [{ questionId: 'q2', optionIndex: 1 }] }));
  const conflict = createTestAnswerQueue({ ...callbacks, storage, recover: async () => server, send: assert.fail });
  assert.throws(() => conflict.reset({ ...server, revision: 2 }), /another tab/);
  await assert.rejects(conflict.flush(), /another tab/);
  assert.equal(JSON.parse(storage.getItem('medulla-test-pending:attempt')).queue.length, 1);
});
