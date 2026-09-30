import { randomBytes } from 'node:crypto';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';
import { HttpError } from './security.mjs';

export function decodeImage(dataUrl) {
  const match = typeof dataUrl === 'string' && dataUrl.match(/^data:(image\/(?:png|jpeg|webp|gif));base64,([A-Za-z0-9+/]+={0,2})$/);
  if (!match || match[2].length > 7 * 1024 * 1024) throw new HttpError(400, 'Send a PNG, JPEG, WebP or GIF image up to 5 MB.');
  const bytes = Buffer.from(match[2], 'base64');
  if (!bytes.length || bytes.length > 5 * 1024 * 1024 || bytes.toString('base64') !== match[2]) throw new HttpError(400, 'Invalid image encoding or size.');
  const mime = match[1];
  const valid = mime === 'image/png' ? bytes.subarray(0, 8).equals(Buffer.from('89504e470d0a1a0a', 'hex'))
    : mime === 'image/jpeg' ? bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255
    : mime === 'image/gif' ? /GIF8[79]a/.test(bytes.subarray(0, 6).toString('ascii'))
    : bytes.subarray(0, 4).toString() === 'RIFF' && bytes.subarray(8, 12).toString() === 'WEBP';
  if (!valid) throw new HttpError(400, 'Image content does not match its file type.');
  return { bytes, mime, extension: { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/gif': 'gif', 'image/webp': 'webp' }[mime] };
}

export function createUploads({ url, key, bucket, directory, fetchImpl = fetch }) {
  const headers = { apikey: key, Authorization: `Bearer ${key}` };
  const endpoint = name => `${url}/storage/v1/object/${encodeURIComponent(bucket)}/${encodeURIComponent(name)}`;
  return {
    async save(dataUrl) {
      const { bytes, mime, extension } = decodeImage(dataUrl);
      const name = `user-${randomBytes(24).toString('hex')}.${extension}`;
      if (bucket) {
        const response = await fetchImpl(endpoint(name), { method: 'POST', headers: { ...headers, 'Content-Type': mime }, body: bytes, signal: AbortSignal.timeout(15000) });
        if (!response.ok) throw new HttpError(503, 'Image storage is unavailable.');
      } else await writeFile(path.join(directory, name), bytes, { flag: 'wx' });
      return name;
    },
    async read(name) {
      const response = await fetchImpl(endpoint(name), { headers, signal: AbortSignal.timeout(15000) });
      if (!response.ok) throw new HttpError(response.status === 404 ? 404 : 503, 'Image is unavailable.');
      const bytes = Buffer.from(await response.arrayBuffer());
      if (bytes.length > 5 * 1024 * 1024) throw new HttpError(502, 'Invalid stored image.');
      return bytes;
    },
    async check() {
      if (!bucket) return;
      const response = await fetchImpl(`${url}/storage/v1/bucket/${encodeURIComponent(bucket)}`, { headers, signal: AbortSignal.timeout(10000) });
      if (!response.ok) throw new Error('Upload bucket is unavailable.');
      const metadata = await response.json();
      if (metadata.public !== false) throw new Error('The upload bucket must be private.');
    },
  };
}
