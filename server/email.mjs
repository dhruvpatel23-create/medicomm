import { HttpError } from './security.mjs';
import { PAYMENT_PLANS } from '../src/data/paymentPlans.js';
import { updateTokenState } from './tokens.mjs';
import { randomUUID } from 'node:crypto';

const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
export function emailMessage(subject, lines) {
  return { subject, text: lines.join('\n\n'), html: `<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#172033"><h1 style="font-size:24px">Medulla</h1>${lines.map(line => `<p style="line-height:1.6;white-space:pre-line">${escape(line)}</p>`).join('')}</div>` };
}
export function createMailer({ apiKey = process.env.RESEND_API_KEY, from = process.env.EMAIL_FROM, fetchImpl = fetch } = {}) {
  return {
    configured: Boolean(apiKey && from), from,
    async send({ to, subject, text, html, from: savedFrom }, idempotencyKey) {
      if (!apiKey || !from) throw new HttpError(503, 'Email delivery is not configured.');
      try {
        const response = await fetchImpl('https://api.resend.com/emails', { method: 'POST',
          headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json', 'Idempotency-Key': idempotencyKey },
          body: JSON.stringify({ from: savedFrom || from, to: [to], subject, text, html }), signal: AbortSignal.timeout(15000) });
        if (!response.ok) throw new Error('Delivery rejected');
        const result = await response.json();
        if (typeof result.id !== 'string' || !result.id) throw new Error('Invalid delivery response');
        return result.id;
      } catch { throw new HttpError(503, 'Email delivery is temporarily unavailable. Please try again shortly.'); }
    },
  };
}

// Enqueue in the same database transaction that records confirmed payment.
export function queueThankYou(order, user, mailer, now = Date.now()) {
  if (!mailer.configured || order.status !== 'paid' || order.thankYouEmail || !user?.emailVerifiedAt) return;
  const plan = PAYMENT_PLANS.find(item => item.id === order.planId);
  const amount = new Intl.NumberFormat('en-IN', { style: 'currency', currency: order.currency }).format(order.amount / 100);
  order.thankYouEmail = { status: 'pending', attempts: 0, nextAttemptAt: now, createdAt: now,
    message: { from: mailer.from, to: user.email, ...emailMessage(`${order.testMode ? '[Test] ' : ''}Thank you for subscribing to Medulla`, [
      `Hi ${user.name || 'there'},`, 'Thank you for choosing Medulla. Your subscription is active.',
      `Plan: ${plan?.name || order.planId}\nAmount paid: ${amount}\nOrder: ${order.orderId}\nPayment: ${order.paymentId}`,
      `Access expires: ${new Date(order.expiresAt).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', dateStyle: 'long' })}`,
      ...(order.testMode ? ['This was a test-mode payment. No live charge was made.'] : []),
      'Continue your preparation at https://medullaprep.com', 'Thank you,\nTeam Medulla',
    ]) } };
}

export function createEmailWorker({ mailer, readDatabase, writeDatabase, now = Date.now }) {
  let running = false;
  return async function drainEmailQueue() {
    if (running || !mailer.configured) return;
    running = true;
    try {
      const candidates = (readDatabase().paymentOrders || []).filter(order => {
        const mail = order.thankYouEmail;
        return order.status === 'paid' && mail?.status === 'pending' && mail.nextAttemptAt <= now() && (!mail.leaseUntil || mail.leaseUntil <= now());
      }).slice(0, 10);
      for (const order of candidates) {
        const lease = randomUUID(); let claimed;
        await updateTokenState(readDatabase, writeDatabase, db => {
          claimed = null;
          const mail = db.paymentOrders.find(item => item.orderId === order.orderId)?.thankYouEmail;
          if (!mail || mail.status !== 'pending' || mail.nextAttemptAt > now() || mail.leaseUntil > now()) return;
          // Resend retains idempotency keys for 24 hours. Never resend an
          // uncertain delivery outside that window without operator review.
          if (mail.attempts >= 10 || (mail.firstAttemptAt != null && now() - mail.firstAttemptAt >= 23 * 3600000)) { mail.status = 'needs_review'; return; }
          mail.firstAttemptAt ??= now(); mail.attempts++; mail.lease = lease; mail.leaseUntil = now() + 60000;
          claimed = structuredClone(mail);
        });
        if (!claimed) continue;
        let providerId;
        try { providerId = await mailer.send(claimed.message, `subscription-${order.orderId}`); }
        catch { /* Payment stays successful; the durable queue retries later. */ }
        await updateTokenState(readDatabase, writeDatabase, db => {
          const mail = db.paymentOrders.find(item => item.orderId === order.orderId)?.thankYouEmail;
          if (mail?.lease !== lease) return;
          delete mail.lease; delete mail.leaseUntil;
          if (providerId) { mail.status = 'sent'; mail.sentAt = new Date(now()).toISOString(); mail.providerId = providerId; delete mail.message; }
          else mail.nextAttemptAt = now() + Math.min(3600000, 60000 * 2 ** (mail.attempts - 1));
        });
      }
    } catch { console.warn('Email queue paused; it will retry.'); }
    finally { running = false; }
  };
}
