import { hasQuestionImage } from '../src/lib/practiceImageVisibility.js';

// Final-year image questions remain excluded until their img1 rollout is ready.
// General Surgery is the explicitly approved exception.
export function isDuelImageEligible(question, subject, finalYearSubjectIds) {
  const finalYear = subject.yearId === 'final-year' || finalYearSubjectIds.has(subject.id);
  return !finalYear || subject.id === 'general-surgery' || !hasQuestionImage(question);
}
