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
export function createTestAnswerQueue({ send, onChange, onSaving, onError }) {
  let base, queue = [], running = null, failure = null;
  const publish = () => onChange(queue.reduce(applyTestChange, base));
  function drain() {
    if (running || failure || !queue.length) return;
    onSaving(true);
    running = Promise.resolve().then(async () => {
      while (queue.length) {
        const change = queue[0];
        const saved = await send(base, change);
        queue.shift();
        base = saved;
        if (saved.status !== 'active') queue = [];
        publish();
      }
    }).catch(error => { failure = error; onError(error); }).finally(() => {
      running = null; onSaving(false);
    });
  }
  return {
    get pending() { return Boolean(running || queue.length); },
    reset(attempt) { if (running) throw new Error('Answers are still saving.'); base = attempt; queue = []; failure = null; },
    enqueue(change) {
      if (failure || base?.status !== 'active') return;
      // Coalesce rapid changes still waiting behind the in-flight write.
      const start = running ? 1 : 0;
      const index = queue.findIndex((item, i) => i >= start && item.questionId === change.questionId);
      if (index >= 0) queue[index] = { ...queue[index], ...change };
      else queue.push(change);
      publish(); drain();
    },
    async flush() { drain(); if (running) await running; if (failure) throw failure; },
  };
}
