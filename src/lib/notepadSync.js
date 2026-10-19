// One session per open sheet. Local drafts remain usable when offline.
export function createNotepadSync({ key, id, read, apply, status, isEditing = () => false, storage = localStorage, fetchImpl = fetch }) {
  const metaKey = `${key}:sync`;
  let meta;
  try { meta = JSON.parse(storage.getItem(metaKey)) || {}; } catch { meta = {}; }
  let revision = meta.revision ?? 0, dirty = Boolean(meta.dirty), ready = false, busy = false, conflict = false, closed = false;
  let timer, remote = null, generation = 0;
  const saveMeta = () => { try { storage.setItem(metaKey, JSON.stringify({ revision, dirty })); } catch { /* draft UI reports storage errors */ } };
  async function request(method, body) {
    const response = await fetchImpl(`/api/notepad/draft?id=${encodeURIComponent(id)}`, { method, credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(20000) });
    const data = await response.json();
    if (!response.ok) { const error = new Error(data.message || 'Sync unavailable'); error.status = response.status; throw error; }
    return data.record;
  }
  const notify = message => { if (!closed) status(message); };
  async function pull() {
    if (busy || conflict || isEditing()) return;
    busy = true;
    try {
      remote = await request('GET');
      if (closed) return;
      // An old local draft without sync metadata must never be silently discarded.
      if (!ready && !meta.revision && read().pages.some(p => p.strokes.length)) dirty = true;
      const nextRevision = remote?.revision ?? 0;
      if (dirty && nextRevision !== revision) { conflict = true; notify('Conflict: choose which draft to keep.'); }
      else if (!dirty && remote) { if (!ready || revision !== nextRevision) apply(remote.draft); revision = nextRevision; notify('Synced across devices'); }
      else if (!dirty) notify('Synced across devices');
      ready = true; saveMeta();
    } catch { notify('Saved on this device · waiting to sync'); }
    finally { busy = false; }
    if (ready && dirty && !conflict) await flush();
  }
  async function flush() {
    clearTimeout(timer);
    if (!ready || busy || conflict || !dirty || isEditing()) return;
    busy = true;
    const sent = generation;
    notify('Syncing…');
    try {
      const record = await request('PUT', { revision, draft: { version: 2, ...read() } });
      revision = record.revision; dirty = generation !== sent; saveMeta();
      notify(dirty ? 'Syncing…' : 'Synced across devices');
    } catch (error) {
      if (error.status === 409) { ready = false; }
      notify('Saved on this device · waiting to sync');
    } finally { busy = false; }
    if (!ready) await pull();
    else if (dirty && !conflict && !closed) timer = setTimeout(flush, 3000);
  }
  const interval = setInterval(() => { if (dirty && ready) flush(); else pull(); }, 15000);
  pull();
  return {
    changed() { generation++; dirty = true; saveMeta(); notify(conflict ? 'Conflict: choose which draft to keep.' : 'Saved on this device · syncing soon'); clearTimeout(timer); timer = setTimeout(flush, 1200); },
    async resolve(useLocal) {
      if (!conflict) return;
      // Preserve the losing draft locally for recovery, including intentional clears.
      try { storage.setItem(`${key}:conflict:${Date.now()}`, JSON.stringify(useLocal ? remote?.draft : read())); } catch { notify('Cannot preserve conflict copy. Free device storage first.'); return; }
      revision = remote?.revision ?? 0; conflict = false;
      if (useLocal) { dirty = true; saveMeta(); await flush(); }
      else { if (remote) apply(remote.draft); dirty = false; saveMeta(); notify('Synced across devices'); }
    },
    close() { closed = true; clearInterval(interval); clearTimeout(timer); flush(); },
    flush,
  };
}
