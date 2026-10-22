import { useEffect, useRef, useState, useCallback } from 'react';
import { apiRequest } from './api';

export function useAccountOverview(userId, activeView, revision) {
  const [state, setState] = useState({ data: null, error: '', loading: true });
  const [refresh, setRefresh] = useState(0);
  const reload = useCallback(() => setRefresh(value => value + 1), []);
  useEffect(() => {
    if (!['Dashboard', 'Profile'].includes(activeView)) return;
    let active = true;
    if (!userId || userId === 'guest') { setState({ data: null, error: '', loading: false }); return; }
    setState({ data: null, error: '', loading: true });
    apiRequest('/api/dashboard').then(data => { if (active) setState({ data, error: '', loading: false }); })
      .catch(error => { if (active) setState({ data: null, error: error.message, loading: false }); });
    const focus = () => reload();
    window.addEventListener('focus', focus);
    return () => { active = false; window.removeEventListener('focus', focus); };
  }, [userId, activeView, revision, refresh, reload]);
  return { ...state, reload };
}

export function usePracticeRecorder(userId, onSaved, onProgress) {
  const callback = useRef(onSaved); callback.current = onSaved;
  const progressCallback = useRef(onProgress); progressCallback.current = onProgress;
  const [message, setMessage] = useState('');
  const session = useRef(null);
  useEffect(() => {
    const current = { userId, queue: [], busy: false, active: true, revision: 0 };
    session.current = current;
    if (userId && userId !== 'guest') {
      try { current.queue = JSON.parse(localStorage.getItem(`medicomm-pending-attempts:${userId}`) || '[]'); if (!Array.isArray(current.queue)) current.queue = []; } catch { current.queue = []; }
    }
    setMessage('');
    const live = userId && userId !== 'guest' && typeof EventSource !== 'undefined'
      ? new EventSource('/api/practice/live') : null;
    live?.addEventListener('account', event => {
      if (!current.active) return;
      try {
        const data = JSON.parse(event.data);
        if (data.user?.id !== current.userId) return;
        current.revision++;
        current.latestUser = data.user;
        callback.current(data.user);
        progressCallback.current?.(data.progress);
      } catch { /* The retry fetch below also recovers malformed or interrupted events. */ }
    });
    const retry = () => { void drain(current); void refreshProgress(current); };
    retry(); window.addEventListener('online', retry); window.addEventListener('focus', retry);
    const timer = window.setInterval(retry, 15000);
    return () => { current.active = false; live?.close(); window.clearInterval(timer); window.removeEventListener('online', retry); window.removeEventListener('focus', retry); };
  }, [userId]);
  async function refreshProgress(current) {
    if (!current.active || !current.userId || current.userId === 'guest' || current.busy || current.loadingProgress) return;
    current.loadingProgress = true;
    const revision = current.revision;
    try {
      const data = await apiRequest('/api/practice/progress');
      if (current.active && current.revision === revision) {
        progressCallback.current?.(data.progress);
        if (data.user?.id === current.userId) callback.current(data.user);
      }
    } catch (error) {
      if (current.active) setMessage(`Practice progress has not synced: ${error.message}`);
    } finally { current.loadingProgress = false; }
  }
  function store(current) {
    try { localStorage.setItem(`medicomm-pending-attempts:${current.userId}`, JSON.stringify(current.queue)); return true; } catch { return false; }
  }
  async function drain(current) {
    if (!current?.active || current.busy || current.userId === 'guest' || !current.userId) return;
    current.busy = true;
    while (current.active && current.queue.length) {
      setMessage('Saving practice results…');
      try {
        const revision = current.revision;
        const data = await apiRequest('/api/practice/attempts', { method: 'POST', body: JSON.stringify(current.queue[0]) });
        current.queue.shift(); store(current);
        const savedUser = current.revision !== revision && current.latestUser ? current.latestUser : data.user;
        current.revision++;
        if (current.active) callback.current(savedUser, data.attempt, data.progress);
      } catch (error) {
        if (current.active) setMessage(`Practice results have not synced: ${error.message}`);
        current.busy = false; return;
      }
    }
    current.busy = false;
    if (current.active) setMessage('');
    void refreshProgress(current);
  }
  function record(attempt) {
    const current = session.current;
    if (!current || current.userId === 'guest' || !current.userId) return;
    current.queue.push(attempt);
    if (!store(current)) setMessage('Keep this tab open until your results finish saving.');
    void drain(current);
  }
  return { record, message, retry: () => drain(session.current) };
}
