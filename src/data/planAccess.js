const PAID_PLANS = ['lite', 'ultra', 'premium'];

export function canAccessFeature(membership, feature) {
  if (!membership?.hasPracticeAccess || membership.subscriptionStatus === 'expired') return false;
  const plan = String(membership.plan || membership.subscription || '').toLowerCase();
  if (feature === 'theory') return ['ultra', 'premium'].includes(plan);
  if (feature === 'usmle' || feature === 'tests') return plan === 'premium';
  // Legacy paid accounts retain basic practice while their plan is reconciled.
  return PAID_PLANS.includes(plan) || !plan;
}

export function practiceFeature(id) {
  if (id === 'theory') return 'theory';
  if (id === 'usmle') return 'usmle';
  if (id === 'neetpg-tests' || id === 'fmge-tests') return 'tests';
  return 'practice';
}

export const FEATURE_NAMES = {
  practice: 'Practice Questions', theory: 'Theory Practice', usmle: 'USMLE Practice Questions',
  tests: 'MEDULLA Practice Test', community: 'Community Access', inbox: 'Personal Inbox',
};

export function requiredPlans(feature) {
  if (feature === 'theory') return 'Ultra or Premium';
  if (feature === 'usmle' || feature === 'tests') return 'Premium';
  return 'Lite, Ultra, or Premium';
}

export function filterLibraryByPlan(library, membership) {
  if (canAccessFeature(membership, 'usmle')) return library;
  return { ...library, usmleSubjects: [], usmleModules: [] };
}
