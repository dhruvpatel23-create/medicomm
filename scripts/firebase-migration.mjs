import { existsSync, readFileSync } from 'node:fs';
import { mkdir, readFile, writeFile, copyFile, rename } from 'node:fs/promises';
import path from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { firebaseServices } from '../server/firebaseAdmin.mjs';
import { createFirebaseState, digest, fingerprint } from '../server/firebaseStore.mjs';
import { createFirebaseNotepad } from '../server/firebaseNotepad.mjs';
import { createFirebaseUploads } from '../server/firebaseUploads.mjs';

for (const file of ['.env.local', '.env']) if (existsSync(file)) process.loadEnvFile(file);
const args = process.argv.slice(2), command = args[0] || 'check';
const option = (key, fallback) => { const i = args.indexOf(key); return i < 0 ? fallback : args[i + 1]; };
const dir = path.resolve(option('--dir', 'tmp/firebase-migration'));
const namespace = process.env.FIREBASE_NAMESPACE || process.env.SUPABASE_STATE_KEY || 'medicomm';
const json = async file => JSON.parse((await readFile(file, 'utf8')).replace(/^\uFEFF/, ''));
const safeFile = (base, name) => {
  if (typeof name !== 'string' || !name || name.includes('\\') || name.split('/').some(p => ['..', '.', ''].includes(p)) || path.isAbsolute(name)) throw new Error('Unsafe migration filename.');
  const target = path.resolve(base, name);
  if (!target.startsWith(path.resolve(base) + path.sep)) throw new Error('Unsafe migration path.');
  return target;
};
const counts = data => Object.fromEntries(Object.entries(data).map(([k,v]) => [k, Array.isArray(v) ? v.length : v && typeof v === 'object' ? Object.keys(v).length : 1]));

function sourceClient() {
  const base = process.env.SUPABASE_URL, secret = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_KEY;
  if (!base || !secret) throw new Error('Supabase source credentials are missing. Export on the existing server using its current environment.');
  if (new URL(base).protocol !== 'https:') throw new Error('Supabase source must use HTTPS.');
  return async (pathname, query = {}, method = 'GET', body, binary = false) => {
    const url = new URL(pathname, base);
    for (const [key,value] of Object.entries(query)) url.searchParams.set(key,value);
    const response = await fetch(url, { method, signal: AbortSignal.timeout(60000),
      headers: { apikey: secret, ...(!secret.startsWith('sb_secret_') ? { Authorization: `Bearer ${secret}` } : {}), 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body) });
    if (!response.ok) throw new Error(`Supabase source request failed (HTTP ${response.status}, ${pathname.split('/')[2]}).`);
    return binary ? Buffer.from(await response.arrayBuffer()) : response.json();
  };
}

