import { HttpError } from './security.mjs';

// Optimistic snapshots: never publish uncommitted data or silently overwrite a
// snapshot read before another commit. The adapter performs the remote CAS too.
export function createStateStore({ initial, revision = 0, persist, reload }) {
  let current = structuredClone(initial);
  let version = revision;
  let healthy = true;
  let chain = Promise.resolve();
  const versions = new WeakMap();
  return {
    get healthy() { return healthy; },
    read() {
      if (!healthy) throw new HttpError(503, 'Storage is unavailable.');
      const snapshot = structuredClone(current);
      versions.set(snapshot, version);
      return snapshot;
    },
    write(snapshot) {
      const expected = versions.get(snapshot);
      const next = structuredClone(snapshot);
      const operation = chain.then(async () => {
        if (!healthy) throw new HttpError(503, 'Storage is unavailable.');
        if (expected !== version) throw new HttpError(409, 'Data changed during this request. Please try again.');
        try {
          await persist(next, version);
          current = next;
          version++;
          versions.set(snapshot, version);
        } catch (error) {
          // An interrupted response may have committed remotely. Reload before
          // allowing more traffic; never retry an uncertain write automatically.
          healthy = false;
          if (reload) {
            try {
              const loaded = await reload();
              current = loaded.data;
              version = loaded.revision;
              healthy = true;
            } catch { /* Remain unready until restart/recovery. */ }
          }
          throw error.status === 409 ? error : new HttpError(503, 'Storage is unavailable. Please check before retrying.');
        }
      });
      chain = operation.catch(() => {});
      return operation;
    },
    drain() { return chain; },
  };
}
