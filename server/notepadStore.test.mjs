import test from 'node:test';
import assert from 'node:assert/strict';
import { createNotepadStore, createDraftHandler, validateDraft } from './notepadStore.mjs';
import { createNotepadSync } from '../src/lib/notepadSync.js';

const draft = { version: 2, pages: [{ paper: 'ruled', strokes: [] }], pageIndex: 0 };
const ink = { ...draft, pages: [{ paper: 'plain', strokes: [{ tool: 'pen', color: '#000', size: 3, points: [{ x: 1, y: 2, pressure: .5 }] }] }] };
test('rejects malformed and oversized drawing data', () => {
  assert.equal(validateDraft(ink), ink);
  for (const value of [{}, { ...draft, pageIndex: 4 }, { ...draft, pages: Array(9).fill(draft.pages[0]) },
    { ...draft, padding: 'a'.repeat(2100000) }, { ...ink, pages: [{ ...ink.pages[0], strokes: [{ ...ink.pages[0].strokes[0], points: [{ x: Infinity, y: 0, pressure: 1 }] }] }] }]) {
    assert.throws(() => validateDraft(value), { status: 400 });
  }
});
test('authenticated ownership comes from session, never request body', async () => {
  let saved;
  const handler = createDraftHandler({ store: { putDraft: async (...args) => { saved = args; return {}; } },
    readDatabase: () => ({}), requireSessionUser: req => req.user, parseRequestBody: async req => req.body,
    sendJson: (res, code) => { res.code = code; } });
  const url = new URL('http://localhost/api/notepad/draft?id=short-notes:owner:q');
  await handler({ method: 'PUT', user: { id: 'owner' }, body: { userId: 'victim', draft, revision: 0 } }, {}, url);
  assert.equal(saved[0], 'owner');
  await assert.rejects(handler({ method: 'GET', user: { id: 'other' } }, {}, url), { status: 403 });
  saved = null;
  await handler({ method: 'GET', user: null }, {}, url);
  assert.equal(saved, null);
});
test('draft writes use conditional revision and private owner filters', async () => {
  let request;
  const store = createNotepadStore({ url: 'https://example.test', key: 'server-only', fetchImpl: async (url, options) => {
    request = { url, options }; return { ok: true, json: async () => [] };
  } });
  await assert.rejects(store.putDraft('owner', 'q', draft, 3), { status: 409 });
  assert.match(request.url, /user_id=eq.owner.*revision=eq.3/);
  assert.equal(request.options.method, 'PATCH');
  assert.equal(JSON.parse(request.options.body).revision, 4);
});
test('image access and paginated review reads are owner scoped', async () => {
  const calls = [];
  const store = createNotepadStore({ url: 'https://example.test', key: 'k', fetchImpl: async url => {
    calls.push(url); return { ok: true, json: async () => [] };
  } });
  assert.equal(await store.ownsImage('owner', 'user-private.png'), false);
  await store.reviews('owner', 'q', 100);
  await store.summaries('owner', 200);
  assert(calls.every(url => url.includes('user_id=eq.owner')));
  assert.match(calls[1], /offset=100&limit=100/);
  assert.match(calls[2], /notepad_review_summaries/);
});

const tick = () => new Promise(resolve => setTimeout(resolve, 5));
function syncFixture(local = draft, server = null, initialMeta = {}) {
  const values = new Map([['key:sync', JSON.stringify(initialMeta)]]);
  let current = structuredClone(local), record = server, offline = false, message;
  const sync = createNotepadSync({ key: 'key', id: 'q', read: () => current, apply: value => { current = value; },
    status: value => { message = value; }, storage: { getItem: key => values.get(key), setItem: (key, value) => values.set(key, value) },
    fetchImpl: async (_, options) => {
      if (offline) throw new Error('Offline');
      if (options.method === 'PUT') {
        const body = JSON.parse(options.body);
        if (body.revision !== (record?.revision ?? 0)) return { ok: false, status: 409, json: async () => ({}) };
        record = { revision: body.revision + 1, draft: body.draft };
      }
      return { ok: true, json: async () => ({ record }) };
    } });
  return { sync, values, get current() { return current; }, get record() { return record; }, get message() { return message; },
    edit(value) { current = value; sync.changed(); }, remote(value) { record = value; }, offline(value) { offline = value; } };
}
test('new device loads cloud ink and edits sync with a revision', async () => {
  const f = syncFixture(draft, { revision: 2, draft: ink });
  try { await tick(); assert.deepEqual(f.current, ink); f.edit(draft); await f.sync.flush(); assert.equal(f.record.revision, 3); assert.deepEqual(f.record.draft, draft); }
  finally { f.sync.close(); }
});
test('legacy local ink is uploaded when no cloud draft exists', async () => {
  const f = syncFixture(ink);
  try { await tick(); assert.deepEqual(f.record.draft, ink); }
  finally { f.sync.close(); }
});
test('two devices cannot silently overwrite one another; conflict copy is kept', async () => {
  const f = syncFixture(draft, { revision: 1, draft }, { revision: 1 });
  try {
    await tick(); f.edit(ink); f.remote({ revision: 2, draft }); await f.sync.flush();
    assert.match(f.message, /Conflict/); assert.deepEqual(f.current, ink); assert.equal(f.record.revision, 2);
    await f.sync.resolve(true); assert.deepEqual(f.record.draft, ink); assert.equal(f.record.revision, 3);
    assert([...f.values.keys()].some(key => key.startsWith('key:conflict:')));
  } finally { f.sync.close(); }
});
test('offline writes retain pending local state and retry on reconnect', async () => {
  const f = syncFixture();
  try {
    await tick(); f.offline(true); f.edit(ink); await f.sync.flush();
    assert.equal(JSON.parse(f.values.get('key:sync')).dirty, true); assert.deepEqual(f.current, ink);
    f.offline(false); await f.sync.flush(); assert.deepEqual(f.record.draft, ink);
  } finally { f.sync.close(); }
});
