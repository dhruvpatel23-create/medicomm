import test from 'node:test';
import assert from 'node:assert/strict';
import { createFirebaseEmailAuth } from './firebaseEmailAuth.mjs';
import { issueSession } from './security.mjs';

const old = { id: 'app-1', email: 'user@example.com', name: 'Learner', passwordHash: 'legacy', passwordSalt: 'salt', passwordIterations: 220000, emailVerifiedAt: '2026-01-01', subscription: 'premium', progress: [1,2] };
function fixture(users = [old], { mailer, deliveryError } = {}) {
  let db = { users: structuredClone(users), sessions: {}, passwordResets: [] }, revision = 0, time = 1800000000000;
  const revisions = new WeakMap(), identities = new Map(), deliveries = [], created = [], proofs = [], logs = [];
  const readDatabase = () => { const snapshot = structuredClone(db); revisions.set(snapshot, revision); return snapshot; };
  const writeDatabase = async snapshot => { if (revisions.get(snapshot) !== revision) throw Object.assign(Error('conflict'), { status: 409 }); db = structuredClone(snapshot); revision++; };
  const missing = () => { throw Object.assign(Error('missing'), { code: 'auth/user-not-found' }); };
  const auth = {
    getUserByEmail: async email => structuredClone([...identities.values()].find(u => u.email === email) || missing()),
    getUser: async uid => structuredClone(identities.get(uid) || missing()),
    createUser: async value => {
      if ([...identities.values()].some(u => u.email === value.email)) throw Object.assign(Error('exists'), { code: 'auth/email-already-exists' });
      created.push(value);
      const result = { ...value, tokensValidAfterTime: new Date(time).toUTCString() }; identities.set(value.uid, result); return structuredClone(result);
    },
    verifyIdToken: async token => {
      const identity = identities.get(token.slice(6)); if (!identity) throw Error('invalid');
      return { uid: identity.uid, email: identity.email, firebase: { sign_in_provider: 'password' } };
    },
  };
  const service = createFirebaseEmailAuth({ auth, getConfig: async () => ({ apiKey: 'public-test-key' }), readDatabase, writeDatabase,
    mailer,
    verifyPassword: async (password, salt, hash) => { proofs.push(password); return password === 'Original1!' && hash === 'legacy'; },
    now: () => time, log: value => logs.push(value),
    fetchImpl: async (url, options) => {
      const body = JSON.parse(options.body);
      if (url.includes('signInWithPassword')) {
        const identity = [...identities.values()].find(u => u.email === body.email && u.password === body.password);
        return identity ? Response.json({ idToken: `token-${identity.uid}` }) : Response.json({ error: { message: 'INVALID_LOGIN_CREDENTIALS' } }, { status: 400 });
      }
      deliveries.push(body);
      if (deliveryError) return Response.json({ error: { message: deliveryError } }, { status: 400 });
      return Response.json({ email: body.email });
    },
  });
  return { service, auth, identities, created, proofs, deliveries, logs, db: () => db, advance: ms => { time += ms; },
    flush: () => new Promise(resolve => setImmediate(resolve)),
    session: async () => { const snapshot = readDatabase(); const token = issueSession(snapshot, snapshot.users[0].id, time); await writeDatabase(snapshot); return { headers: { cookie: `medicomm_session=${token}` } }; } };
}
test('legacy password migrates once, preserves account data and then Firebase is authoritative', async () => {
  const f = fixture();
  await assert.rejects(f.service.login(old.email, 'wrong'), { status: 401 });
  assert.equal(f.created.length, 0);
  const result = await f.service.login(old.email, 'Original1!');
  assert.equal(result.user.id, old.id); assert.equal(result.user.firebaseAuthUid, old.id);
  assert.equal(result.user.subscription, 'premium'); assert.deepEqual(result.user.progress, [1,2]);
  assert.equal(result.user.passwordHash, undefined); assert.equal(f.created.length, 1);
  f.identities.get(old.id).password = 'Reset2!';
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 401 });
  assert.equal((await f.service.login(old.email, 'Reset2!')).user.id, old.id);
  assert.equal(f.created.length, 1);
});
test('forgotten legacy password uses Firebase email without overwriting an existing identity', async () => {
  const f = fixture();
  assert.deepEqual(await f.service.start(old.email), await f.service.start('absent@example.com'));
  await f.flush();
  assert.equal(f.created.length, 1); assert.equal(f.created[0].password, undefined);
  assert.equal(f.db().users[0].firebaseAuthUid, old.id);
  assert.equal(f.deliveries.filter(m => m.requestType === 'PASSWORD_RESET').length, 2);
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 401 });
  assert.equal(f.identities.get(old.id).password, undefined);
  f.identities.get(old.id).password = 'Reset2!';
  assert.equal((await f.service.login(old.email, 'Reset2!')).user.id, old.id);
  await f.service.start(old.email); await f.flush();
  assert.equal(f.deliveries.filter(m => m.email === old.email).length, 1);
});
test('new users must verify Firebase email before receiving an application session', async () => {
  const f = fixture([]);
  const pending = await f.service.signup({ id: 'new', email: 'new@example.com', name: 'New learner' }, 'Newpass1!', () => {});
  assert.equal(pending.firebase, true); assert.equal(pending.verificationRequired, true);
  assert.equal(Object.keys(f.db().sessions).length, 0);
  assert.equal(f.deliveries[0].requestType, 'VERIFY_EMAIL');
  assert.equal(f.db().users[0].passwordHash, undefined);
  const next = await f.service.login('new@example.com', 'Newpass1!');
  assert.equal(next.verificationRequired, true);
  f.identities.get('new').emailVerified = true;
  assert.ok((await f.service.login('new@example.com', 'Newpass1!')).token);
});

