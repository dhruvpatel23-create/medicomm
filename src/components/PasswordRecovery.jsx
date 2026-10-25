import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

export default function PasswordRecovery({ initialEmail, onBack, challenge }) {
  const [email, setEmail] = useState(initialEmail || '');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState(challenge ? challenge.sent === false ? 'Your account is saved, but the email could not be sent. Please resend it.' : 'Verification email sent. Check your inbox and spam folder.' : '');
  const [error, setError] = useState('');
  const [until, setUntil] = useState(challenge ? Date.now() + 60000 : 0);
  const [clock, setClock] = useState(Date.now());
  useEffect(() => { const timer = setInterval(() => setClock(Date.now()), 1000); return () => clearInterval(timer); }, []);
  const seconds = Math.max(0, Math.ceil((until - clock) / 1000));
  async function submit(event) {
    event.preventDefault();
    if (busy || seconds) return;
    setBusy(true); setError('');
    try {
      const result = await apiRequest(challenge ? '/api/auth/firebase/resend-verification' : '/api/auth/forgot-password', {
        method: 'POST', timeoutMs: 30000, body: JSON.stringify(challenge ? { idToken: challenge.idToken } : { email }),
      });
      setMessage(challenge ? 'A new verification email has been sent.' : result.message);
      setUntil(Date.now() + (result.resendAfter || 60) * 1000);
    } catch (failure) { setError(failure.message); }
    finally { setBusy(false); }
  }
  return <form className="grid gap-5 [&_input]:!min-h-12 [&_input]:!rounded-lg" onSubmit={submit}>
    <p className="text-sm leading-6 text-slate-600 dark:text-slate-300">{challenge ? <>Open the Firebase verification link sent to <strong className="break-all">{challenge.email}</strong>. After verifying, return here and sign in.</> : 'Enter your account email. Firebase will email you a secure link to choose a new password. Complete the reset on that page, then return here to sign in. Your subscription and progress stay on your account.'}</p>
    {!challenge && <label className="field"><span>Account email</span><input type="email" autoComplete="email" required maxLength={254} value={email} disabled={busy} onChange={e => setEmail(e.target.value)} /></label>}
    {message && <p role="status" className="rounded-lg bg-teal-50 p-4 text-sm leading-6 text-teal-900 dark:bg-teal-950 dark:text-teal-100">{message}</p>}
    {error && <p role="alert" className="rounded-lg bg-rose-50 p-4 text-sm text-rose-800 dark:bg-rose-950 dark:text-rose-200">{error}</p>}
    <button className="min-h-12 rounded-lg bg-teal-700 px-5 py-3 font-semibold text-white hover:bg-teal-800 disabled:opacity-50" disabled={busy || seconds > 0} type="submit">{busy ? 'Please wait…' : seconds ? `Send again in ${seconds}s` : challenge ? 'Resend verification email' : 'Send recovery link'}</button>
    <button type="button" disabled={busy} onClick={onBack} className="min-h-11 text-sm font-medium text-slate-600 dark:text-slate-300">Back to sign in</button>
  </form>;
}
