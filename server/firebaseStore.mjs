import { createHash } from 'node:crypto';
import { gzip, gunzip } from 'node:zlib';
import { promisify } from 'node:util';
import { HttpError } from './security.mjs';
import { paidOrderDates } from './subscriptions.mjs';
import { liveStateStats, countNotepadRecords } from './firebaseStats.mjs';

const CHUNK = 512 * 1024;
const compress = promisify(gzip), decompress = promisify(gunzip);
export const digest = bytes => createHash('sha256').update(bytes).digest('hex');
export const jsonBytes = value => Buffer.from(JSON.stringify(value));
export const fingerprint = value => digest(jsonBytes(value));

// Immutable, content-addressed chunks keep every Firestore document below 1 MiB.
// A small transactional pointer publishes all changed fields atomically. Old
// chunks remain available for consistent reads, interrupted imports and rollback.
export function createFirebaseBlobs(root) {
  const known = new Set();
  return {
    async put(value) {
      const raw = jsonBytes(value), compressed = await compress(raw);
      const hashes = [];
      for (let offset = 0; offset < compressed.length; offset += CHUNK) {
        const payload = compressed.subarray(offset, offset + CHUNK), hash = digest(payload);
        hashes.push(hash);
        if (known.has(hash)) continue;
        try { await root.collection('blobs').doc(hash).create({ payload }); }
        catch (error) { if (error.code !== 6 && error.code !== 'already-exists') throw error; }
        known.add(hash);
      }
      return { codec: 'gzip-json-v1', hashes, digest: digest(raw), bytes: raw.length };
    },
    async get(ref) {
      if (ref?.codec !== 'gzip-json-v1' || !Array.isArray(ref.hashes) || !ref.hashes.length ||
          !Number.isSafeInteger(ref.bytes) || ref.bytes < 0 || !/^[a-f0-9]{64}$/.test(ref.digest)) throw new Error('Invalid Firebase data reference.');
      const chunks = [];
      for (const hash of ref.hashes) {
        if (!/^[a-f0-9]{64}$/.test(hash)) throw new Error('Invalid Firebase chunk identifier.');
        const snap = await root.collection('blobs').doc(hash).get();
        if (!snap.exists) throw new Error('A Firebase data chunk is missing.');
        const payload = Buffer.from(snap.data().payload);
        if (payload.length > CHUNK || digest(payload) !== hash) throw new Error('Firebase data integrity check failed.');
        chunks.push(payload); known.add(hash);
      }
      const raw = await decompress(Buffer.concat(chunks), { maxOutputLength: Math.max(1, ref.bytes) });
      if (raw.length !== ref.bytes || digest(raw) !== ref.digest) throw new Error('Firebase data integrity check failed.');
      return JSON.parse(raw.toString('utf8'));
    },
  };
}

export function preserveMemberships(data, previous = []) {
  const ledger = new Map(previous.map(row => [row.order_id, { ...row }]));
  for (const order of data.paymentOrders ?? []) {
    const dates = paidOrderDates(order);
    if (!dates || !order.orderId || !order.userId || ledger.has(order.orderId)) continue;
    ledger.set(order.orderId, { order_id: order.orderId, user_id: order.userId, payment_id: order.paymentId,
      plan_id: order.planId ?? null, amount_paise: order.amount ?? null, currency: order.currency ?? null,
      recorded_at: order.verifiedAt, purchased_at: dates.purchasedAt, expires_at: dates.expiresAt,
      purchase_date_source: order.purchaseDateSource || 'saved_verification' });
  }
  for (const order of data.paymentOrders ?? []) {
    const term = ledger.get(order.orderId);
    if (term) Object.assign(order, { purchasedAt: term.purchased_at, expiresAt: term.expires_at,
      purchaseDateSource: term.purchase_date_source, ...(term.plan_id ? { planId: term.plan_id } : {}) });
  }
  for (const user of data.users ?? []) {
    const term = [...ledger.values()].filter(t => t.user_id === user.id)
      .sort((a, b) => Date.parse(b.expires_at) - Date.parse(a.expires_at) || a.order_id.localeCompare(b.order_id))[0];
    if (term) Object.assign(user, { subscriptionPurchasedAt: term.purchased_at, subscriptionExpiresAt: term.expires_at,
      subscriptionOrderId: term.order_id, plan: term.plan_id });
  }
  return [...ledger.values()];
}

