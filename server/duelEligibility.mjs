import { hasUnresolvedStatementAudit } from '../src/lib/practiceImageVisibility.js';

// Topic-wise questions from every subject are allowed. PYQs are restricted to
// the first three academic years, including text-only and reviewed images.
export function isDuelQuestionEligible(question, subject, allowedSubjectIds, finalYearSubjectIds) {
  if (question.source === 'ai') return true;
  if (hasUnresolvedStatementAudit(question)) return false;
  if (question.source && question.source !== 'official') return false;
  const finalYear = subject.yearId === 'final-year' || finalYearSubjectIds.has(subject.id);
  return !finalYear && (allowedSubjectIds.has(subject.id) ||
    ['first-year', 'second-year', 'third-year'].includes(subject.yearId));
}
