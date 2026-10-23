import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Test the route against isolated storage, never real account data.
const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
const handler = source.slice(source.indexOf('async function handleFriends('), source.indexOf('function handleDirectConversationsList('));
const sanitizer = source.slice(source.indexOf('function sanitizeSearchableUser('), source.indexOf('function sanitizeDuelOpponent('));

function fixture() {
  let database = { users: ['alice', 'bob', 'carol'].map(id => ({ id, name: id, medicalCollege: 'College', email: `${id}@example.test`, passwordHash: 'private' })), friendRequests: [] };
  let writes = 0;
  const dependencies = {
    subscriptionDetails: () => ({ hasPracticeAccess: false }),
    readDatabase: () => structuredClone(database),
    writeDatabase: async data => { database = structuredClone(data); writes++; },
    requireSessionUser: (req, res, db) => { const user = db.users.find(entry => entry.id === req.user); if (!user) res.status = 401; return user; },
    parseRequestBody: async req => { if (req.wait) await req.wait; return req.body; },
    sendJson: (res, status, body) => ({ status, body }),
    getLeaderboardRegion: () => 'Region', DEFAULT_USER_RATING: 1480, DEFAULT_USER_STREAK: 1,
  };
  const api = new Function(...Object.keys(dependencies), `${sanitizer}\n${handler}\nreturn handleFriends;`)(...Object.values(dependencies));
  return {
    call: (user, method = 'GET', body = {}, wait, url = null) => api({ user, method, body, wait, url }, {}),
    api, database: () => database, writes: () => writes,
  };
}

test('adding a friend sends a request first; friend is added only after accepting', async () => {
  const f = fixture();
  // Initially no friends or requests
  assert.deepEqual((await f.call('alice')).body.friends, []);
  assert.deepEqual((await f.call('alice')).body.outgoingRequests, []);
  assert.deepEqual((await f.call('bob')).body.incomingRequests, []);

  // Alice sends request to Bob
  const requested = await f.call('alice', 'POST', { userId: 'bob' });
  assert.equal(requested.status, 200);

  // Alice has not yet added Bob as friend
  const aliceAfterReq = await f.call('alice');
  assert.deepEqual(aliceAfterReq.body.friends, []);
  assert.equal(aliceAfterReq.body.outgoingRequests.length, 1);
  assert.equal(aliceAfterReq.body.outgoingRequests[0].user.id, 'bob');

  // Bob sees incoming request from Alice
  const bobAfterReq = await f.call('bob');
  assert.deepEqual(bobAfterReq.body.friends, []);
  assert.equal(bobAfterReq.body.incomingRequests.length, 1);
  assert.equal(bobAfterReq.body.incomingRequests[0].user.id, 'alice');

  // Bob accepts the request
  const accepted = await f.call('bob', 'POST', { action: 'accept', userId: 'alice' });
  assert.equal(accepted.status, 200);

  // Both are now friends
  const aliceFinal = await f.call('alice');
  const bobFinal = await f.call('bob');
  assert.deepEqual(aliceFinal.body.friends.map(u => u.id), ['bob']);
  assert.deepEqual(bobFinal.body.friends.map(u => u.id), ['alice']);
  assert.deepEqual(aliceFinal.body.outgoingRequests, []);
  assert.deepEqual(bobFinal.body.incomingRequests, []);
  assert.doesNotMatch(JSON.stringify(aliceFinal.body), /password|email/);
});

test('duplicate request is rejected', async () => {
  const f = fixture();
  await f.call('alice', 'POST', { userId: 'bob' });
  const duplicate = await f.call('alice', 'POST', { userId: 'bob' });
  assert.equal(duplicate.status, 400);
  assert.match(duplicate.body.message, /already sent/i);
});

test('declining a request removes it without adding friend', async () => {
  const f = fixture();
  await f.call('alice', 'POST', { userId: 'bob' });
  const declined = await f.call('bob', 'POST', { action: 'decline', userId: 'alice' });
  assert.equal(declined.status, 200);

  assert.deepEqual((await f.call('alice')).body.friends, []);
  assert.deepEqual((await f.call('bob')).body.friends, []);
  assert.deepEqual((await f.call('bob')).body.incomingRequests, []);
});

test('mutual requests auto-accept immediately', async () => {
  const f = fixture();
  await f.call('alice', 'POST', { userId: 'bob' });
  const mutual = await f.call('bob', 'POST', { userId: 'alice' });
  assert.equal(mutual.status, 200);
  assert.equal(mutual.body.accepted, true);

  assert.deepEqual((await f.call('alice')).body.friends.map(u => u.id), ['bob']);
  assert.deepEqual((await f.call('bob')).body.friends.map(u => u.id), ['alice']);
});

test('self, missing, and nonexistent users cannot be added', async () => {
  const f = fixture();
  for (const userId of ['', 'alice']) assert.equal((await f.call('alice', 'POST', { userId })).status, 400);
  assert.equal((await f.call('alice', 'POST', { userId: 'missing' })).status, 404);
});

test('unauthenticated requests cannot read or modify friends', async () => {
  const f = fixture();
  for (const method of ['GET', 'POST']) {
    const response = {};
    await f.api({ method, body: { userId: 'bob' } }, response);
    assert.equal(response.status, 401);
  }
});


test('friend head-to-head counts completed human matches from each viewer perspective', async () => {
  const f = fixture();
  const db = f.database();
  db.users.find(u => u.id === 'alice').friendIds = ['bob', 'carol'];
  db.users.find(u => u.id === 'bob').friendIds = ['alice'];
  const match = (id, verdict, type = 'rated', status = 'completed', playerIds = ['alice', 'bob']) => ({
    id, type, status, playerIds, results: { alice: { verdict }, bob: { verdict: verdict === 'win' ? 'loss' : verdict === 'loss' ? 'win' : verdict } },
  });
  db.duels = [match('1', 'win'), match('2', 'win', 'challenge'), match('3', 'loss'), match('4', 'draw'),
    match('5', 'win', 'rated', 'matched'), match('6', 'win', 'bot'), match('7', 'win', 'rated', 'completed', ['bob', 'carol']),
    match('8', 'invalid')];
  const alice = (await f.call('alice')).body.friends;
  assert.deepEqual(alice.find(u => u.id === 'bob').headToHead, { wins: 2, losses: 1, draws: 1, total: 4 });
  assert.deepEqual(alice.find(u => u.id === 'carol').headToHead, { wins: 0, losses: 0, draws: 0, total: 0 });
  const bob = (await f.call('bob')).body.friends;
  assert.deepEqual(bob.find(u => u.id === 'alice').headToHead, { wins: 1, losses: 2, draws: 1, total: 4 });
  assert.equal(f.writes(), 0);
});
