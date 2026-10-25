import { createHash, randomBytes } from 'node:crypto';
import { HttpError } from './security.mjs';
import { updateTokenState } from './tokens.mjs';
import { emailMessage } from './email.mjs';

const hash = value => createHash('sha256').update(value).digest('hex');
const credential = user => hash(JSON.stringify([user.passwordHash || null, user.passwordSalt || null, user.passwordChangedAt || null]));
const TTL = 15 * 60000;
export function passwordError(value) {
  if (typeof value !== 'string' || value.length < 8 || value.length > 128) return 'Use 8 to 128 characters for your password.';
  if (!/[0-9]/.test(value) || !/[^\p{L}\p{N}\s]/u.test(value)) return 'Include at least one number and one special character.';
  return null;
}

export function createPasswordRecovery({ readDatabase, writeDatabase, mailer, origin, hashPassword,
  revokeGoogleSessions, now = Date.now, log = () => {} }) {
  const url = new URL(origin);
  if (url.origin !== origin || !['http:', 'https:'].includes(url.protocol)) throw new Error('Use an exact trusted password-recovery origin.');
  const message = 'If an account exists for this email, you will receive a password-reset link. Check your inbox and spam folder.';
  function find(database, token) {
    if (typeof token !== 'string' || !/^[a-f0-9]{64}$/.test(token)) throw new HttpError(400, 'This recovery link is invalid. Request a new one.');
    const record = (database.passwordResets || []).find(r => r.hash === hash(token));
    const user = record && database.users.find(u => u.id === record.userId && u.email.toLowerCase() === record.email);
    if (!record || record.expiresAt <= now() || !user || record.credential !== credential(user)) throw new HttpError(400, 'This recovery link expired or was already used. Request a new one.');
    return { record, user };
  }
  return {
    async start(value) {
      const email = String(value || '').trim().toLowerCase();
      if (!/^\S+@\S+\.\S+$/.test(email) || email.length > 254) throw new HttpError(400, 'Enter a valid email address.');
      if (!mailer.configured) throw new HttpError(503, 'Password recovery is temporarily unavailable. Please try again later.');
      const token = randomBytes(32).toString('hex'), id = randomBytes(16).toString('hex');
      let delivery;
      await updateTokenState(readDatabase, writeDatabase, database => {
        delivery = null;
        database.passwordResets = (database.passwordResets || []).filter(r => r.expiresAt > now());
        database.passwordResetLimits ||= {};
        for (const [key,times] of Object.entries(database.passwordResetLimits)) {
          const recent = times.filter(t => t > now() - 3600000);
          if (recent.length) database.passwordResetLimits[key] = recent; else delete database.passwordResetLimits[key];
        }
        const key = hash(email), times = database.passwordResetLimits[key] || [];
        if (times.length >= 5 || times.some(t => t > now() - 60000)) return;
        if (!times.length && Object.keys(database.passwordResetLimits).length >= 10000) throw new HttpError(429, 'Password recovery is busy. Please try later.');
        database.passwordResetLimits[key] = [...times, now()];
        const matches = database.users.filter(u => u.email.toLowerCase() === email);
        if (matches.length !== 1) return;
        const user = matches[0];
        database.passwordResets = database.passwordResets.filter(r => r.userId !== user.id);
        database.passwordResets.push({ id, userId: user.id, email, hash: hash(token), expiresAt: now() + TTL, credential: credential(user) });
        delivery = email;
      });
      if (delivery) {
        const resetUrl = `${origin}/#reset-password=${token}`;
        const content = emailMessage('Reset your Medulla password', [
          'We received a request to reset your Medulla password.',
          'Use the link below within 15 minutes. It works once. Your subscription, progress and saved work will remain on your account.',
          resetUrl, 'If you did not request this, you can ignore this email. Your password has not changed.',
        ]);
        content.html += `<p><a href="${resetUrl}" style="display:inline-block;background:#0f766e;color:white;padding:12px 20px;border-radius:8px;text-decoration:none">Reset password</a></p>`;
        // Same immediate response for existing and unknown accounts. Do not
        // persist the raw recovery token or expose provider delivery errors.
        void Promise.resolve().then(() => mailer.send({ to: delivery, ...content }, `password-reset-${id}`))
          .catch(() => log({ event: 'password_reset_delivery_failed' }));
      }
      return { message, resendAfter: 60 };
    },
    async reset(token, password) {
      const error = passwordError(password); if (error) throw new HttpError(400, error);
      const initial = find(readDatabase(), token);
      const credentials = await hashPassword(password);
      if (initial.user.googleUid && revokeGoogleSessions) {
        try { await revokeGoogleSessions(initial.user.googleUid); }
        catch { throw new HttpError(503, 'Password recovery is temporarily unavailable. Please try again.'); }
      }
      await updateTokenState(readDatabase, writeDatabase, database => {
        const { user } = find(database, token);
        if (user.googleUid !== initial.user.googleUid) throw new HttpError(409, 'Your account changed. Please try again.');
        Object.assign(user, { passwordHash: credentials.hash, passwordSalt: credentials.salt,
          passwordIterations: credentials.iterations, passwordChangedAt: new Date(now()).toISOString() });
        user.emailVerifiedAt ||= new Date(now()).toISOString();
        user.emailVerificationSource ||= 'password_recovery';
        database.passwordResets = database.passwordResets.filter(r => r.userId !== user.id);
        database.emailChallenges = (database.emailChallenges || []).filter(c => c.email?.toLowerCase() !== user.email.toLowerCase());
        for (const [key,session] of Object.entries(database.sessions || {})) if (session?.userId === user.id) delete database.sessions[key];
      });
      return { success: true, message: 'Your password is updated. Sign in again with your new password.' };
    },
  };
}
