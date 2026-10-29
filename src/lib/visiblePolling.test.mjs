import test from "node:test";
import assert from "node:assert/strict";
import { startVisiblePolling } from "./visiblePolling.js";

function fixture(t, hidden = false) {
  const previousWindow = globalThis.window;
  const previousDocument = globalThis.document;
  const document = new EventTarget();
  document.hidden = hidden;
  const timers = new Map();
  let nextId = 0;
  globalThis.document = document;
  globalThis.window = {
    setTimeout(callback) {
      const id = ++nextId;
      timers.set(id, callback);
      return id;
    },
    clearTimeout(id) {
      timers.delete(id);
    },
  };
  t.after(() => {
    globalThis.window = previousWindow;
    globalThis.document = previousDocument;
  });
  return {
    timers,
    visibility(hidden) {
      document.hidden = hidden;
      document.dispatchEvent(new Event("visibilitychange"));
    },
    async tick() {
      const [id, callback] = timers.entries().next().value;
      timers.delete(id);
      await callback();
    },
  };
}

const flush = async () => {
  await Promise.resolve();
  await Promise.resolve();
};

test("hidden tabs pause polling and refresh when visible again", async (t) => {
  const clock = fixture(t, true);
  let calls = 0;
  const stop = startVisiblePolling(async () => {
    calls++;
  }, 8000);
  assert.equal(calls, 0);
  assert.equal(clock.timers.size, 0);
  clock.visibility(false);
  await flush();
  assert.equal(calls, 1);
  assert.equal(clock.timers.size, 1);
  clock.visibility(true);
  assert.equal(clock.timers.size, 0);
  clock.visibility(false);
  await flush();
  assert.equal(calls, 2);
  await clock.tick();
  assert.equal(calls, 3);
  stop();
  assert.equal(clock.timers.size, 0);
});

test("visibility changes cannot overlap a slow request", async (t) => {
  const clock = fixture(t);
  let finish;
  let calls = 0;
  const stop = startVisiblePolling(() => {
    calls++;
    return new Promise((resolve) => {
      finish = resolve;
    });
  }, 8000);
  clock.visibility(true);
  clock.visibility(false);
  assert.equal(calls, 1);
  assert.equal(clock.timers.size, 0);
  finish();
  await flush();
  assert.equal(clock.timers.size, 1);
  stop();
});

test("cleanup prevents pending requests from restarting polling", async (t) => {
  const clock = fixture(t);
  let finish;
  let calls = 0;
  const stop = startVisiblePolling(() => {
    calls++;
    return new Promise((resolve) => {
      finish = resolve;
    });
  }, 8000);
  stop();
  finish();
  await flush();
  clock.visibility(true);
  clock.visibility(false);
  assert.equal(clock.timers.size, 0);
  assert.equal(calls, 1);
});

test("a failed request still schedules a later retry", async (t) => {
  const clock = fixture(t);
  let calls = 0;
  const stop = startVisiblePolling(async () => {
    calls++;
    if (calls === 1) throw new Error("offline");
  }, 8000);
  await flush();
  assert.equal(clock.timers.size, 1);
  await clock.tick();
  assert.equal(calls, 2);
  stop();
});
