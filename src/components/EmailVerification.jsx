import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

export default function EmailVerification({ challenge, onVerified, onCancel }) {
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [nextSend, setNextSend] = useState(() => Date.now() + (challenge.resendAfter || 60) * 1000);
  const [clock, setClock] = useState(Date.now());
  useEffect(() => { const timer = setInterval(() => setClock(Date.now()), 1000); return () => clearInterval(timer); }, []);
  const remaining = Math.max(0, Math.ceil((nextSend - clock) / 1000));
  async function verify(event) {
    event.preventDefault();
    if (busy || code.length !== 6) return;
    setBusy(true); setMessage('');
    try {
      const data = await apiRequest('/api/auth/verify-email', { method: 'POST', body: JSON.stringify({ challengeId: challenge.challengeId, code }), timeoutMs: 25000 });
      await onVerified(data);
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }
  async function resend() {
    if (busy || remaining) return;
    setBusy(true); setMessage('');
    try {
      const data = await apiRequest('/api/auth/resend-email', { method: 'POST', body: JSON.stringify({ challengeId: challenge.challengeId }), timeoutMs: 25000 });
      setNextSend(Date.now() + data.resendAfter * 1000); setCode('');
      setMessage('A new code has been sent. Use the latest email.');
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }
  return <form className="auth-form" onSubmit={verify}>
    <p>Enter the 6-digit code sent to <strong>{challenge.email}</strong>. Check your spam folder too. The code expires in 10 minutes.</p>
    <label className="field"><span>Email verification code</span><input autoFocus type="text" inputMode="numeric" autoComplete="one-time-code"
      pattern="[0-9]{6}" maxLength={6} required value={code} disabled={busy}
      onChange={event => setCode(event.target.value.replace(/\D/g, '').slice(0, 6))} placeholder="000000" /></label>
    {message && <p className="form-message" role="status">{message}</p>}
    <button className="button button-primary auth-submit" disabled={busy || code.length !== 6}>{busy ? 'Please wait...' : 'Verify email and continue'}</button>
    <button className="button button-secondary" type="button" disabled={busy || remaining > 0} onClick={resend}>{remaining ? `Resend code in ${remaining}s` : 'Resend code'}</button>
    <button className="text-button" type="button" disabled={busy} onClick={onCancel}>Back to sign in / change email</button>
  </form>;
}
