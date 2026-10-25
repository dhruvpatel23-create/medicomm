import { createFirebaseBlobs, digest, fingerprint } from './firebaseStore.mjs';
import { validateDraft } from './notepadStore.mjs';
import { HttpError } from './security.mjs';

export function createFirebaseNotepad({ db, namespace = 'medicomm' }) {
  const root = db.collection('medullaApps').doc(namespace), blobs = createFirebaseBlobs(root);
  const records = (user, kind) => root.collection('notepadUsers').doc(digest(user)).collection(kind);
  const ref = (user, kind, id) => records(user, kind).doc(digest(id));
  const decode = async snap => snap.exists ? blobs.get(snap.data().payload) : null;
  async function list(user) {
    const snaps = await records(user, 'reviews').get();
    return snaps.docs.sort((a,b) => Date.parse(b.data().submittedAt) - Date.parse(a.data().submittedAt) || b.data().id.localeCompare(a.data().id));
  }
  async function importRow(kind, row) {
    if (!['drafts', 'reviews'].includes(kind) || row.namespace !== namespace || !row.user_id || !(row.draft_id || row.id)) throw new Error('Invalid migrated notepad row.');
    const id = kind === 'drafts' ? row.draft_id : row.id;
    const record = ref(row.user_id, kind, id), payload = await blobs.put(row);
    const meta = { payload, ...(kind === 'drafts' ? { revision: row.revision } : {
      id: row.id, questionId: row.question_id, submittedAt: row.submitted_at,
      imageNames: (row.review.answerPages ?? []).map(p => p.imagePath).filter(Boolean),
    }) };
    await db.runTransaction(async tx => {
      const old = await tx.get(record);
      if (old.exists) {
        if (old.data().payload.digest !== payload.digest) throw new HttpError(409, 'A different notepad record already exists.');
      } else tx.create(record, meta);
    });
  }
  return {
    importRow,
    async getDraft(user, id) { return decode(await ref(user, 'drafts', id).get()); },
    async putDraft(user, id, draft, revision) {
      validateDraft(draft);
      if (!Number.isSafeInteger(revision) || revision < 0) throw new HttpError(400, 'Invalid draft revision.');
      const row = { namespace, user_id: user, draft_id: id, draft, revision: revision + 1, updated_at: new Date().toISOString() };
      const record = ref(user, 'drafts', id), payload = await blobs.put(row);
      await db.runTransaction(async tx => {
        const old = await tx.get(record);
        if ((old.exists ? old.data().revision : 0) !== revision) throw new HttpError(409, 'This draft changed on another device.');
        tx.set(record, { payload, revision: row.revision });
      });
      return row;
    },
    async reviews(user, questionId = null, offset = 0, since = null) {
      const rows = (await list(user)).filter(s => (!questionId || s.data().questionId === questionId) &&
        (!since || Date.parse(s.data().submittedAt) >= Date.parse(since))).slice(offset, offset + 100);
      return Promise.all(rows.map(async s => (await decode(s)).review));
    },
    async summaries(user, offset = 0) {
      const groups = new Map();
      for (const snap of await list(user)) {
        const q = snap.data().questionId;
        if (groups.has(q)) groups.get(q).count++;
        else groups.set(q, { snap, count: 1 });
      }
      return Promise.all([...groups.values()].slice(offset, offset + 100).map(async ({snap,count}) => {
        const r = (await decode(snap)).review;
        return { id: r.id, questionId: r.questionId, submittedAt: r.submittedAt, score: r.score, attemptCount: count };
      }));
    },
    async saveReview(review) {
      return importRow('reviews', { namespace, user_id: review.userId, id: review.id,
        question_id: review.questionId, submitted_at: review.submittedAt, review });
    },
    async hasReview(user, id) { return (await ref(user, 'reviews', id).get()).exists; },
    async ownsImage(user, name) { return !(await records(user, 'reviews').where('imageNames', 'array-contains', name).limit(1).get()).empty; },
    async verifyRow(kind, row) {
      const snap = await ref(row.user_id, kind, kind === 'drafts' ? row.draft_id : row.id).get();
      const saved = await decode(snap);
      if (!saved || fingerprint(saved) !== fingerprint(row)) throw new Error('Notepad verification failed.');
    },
  };
}
