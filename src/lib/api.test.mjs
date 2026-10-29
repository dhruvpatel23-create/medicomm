import test from "node:test";
import assert from "node:assert/strict";
import { apiRequest } from "./api.js";

test("token refreshes follow successful mutations, not read-only polling or errors", async (t) => {
  const previous = {
    window: globalThis.window,
    localStorage: globalThis.localStorage,
    fetch: globalThis.fetch,
  };
  const events = [];
  globalThis.window = {
    setTimeout,
    clearTimeout,
    dispatchEvent: (event) => events.push(event.type),
  };
  globalThis.localStorage = { removeItem() {} };
  globalThis.fetch = async () => new Response("{}", { status: 200 });
  t.after(() => Object.assign(globalThis, previous));

  await apiRequest("/api/duels/status");
  await apiRequest("/api/short-notes");
  assert.deepEqual(events, []);
  await apiRequest("/api/duels/challenge/create", { method: "POST" });
  assert.deepEqual(events, ["tokens-changed"]);

  globalThis.fetch = async () =>
    new Response('{"message":"Please try later"}', { status: 503 });
  await assert.rejects(
    apiRequest("/api/duels/challenge/create", { method: "POST" }),
    /Please try later/,
  );
  assert.deepEqual(events, ["tokens-changed"]);
});
