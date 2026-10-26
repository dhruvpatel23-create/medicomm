import { useEffect, useState } from 'react';
import { apiRequest } from './api';

const supported = () => window.isSecureContext && 'Notification' in window && 'serviceWorker' in navigator && 'PushManager' in window;
const deviceKey = id => `medulla-push-disabled:${id}`;
const promptKey = id => `medulla-push-prompt:${id}`;
const applicationKey = value => Uint8Array.from(atob(value.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(value.length / 4) * 4, '=')), char => char.charCodeAt(0));

export async function detachPushDevice() {
  if (!supported()) return null;
  const registration = await navigator.serviceWorker.getRegistration('/');
  const subscription = await registration?.pushManager.getSubscription();
  if (!subscription) return null;
  const endpoint = subscription.endpoint;
  await subscription.unsubscribe();
  return endpoint;
}

export function usePushNotifications(userId) {
  const [config, setConfig] = useState(null);
  const [registration, setRegistration] = useState(null);
  const [enabled, setEnabled] = useState(false);
  const [showPrompt, setShowPrompt] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    let cancelled = false;
    setConfig(null); setEnabled(false); setRegistration(null); setShowPrompt(false); setError('');
    if (!userId) return;
    (async () => {
      const config = await apiRequest('/api/notifications');
      if (cancelled) return;
      setConfig(config);
      if (!config.configured || !supported()) return;
      const registration = await navigator.serviceWorker.register('/push-sw.js', { scope: '/', updateViaCache: 'none' });
      await navigator.serviceWorker.ready;
      if (cancelled) return;
      setRegistration(registration);
      const disabled = localStorage.getItem(deviceKey(userId));
      setShowPrompt(!disabled && Notification.permission === 'default' && !localStorage.getItem(promptKey(userId)));
      let subscription = await registration.pushManager.getSubscription();
      if (Notification.permission === 'granted' && !disabled && !cancelled) {
        subscription ??= await registration.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: applicationKey(config.publicKey) });
        if (cancelled) return;
        await apiRequest('/api/notifications', { method: 'POST', body: JSON.stringify({ subscription }) });
        if (!cancelled) setEnabled(true);
      }
    })().catch(error => { if (!cancelled) setError(error.message); });
    return () => { cancelled = true; };
  }, [userId]);

  const dismiss = () => { localStorage.setItem(promptKey(userId), 'dismissed'); setShowPrompt(false); };
  async function enable() {
    if (!registration || busy) return;
    setBusy(true); setError('');
    try {
      // Must run before any await so Safari/Firefox retain the click gesture.
      const permission = await Notification.requestPermission();
      localStorage.setItem(promptKey(userId), 'asked');
      if (permission !== 'granted') throw new Error(permission === 'denied' ? 'Notifications are blocked. Allow them in your browser’s site settings to enable them.' : 'Permission was not granted. You can enable notifications here later.');
      let subscription = await registration.pushManager.getSubscription();
      if (subscription && btoa(String.fromCharCode(...new Uint8Array(subscription.options.applicationServerKey))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '') !== config.publicKey) {
        await subscription.unsubscribe(); subscription = null;
      }
      subscription ??= await registration.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: applicationKey(config.publicKey) });
      await apiRequest('/api/notifications', { method: 'POST', body: JSON.stringify({ subscription }) });
      localStorage.removeItem(deviceKey(userId));
      setEnabled(true); dismiss();
    } catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }
  async function disable() {
    setBusy(true); setError('');
    try {
      const subscription = await registration?.pushManager.getSubscription();
      if (subscription) {
        await apiRequest('/api/notifications', { method: 'DELETE', body: JSON.stringify({ endpoint: subscription.endpoint }) });
        await subscription.unsubscribe();
      }
      localStorage.setItem(deviceKey(userId), 'true'); setEnabled(false); dismiss();
    } catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }
  async function preference(kind, value) {
    setBusy(true); setError('');
    try {
      const result = await apiRequest('/api/notifications', { method: 'PATCH', body: JSON.stringify({ preferences: { [kind]: value } }) });
      setConfig(current => ({ ...current, preferences: result.preferences }));
    } catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }
  async function saveDailyGoal(value) {
    setBusy(true); setError('');
    try {
      const result = await apiRequest('/api/notifications', { method: 'PATCH', body: JSON.stringify({ dailyQuestionGoal: value }) });
      setConfig(current => ({ ...current, dailyQuestionGoal: result.dailyQuestionGoal }));
      return true;
    } catch (error) { setError(error.message); return false; }
    finally { setBusy(false); }
  }
  return { config, enabled, showPrompt, busy, error, enable, disable, dismiss, preference, saveDailyGoal, supported: supported(), ready: Boolean(registration) };
}
