import { randomBytes } from 'node:crypto';
import { HttpError } from './security.mjs';
import { decodeImage } from './uploads.mjs';

export function createFirebaseUploads(bucket) {
  if (!bucket) throw new Error('Configure FIREBASE_STORAGE_BUCKET.');
  return {
    async save(dataUrl) {
      const { bytes, mime, extension } = decodeImage(dataUrl);
      const name = `user-${randomBytes(24).toString('hex')}.${extension}`;
      await bucket.file(name).save(bytes, { resumable: false, contentType: mime });
      return name;
    },
    async read(name) {
      try {
        const file = bucket.file(name), [meta] = await file.getMetadata();
        if (Number(meta.size) > 5 * 1024 * 1024) throw new HttpError(502, 'Invalid stored image.');
        return (await file.download())[0];
      } catch (error) { throw new HttpError(error.code === 404 ? 404 : 503, 'Image is unavailable.'); }
    },
    async remove(name) {
      if (!/^user-[a-f0-9]{48}\.(png|jpg|gif|webp)$/.test(name)) throw new Error('Invalid upload name.');
      await bucket.file(name).delete({ ignoreNotFound: true });
    },
    async check() {
      await bucket.getMetadata();
      const [policy] = await bucket.iam.getPolicy();
      if (policy.bindings?.some(b => b.members?.some(m => ['allUsers', 'allAuthenticatedUsers'].includes(m)))) throw new Error('Firebase upload bucket must be private.');
    },
  };
}
