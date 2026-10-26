import { createHash, randomUUID } from 'node:crypto';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { HttpError } from './security.mjs';
import { createFirebaseBlobs } from './firebaseStore.mjs';

const hash = value => createHash('sha256').update(value).digest('hex');
const participantKey = (test, userId) => hash(JSON.stringify([test.id, test.eventId, userId]));
const eventKey = test => hash(JSON.stringify([test.id, test.eventId]));
export function massAttemptId(test, userId) {
  const id = participantKey(test, userId).slice(0, 32);
  return `${id.slice(0, 8)}-${id.slice(8, 12)}-${id.slice(12, 16)}-${id.slice(16, 20)}-${id.slice(20)}`;
}

// Each participant has an independent transaction. Immutable question sets are
// shared once, rather than rewriting 300 questions on every answer selection.
export function createMassTestStore({ directory, db, namespace = 'medicomm' }) {
  const root = db?.collection('medullaApps').doc(namespace);
  const blobs = root && createFirebaseBlobs(root);
  const questionsCache = new Map();
  const empty = (test, userId) => ({ testId: test.id, eventId: test.eventId, eventKey: eventKey(test), userId, waitingJoinedAt: null, attempt: null });
  const file = key => path.join(directory, `${key}.json`);
  const ref = key => root.collection('massTestParticipants').doc(key);

  async function questions(id, value) {
    if (!questionsCache.has(id)) {
      const pending = (async () => {
        if (root) {
          const doc = root.collection('massTestQuestionSets').doc(id);
          if (value) {
            const blob = await blobs.put(value);
            try { await doc.create({ blob }); } catch (e) { if (e.code !== 6 && e.code !== 'already-exists') throw e; }
          } else {
            const snap = await doc.get();
            if (!snap.exists) throw new Error('Question set is missing.');
            value = await blobs.get(snap.data().blob);
          }
        } else {
          const target = path.join(directory, `questions-${id}.json`);
          if (value) {
            await fs.mkdir(directory, { recursive: true });
            // Atomic publication prevents another worker reading a partial set.
            const temporary = `${target}.${randomUUID()}.tmp`;
            await fs.writeFile(temporary, JSON.stringify(value), { mode: 0o600 });
            await fs.rename(temporary, target);
          } else value = JSON.parse(await fs.readFile(target, 'utf8'));
        }
        if (hash(JSON.stringify(value)) !== id) throw new Error('Question set integrity check failed.');
        return value;
      })();
      questionsCache.set(id, pending);
      pending.catch(() => questionsCache.delete(id));
    }
    return questionsCache.get(id);
  }
  async function hydrate(record) {
    if (record.attempt) record.attempt.questions = await questions(record.attempt.questionSet);
    return record;
  }
  async function pack(record) {
    const next = { ...record };
    if (record.attempt) {
      const { questions: value, ...attempt } = record.attempt;
      if (!attempt.questionSet) {
        attempt.questionSet = hash(JSON.stringify(value));
        await questions(attempt.questionSet, value);
      }
      next.attempt = attempt;
      if (attempt.status === 'completed') {
        next.ranking = { attemptId: attempt.id, name: String(record.participantName || 'Participant').slice(0, 254),
          score: value.filter(question => attempt.answers[question.id] === question.answerIndex).length,
          completedAt: attempt.completedAt };
      }
    }
    return next;
  }
  async function readLocal(key, test, userId) {
    try { return JSON.parse(await fs.readFile(file(key), 'utf8')); }
    catch (e) { if (e.code === 'ENOENT') return empty(test, userId); throw e; }
  }
  async function lock(key) {
    await fs.mkdir(directory, { recursive: true });
    const name = `${file(key)}.lock`;
    for (let i = 0; i < 250; i++) {
      try {
        const handle = await fs.open(name, 'wx', 0o600);
        await handle.writeFile(String(process.pid));
        return async () => { await handle.close(); await fs.unlink(name); };
      } catch (e) {
        if (e.code !== 'EEXIST') throw e;
        // Recover locks abandoned by a crashed worker, never steal a live lock.
        try {
          const owner = Number(await fs.readFile(name, 'utf8'));
          if (Number.isSafeInteger(owner) && owner > 0) {
            try { process.kill(owner, 0); }
            catch (error) { if (error.code === 'ESRCH') await fs.unlink(name); }
          }
        } catch (error) { if (error.code !== 'ENOENT') throw error; }
        await new Promise(resolve => setTimeout(resolve, 20));
      }
    }
    throw new HttpError(503, 'Your test is still saving. Please try again.');
  }
  return {
    async completedRows(test) {
      if (root) {
        const snapshot = await root.collection('massTestParticipants').where('eventKey', '==', eventKey(test))
          .select('ranking', 'userId').get();
        return snapshot.docs.filter(doc => doc.data().ranking).map(doc => ({ ...doc.data().ranking, userId: doc.data().userId }));
      }
      let names;
      try { names = (await fs.readdir(directory)).filter(name => /^[a-f0-9]{64}\.json$/.test(name)); }
      catch (error) { if (error.code === 'ENOENT') return []; throw error; }
      const rows = [];
      // Bound local I/O even when thousands of candidates have participant files.
      let index = 0;
      await Promise.all(Array.from({ length: Math.min(16, names.length) }, async () => {
        while (index < names.length) {
          const name = names[index++];
          const record = JSON.parse(await fs.readFile(path.join(directory, name), 'utf8'));
          if (record.testId === test.id && record.eventId === test.eventId && record.ranking) {
            rows.push({ ...record.ranking, userId: record.userId });
          }
        }
      }));
      return rows;
    },
    async get(test, userId) {
      const key = participantKey(test, userId);
      const row = root ? (await ref(key).get()).data() ?? empty(test, userId) : await readLocal(key, test, userId);
      return hydrate(row);
    },
    async transact(test, userId, operation) {
      const key = participantKey(test, userId);
      if (root) return db.runTransaction(async transaction => {
        const snap = await transaction.get(ref(key));
        const record = await hydrate(snap.data() ?? empty(test, userId));
        const result = operation(record);
        if (result.changed) transaction.set(ref(key), await pack(record));
        return result.value;
      });
      const release = await lock(key);
      try {
        const record = await hydrate(await readLocal(key, test, userId));
        const result = operation(record);
        if (result.changed) {
          const temporary = `${file(key)}.${randomUUID()}.tmp`;
          await fs.writeFile(temporary, JSON.stringify(await pack(record)), { mode: 0o600 });
          await fs.rename(temporary, file(key));
        }
        return result.value;
      } finally { await release(); }
    },
  };
}
