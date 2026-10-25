import { existsSync, readFileSync } from 'node:fs';
import { firebaseServices } from '../server/firebaseAdmin.mjs';
import { createFirebaseState } from '../server/firebaseStore.mjs';
import { subscriptionDetails } from '../server/subscriptions.mjs';

for (const file of ['.env.local', '.env']) if (existsSync(file)) process.loadEnvFile(file);
// The existing VPS credential location is private and outside the deployment.
if (!process.env.GOOGLE_APPLICATION_CREDENTIALS && existsSync('/etc/medulla/firebase-admin.json')) {
  process.env.GOOGLE_APPLICATION_CREDENTIALS = '/etc/medulla/firebase-admin.json';
}
const mode = process.argv[2] || 'stats';
const args = process.argv.slice(3);
if (!['stats', 'users'].includes(mode)) throw new Error('Use stats or users.');
let db;
try {
  const firebase = firebaseServices(); db = firebase.db;
  const namespace = process.env.FIREBASE_NAMESPACE || process.env.SUPABASE_STATE_KEY || 'medicomm';
  const store = createFirebaseState({ db, namespace });
  const { data, revision, membershipCount } = await store.load();
  const now = Date.now();
  const users = (data.users || []).map(user => {
    const membership = subscriptionDetails(data, user.id, now);
    return { id: user.id, name: user.name || '', email: user.email || '',
      plan: membership.plan || 'free', subscriptionStatus: membership.subscriptionStatus,
      expiresAt: membership.subscriptionExpiresAt || null };
  });
  if (mode === 'users') {
    const index = args.indexOf('--email');
    if (index >= 0 && !args[index + 1]) throw new Error('Supply an email after --email.');
    const selected = index < 0 ? users : users.filter(u => u.email.toLowerCase() === args[index + 1].trim().toLowerCase());
    console.table(selected);
    console.log(`${selected.length} account(s). Passwords, session tokens and private keys are never included.`);
  } else {
    const stateCounts = Object.fromEntries(Object.entries(data).map(([key,value]) =>
      [key, Array.isArray(value) ? value.length : value && typeof value === 'object' ? Object.keys(value).length : value == null ? 0 : 1]));
    const plans = {};
    for (const user of users) {
      const label = `${user.plan} / ${user.subscriptionStatus}`;
      plans[label] = (plans[label] || 0) + 1;
    }
    // listDocuments includes missing parent documents with subcollections, so
    // users with drafts/reviews are counted even without a notepadUsers profile.
    const owners = await store.root.collection('notepadUsers').listDocuments();
    const notepad = { drafts: 0, reviews: 0 };
    for (const owner of owners) for (const kind of ['drafts', 'reviews']) {
      notepad[kind] += (await owner.collection(kind).count().get()).data().count;
    }
    let bundledQuestions = null;
    if (existsSync('data/practice-question-bank.json')) {
      const bank = JSON.parse(readFileSync('data/practice-question-bank.json', 'utf8').replace(/^\uFEFF/, ''));
      bundledQuestions = new Set((bank.subjects || []).flatMap(s => (s.questions || []).map(q => q.id))).size;
    }
    console.log(JSON.stringify({ readOnly: true, projectId: firebase.projectId, namespace, revision,
      reportedAt: new Date().toISOString(), users: users.length, memberships: membershipCount,
      subscriptionBreakdown: plans, stateRecordCounts: stateCounts, notepad,
      bundledPracticeQuestions: bundledQuestions,
      note: 'stateRecordCounts.questions counts app-saved question records; the bundled practice bank is counted separately. Notepad totals are live queries.' }, null, 2));
  }
} catch (error) {
  console.error(error.code ? `Firebase report failed (provider code ${error.code}).` : 'Firebase report failed. Check the private credentials, project and migration status.');
  process.exitCode = 1;
} finally { if (db) await db.terminate(); }
