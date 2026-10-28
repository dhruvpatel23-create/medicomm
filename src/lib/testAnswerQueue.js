export function applyTestChange(attempt, change) {
  const next = { ...attempt, answers: { ...attempt.answers }, marked: { ...attempt.marked } };
  if ('currentIndex' in change) next.currentIndex = change.currentIndex;
  if ('optionIndex' in change) {
    if (change.optionIndex === null) delete next.answers[change.questionId];
    else next.answers[change.questionId] = change.optionIndex;
  }
  if ('marked' in change) {
    if (change.marked) next.marked[change.questionId] = true;
    else delete next.marked[change.questionId];
  }
  return next;
}

// Immediate local feedback; one revision-checked write at a time. Server replies
// are overlaid with newer queued choices so an old reply cannot revert a click.
export function createTestAnswerQueue({ send, onChange, onSaving, onError, recover,
  storage, batchSize = 1, debounceMs = 0, onStorageError = () => {} }) {
  let base, queue = [], running = null, failure = null, timer = null, inFlight = null, position, conflict = false;
  const key = () => `medulla-test-pending:${base.id}`;
  function persist() {
    if (!storage || !base) return;
    try {
      if (base.status !== 'active') storage.removeItem(key());
      else storage.setItem(key(), JSON.stringify({ part: base.part, revision: base.revision, currentIndex: position, queue, inFlight }));
    } catch { onStorageError(); }
  }
  const publish = () => onChange({ ...queue.reduce(applyTestChange, base), ...(position === undefined ? {} : { currentIndex: position }) });
  function drain() {
    if (running || failure || !queue.length) return;
    onSaving(true);
    running = Promise.resolve().then(async () => {
      while (queue.length) {
        const count = inFlight?.count ?? Math.min(batchSize, queue.length);
        inFlight ??= { count, mutationId: globalThis.crypto.randomUUID(), revision: base.revision };
        persist();
        const changes = queue.slice(0, count);
        const transmit = () => send({ ...base, currentIndex: position ?? base.currentIndex, revision: inFlight.revision }, batchSize === 1 ? changes[0] : changes, inFlight.mutationId);
        let saved;
        try { saved = await transmit(); }
        catch (error) {
          if (!recover || (error.status && error.status !== 409 && error.status < 500)) throw error;
          // A lost response may already have committed. Read before retrying;
          // never rebase pending choices over another tab's newer revision.
          const fresh = await recover(base);
          if (fresh.status !== 'active' || fresh.part !== base.part || fresh.lastMutationId === inFlight.mutationId) saved = fresh;
          else if (fresh.revision === inFlight.revision) saved = await transmit();
          else {
            conflict = true;
            throw new Error('This attempt changed in another tab. Your pending answers are kept on this device.');
          }
        }
        queue.splice(0, count);
        inFlight = null;
        if (saved.part !== base.part || saved.status !== 'active') { queue = []; position = saved.currentIndex; }
        base = saved;
        persist();
        publish();
      }
    }).catch(error => { failure = error; onError(error); }).finally(() => {
      running = null; onSaving(false);
    });
  }
  return {
    get pending() { return Boolean(running || queue.length); },
    reset(attempt) {
      if (running) throw new Error('Answers are still saving.');
      clearTimeout(timer); timer = null;
      base = attempt; queue = []; failure = null; inFlight = null; position = undefined; conflict = false;
      if (storage) {
        let pending;
        try { pending = JSON.parse(storage.getItem(key()) || 'null'); } catch { onStorageError(); }
        if (pending && pending.part === base.part && base.status === 'active' && Array.isArray(pending.queue)) {
          if (Number.isInteger(pending.currentIndex) && pending.currentIndex >= 0 && pending.currentIndex < 150) position = pending.currentIndex;
          queue = pending.queue; inFlight = pending.inFlight;
          if (inFlight && base.lastMutationId === inFlight.mutationId) {
            queue.splice(0, inFlight.count); inFlight = null;
          } else if (queue.length && pending.revision !== base.revision) {
            conflict = true;
            failure = new Error('This attempt changed in another tab. Pending answers were kept; return to the original tab to sync them.');
            publish();
            onError(failure);
            throw failure;
          }
        }
      }
      persist(); publish();
      if (queue.length) drain();
    },
    navigate(index) {
      if (base?.status !== 'active' || !Number.isInteger(index) || index < 0 || index >= 150) return;
      position = index; persist(); publish();
    },
    enqueue(change) {
      if (failure || base?.status !== 'active') return;
      // Coalesce rapid changes still waiting behind the in-flight write.
      const start = inFlight?.count ?? 0;
      const index = queue.findIndex((item, i) => i >= start && item.questionId === change.questionId);
      if (index >= 0) queue[index] = { ...queue[index], ...change };
      else queue.push(change);
      persist(); publish();
      clearTimeout(timer);
      if (debounceMs) timer = setTimeout(() => { timer = null; drain(); }, debounceMs);
      else drain();
    },
    async flush() {
      clearTimeout(timer); timer = null;
      // Explicit retry keeps the same save ID after an uncertain outcome.
      if (!running && recover && !conflict) failure = null;
      drain(); if (running) await running; if (failure) throw failure;
    },
  };
}
