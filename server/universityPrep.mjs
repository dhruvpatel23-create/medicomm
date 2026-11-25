import { posix } from 'node:path';
import { UNIVERSITY_PREP_SAMPLE_LIMIT, UNIVERSITY_PREP_SUBJECTS } from '../src/data/universityPrep.js';

export const UNIVERSITY_PREP_UPGRADE_MESSAGE = 'Buy a subscription to unlock more short notes.';

export function createShortNoteAccess(bank) {
  const subjectIds = new Set(UNIVERSITY_PREP_SUBJECTS.map(subject => subject.id));
  const sampleIds = new Set();
  const listedAssets = new Set();
  const freeAssets = new Set();
  const trialSubjects = bank.subjects.map(subject => {
    const limited = subjectIds.has(subject.id);
    const questions = subject.topics.flatMap(topic => topic.questions);
    if (limited) {
      const samples = questions.filter(question => question.kind === 'short-note' && question.answerDocument?.pages?.length);
      for (const question of samples.slice(0, UNIVERSITY_PREP_SAMPLE_LIMIT)) sampleIds.add(question.id);
    }
    for (const question of questions) {
      const document = question.answerDocument;
      if (!document) continue;
      for (const url of [document.pdf, document.managementPdf, ...(document.pages ?? [])].filter(Boolean)) {
        const asset = posix.normalize(decodeURIComponent(url)).toLowerCase();
        listedAssets.add(asset);
        if (!limited || sampleIds.has(question.id)) freeAssets.add(asset);
      }
    }
    if (!limited) return subject;
    return { ...subject, topics: subject.topics.map(topic => ({
      ...topic,
      questions: topic.questions.map(question => {
        if (sampleIds.has(question.id)) return { ...question, isSample: true };
        const { id, prompt, kind, emphasis } = question;
        return { id, prompt, kind, emphasis, locked: true };
      }),
    })) };
  });

  return {
    isUniversityPrepSubject: subjectId => subjectIds.has(subjectId),
    isSample: question => sampleIds.has(question.id),
    isListedAsset: asset => listedAssets.has(asset.toLowerCase()),
    isFreeAsset: asset => freeAssets.has(asset.toLowerCase()),
    catalog(subjectId, subscribed) {
      const subjects = subscribed ? bank.subjects : trialSubjects;
      if (!subjectId) return { ...bank, subjects };
      const selected = subjects.filter(subject => subject.id === subjectId);
      return {
        ...bank,
        questionCount: selected.reduce((count, subject) => count
          + subject.topics.reduce((total, topic) => total + topic.questions.length, 0), 0),
        subjects: selected,
      };
    },
  };
}
