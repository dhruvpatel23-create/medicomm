import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

export default function PasswordRecovery({ token, initialEmail, onBack, onReset }) {
  const [email, setEmail] = useState(initialEmail || '');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [visible, setVisible] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [done, setDone] = useState(false);
  const [requestNew, setRequestNew] = useState(false);
  const [until, setUntil] = useState(0);
  const [clock, setClock] = useState(Date.now());
  useEffect(() => { const timer = setInterval(() => setClock(Date.now()), 1000); return () => clearInterval(timer); }, []);
  const seconds = Math.max(0, Math.ceil((until - clock) / 1000));
  const resetting = Boolean(token) && !requestNew;
  async function submit(event) {
    event.preventDefault();
    if (busy || (!resetting && seconds)) return;
    setError('');
    if (resetting && password !== confirm) { setError('The passwords do not match.'); return; }
    if (resetting && (!/[0-9]/.test(password) || !/[^\p{L}\p{N}\s]/u.test(password))) {
      setError('Include at least one number and one special character.'); return;
    }
    setBusy(true);
    try {
      const result = await apiRequest(resetting ? '/api/auth/reset-password' : '/api/auth/forgot-password', {
        method: 'POST', timeoutMs: 30000,
        body: JSON.stringify(resetting ? { token, password } : { email }),
      });
      setMessage(result.message);
      if (resetting) { setPassword(''); setConfirm(''); setDone(true); onReset(); }
      else setUntil(Date.now() + (result.resendAfter || 60) * 1000);
    } catch (failure) { setError(failure.message); }
    finally { setBusy(false); }
  }
  const button = 'min-h-12 rounded-lg bg-teal-700 px-5 py-3 font-semibold text-white hover:bg-teal-800 disabled:opacity-50';
  return <form className="grid gap-5 [&_input]:!min-h-12 [&_input]:!rounded-lg" onSubmit={submit}>
    <p className="text-sm leading-6 text-slate-600 dark:text-slate-300">{done ? 'Your account, subscription and progress are ready for you.' : resetting ? 'Choose a new password for your account. This link expires after 15 minutes and works once.' : 'Enter your account email. We will send you a secure link to choose a new password.'}</p>
    {!done && (resetting ? <>
      <label className="field"><span>New password</span><input type={visible ? 'text' : 'password'} autoComplete="new-password" required minLength={8} maxLength={128} value={password} disabled={busy} onChange={e => setPassword(e.target.value)} aria-describedby="recovery-password-help" />
        <small id="recovery-password-help">8–128 characters, including a number and a special character.</small></label>
      <label className="field"><span>Confirm new password</span><input type={visible ? 'text' : 'password'} autoComplete="new-password" required minLength={8} maxLength={128} disabled={busy} value={confirm} onChange={e => setConfirm(e.target.value)} /></label>
      <button className="justify-self-start text-sm text-teal-700 dark:text-teal-400" type="button" onClick={() => setVisible(!visible)}>{visible ? 'Hide passwords' : 'Show passwords'}</button>
    </> : <label className="field"><span>Account email</span><input type="email" autoComplete="email" required maxLength={254} value={email} disabled={busy} onChange={e => setEmail(e.target.value)} /></label>)}
    {message && <p role="status" className="rounded-lg bg-teal-50 p-4 text-sm leading-6 text-teal-900 dark:bg-teal-950 dark:text-teal-100">{message}</p>}
    {error && <p role="alert" className="rounded-lg bg-rose-50 p-4 text-sm text-rose-800 dark:bg-rose-950 dark:text-rose-200">{error}</p>}
    {!done && <button className={button} disabled={busy || (!resetting && seconds > 0)} type="submit">{busy ? 'Please wait…' : resetting ? 'Update password' : seconds ? `Send again in ${seconds}s` : 'Send recovery link'}</button>}
    {resetting && !done && <button type="button" disabled={busy} className="text-sm text-teal-700 dark:text-teal-400" onClick={() => { setRequestNew(true); setError(''); setMessage(''); setPassword(''); setConfirm(''); }}>Link expired? Request a new one</button>}
    <button type="button" disabled={busy} onClick={onBack} className="min-h-11 text-sm font-medium text-slate-600 dark:text-slate-300">Back to sign in</button>
  </form>;
}
