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
  if (id === 'fmge' || id === 'custom-modules') return 'fullPractice';
  return 'practice';
}

// Opening a trial directory is separate from entitlement to the full bank.
export function canOpenFeature(membership, feature) {
  return canAccessFeature(membership, feature)
    || Boolean(membership && (feature === 'practice' || feature === 'usmle'));
}

export const FEATURE_NAMES = {
  practice: 'Practice Questions', theory: 'Theory Practice', usmle: 'USMLE Practice Questions',
  fullPractice: 'Practice Questions',
  tests: 'MEDULLA Practice Test', community: 'Community Access', inbox: 'Personal Inbox',
};

export function requiredPlans(feature) {
  if (feature === 'theory') return 'Ultra or Premium';
  if (feature === 'usmle' || feature === 'tests') return 'Premium';
  return 'Lite, Ultra, or Premium';
}

// Keep catalog metadata visible without delivering paid question content.
function lockedQuestion(question) {
  const fields = ['id', 'subjectId', 'subjectTitle', 'yearId', 'year', 'examId', 'examTitle',
    'source', 'chapterTitle', 'chapterOrder', 'topic', 'topicTitle', 'topicOrder', 'questionNumber'];
  return { ...Object.fromEntries(fields.filter(key => question[key] !== undefined).map(key => [key, question[key]])), locked: true };
}

const lockSet = set => {
  const questions = (set.questions ?? []).map(lockedQuestion);
  return { ...set, questions, questionCount: questions.length, locked: questions.length > 0 };
};

export function filterLibraryByPlan(library, membership) {
  if (canAccessFeature(membership, 'usmle')) return library;
  const usmleModules = (library.usmleModules ?? []).map(module => {
    return Number(module.moduleNumber) === 1 ? module : lockSet(module);
  });
  if (canAccessFeature(membership, 'practice')) {
    return { ...library, usmleSubjects: (library.usmleSubjects ?? []).map(lockSet), usmleModules, questions: [] };
  }
  const trialSubjects = new Set((library.years ?? [])
    .filter(year => ['first-year', 'second-year'].includes(year.id))
    .flatMap(year => year.subjectIds ?? []));
  const subjects = (library.subjects ?? []).map(subject => {
    const eligible = trialSubjects.has(subject.id) || ['first-year', 'second-year'].includes(subject.yearId);
    const questions = (subject.questions ?? []).map(question =>
      eligible && Number(question.year) === 2020 && /^neet-pg(?:-2020|-pyqs)?$/i.test(question.examId ?? '')
      && (!question.source || question.source === 'official') ? question : lockedQuestion(question));
    return { ...subject, questions, questionCount: questions.length };
  });
  const aiSubjects = (library.aiSubjects ?? []).map(subject => {
    const chapters = new Map();
    for (const question of subject.questions ?? []) {
      const title = question.chapterTitle || 'General Pathology';
      const order = question.chapterOrder != null && Number.isFinite(Number(question.chapterOrder))
        ? Number(question.chapterOrder) : Number.MAX_SAFE_INTEGER;
      chapters.set(title, Math.min(chapters.get(title) ?? Number.MAX_SAFE_INTEGER, order));
    }
    const first = [...chapters].sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0]))[0]?.[0];
    const questions = (subject.questions ?? []).map(question =>
      (question.chapterTitle || 'General Pathology') === first ? question : lockedQuestion(question));
    return { ...subject, questions, questionCount: questions.length };
  });
  return {
    ...library, subjects, aiSubjects, usmleSubjects: (library.usmleSubjects ?? []).map(lockSet),
    usmleModules, fmgeSessions: (library.fmgeSessions ?? []).map(lockSet),
    questions: [],
    exam: { ...library.exam, questionCount: subjects.reduce((sum, subject) => sum + subject.questions.length, 0) },
  };
}
