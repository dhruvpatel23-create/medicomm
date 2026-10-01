import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Test the route against isolated storage, never real account data.
const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
const handler = source.slice(source.indexOf('async function handleFriends('), source.indexOf('function handleDirectConversationsList('));
const sanitizer = source.slice(source.indexOf('function sanitizeSearchableUser('), source.indexOf('function sanitizeDuelOpponent('));

function fixture() {
  let database = { users: ['alice', 'bob', 'carol'].map(id => ({ id, name: id, medicalCollege: 'College', email: `${id}@example.test`, passwordHash: 'private' })) };
  let writes = 0;
  const dependencies = {
    readDatabase: () => structuredClone(database),
    writeDatabase: async data => { database = structuredClone(data); writes++; },
    requireSessionUser: (req, res, db) => { const user = db.users.find(entry => entry.id === req.user); if (!user) res.status = 401; return user; },
    parseRequestBody: async req => { if (req.wait) await req.wait; return req.body; },
    sendJson: (res, status, body) => ({ status, body }),
    getLeaderboardRegion: () => 'Region', DEFAULT_USER_RATING: 1480, DEFAULT_USER_STREAK: 1,
  };
  const api = new Function(...Object.keys(dependencies), `${sanitizer}\n${handler}\nreturn handleFriends;`)(...Object.values(dependencies));
  return {
    call: (user, method = 'GET', body = {}, wait) => api({ user, method, body, wait }, {}),
    api, database: () => database, writes: () => writes,
  };
}

test('friends persist, are private to the owner, and expose only public profile fields', async () => {
  const f = fixture();
  assert.deepEqual((await f.call('alice')).body.friends, []);
  const added = await f.call('alice', 'POST', { userId: 'bob' });
  assert.equal(added.status, 200);
  assert.deepEqual((await f.call('alice')).body.friends.map(user => user.id), ['bob']);
  assert.deepEqual((await f.call('bob')).body.friends, []);
  assert.doesNotMatch(JSON.stringify(added.body), /password|email|friendIds/);
  assert.deepEqual(f.database().users[0].friendIds, ['bob']);
});

test('duplicate additions do not duplicate friends or write again', async () => {
  const f = fixture();
  await f.call('alice', 'POST', { userId: 'bob' });
  await f.call('alice', 'POST', { userId: 'bob' });
  assert.equal(f.writes(), 1);
  assert.equal((await f.call('alice')).body.friends.length, 1);
});

test('self, missing, and nonexistent users cannot be added', async () => {
  const f = fixture();
  for (const userId of ['', 'alice']) assert.equal((await f.call('alice', 'POST', { userId })).status, 400);
  assert.equal((await f.call('alice', 'POST', { userId: 'missing' })).status, 404);
  assert.equal(f.writes(), 0);
});

test('unauthenticated requests cannot read or modify friends', async () => {
  const f = fixture();
  for (const method of ['GET', 'POST']) {
    const response = {};
    await f.api({ method, body: { userId: 'bob' } }, response);
    assert.equal(response.status, 401);
  }
  assert.equal(f.writes(), 0);
});

test('slow request bodies do not overwrite a friend added meanwhile', async () => {
  const f = fixture();
  let release;
  const wait = new Promise(resolve => { release = resolve; });
  const pending = f.call('alice', 'POST', { userId: 'bob' }, wait);
  await f.call('alice', 'POST', { userId: 'carol' });
  release();
  await pending;
  assert.deepEqual((await f.call('alice')).body.friends.map(user => user.id), ['bob', 'carol']);
});