test('configured sender delivers Firebase links for signup, login and resend without issuing sessions', async () => {
  const messages = [], links = [];
  const f = fixture([], { mailer: { configured: true, send: async (message, key) => messages.push({ message, key }) } });
  f.auth.generateEmailVerificationLink = async email => { links.push(email); return 'https://project.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=secret'; };
  const user = { id: 'new', email: 'new@example.com', name: 'New learner' };
  const pending = await f.service.signup(user, 'Newpass1!', () => {});
  assert.equal(pending.sent, true);
  await f.service.login(user.email, 'Newpass1!');
  await f.service.resend(pending.idToken);
  assert.deepEqual(links, [user.email, user.email, user.email]);
  assert.equal(messages.length, 3);
  assert.equal(new Set(messages.map(m => m.key)).size, 3);
  assert.equal(messages[0].message.to, user.email);
  assert.match(messages[0].message.text, /oobCode=secret/);
  assert.match(messages[0].message.html, /&amp;oobCode=secret/);
  assert.match(messages[0].message.html, /<a href="https:\/\/project.firebaseapp.com\/__\/auth\/action\?mode=verifyEmail&amp;oobCode=secret">Verify email address<\/a>/);
  assert.equal(f.deliveries.length, 0);
  assert.equal(Object.keys(f.db().sessions).length, 0);
  assert.ok(!JSON.stringify(f.logs).includes('secret'));
  f.identities.get('new').emailVerified = true;
  assert.ok((await f.service.login(user.email, 'Newpass1!')).token);
});

test('custom sender failure falls back to native Firebase delivery', async () => {
  const f = fixture([], { mailer: { configured: true, send: async () => { throw Error('private provider details'); } } });
  f.auth.generateEmailVerificationLink = async () => 'https://project.firebaseapp.com/secret';
  const pending = await f.service.signup({ id: 'new', email: 'new@example.com', name: 'Learner' }, 'Newpass1!', () => {});
  assert.equal(pending.sent, true);
  assert.equal(f.deliveries[0].requestType, 'VERIFY_EMAIL');
  assert.deepEqual(f.logs, [
    { event: 'firebase_verification_delivery_failed', provider: 'resend' },
    { event: 'firebase_verification_accepted', provider: 'firebase' },
  ]);
});

test('failed verification delivery keeps the account recoverable with immediate retry and safe diagnostics', async () => {
  const f = fixture([], { deliveryError: 'QUOTA_EXCEEDED : private user@example.com' });
  const pending = await f.service.signup({ id: 'new', email: 'new@example.com', name: 'Learner' }, 'Newpass1!', () => {});
  assert.equal(pending.sent, false);
  assert.equal(pending.resendAfter, 0);
  assert.equal(f.db().users.length, 1);
  assert.equal(Object.keys(f.db().sessions).length, 0);
  assert.deepEqual(f.logs, [
    { event: 'firebase_auth_request_failed', operation: 'sendOobCode', status: 400, code: 'QUOTA_EXCEEDED' },
    { event: 'firebase_verification_delivery_failed', provider: 'firebase' },
  ]);
  await assert.rejects(f.service.resend(pending.idToken), { status: 429 });
});

