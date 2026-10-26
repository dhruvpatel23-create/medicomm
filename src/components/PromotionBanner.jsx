import { useEffect, useRef, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import * as Dialog from '@radix-ui/react-dialog';
import { ArrowUpRight, CalendarDays, Check, CheckCircle2, Clock3, LoaderCircle, Sparkles, X } from 'lucide-react';
import { apiRequest } from '../lib/api';
import './promotion-banner.css';

export default function PromotionBanner({ userId, onSignIn }) {
  const queryClient = useQueryClient();
  const queryKey = ['home-promotion', userId];
  const { data, isPending, error: loadError, refetch } = useQuery({ queryKey,
    queryFn: () => apiRequest('/api/promotions/current'), refetchOnWindowFocus: true, retry: 1 });
  const [clock, setClock] = useState(Date.now);
  const [busy, setBusy] = useState(false);
  const pending = useRef(false);
  const [error, setError] = useState('');
  const [confirmation, setConfirmation] = useState('');
  useEffect(() => {
    const timer = window.setInterval(() => setClock(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  if (isPending) return <div className="promotion-loading" role="status">Loading upcoming events…</div>;
  if (loadError) return <div className="promotion-loading">Upcoming events could not be loaded. <button type="button" onClick={() => refetch()}>Try again</button></div>;
  if (!data?.promotion) return null;
  const promotion = data.promotion;
  const remaining = Math.max(0, Date.parse(promotion.startsAt) - clock);
  const open = data.registrationOpen && remaining > 0;
  const date = new Date(promotion.startsAt);
  const eventDate = date.toLocaleDateString('en-GB', { timeZone: promotion.timeZone, day: 'numeric', month: 'long', year: 'numeric' });
  const eventTime = date.toLocaleTimeString('en-IN', { timeZone: promotion.timeZone, hour: 'numeric', minute: '2-digit', hour12: true });
  const countdown = [
    [Math.floor(remaining / 86400000), 'Days'],
    [Math.floor(remaining / 3600000) % 24, 'Hrs'],
    [Math.floor(remaining / 60000) % 60, 'Min'],
    [Math.floor(remaining / 1000) % 60, 'Sec'],
  ];

  async function register() {
    if (!userId) { onSignIn(); return; }
    if (pending.current || data.registered || !open) return;
    pending.current = true;
    setBusy(true);
    setError('');
    try {
      const result = await apiRequest(`/api/promotions/${encodeURIComponent(promotion.id)}/register`, { method: 'POST', body: '{}' });
      queryClient.setQueryData(queryKey, result);
      setConfirmation(result.message);
    } catch (failure) {
      setError(failure.message || 'Registration could not be saved. Please try again.');
      refetch();
    } finally { pending.current = false; setBusy(false); }
  }

  return <>
    <section className="promotion-banner" aria-labelledby="promotion-title">
      <div className="promotion-orbit promotion-orbit-one" aria-hidden="true" />
      <div className="promotion-orbit promotion-orbit-two" aria-hidden="true" />
      <div className="promotion-copy">
        <div className="promotion-topline"><span className="promotion-tag"><Sparkles size={13} aria-hidden="true" /> IN THE SPOTLIGHT</span><span className="promotion-status"><i aria-hidden="true" />{open ? 'Registration open' : 'Registration closed'}</span></div>
        <p className="promotion-eyebrow">{promotion.eyebrow}</p>
        <h2 id="promotion-title">{promotion.title}<span>Your preparation. Your next milestone.</span></h2>
        <p className="promotion-description">{promotion.description}</p>
        <div className="promotion-meta"><span><CalendarDays size={16} aria-hidden="true" /><time dateTime={promotion.startsAt}>{eventDate}</time></span><span><Clock3 size={16} aria-hidden="true" />{eventTime} IST</span></div>
      </div>
      <div className="promotion-action-panel">
        <span className="promotion-countdown-label">{remaining ? 'THE COUNTDOWN IS ON' : 'THE WAIT IS OVER'}</span>
        <div className="promotion-countdown" role="timer" aria-label="Time until the grand test" aria-live="off">
          {countdown.map(([value, label]) => <div key={label}><strong>{String(value).padStart(2, '0')}</strong><span>{label}</span></div>)}
        </div>
        <button className="promotion-register" type="button" onClick={register} disabled={busy || data.registered || !open}>
          {busy ? <><LoaderCircle size={18} className="promotion-spinner" aria-hidden="true" /> Registering…</> : data.registered ? <><Check size={18} aria-hidden="true" /> You're registered</> : open ? <>Register for the grand test <ArrowUpRight size={19} aria-hidden="true" /></> : 'Registration closed'}
        </button>
        <p className="promotion-action-note">{data.registered ? 'Your registration is confirmed. See you at the test!' : userId ? 'One click. A step closer to exam day.' : 'Sign in to register with your Medulla account.'}</p>
        {error && <p className="promotion-error" role="alert">{error}</p>}
      </div>
    </section>
    <Dialog.Root open={Boolean(confirmation)} onOpenChange={open => { if (!open) setConfirmation(''); }}>
      <Dialog.Portal><Dialog.Overlay className="promotion-dialog-overlay" /><Dialog.Content className="promotion-dialog">
        <span className="promotion-success-icon"><CheckCircle2 size={30} aria-hidden="true" /></span>
        <Dialog.Title>{confirmation}</Dialog.Title>
        <Dialog.Description>Your registration for {promotion.title} is confirmed.<br />{eventDate} · {eventTime} IST</Dialog.Description>
        <Dialog.Close className="promotion-dialog-dismiss" aria-label="Close confirmation"><X size={19} /></Dialog.Close>
        <Dialog.Close className="promotion-register">Got it <Check size={17} aria-hidden="true" /></Dialog.Close>
      </Dialog.Content></Dialog.Portal>
    </Dialog.Root>
  </>;
}
