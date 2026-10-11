import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { filterPracticeLibraryForUi, hasQuestionImage } from '../src/lib/practiceImageVisibility.js';

const image = '/uploads/medicomm-img1-example.png';

test('detects question and explanation images without counting source references', () => {
  assert.equal(hasQuestionImage({ prompt: 'Text only', sourceImageUrls: [image], atlasImageTargetUrls: [image] }), false);
  assert.equal(hasQuestionImage({ imageUrls: [], image: '  ' }), false);
  for (const question of [{ imageUrls: [image] }, { images: [image] }, { imageUrl: image }, { image }, { explanationImageUrls: [image] }]) {
    assert.equal(hasQuestionImage(question), true);
  }
});

test('only final-year PYQ and FMGE image questions are hidden, including treated images', () => {
  const library = {
    exam: { questionCount: 5 },
    years: [{ id: 'final-year', subjectIds: ['surgery'] }],
    subjects: [
      { id: 'anatomy', yearId: 'first-year', questions: [{ id: 'early-image', imageUrls: [image] }] },
      { id: 'surgery', questions: [{ id: 'text' }, { id: 'hidden', imageUrls: [image] }] },
      { id: 'medicine', yearId: 'final-year', questions: [{ id: 'medicine-text' }, { id: 'medicine-hidden', image: '/original.png' }] },
    ],
    fmgeSessions: [{ id: 'fmge', questions: [{ id: 'fmge-text' }, { id: 'fmge-hidden', explanationImageUrls: [image] }] }],
    usmleSubjects: [{ questions: [{ id: 'usmle', imageUrls: [image] }] }],
    aiSubjects: [{ questions: [{ id: 'ai', imageUrls: [image] }] }],
  };
  const before = structuredClone(library);
  const visible = filterPracticeLibraryForUi(library);
  assert.deepEqual(library, before);
  assert.strictEqual(visible.subjects[0], library.subjects[0]);
  assert.deepEqual(visible.subjects[1].questions.map(q => q.id), ['text']);
  assert.deepEqual(visible.subjects[2].questions.map(q => q.id), ['medicine-text']);
  assert.equal(visible.subjects[1].questionCount, 1);
  assert.equal(visible.exam.questionCount, 3);
  assert.equal(visible.fmgeSessions[0].questionCount, 1);
  assert.deepEqual([...visible.hiddenQuestionIds], ['hidden', 'medicine-hidden', 'fmge-hidden']);
  assert.strictEqual(visible.usmleSubjects, library.usmleSubjects);
  assert.strictEqual(visible.aiSubjects, library.aiSubjects);
  assert.deepEqual(filterPracticeLibraryForUi(JSON.parse(JSON.stringify(library))).subjects, visible.subjects);
});

test('actual banks preserve every record and all earlier-year image questions', () => {
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url)));
  const fmge = JSON.parse(readFileSync(new URL('../data/fmge-question-bank.json', import.meta.url)));
  const library = { ...bank, fmgeSessions: fmge.sessions };
  const before = JSON.stringify(library);
  const visible = filterPracticeLibraryForUi(library);
  for (const [index, subject] of library.subjects.entries()) {
    const shown = visible.subjects[index];
    if (subject.yearId !== 'final-year') assert.strictEqual(shown, subject);
    else assert.deepEqual(shown.questions, subject.questions.filter(q => !hasQuestionImage(q)));
  }
  for (const [index, session] of library.fmgeSessions.entries()) {
    assert.deepEqual(visible.fmgeSessions[index].questions, session.questions.filter(q => !hasQuestionImage(q)));
  }
  for (const key of ['subjects', 'fmgeSessions']) {
    const total = library[key].reduce((sum, set) => sum + set.questions.length, 0);
    const shown = visible[key].reduce((sum, set) => sum + set.questions.length, 0);
    console.log(`${key}: ${shown} visible, ${total - shown} hidden, ${total} stored`);
  }
  assert.equal(JSON.stringify(library), before);
});