async function exportSource() {
  if (existsSync(path.join(dir, 'manifest.json'))) throw new Error('A backup already exists here. Use a new --dir; existing backups are never overwritten.');
  const request = sourceClient(), key = process.env.SUPABASE_STATE_KEY || 'medicomm';
  if (namespace !== key) throw new Error('Keep FIREBASE_NAMESPACE equal to the source state key during migration.');
  const table = process.env.SUPABASE_STATE_TABLE || 'app_state';
  const stateRows = await request(`/rest/v1/${encodeURIComponent(table)}`, { key: `eq.${key}`, select: 'data,revision' });
  if (stateRows.length !== 1 || !Number.isSafeInteger(stateRows[0].revision) || !Array.isArray(stateRows[0].data?.users)) throw new Error('Invalid Supabase source state.');
  const state = stateRows[0];
  const rows = async (name, filter, order) => {
    const all = [];
    for (let offset = 0; ; offset += 500) {
      const page = await request(`/rest/v1/${name}`, { ...filter, order, limit: '500', offset: String(offset) });
      all.push(...page); if (page.length < 500) return all;
    }
  };
  const ledger = await rows('medicomm_paid_memberships', { app_key: `eq.${key}` }, 'order_id.asc');
  const drafts = await rows('notepad_drafts', { namespace: `eq.${key}` }, 'user_id.asc,draft_id.asc');
  const reviews = await rows('notepad_reviews', { namespace: `eq.${key}` }, 'user_id.asc,id.asc');
  // Older installations also keep reviews in app state; retain those too.
  const seen = new Set(reviews.map(r => `${r.user_id}:${r.id}`));
  for (const review of state.data.shortNoteReviews || []) {
    if (!seen.has(`${review.userId}:${review.id}`)) reviews.push({ namespace: key, user_id: review.userId,
      id: review.id, question_id: review.questionId, submitted_at: review.submittedAt, review });
  }
  await mkdir(dir, { recursive: true, mode: 0o700 });
  const files = [];
  async function store(name, bytes) {
    const target = safeFile(dir, name); await mkdir(path.dirname(target), { recursive: true, mode: 0o700 });
    await writeFile(target, bytes, { mode: 0o600 }); files.push({ name, bytes: bytes.length, sha256: digest(bytes) });
  }
  for (const [name,value] of Object.entries({ 'state.json': state, 'memberships.json': ledger, 'drafts.json': drafts, 'reviews.json': reviews })) {
    await store(name, Buffer.from(JSON.stringify(value)));
  }
  const bucket = process.env.SUPABASE_UPLOAD_BUCKET || 'medicomm-uploads';
  const objects = [], prefixes = [''];
  while (prefixes.length) {
    const prefix = prefixes.shift();
    for (let offset = 0; ; offset += 500) {
      const page = await request(`/storage/v1/object/list/${encodeURIComponent(bucket)}`, {}, 'POST', { prefix, limit: 500, offset, sortBy: { column: 'name', order: 'asc' } });
      for (const item of page) {
        const name = prefix ? `${prefix}/${item.name}` : item.name;
        safeFile(dir, `uploads/${name}`);
        if (item.id === null) prefixes.push(name);
        else {
          const bytes = await request(`/storage/v1/object/${encodeURIComponent(bucket)}/${name.split('/').map(encodeURIComponent).join('/')}`, {}, 'GET', undefined, true);
          await store(`uploads/${name}`, bytes); objects.push(name);
        }
      }
      if (page.length < 500) break;
    }
  }
  const [latest] = await request(`/rest/v1/${encodeURIComponent(table)}`, { key: `eq.${key}`, select: 'revision' });
  if (latest?.revision !== state.revision) throw new Error('Source changed during export. Stop all app writers and export into a new directory.');
  const manifest = { format: 1, namespace, sourceRevision: state.revision, sourcePaused: args.includes('--source-paused'),
    createdAt: new Date().toISOString(), files, objects, counts: counts(state.data), ledger: ledger.length, drafts: drafts.length, reviews: reviews.length };
  await writeFile(path.join(dir, 'manifest.json'), JSON.stringify(manifest, null, 2), { mode: 0o600 });
  console.log(JSON.stringify({ exported: true, directory: dir, counts: manifest.counts, memberships: ledger.length, drafts: drafts.length, reviews: reviews.length, uploads: objects.length, sourcePaused: manifest.sourcePaused }));
}

async function loadBackup() {
  const manifest = await json(path.join(dir, 'manifest.json'));
  if (manifest.format !== 1 || manifest.namespace !== namespace || !manifest.sourcePaused) throw new Error('Import requires a final backup exported with --source-paused after stopping every Supabase writer.');
  const names = new Set();
  for (const file of manifest.files) {
    if (names.has(file.name)) throw new Error('Duplicate backup filename.'); names.add(file.name);
    const bytes = await readFile(safeFile(dir, file.name));
    if (bytes.length !== file.bytes || digest(bytes) !== file.sha256) throw new Error(`Backup integrity check failed: ${file.name}`);
  }
  for (const name of ['state.json', 'memberships.json', 'drafts.json', 'reviews.json', ...manifest.objects.map(n => `uploads/${n}`)]) {
    if (!names.has(name)) throw new Error('Incomplete backup manifest.');
  }
  return { manifest, state: await json(path.join(dir,'state.json')), ledger: await json(path.join(dir,'memberships.json')),
    drafts: await json(path.join(dir,'drafts.json')), reviews: await json(path.join(dir,'reviews.json')) };
}

