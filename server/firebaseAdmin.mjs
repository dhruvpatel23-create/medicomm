import { applicationDefault, getApps, initializeApp } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';
import { getStorage } from 'firebase-admin/storage';
import { getAuth } from 'firebase-admin/auth';
import { readFileSync } from 'node:fs';

export function firebaseServices(env = process.env) {
  const projectId = env.FIREBASE_PROJECT_ID || env.GOOGLE_CLOUD_PROJECT ||
    (env.GOOGLE_APPLICATION_CREDENTIALS && JSON.parse(readFileSync(env.GOOGLE_APPLICATION_CREDENTIALS, 'utf8')).project_id);
  if (!projectId) throw new Error('Set FIREBASE_PROJECT_ID and server application credentials.');
  const name = `medulla-${projectId}`;
  const app = getApps().find(a => a.name === name) || initializeApp({
    credential: applicationDefault(), projectId,
  }, name);
  return { app, auth: getAuth(app), projectId, db: getFirestore(app), bucket: env.FIREBASE_STORAGE_BUCKET ? getStorage(app).bucket(env.FIREBASE_STORAGE_BUCKET) : null };
}