test('resend rejects invalid tokens and identities that do not match the saved account', async () => {
  const f = fixture([]);
  await assert.rejects(f.service.resend('invalid'), { status: 401 });
  const pending = await f.service.signup({ id: 'new', email: 'new@example.com', name: 'Learner' }, 'Newpass1!', () => {});
  const count = f.deliveries.length;
  f.db().users[0].firebaseAuthUid = 'another-uid';
  await assert.rejects(f.service.resend(pending.idToken), { status: 409 });
  assert.equal(f.deliveries.length, count);
});
test('existing Firebase credentials never get replaced by a legacy password', async () => {
  const f = fixture();
  f.identities.set('google-1', { uid: 'google-1', email: old.email, password: 'Firebase2!', emailVerified: true });
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 401 });
  assert.equal(f.proofs.length, 0); assert.equal(f.created.length, 0);
  assert.equal((await f.service.login(old.email, 'Firebase2!')).user.id, old.id);
  assert.equal(f.db().users[0].firebaseAuthUid, 'google-1');
});
test('UID conflicts cannot join accounts', async () => {
  const f = fixture([{ ...old, firebaseAuthUid: 'expected' }]);
  f.identities.set('other', { uid: 'other', email: old.email, password: 'Known1!', emailVerified: true });
  await assert.rejects(f.service.login(old.email, 'Known1!'), { status: 409 });
  assert.equal(f.db().users[0].firebaseAuthUid, 'expected');
});

function linkedGoogleFixture() {
  const f = fixture([{ ...old, googleUid: 'google-1', firebaseAuthUid: 'google-1' }]);
  f.identities.set('google-1', { uid: 'google-1', email: old.email, emailVerified: true,
    providerData: [{ providerId: 'google.com', email: old.email }] });
  return f;
}

test('Google-linked legacy accounts keep email/password login until a Firebase password is set', async () => {
  const f = linkedGoogleFixture();
  await assert.rejects(f.service.login(old.email, 'wrong'), { status: 401 });
  assert.equal(Object.keys(f.db().sessions).length, 0);
  const result = await f.service.login(' USER@EXAMPLE.COM ', 'Original1!');
  assert.ok(result.token);
  assert.equal(result.user.id, old.id);
  assert.equal(result.user.subscription, old.subscription);
  assert.deepEqual(result.user.progress, old.progress);
  assert.equal(f.db().users[0].passwordHash, 'legacy');
  assert.equal(f.created.length, 0);
  const identity = f.identities.get('google-1');
  identity.password = 'Reset2!';
  identity.providerData.push({ providerId: 'password', email: old.email });
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 401 });
  assert.ok((await f.service.login(old.email, 'Reset2!')).token);
  assert.equal(f.db().users[0].passwordHash, undefined);
});

test('legacy Google login fails closed for missing metadata, unverified and disabled identities', async () => {
  for (const change of [u => { delete u.providerData; }, u => { u.emailVerified = false; }, u => { u.disabled = true; }]) {
    const f = linkedGoogleFixture(); change(f.identities.get('google-1'));
    await assert.rejects(f.service.login(old.email, 'Original1!'));
    assert.equal(Object.keys(f.db().sessions).length, 0);
  }
});

test('Firebase reset during legacy password verification prevents a session', async () => {
  const f = linkedGoogleFixture(), lookup = f.auth.getUserByEmail;
  let calls = 0;
  f.auth.getUserByEmail = async email => {
    if (++calls === 2) f.identities.get('google-1').providerData.push({ providerId: 'password' });
    return lookup(email);
  };
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 401 });
  assert.equal(Object.keys(f.db().sessions).length, 0);
});

test('Firebase infrastructure failures are not reported as incorrect passwords', async () => {
  const f = fixture();
  f.auth.verifyIdToken = async () => { throw Object.assign(Error('network failure'), { code: 'app/network-error' }); };
  await assert.rejects(f.service.login(old.email, 'Original1!'), { status: 503 });
  assert.equal(Object.keys(f.db().sessions).length, 0);
  assert.deepEqual(f.logs, [{ event: 'firebase_password_identity_check_failed' }]);
});
test('Firebase password reset or account disable invalidates app cookies within ten seconds', async () => {
  const f = fixture(); await f.service.login(old.email, 'Original1!');
  const request = await f.session(); await f.service.checkSession(request);
  f.advance(11000); f.identities.get(old.id).tokensValidAfterTime = new Date(1800000005000).toUTCString();
  await assert.rejects(f.service.checkSession(request), { status: 401 });
  f.identities.get(old.id).tokensValidAfterTime = new Date(0).toUTCString();
  f.identities.get(old.id).disabled = true; f.advance(11000);
  await assert.rejects(f.service.checkSession(request), { status: 401 });
});
test('provider delivery failure stays generic and is logged without tokens', async () => {
  const f = fixture();
  f.identities.set(old.id, { uid: old.id, email: old.email, disabled: true });
  const result = await f.service.start(old.email); await f.flush();
  assert.match(result.message, /If an account exists/);
  assert.deepEqual(f.logs, [{ event: 'firebase_recovery_delivery_failed' }]);
});
