import test from 'node:test';
import assert from 'node:assert/strict';
import { randomBytes } from 'node:crypto';
import { createFirebaseState, preserveMemberships } from './firebaseStore.mjs';
import { createFirebaseNotepad } from './firebaseNotepad.mjs';
import { deploymentConfig } from './config.mjs';

function memoryFirestore() {
  const data = new Map(); let chain = Promise.resolve();
  const snapshot = path => ({ exists: data.has(path), id: path.split('/').at(-1), data: () => structuredClone(data.get(path)) });
  const collection = prefix => ({
    doc: id => doc(`${prefix}/${id}`),
    async get() { const docs = [...data.keys()].filter(p => p.startsWith(`${prefix}/`) && !p.slice(prefix.length + 1).includes('/')).map(snapshot); return { docs, empty: !docs.length }; },
    where(field, op, value) { return { limit() { return this; }, async get() {
      const all = await collection(prefix).get();
      const docs = all.docs.filter(d => op === 'array-contains' && d.data()[field]?.includes(value));
      return { docs, empty: !docs.length };
    } }; },
  });
  const doc = path => ({ path, collection: name => collection(`${path}/${name}`), get: async () => snapshot(path),
    async create(value) { if (data.has(path)) throw Object.assign(new Error('exists'), { code: 6 }); data.set(path, structuredClone(value)); },
  });
  const db = { collection, data, failNextCommit: false,
    runTransaction(callback) {
      const result = chain.then(async () => {
        const writes = [];
        const value = await callback({ get: ref => ref.get(),
          set: (ref, value) => writes.push([ref.path, value]),
          create: (ref, value) => { if (data.has(ref.path)) throw new Error('exists'); writes.push([ref.path, value]); },
        });
        if (db.failNextCommit) { db.failNextCommit = false; throw new Error('interrupted commit'); }
        for (const [p,v] of writes) data.set(p, structuredClone(v));
        return value;
      });
      chain = result.catch(() => {}); return result;
    },
  };
  return db;
}
const migration = { fingerprint: 'fixture', counts: {} };

test('large state round-trips in bounded chunks; unchanged fields are reused', async () => {
  const db = memoryFirestore(), store = createFirebaseState({db});
  const state = { users: [{id:'u'}], sessions:{}, questions:[{id:'q',payload:randomBytes(1800000).toString('base64')}] };
  await store.importState(state,[],migration);
  assert.deepEqual((await store.load()).data,state);
  const before = (await store.root.get()).data().fields.questions;
  assert.ok(before.hashes.length > 1);
  for (const [p,value] of db.data) if(p.includes('/blobs/')) assert.ok(value.payload.length <= 512*1024);
  state.users[0].name='New name';await store.save(state,0);
  assert.deepEqual((await store.root.get()).data().fields.questions,before);
  assert.equal((await store.load()).revision,1);
});
test('stale writers and different imports cannot replace committed data', async () => {
  const db=memoryFirestore(), first=createFirebaseState({db}), second=createFirebaseState({db});
  await first.importState({users:[],sessions:{}},[],migration);await second.load();
  await first.save({users:[{id:'u'}],sessions:{}},0);
  await assert.rejects(second.save({users:[],sessions:{}},0),{status:409});
  await assert.rejects(second.importState({users:[]},[],{fingerprint:'other'}),/Refusing to overwrite/);
  assert.equal((await second.load()).data.users[0].id,'u');
});
test('interrupted commits leave the previous snapshot readable and imports resume', async () => {
  const db=memoryFirestore(), store=createFirebaseState({db});
  db.failNextCommit=true;
  await assert.rejects(store.importState({users:[]},[],migration),/interrupted/);
  assert.equal((await store.root.get()).exists,false);
  await store.importState({users:[]},[],migration);
  db.failNextCommit=true;
  await assert.rejects(store.save({users:[{id:'u'}]},0),/interrupted/);
  assert.deepEqual((await store.load()).data,{users:[]});
});
test('missing or corrupted chunks fail closed; empty Firebase never seeds itself', async () => {
  const db=memoryFirestore(), store=createFirebaseState({db});
  await assert.rejects(store.load(),/not been migrated/);
  await store.importState({users:[]},[],migration);
  const hash=(await store.root.get()).data().fields.users.hashes[0];
  const p=`medullaApps/medicomm/blobs/${hash}`;
  db.data.set(p,{payload:Buffer.from('corrupt')});
  await assert.rejects(store.load(),/integrity check/);
  db.data.delete(p);await assert.rejects(store.load(),/chunk is missing/);
});
test('independent purchase ledger restores dates and plan without inventing payment evidence', () => {
  const term={order_id:'owner-term',user_id:'u',plan_id:'premium',purchased_at:'2026-10-25T00:00:00Z',expires_at:'2027-10-25T00:00:00Z',purchase_date_source:'owner_confirmed'};
  const data={users:[{id:'u'}],paymentOrders:[]};
  const ledger=preserveMemberships(data,[term]);
  assert.deepEqual(ledger,[term]);assert.equal(data.users[0].plan,'premium');
  assert.equal(data.users[0].subscriptionExpiresAt,term.expires_at);
  data.paymentOrders.push({orderId:'failed',userId:'u',status:'created'});
  assert.equal(preserveMemberships(data,ledger).length,1);
  data.paymentOrders.push({orderId:'owner-term',userId:'u',planId:'lite',purchasedAt:'2099-01-01T00:00:00Z'});
  preserveMemberships(data,ledger);
  assert.equal(data.paymentOrders[1].purchasedAt,term.purchased_at);
  assert.equal(data.paymentOrders[1].planId,'premium');
});
test('draft revisions, private review ownership and resumable row imports are preserved', async () => {
  const db=memoryFirestore(), notes=createFirebaseNotepad({db});
  const draft={version:2,pages:[{paper:'plain',strokes:[]}],pageIndex:0};
  const row=await notes.putDraft('u','short-notes:u:q',draft,0);
  assert.equal(row.revision,1);
  await assert.rejects(notes.putDraft('u','short-notes:u:q',draft,0),{status:409});
  assert.equal(await notes.getDraft('other','short-notes:u:q'),null);
  await notes.importRow('drafts',row);await notes.verifyRow('drafts',row);
  const review={id:'r',userId:'u',questionId:'q',submittedAt:'2026-10-25T00:00:00Z',score:3,answerPages:[{imagePath:'private.png'}]};
  await notes.saveReview(review);await notes.saveReview(review);
  assert.equal(await notes.ownsImage('u','private.png'),true);
  assert.equal(await notes.ownsImage('other','private.png'),false);
  assert.deepEqual(await notes.reviews('u'),[review]);
  assert.equal((await notes.summaries('u'))[0].attemptCount,1);
});
test('production Firebase requires explicit provider, project and persistent/private upload configuration', () => {
  const env={NODE_ENV:'production',DATABASE_PROVIDER:'firebase',FIREBASE_PROJECT_ID:'medullaprep',APP_ORIGINS:'https://medullaprep.com',UPLOAD_STORAGE:'local',RUNTIME_DATA_DIR:'/var/lib/medulla'};
  assert.equal(deploymentConfig(env).databaseProvider,'firebase');
  assert.throws(()=>deploymentConfig({...env,RUNTIME_DATA_DIR:''}),/RUNTIME_DATA_DIR/);
  assert.throws(()=>deploymentConfig({...env,FIREBASE_PROJECT_ID:''}),/FIREBASE_PROJECT_ID/);
  assert.throws(()=>deploymentConfig({...env,UPLOAD_STORAGE:'firebase'}),/FIREBASE_STORAGE_BUCKET/);
});
