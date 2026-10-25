import { HttpError, issueSession, sessionUser } from './security.mjs';
import { updateTokenState } from './tokens.mjs';

export function createGoogleAuth({ auth, readDatabase, writeDatabase, verifyPassword, createUser, now = Date.now }) {
  return async function signIn(payload, request) {
    if (!auth) throw new HttpError(503, 'Google sign-in is temporarily unavailable.');
    const idToken = payload.idToken;
    if (typeof idToken !== 'string' || idToken.length < 20 || idToken.length > 20000) throw new HttpError(400, 'Sign in with Google again.');
    let claims, identity;
    try {
      claims = await auth.verifyIdToken(idToken, true);
      identity = await auth.getUser(claims.uid);
    } catch { throw new HttpError(401, 'Google sign-in expired or was revoked. Please try again.'); }
    const email = String(claims.email || '').trim().toLowerCase();
    if (claims.firebase?.sign_in_provider !== 'google.com' || claims.email_verified !== true || identity.disabled ||
        identity.emailVerified !== true || identity.email?.toLowerCase() !== email ||
        !identity.providerData?.some(p => p.providerId === 'google.com' && p.email?.toLowerCase() === email) ||
        !Number.isInteger(claims.auth_time) || now() / 1000 - claims.auth_time > 600 || claims.auth_time > now() / 1000 + 60 ||
        !/^\S+@\S+\.\S+$/.test(email) || email.length > 254) {
      throw new HttpError(401, 'Use a recently authenticated Google account with a verified email.');
    }
    const matches = database => {
      const byUid = database.users.filter(u => u.googleUid === claims.uid);
      const byEmail = database.users.filter(u => u.email.toLowerCase() === email);
      if (byUid.length > 1 || byEmail.length > 1 || (byUid[0] && byUid[0].email.toLowerCase() !== email) ||
          (byEmail[0]?.googleUid && byEmail[0].googleUid !== claims.uid)) throw new HttpError(409, 'This Google identity cannot be linked automatically. Please contact support.');
      return byUid[0] || byEmail[0];
    };
    const initial = readDatabase(), existing = matches(initial);
    let passwordProof = null;
    if (existing && !existing.googleUid && sessionUser(request, initial, now())?.id !== existing.id) {
      if (!payload.linkPassword) return { linkRequired: true, email };
      if (typeof payload.linkPassword !== 'string' || payload.linkPassword.length > 128 ||
          !existing.passwordHash || !existing.passwordSalt ||
          !await verifyPassword(payload.linkPassword, existing.passwordSalt, existing.passwordHash, existing.passwordIterations)) {
        throw new HttpError(401, 'The existing account password is incorrect.');
      }
      passwordProof = { id: existing.id, hash: existing.passwordHash };
    }
    if (!existing && !payload.profile) return { profileRequired: true, email, name: identity.displayName || '' };
    let result;
    await updateTokenState(readDatabase, writeDatabase, database => {
      let user = matches(database);
      if (user && !user.googleUid && sessionUser(request, database, now())?.id !== user.id &&
          (!passwordProof || passwordProof.id !== user.id || passwordProof.hash !== user.passwordHash)) {
        throw new HttpError(409, 'Your account changed. Please continue with Google again.');
      }
      if (!user) {
        if (existing) throw new HttpError(409, 'Your account changed. Please try again.');
        if (!payload.profile) throw new HttpError(400, 'Complete your profile to continue.');
        user = createUser(database, { ...payload.profile, email });
        database.users.push(user);
      }
      // Preserve IDs, password hashes, subscriptions, attempts and all other data.
      user.googleUid = claims.uid;
      user.emailVerifiedAt ||= new Date(now()).toISOString();
      user.emailVerificationSource ||= 'google';
      database.emailChallenges = (database.emailChallenges || []).filter(c => c.email.toLowerCase() !== email);
      result = { user, token: issueSession(database, user.id, now()) };
    });
    return result;
  };
}