async function transfer(command) {
  const backup = await loadBackup(), { manifest, state, ledger, drafts, reviews } = backup;
  const firebase = firebaseServices(), store = createFirebaseState({ db: firebase.db, namespace });
  const notes = createFirebaseNotepad({ db: firebase.db, namespace });
  const migration = { fingerprint: fingerprint(manifest), sourceRevision: manifest.sourceRevision, counts: manifest.counts, uploads: manifest.objects.length };
  const existing = await store.root.get();
  if (existing.exists && (existing.data().migration?.fingerprint !== migration.fingerprint || existing.data().revision !== 0)) throw new Error('Firebase already contains different or live data. Refusing a migration over it.');
  const useCloud = process.env.UPLOAD_STORAGE === 'firebase';
  if (useCloud) await createFirebaseUploads(firebase.bucket).check();
  const uploadDir = path.join(path.resolve(process.env.RUNTIME_DATA_DIR || 'runtime-data'), 'uploads');
  for (const name of manifest.objects) {
    const source = safeFile(dir, `uploads/${name}`), bytes = await readFile(source);
    if (useCloud) {
      const file = firebase.bucket.file(name), [exists] = await file.exists();
      if (!exists && command === 'import') await file.save(bytes, { resumable: false, preconditionOpts: { ifGenerationMatch: 0 } });
      const saved = (await file.download())[0];
      if (digest(saved) !== digest(bytes)) throw new Error('Firebase upload verification failed.');
    } else {
      const target = safeFile(uploadDir, name);
      if (!existsSync(target) && command === 'import') {
        await mkdir(path.dirname(target), { recursive: true, mode: 0o700 });
        const temp = `${target}.migration-part`; await copyFile(source, temp); await rename(temp, target);
      }
      if (digest(await readFile(target)) !== digest(bytes)) throw new Error('Private upload verification failed.');
    }
  }
  let legacyReviewIds = 0;
  for (const [kind,rows] of [['drafts',drafts], ['reviews',reviews]]) for (const [index,row] of rows.entries()) {
    // The source array position distinguishes even identical legacy records.
    // Keep the original row untouched so its backup hash still verifies exactly.
    const legacyId = kind === 'reviews' && !row.id ? `legacy-${fingerprint({ row, index })}` : undefined;
    if (legacyId) legacyReviewIds++;
    if (command === 'import') await notes.importRow(kind,row,legacyId);
    await notes.verifyRow(kind,row,legacyId);
  }
  if (command === 'import') await store.importState(state.data, ledger, migration);
  const saved = await store.load();
  if (!isDeepStrictEqual(saved.data, state.data)) throw new Error('App-state verification failed.');
  const root = (await store.root.get()).data();
  if (fingerprint(await store.blobs.get(root.ledger)) !== fingerprint(ledger)) throw new Error('Membership-ledger verification failed.');
  if (root.revision !== 0 || root.migration?.fingerprint !== migration.fingerprint) throw new Error('Migration verification failed.');
  console.log(JSON.stringify({ verified: true, projectId: firebase.projectId, namespace, counts: counts(saved.data), memberships: ledger.length,
    drafts: drafts.length, reviews: reviews.length, legacyReviewIds, uploads: manifest.objects.length, uploadStorage: useCloud ? 'firebase' : 'private server files' }));
}

async function main() {
  if (command === 'export') return exportSource();
  if (['import','verify'].includes(command)) return transfer(command);
  if (command !== 'check') throw new Error('Use check, export, import or verify.');
  const firebase = firebaseServices();
  const snap = await firebase.db.collection('medullaApps').doc(namespace).get();
  console.log(JSON.stringify({ firestoreReachable: true, projectId: firebase.projectId, namespace, migrated: snap.exists }));
}
main().catch(error => {
  // SDK/network diagnostics may contain request credentials; emit only safe
  // application errors or a provider error code, never raw SDK stacks/objects.
  console.error(error.code ? `Migration failed (provider code ${String(error.code)}). No source data was changed.` : error instanceof TypeError ? 'Network/SDK operation failed. No source data was changed.' : error.message);
  process.exitCode = 1;
});
