import { createHmac, randomBytes, randomInt, timingSafeEqual } from 'node:crypto';
import { HttpError, issueSession } from './security.mjs';
import { updateTokenState } from './tokens.mjs';
import { emailMessage } from './email.mjs';

const TTL = 10 * 60000;
export function createEmailVerification({ readDatabase, writeDatabase, mailer, validateNewUser,
  secret = process.env.EMAIL_OTP_SECRET, enabled = process.env.EMAIL_VERIFICATION_REQUIRED === 'true', now = Date.now }) {
  if (enabled && (!mailer.configured || !secret || secret.length < 32)) throw new Error('Email verification requires RESEND_API_KEY, EMAIL_FROM and EMAIL_OTP_SECRET (at least 32 characters).');
  const digest = (id, code) => createHmac('sha256', secret).update(`${id}:${code}`).digest('hex');
  function rateLimit(db, email) {
    db.emailVerificationLimits ??= {};
    for (const [key, times] of Object.entries(db.emailVerificationLimits)) {
      const recent = times.filter(time => time > now() - 3600000);
      if (recent.length) db.emailVerificationLimits[key] = recent; else delete db.emailVerificationLimits[key];
    }
    const key = digest('email-rate', email), times = db.emailVerificationLimits[key] || [];
    if (times.length >= 5 || times.some(time => time > now() - 60000)) throw new HttpError(429, 'Please wait before requesting another code. You can request up to 5 codes per hour.');
    if (Object.keys(db.emailVerificationLimits).length >= 10000 && !times.length) throw new HttpError(429, 'Verification is busy. Please try later.');
    db.emailVerificationLimits[key] = [...times, now()];
  }
  async function deliver(challenge, code) {
    await mailer.send({ to: challenge.email, ...emailMessage('Your Medulla verification code', [
      `Your verification code is: ${code}`, 'Enter this code on Medulla to verify your email. It expires in 10 minutes.',
      'Do not share this code. If you did not request it, you can ignore this email.',
    ]) }, `otp-${challenge.id}-${challenge.generation}`);
    return { verificationRequired: true, challengeId: challenge.id, email: challenge.email, expiresAt: challenge.expiresAt, resendAfter: 60 };
  }
  return {
    enabled,
    async start({ user, signup = false }) {
      if (!enabled) throw new HttpError(503, 'Email verification is not enabled.');
      const code = String(randomInt(0, 1000000)).padStart(6, '0');
      const id = randomBytes(24).toString('hex');
      const challenge = { id, email: user.email, userId: user.id, ...(signup ? { newUser: user } : {}),
        hash: digest(id, code), attempts: 0, generation: 1, expiresAt: now() + TTL, createdAt: now() };
      await updateTokenState(readDatabase, writeDatabase, db => {
        rateLimit(db, user.email);
        // Latest successful request replaces earlier challenges for this email.
        db.emailChallenges = [...(db.emailChallenges || []).filter(item => item.expiresAt > now() && item.email !== user.email), challenge];
      });
      return deliver(challenge, code);
    },
    async resend(id) {
      if (!enabled || !/^[a-f0-9]{48}$/.test(id || '')) throw new HttpError(400, 'Please start signing in again.');
      const code = String(randomInt(0, 1000000)).padStart(6, '0'); let challenge;
      await updateTokenState(readDatabase, writeDatabase, db => {
        const item = (db.emailChallenges || []).find(entry => entry.id === id);
        if (!item || now() - item.createdAt > 3600000) throw new HttpError(400, 'Verification expired. Please start again.');
        rateLimit(db, item.email);
        item.hash = digest(id, code); item.attempts = 0; item.generation++; item.expiresAt = now() + TTL;
        challenge = structuredClone(item);
      });
      return deliver(challenge, code);
    },
    async verify(id, code) {
      if (!enabled || !/^[a-f0-9]{48}$/.test(id || '') || !/^\d{6}$/.test(code || '')) throw new HttpError(400, 'Enter the 6-digit code from your email.');
      let result, invalid;
      await updateTokenState(readDatabase, writeDatabase, db => {
        result = null; invalid = false;
        const item = (db.emailChallenges || []).find(entry => entry.id === id);
        if (!item || item.expiresAt <= now() || item.attempts >= 5) throw new HttpError(400, 'Code expired or attempt limit reached. Request a new code.');
        item.attempts++;
        if (!timingSafeEqual(Buffer.from(item.hash, 'hex'), Buffer.from(digest(id, code), 'hex'))) { invalid = true; return; }
        let user;
        if (item.newUser) {
          validateNewUser(db, item.newUser);
          user = { ...item.newUser }; db.users.push(user);
        } else user = db.users.find(entry => entry.id === item.userId && entry.email === item.email);
        if (!user) throw new HttpError(400, 'This account changed. Please sign in again.');
        user.emailVerifiedAt = new Date(now()).toISOString();
        db.emailChallenges = db.emailChallenges.filter(entry => entry.email !== item.email);
        result = { user, token: issueSession(db, user.id, now()) };
      });
      if (invalid) throw new HttpError(400, 'Incorrect verification code. Please try again.');
      return result;
    },
  };
}
