import { HttpError, issueSession, sessionHash, sessionToken } from './security.mjs';
import { updateTokenState } from './tokens.mjs';

const emailOf = value => String(value || '').trim().toLowerCase();
const unavailable = () => new HttpError(503, 'Firebase authentication is temporarily unavailable. Please try again.');
const invalid = () => new HttpError(401, 'Invalid email or password. If you requested recovery, finish resetting your password first.');

// Firebase password credentials are authoritative. Google linking can bind a UID
// without migrating the application's password; retain that login until Firebase
// has a password provider. Never fall back after a failed Firebase password login.
export function createFirebaseEmailAuth({ auth, getConfig, readDatabase, writeDatabase, verifyPassword, readAccess,
  fetchImpl = fetch, now = Date.now, log = () => {} }) {
  const cachedIdentities = new Map();
  async function rest(method, body) {
    let response, data;
    try {
      const { apiKey } = await getConfig();
      response = await fetchImpl(`https://identitytoolkit.googleapis.com/v1/accounts:${method}?key=${encodeURIComponent(apiKey)}`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: AbortSignal.timeout(15000),
      });
      data = await response.json();
    } catch { throw unavailable(); }
    if (!response.ok) {
      const code = data?.error?.message || '';
      if (/TOO_MANY_ATTEMPTS|QUOTA_EXCEEDED/.test(code)) throw new HttpError(429, 'Too many attempts. Please try again later.');
      if (/INVALID_PASSWORD|INVALID_LOGIN_CREDENTIALS|EMAIL_NOT_FOUND|USER_DISABLED/.test(code)) throw invalid();
      if (/PASSWORD_DOES_NOT_MEET_REQUIREMENTS|WEAK_PASSWORD/.test(code)) throw new HttpError(400, 'Your password needs updating. Use Forgot password to choose a password with at least eight characters, a number and a special character.');
      if (/EMAIL_EXISTS/.test(code)) throw new HttpError(409, 'This email already has an account. Please sign in.');
      throw unavailable();
    }
    return data;
  }
  async function lookup(email) {
    try { return await auth.getUserByEmail(email); }
    catch (error) { if (error.code === 'auth/user-not-found') return null; throw unavailable(); }
  }
  function account(database, email) {
    const users = database.users.filter(u => emailOf(u.email) === email);
    if (users.length > 1) throw new HttpError(409, 'This account needs support before it can sign in.');
    return users[0];
  }
  function checkIdentity(user, identity, database = readDatabase()) {
    if (!user || !identity || identity.disabled || emailOf(identity.email) !== emailOf(user.email) ||
      (user.firebaseAuthUid && user.firebaseAuthUid !== identity.uid) || (user.googleUid && user.googleUid !== identity.uid) ||
      database.users.some(u => u.id !== user.id && (u.firebaseAuthUid === identity.uid || u.googleUid === identity.uid))) {
      throw new HttpError(409, 'This identity cannot be connected automatically. Please contact support.');
    }
  }
  async function bind(user, identity, credentials = {}) {
    await updateTokenState(readDatabase, writeDatabase, database => {
      const current = database.users.find(u => u.id === user.id);
      if (!current || emailOf(current.email) !== emailOf(user.email)) throw new HttpError(409, 'Your account changed. Please try again.');
      checkIdentity(current, identity, database);
      if (credentials.legacyHash && current.passwordHash !== credentials.legacyHash) throw new HttpError(409, 'Your password changed. Please try again.');
      current.firebaseAuthUid = identity.uid;
      current.authProvider = 'firebase';
      if (!credentials.preserveLegacy) {
        delete current.passwordHash; delete current.passwordSalt; delete current.passwordIterations;
      }
      database.passwordResets = (database.passwordResets || []).filter(r => r.userId !== current.id);
      if (identity.emailVerified) {
        current.emailVerifiedAt ||= new Date(now()).toISOString();
        current.emailVerificationSource ||= 'firebase';
      }
    });
  }
  async function passwordSignIn(email, password) {
    const result = await rest('signInWithPassword', { email, password, returnSecureToken: true });
    let claims, identity;
    try { claims = await auth.verifyIdToken(result.idToken, true); identity = await auth.getUser(claims.uid); }
    catch (error) {
      if (['auth/id-token-expired', 'auth/id-token-revoked', 'auth/invalid-id-token', 'auth/user-disabled', 'auth/user-not-found'].includes(error.code)) throw invalid();
      log({ event: 'firebase_password_identity_check_failed' });
      throw unavailable();
    }
    if (emailOf(claims.email) !== email || emailOf(identity.email) !== email || identity.disabled ||
        claims.firebase?.sign_in_provider !== 'password') throw invalid();
    return { result, identity };
  }
  async function verification(result, email) {
    let sent = true;
    try { await rest('sendOobCode', { requestType: 'VERIFY_EMAIL', idToken: result.idToken }); }
    catch { sent = false; log({ event: 'firebase_verification_delivery_failed' }); }
    return { verificationRequired: true, firebase: true, email, idToken: result.idToken, resendAfter: 60, sent };
  }
  return {
    async signup(user, password, validateNewUser) {
      let identity = await lookup(user.email);
      if (!identity) {
        try { identity = await auth.createUser({ uid: user.id, email: user.email, password, emailVerified: false, displayName: user.name }); }
        catch (error) { if (error.code !== 'auth/email-already-exists') throw unavailable(); identity = await lookup(user.email); }
      }
      const signed = await passwordSignIn(user.email, password);
      if (signed.identity.uid !== identity.uid) throw invalid();
      await updateTokenState(readDatabase, writeDatabase, database => {
        if (account(database, user.email)) throw new HttpError(409, 'This email already has an account. Please sign in.');
        checkIdentity(user, identity, database);
        validateNewUser(database, user);
        database.users.push({ ...user, firebaseAuthUid: identity.uid, authProvider: 'firebase' });
      });
      return verification(signed.result, user.email);
    },
    async login(email, password) {
      email = emailOf(email);
      const user = account(readDatabase(), email);
      if (!user) throw invalid();
      let identity = await lookup(email), legacyHash;
      if (!identity && !user.firebaseAuthUid && !user.googleUid && user.passwordHash && user.passwordSalt) {
        if (!await verifyPassword(password, user.passwordSalt, user.passwordHash, user.passwordIterations)) throw invalid();
        legacyHash = user.passwordHash;
        // Only create a missing identity. Existing Firebase credentials are
        // never overwritten by a legacy password, including reset races.
        try { identity = await auth.createUser({ uid: user.id, email, password, emailVerified: Boolean(user.emailVerifiedAt), displayName: user.name }); }
        catch (error) { if (error.code !== 'auth/email-already-exists') throw unavailable(); identity = await lookup(email); }
      }
      if (!identity) throw invalid();
      checkIdentity(user, identity);
      // Google linking preserves the legacy hash but does not create a Firebase
      // password. Only an explicitly linked, verified Google identity qualifies;
      // absent provider metadata must never enable this compatibility path.
      const usesLinkedLegacyPassword = (current, record) => current.googleUid === record.uid &&
        record.emailVerified && Array.isArray(record.providerData) &&
        record.providerData.some(provider => provider.providerId === 'google.com') &&
        !record.providerData.some(provider => provider.providerId === 'password') &&
        current.passwordHash && current.passwordSalt;
      if (usesLinkedLegacyPassword(user, identity)) {
        if (!await verifyPassword(password, user.passwordSalt, user.passwordHash, user.passwordIterations)) throw invalid();
        let result;
        await updateTokenState(readDatabase, writeDatabase, async database => {
          const current = account(database, email);
          // Refresh after password verification (and on transaction retries), so
          // a completed Firebase reset cannot revive the old password.
          const fresh = await lookup(email);
          checkIdentity(current, fresh, database);
          if (!usesLinkedLegacyPassword(current, fresh) || current.passwordHash !== user.passwordHash ||
              current.passwordSalt !== user.passwordSalt || current.passwordIterations !== user.passwordIterations) throw invalid();
          result = { user: current, token: issueSession(database, current.id, now()) };
        });
        return result;
      }
      const signed = await passwordSignIn(email, password);
      checkIdentity(user, signed.identity);
      await bind(user, signed.identity, { legacyHash });
      if (!signed.identity.emailVerified) return verification(signed.result, email);
      let result;
      await updateTokenState(readDatabase, writeDatabase, database => {
        const current = account(database, email); checkIdentity(current, signed.identity, database);
        result = { user: current, token: issueSession(database, current.id, now()) };
      });
      return result;
    },
    async verifyExisting(user, password) {
      const signed = await passwordSignIn(emailOf(user.email), password);
      checkIdentity(user, signed.identity);
      return true;
    },
    async resend(idToken) {
      if (typeof idToken !== 'string' || idToken.length > 20000) throw new HttpError(400, 'Sign in again to request verification.');
      let claims;
      try { claims = await auth.verifyIdToken(idToken, true); } catch { throw new HttpError(401, 'Sign in again to request verification.'); }
      if (claims.firebase?.sign_in_provider !== 'password') throw invalid();
      await rest('sendOobCode', { requestType: 'VERIFY_EMAIL', idToken });
      return { resendAfter: 60 };
    },
    async start(value) {
      const email = emailOf(value);
      if (!/^\S+@\S+\.\S+$/.test(email) || email.length > 254) throw new HttpError(400, 'Enter a valid email address.');
      let allowed = false;
      await updateTokenState(readDatabase, writeDatabase, database => {
        allowed = false; database.passwordResetLimits ||= {};
        for (const [key,times] of Object.entries(database.passwordResetLimits)) {
          const recent = times.filter(t => t > now() - 3600000);
          if (recent.length) database.passwordResetLimits[key] = recent; else delete database.passwordResetLimits[key];
        }
        const key = sessionHash(email), times = database.passwordResetLimits[key] || [];
        if (times.length >= 5 || times.some(t => t > now() - 60000)) return;
        if (Object.keys(database.passwordResetLimits).length >= 10000 && !times.length) throw new HttpError(429, 'Please try again later.');
        database.passwordResetLimits[key] = [...times, now()]; allowed = true;
      });
      if (allowed) {
        // Generic response and asynchronous delivery for known and unknown emails.
        void (async () => {
          const user = account(readDatabase(), email);
          if (user) {
            let identity = await lookup(email);
            if (!identity && !user.firebaseAuthUid && !user.googleUid) {
              try { identity = await auth.createUser({ uid: user.id, email, emailVerified: Boolean(user.emailVerifiedAt), displayName: user.name }); }
              catch (error) { if (error.code !== 'auth/email-already-exists') throw unavailable(); identity = await lookup(email); }
            }
            checkIdentity(user, identity);
            if (!user.firebaseAuthUid) await bind(user, identity, { preserveLegacy: true });
            // Do not discard the old hash until successful Firebase sign-in.
            // login() never applies it to an identity that already exists.
          }
          await rest('sendOobCode', { requestType: 'PASSWORD_RESET', email });
        })().catch(() => log({ event: 'firebase_recovery_delivery_failed' }));
      }
      return { message: 'If an account exists for this email, Firebase will send you a password-reset link. Check your inbox and spam folder.', resendAfter: 60 };
    },
    async checkSession(request) {
      const database = readAccess ? readAccess(request) : readDatabase(), token = sessionToken(request);
      const session = token && database.sessions[sessionHash(token)];
      const user = session && database.users.find(u => u.id === session.userId);
      const uid = user?.firebaseAuthUid || user?.googleUid;
      if (!uid || session.expiresAt <= now()) return;
      let identity;
      const cached = cachedIdentities.get(uid);
      if (cached && cached.until > now()) identity = cached.identity;
      else {
        try { identity = await auth.getUser(uid); }
        catch (error) { if (error.code !== 'auth/user-not-found') throw unavailable(); identity = { disabled: true }; }
        if (cachedIdentities.size >= 10000) cachedIdentities.clear();
        cachedIdentities.set(uid, { identity, until: now() + 10000 });
      }
      const revoked = Date.parse(identity.tokensValidAfterTime || '') || 0;
      if (identity.disabled || emailOf(identity.email) !== emailOf(user.email) || Date.parse(session.createdAt) < revoked) {
        throw new HttpError(401, 'Your session expired. Please sign in again.');
      }
    },
  };
}
