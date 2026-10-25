import { useEffect, useRef, useState } from 'react';
import { apiRequest } from '../lib/api';

export default function GoogleSignIn({ disabled, onVerified, onProfileRequired, onBusyChange }) {
  const [client, setClient] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [link, setLink] = useState(null);
  const [password, setPassword] = useState('');
  const active = useRef(true);
  useEffect(() => {
    active.current = true;
    apiRequest('/api/auth/google/config', { timeoutMs: 20000 }).then(async data => {
      if (!data.enabled) return;
      const [appSdk, authSdk] = await Promise.all([import('@firebase/app'), import('@firebase/auth')]);
      const existing = appSdk.getApps().find(a => a.name === 'medulla-google');
      const app = existing || appSdk.initializeApp(data.config, 'medulla-google');
      const auth = existing ? authSdk.getAuth(app) : authSdk.initializeAuth(app, {
        persistence: authSdk.inMemoryPersistence, popupRedirectResolver: authSdk.browserPopupRedirectResolver,
      });
      if (active.current) setClient({ auth, sdk: authSdk });
    }).catch(() => {});
    return () => { active.current = false; };
  }, []);
  async function exchange(idToken, linkPassword) {
    const result = await apiRequest('/api/auth/google', { method: 'POST', timeoutMs: 30000,
      body: JSON.stringify({ idToken, ...(linkPassword ? { linkPassword } : {}) }) });
    if (result.linkRequired) setLink({ idToken, email: result.email });
    else if (result.profileRequired) onProfileRequired({ idToken, email: result.email, name: result.name });
    else { setLink(null); setPassword(''); await onVerified(result); }
  }
  async function signIn() {
    if (!client || busy || disabled) return;
    setBusy(true); onBusyChange(true); setError('');
    try {
      const provider = new client.sdk.GoogleAuthProvider();
      provider.setCustomParameters({ prompt: 'select_account' });
      const result = await client.sdk.signInWithPopup(client.auth, provider);
      await exchange(await result.user.getIdToken(true));
    } catch (e) {
      if (e.code !== 'auth/popup-closed-by-user' && e.code !== 'auth/cancelled-popup-request') {
        setError(e.code === 'auth/popup-blocked' ? 'Allow the Google sign-in popup and try again.' :
          e.code === 'auth/unauthorized-domain' ? 'Google sign-in is unavailable on this address. Please use email sign-in.' :
          e.code?.startsWith('auth/') ? 'Google sign-in could not be completed. Please try again or use email sign-in.' : e.message);
      }
    } finally {
      await client.sdk.signOut(client.auth).catch(() => {});
      setBusy(false); onBusyChange(false);
    }
  }
  if (!client) return null;
  return <div className="mb-6">
    {link ? <form onSubmit={async e => {
      e.preventDefault(); setBusy(true); onBusyChange(true); setError('');
      try { await exchange(link.idToken, password); } catch(e) { setError(e.message); }
      finally { setBusy(false); onBusyChange(false); }
    }} className="grid gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
      <p className="text-sm font-semibold">Connect your existing account</p>
      <p className="text-sm leading-6 text-slate-500">Google verified {link.email}. Enter your Medulla password once to link this account and keep your progress.</p>
      <label className="field"><span>Existing Medulla password</span><input type="password" autoComplete="current-password" required maxLength={128} value={password} onChange={e => setPassword(e.target.value)} /></label>
      <button type="submit" disabled={busy} className="min-h-12 rounded-lg bg-teal-700 px-4 py-3 text-sm font-semibold text-white disabled:opacity-50">{busy ? 'Connecting…' : 'Connect and sign in'}</button>
      <button type="button" disabled={busy} onClick={() => { setLink(null); setPassword(''); setError(''); }} className="text-sm text-slate-500">Cancel</button>
    </form> : <button type="button" disabled={disabled || busy} onClick={signIn}
      className="flex min-h-12 w-full items-center justify-center gap-3 rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-800 transition-colors hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-teal-500 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700">
      <svg aria-hidden="true" width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5Z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6C44.4 38.02 46.98 31.87 46.98 24.55Z"/><path fill="#FBBC05" d="M10.53 28.59A14.41 14.41 0 0 1 9.75 24c0-1.59.27-3.13.76-4.59l-7.98-6.2A23.78 23.78 0 0 0 0 24c0 3.87.93 7.52 2.56 10.78l7.97-6.19Z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.91-5.8l-7.73-6C30.03 37.65 27.26 38.5 24 38.5c-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48Z"/></svg>
      {busy ? 'Signing in…' : 'Continue with Google'}
    </button>}
    {error && <p className="mt-3 text-sm text-rose-600 dark:text-rose-400" role="alert">{error}</p>}
    {!link && <div className="mt-5 flex items-center gap-3 text-xs text-slate-400"><span className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />or use email<span className="h-px flex-1 bg-slate-200 dark:bg-slate-700" /></div>}
  </div>;
}
