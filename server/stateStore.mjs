import { HttpError } from './security.mjs';

export function validateSupabaseState(rows, table, key) {
  const target = `${table} key=${JSON.stringify(key)}`;
  if (!Array.isArray(rows)) throw new Error(`Invalid Supabase response for ${target}: expected rows.`);
  if (!rows.length) throw new Error(`No readable database row for ${target}. Check SUPABASE_URL, SUPABASE_STATE_TABLE, SUPABASE_STATE_KEY and the server key permissions. Do not seed or replace an existing database.`);
  if (rows.length !== 1) throw new Error(`Expected one database row for ${target}.`);
  const row = rows[0];
  if (!row?.data || typeof row.data !== 'object' || Array.isArray(row.data)) {
    throw new Error(`Invalid database data for ${target}: expected a JSON object. Restore the existing state from a verified backup.`);
  }
  if (!Object.hasOwn(row, 'revision')) {
    throw new Error(`Missing revision column for ${target}. Apply supabase/migrations/20260930000100_add_state_revision_and_private_uploads.sql in the Supabase project configured in Render, then reload the PostgREST schema.`);
  }
  if (!Number.isSafeInteger(row.revision) || row.revision < 0) {
    throw new Error(`Invalid revision for ${target}: expected a non-negative safe integer; received type ${typeof row.revision}. Check the revision column in the configured Supabase project.`);
  }
  return row;
}

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
