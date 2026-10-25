import { readFileSync } from 'node:fs';

const manifest = JSON.parse(readFileSync(new URL('../data/topic-wise-option-revisions.json', import.meta.url), 'utf8'));
const cleanup = JSON.parse(readFileSync(new URL('../data/topic-wise-correct-option-cleanup.json', import.meta.url), 'utf8'));
const userEdits = JSON.parse(readFileSync(new URL('../data/topic-wise-user-option-edits.json', import.meta.url), 'utf8'));
const revisions = new Map([...manifest.questions, ...cleanup.questions, ...userEdits.questions].map(revision => [revision.id, revision]));
const sameOptions = (a, b) => Array.isArray(a) && a.length === b.length && a.every((option, i) => option === b[i]);

// Apply reviewed wording to older stored copies without overwriting a question
// whose stem, options or answer key has subsequently changed.
export function reviseTopicWiseOptions(question) {
  const revision = revisions.get(question.id);
  if (question.source !== 'ai' || !revision || question.prompt !== revision.prompt) return question;
  if (sameOptions(question.options, revision.options)) return question;
  const answerIndex = Number.isInteger(question.answerIndex)
    ? question.answerIndex : question.options?.indexOf(question.answer);
  if (answerIndex !== revision.answerIndex || !sameOptions(question.options, revision.beforeOptions)
      || (question.answer && question.answer !== revision.beforeAnswer)) return question;
  return { ...question, options: [...revision.options], answer: revision.options[answerIndex] };
}
