import { useEffect, useState } from 'react';
import { apiRequest } from '../lib/api';

export function DailyQuestionGoal({ notifications: n }) {
  const [value, setValue] = useState('');
  const [saved, setSaved] = useState(false);
  useEffect(() => { setValue(String(n.config?.dailyQuestionGoal ?? '')); }, [n.config?.dailyQuestionGoal]);
  return <form onSubmit={async event => { event.preventDefault(); setSaved(await n.saveDailyGoal(Number(value))); }}>
    <label className="setting-field"><span>Daily question goal<small>Your reminder uses this target and your questions answered today.</small></span>
      <input aria-label="Daily question goal" type="number" min="1" max="5000" step="1" required value={value} disabled={!n.config || n.busy} onChange={event => { setValue(event.target.value); setSaved(false); }} /></label>
    <button className="button button-secondary" disabled={!n.config || n.busy}>{n.busy ? 'Saving…' : 'Save daily goal'}</button>
    {saved && <p role="status" className="panel-copy">Daily goal saved.</p>}
  </form>;
}

export function ChallengeNotificationLanding({ challengeId, onAccept, onDecline, onClose }) {
  const [challenge, setChallenge] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    let active = true;
    apiRequest(`/api/duels/challenge/status?id=${encodeURIComponent(challengeId)}`)
      .then(value => { if (active) setChallenge(value); })
      .catch(error => { if (active) setError(error.message); });
    return () => { active = false; };
  }, [challengeId]);
  const available = challenge?.status === 'waiting' && challenge.expiresAt > Date.now() && challenge.isRecipient;
  async function respond(callback) {
    setBusy(true);
    try { await callback({ type: 'challenge', challengeId, otherParticipant: challenge.opponent }); onClose(); }
    finally { setBusy(false); }
  }
  return <aside role="region" aria-label="1v1 invitation" className="card panel" style={{ position: 'fixed', top: 90, right: 20, zIndex: 1001, width: 'min(380px, calc(100vw - 40px))', boxShadow: '0 12px 50px #0003' }}>
    <h3>{challenge?.opponent?.name ? `${challenge.opponent.name}'s 1v1 challenge` : '1v1 challenge'}</h3>
    <p className="panel-copy">{error || (challenge ? available ? `${challenge.questionCount} questions · ${challenge.subjectTitles.join(', ')}` : 'This invitation is no longer available.' : 'Loading invitation…')}</p>
    <div style={{ display: 'flex', gap: 10, marginTop: 12 }}>
      {available && <><button className="button button-primary" disabled={busy} onClick={() => respond(onAccept)}>Accept</button><button className="button button-secondary" disabled={busy} onClick={() => respond(onDecline)}>Decline</button></>}
      <button className="button button-secondary" disabled={busy} onClick={onClose}>Close</button>
    </div>
  </aside>;
}

export function NotificationSettings({ notifications: n }) {
  return <article className="card panel" id="notification-settings">
    <div className="settings-heading"><h3>Device notifications</h3><p>Messages, friend challenges, and one daily reminder for your daily question goal.</p></div>
    {!n.supported ? <p className="panel-copy">Use a supported browser over HTTPS. On iPhone or iPad, add Medulla to your Home Screen, then open it there to enable notifications.</p>
      : !n.config ? <p className="panel-copy">Loading notification settings…</p>
      : !n.config.configured ? <p className="panel-copy">Device notifications will be available once server setup is complete.</p>
      : <><p className="panel-copy">{n.enabled ? 'Notifications are on for this device.' : 'Notifications are off for this device.'}</p>
        <button className="button button-secondary" disabled={n.busy || !n.ready} onClick={n.enabled ? n.disable : n.enable}>{n.busy ? 'Saving…' : n.enabled ? 'Turn off on this device' : 'Enable notifications'}</button>
        {[['messages', 'Personal inbox', 'Receive alerts for new private messages.'], ['challenges', '1v1 challenges', 'Know when a friend challenges you.'], ['daily', 'Daily study reminder', `At ${String(n.config.reminderHourIST).padStart(2, '0')}:00 India time, at most once a day. Skipped after reaching your goal of ${n.config.dailyQuestionGoal} questions.`]].map(([kind, title, copy]) =>
          <label className="setting-toggle" key={kind}><span>{title}<small>{copy}</small></span><input type="checkbox" checked={n.config.preferences[kind]} disabled={n.busy} onChange={event => n.preference(kind, event.target.checked)} /></label>)}
        <p className="panel-copy">These preferences apply across your devices. Repeated messages and challenges are grouped to keep alerts quiet.</p></>}
    {n.error && <p role="status" className="panel-copy">{n.error}</p>}
  </article>;
}

export function NotificationPrompt({ notifications: n }) {
  if (!n.showPrompt) return null;
  return <aside role="region" aria-label="Enable device notifications" className="card panel" style={{ position: 'fixed', bottom: 24, right: 20, zIndex: 1000, width: 'min(380px, calc(100vw - 40px))', boxShadow: '0 12px 50px #0003' }}>
    <h3>Stay in the loop</h3><p className="panel-copy">Get personal messages, 1v1 challenges, and one daily reminder to finish your daily question goal.</p>
    <div style={{ display: 'flex', gap: 10, marginTop: 12 }}><button className="button button-primary" disabled={n.busy} onClick={n.enable}>{n.busy ? 'Enabling…' : 'Enable notifications'}</button><button className="button button-secondary" disabled={n.busy} onClick={n.dismiss}>Not now</button></div>
    {n.error && <p role="status">{n.error}</p>}
  </aside>;
}
