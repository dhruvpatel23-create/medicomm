import { subscriptionDetails } from './subscriptions.mjs';

export function liveStateStats(data, membershipCount, now = Date.now()) {
  const counts = Object.fromEntries(Object.entries(data).map(([key, value]) => [key,
    Array.isArray(value) ? value.length : value && typeof value === 'object' ? Object.keys(value).length : value == null ? 0 : 1]));
  const activeSubscriptions = {};
  for (const user of data.users || []) {
    const term = subscriptionDetails(data, user.id, now);
    if (term.subscriptionStatus === 'active') activeSubscriptions[term.plan || 'unknown'] = (activeSubscriptions[term.plan || 'unknown'] || 0) + 1;
  }
  return { users: data.users?.length || 0, memberships: membershipCount, counts, activeSubscriptions,
    updatedAt: new Date(now).toISOString() };
}

export async function countNotepadRecords(root) {
  const totals = { drafts: 0, reviews: 0 };
  for (const owner of await root.collection('notepadUsers').listDocuments()) {
    for (const kind of ['drafts', 'reviews']) totals[kind] += (await owner.collection(kind).count().get()).data().count;
  }
  return totals;
}

// Call only after the transaction's reads, in the same transaction as the row.
export function noteStatsWrite(tx, root, snapshot, kind, delta) {
  if (!snapshot.exists) return; // Staged imports must never publish app state.
  const state = snapshot.data(), stats = state.liveStats || {};
  const notepad = { drafts: null, reviews: null, ...stats.notepad };
  const known = Number.isSafeInteger(notepad[kind]);
  if (known) notepad[kind] += delta;
  tx.set(root, { ...state, statsVersion: (state.statsVersion || 0) + 1,
    liveStats: { ...stats, notepad, notepadNeedsRefresh: stats.notepadNeedsRefresh || !known,
      updatedAt: new Date().toISOString() } });
}