export function createFirebaseState({ db, namespace = 'medicomm' }) {
  if (!/^[a-zA-Z0-9_-]{1,100}$/.test(namespace)) throw new Error('Invalid Firebase namespace.');
  const root = db.collection('medullaApps').doc(namespace), blobs = createFirebaseBlobs(root);
  let cached;
  async function load() {
    const snap = await root.get();
    if (!snap.exists) throw new Error('Firebase has not been migrated. Import and verify the Supabase backup first.');
    const manifest = snap.data();
    if (manifest.format !== 1 || !Number.isSafeInteger(manifest.revision) || !manifest.fields || !manifest.ledger) throw new Error('Invalid Firebase app state.');
    const data = Object.fromEntries(await Promise.all(Object.entries(manifest.fields).map(async ([key, ref]) => [key, await blobs.get(ref)])));
    const ledger = await blobs.get(manifest.ledger);
    cached = { manifest, ledger };
    return { data, revision: manifest.revision, membershipCount: ledger.length };
  }
  async function save(data, revision) {
    if (!cached || cached.manifest.revision !== revision) throw new HttpError(409, 'Reload the latest Firebase state.');
    const ledger = preserveMemberships(data, cached.ledger);
    const fields = Object.fromEntries(await Promise.all(Object.entries(data).map(async ([key, value]) => {
      const old = cached.manifest.fields[key];
      return [key, old?.digest === fingerprint(value) ? old : await blobs.put(value)];
    })));
    const ledgerRef = cached.manifest.ledger.digest === fingerprint(ledger) ? cached.manifest.ledger : await blobs.put(ledger);
    const manifest = { format: 1, revision: revision + 1, fields, ledger: ledgerRef, updatedAt: new Date().toISOString(), migration: cached.manifest.migration };
    if (jsonBytes(manifest).length > 700000) throw new Error('Firebase manifest is too large.');
    let committed;
    await db.runTransaction(async tx => {
      const current = await tx.get(root);
      if (!current.exists || current.data().revision !== revision) throw new HttpError(409, 'Data changed on another server. Please retry.');
      const previous = current.data();
      committed = { ...previous, ...manifest, statsVersion: (previous.statsVersion || 0) + 1,
        liveStats: { ...previous.liveStats, ...liveStateStats(data, ledger.length) } };
      tx.set(root, committed);
    });
    cached = { manifest: committed, ledger };
  }
  async function refreshLiveStats() {
    for (let retry = 0; retry < 4; retry++) {
      const loaded = await load(), snapshot = cached.manifest;
      const liveStats = { ...liveStateStats(loaded.data, loaded.membershipCount),
        notepad: await countNotepadRecords(root), notepadNeedsRefresh: false };
      try {
        await db.runTransaction(async tx => {
          const current = await tx.get(root), value = current.exists ? current.data() : {};
          if (value.revision !== loaded.revision || (value.statsVersion || 0) !== (snapshot.statsVersion || 0)) throw new HttpError(409, 'Data changed while refreshing counters.');
          tx.set(root, { ...value, statsVersion: (value.statsVersion || 0) + 1, liveStats });
        });
        return liveStats;
      } catch (error) { if (error.status !== 409 || retry === 3) throw error; }
    }
  }
  return { root, blobs, load, save, refreshLiveStats, async check() {
    const snap = await root.get();
    if (!snap.exists || snap.data().format !== 1) throw new Error('Firebase state is unavailable.');
  }, async importState(data, ledger, migration) {
    const fields = Object.fromEntries(await Promise.all(Object.entries(data).map(async ([key,value]) => [key, await blobs.put(value)])));
    const ledgerRef = await blobs.put(ledger);
    const manifest = { format: 1, revision: 0, fields, ledger: ledgerRef, migration, updatedAt: new Date().toISOString(), statsVersion: 0,
      liveStats: { ...liveStateStats(data, ledger.length), notepad: migration.notepad || { drafts: null, reviews: null },
        notepadNeedsRefresh: !migration.notepad } };
    if (jsonBytes(manifest).length > 700000) throw new Error('Firebase manifest is too large.');
    await db.runTransaction(async tx => {
      const current = await tx.get(root);
      if (current.exists) {
        if (current.data().migration?.fingerprint !== migration.fingerprint) throw new Error('Firebase already contains a different migration. Refusing to overwrite.');
        return;
      }
      tx.create(root, manifest);
    });
    return load();
  } };
}
