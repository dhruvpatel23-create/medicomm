import test from 'node:test';
import assert from 'node:assert/strict';
import { createPasswordRecovery } from './passwordRecovery.mjs';

function fixture(options = {}) {
  let time = 1800000000000;
  let db = { users: [{ id: 'u1', email: 'user@example.com', passwordHash: 'old', passwordSalt: 'salt', subscription: 'premium', progress: [1,2] }], sessions: { mine: { userId: 'u1' }, other: { userId: 'u2' } }, emailChallenges: [{ email: 'user@example.com' }] };
  const messages = [], revoked = [];
  let revision = 0;
  const revisions = new WeakMap();
  const service = createPasswordRecovery({ readDatabase: () => { const value = structuredClone(db); revisions.set(value, revision); return value; }, writeDatabase: async value => {
    if (revisions.get(value) !== revision) throw Object.assign(new Error('Conflict'), { status: 409 });
    db = structuredClone(value); revision++;
  },
    mailer: { configured: true, send: async value => { messages.push(value); } }, origin: 'https://medullaprep.com',
    hashPassword: async () => ({ hash: 'new-hash', salt: 'new-salt', iterations: 220000 }),
    revokeGoogleSessions: async uid => { revoked.push(uid); }, now: () => time, ...options });
  return { service, messages, revoked, db: () => db, advance: ms => { time += ms; },
    token: () => messages.at(-1).text.match(/#reset-password=([a-f0-9]{64})/)[1],
    change: fn => fn(db) };
}
test('recovery hides account existence, stores only token hashes, and throttles resends', async () => {
  const f = fixture();
  assert.deepEqual(await f.service.start(' USER@example.com '), await f.service.start('absent@example.com'));
  await Promise.resolve();
  assert.equal(f.messages.length, 1);
  assert.ok(!JSON.stringify(f.db()).includes(f.token()));
  await f.service.start('user@example.com');
  assert.equal(f.messages.length, 1);
});
test('reset preserves account data, verifies email, revokes sessions and consumes link once', async () => {
  const f = fixture();
  f.change(db => { db.users[0].googleUid = 'google-1'; });
  await f.service.start('user@example.com'); await Promise.resolve();
  const token = f.token();
  await f.service.reset(token, 'Newpassword1!');
  const db = f.db();
  assert.equal(db.users[0].passwordHash, 'new-hash');
  assert.equal(db.users[0].subscription, 'premium');
  assert.deepEqual(db.users[0].progress, [1,2]);
  assert.ok(db.users[0].emailVerifiedAt);
  assert.deepEqual(db.sessions, { other: { userId: 'u2' } });
  assert.deepEqual(f.revoked, ['google-1']);
  assert.equal(db.emailChallenges.length, 0);
  await assert.rejects(f.service.reset(token, 'Otherpassword2!'), /expired|already used/);
});
test('expired, invalid, replaced and stale-credential tokens cannot reset a password', async () => {
  const f = fixture();
  await f.service.start('user@example.com'); await Promise.resolve();
  const old = f.token();
  await assert.rejects(f.service.reset('bad', 'Validpass1!'), /invalid/);
  await assert.rejects(f.service.reset(old, 'weak'), /8 to 128/);
  f.advance(61000);
  await f.service.start('user@example.com'); await Promise.resolve();
  await assert.rejects(f.service.reset(old, 'Validpass1!'), /expired|already used/);
  const current = f.token();
  f.change(db => { db.users[0].passwordHash = 'changed-elsewhere'; });
  await assert.rejects(f.service.reset(current, 'Validpass1!'), /expired|already used/);
  f.advance(16 * 60000);
  await assert.rejects(f.service.reset(current, 'Validpass1!'), /expired|already used/);
});
test('Google-only accounts can set a password; concurrent reuse has one winner', async () => {
  const f = fixture();
  f.change(db => { delete db.users[0].passwordHash; delete db.users[0].passwordSalt; });
  await f.service.start('user@example.com'); await Promise.resolve();
  const results = await Promise.allSettled([f.service.reset(f.token(), 'Validpass1!'), f.service.reset(f.token(), 'Validpass2!')]);
  assert.equal(results.filter(r => r.status === 'fulfilled').length, 1);
});
test('missing mail configuration and failed Google revocation preserve credentials', async () => {
  const absent = fixture({ mailer: { configured: false } });
  await assert.rejects(absent.service.start('user@example.com'), /temporarily unavailable/);
  const f = fixture({ revokeGoogleSessions: async () => { throw Error('private'); } });
  f.change(db => { db.users[0].googleUid = 'google'; });
  await f.service.start('user@example.com'); await Promise.resolve();
  await assert.rejects(f.service.reset(f.token(), 'Validpass1!'), /temporarily unavailable/);
  assert.equal(f.db().users[0].passwordHash, 'old');
  assert.ok(f.db().sessions.mine);
});
