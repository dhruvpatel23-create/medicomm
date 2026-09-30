// Read-only inventory by default. --apply uploads files without changing app state.
// Run on the old host before its ephemeral disk is discarded.
import { readFile, access } from 'node:fs/promises';
import path from 'node:path';
import { decodeImage } from '../server/uploads.mjs';

const url = (process.env.SUPABASE_URL || '').replace(/\/$/, '');
const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SECRET_KEY;
const bucket = process.env.SUPABASE_UPLOAD_BUCKET || 'medicomm-uploads';
if (!url || !key) throw new Error('Set server-side Supabase credentials before running.');
const headers = { apikey: key, Authorization: `Bearer ${key}` };
const stateKey = process.env.SUPABASE_STATE_KEY || 'medicomm';
const table = process.env.SUPABASE_STATE_TABLE || 'app_state';
const state = await fetch(`${url}/rest/v1/${encodeURIComponent(table)}?key=eq.${encodeURIComponent(stateKey)}`, { headers, signal: AbortSignal.timeout(15000) });
if (!state.ok) throw new Error('Could not read remote state.');
const data = (await state.json())[0]?.data;
if (!data) throw new Error('No remote app state found.');
const names = new Set([...(data.users || []).map(user => user.profileImagePath), ...(data.communities || []).flatMap(group => (group.messages || []).map(message => message.imagePath))].filter(Boolean));
const roots = [process.env.RUNTIME_DATA_DIR || 'runtime-data', 'data'].map(root => path.resolve(root, 'uploads'));
let missing = 0;
for (const name of names) {
  if (!/^[a-zA-Z0-9_-]+\.(png|jpg|jpeg|webp|gif)$/.test(name)) throw new Error('Unsafe upload filename in database.');
  let source;
  for (const root of roots) { try { await access(path.join(root, name)); source = path.join(root, name); break; } catch {} }
  const endpoint = `${url}/storage/v1/object/${encodeURIComponent(bucket)}/${encodeURIComponent(name)}`;
  const existing = await fetch(endpoint, { method: 'HEAD', headers, signal: AbortSignal.timeout(15000) });
  if (existing.ok) continue;
  if (![400, 404].includes(existing.status)) throw new Error(`Storage check failed (${existing.status}).`);
  if (!source) { missing++; continue; }
  const mime = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif' }[path.extname(name)];
  const bytes = await readFile(source);
  decodeImage(`data:${mime};base64,${bytes.toString('base64')}`);
  if (process.argv.includes('--apply')) {
    const uploaded = await fetch(endpoint, { method: 'POST', headers: { ...headers, 'Content-Type': mime }, body: bytes, signal: AbortSignal.timeout(15000) });
    if (!uploaded.ok) throw new Error(`Upload failed (${uploaded.status}); no state was changed.`);
  }
}
console.log(JSON.stringify({ referenced: names.size, missing, mode: process.argv.includes('--apply') ? 'apply' : 'dry-run' }));
if (missing) process.exitCode = 1;
