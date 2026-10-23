import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { filterPracticeLibraryForUi, hasQuestionImage, hasUnresolvedStatementAudit } from '../src/lib/practiceImageVisibility.js';

const image = '/uploads/medicomm-img1-example.png';

test('detects question and explanation images without counting source references', () => {
  assert.equal(hasQuestionImage({ prompt: 'Text only', sourceImageUrls: [image], atlasImageTargetUrls: [image] }), false);
  assert.equal(hasQuestionImage({ imageUrls: [], image: '  ' }), false);
  for (const question of [{ imageUrls: [image] }, { images: [image] }, { imageUrl: image }, { image }, { explanationImageUrls: [image] }]) {
    assert.equal(hasQuestionImage(question), true);
  }
});

test('untreated final-year and FMGE images remain hidden while installed img1 images are visible', () => {
  const library = {
    exam: { questionCount: 5 },
    years: [{ id: 'final-year', subjectIds: ['surgery'] }],
    subjects: [
      { id: 'anatomy', yearId: 'first-year', questions: [{ id: 'early-image', imageUrls: [image] }] },
      { id: 'surgery', questions: [{ id: 'text' }, { id: 'treated', imageUrls: [image] }, { id: 'hidden', imageUrls: ['/original.png'], atlasImageTargetUrls: [image] }] },
      { id: 'medicine', yearId: 'final-year', questions: [{ id: 'medicine-text' }, { id: 'medicine-hidden', image: '/original.png' }] },
    ],
    fmgeSessions: [{ id: 'fmge', questions: [{ id: 'fmge-text' }, { id: 'fmge-treated', explanationImageUrls: [image] }, { id: 'fmge-hidden', imageUrls: ['/original.png'] }] }],
    usmleSubjects: [{ questions: [{ id: 'usmle', imageUrls: [image] }] }],
    aiSubjects: [{ questions: [{ id: 'ai', imageUrls: [image] }] }],
  };
  const before = structuredClone(library);
  const visible = filterPracticeLibraryForUi(library);
  assert.deepEqual(library, before);
  assert.strictEqual(visible.subjects[0], library.subjects[0]);
  assert.deepEqual(visible.subjects[1].questions.map(q => q.id), ['text', 'treated']);
  assert.deepEqual(visible.subjects[2].questions.map(q => q.id), ['medicine-text']);
  assert.equal(visible.subjects[1].questionCount, 2);
  assert.equal(visible.exam.questionCount, 4);
  assert.equal(visible.fmgeSessions[0].questionCount, 2);
  assert.deepEqual([...visible.hiddenQuestionIds], ['hidden', 'medicine-hidden', 'fmge-hidden']);
  assert.strictEqual(visible.usmleSubjects, library.usmleSubjects);
  assert.strictEqual(visible.aiSubjects, library.aiSubjects);
  assert.deepEqual(filterPracticeLibraryForUi(JSON.parse(JSON.stringify(library))).subjects, visible.subjects);
});

test('actual banks preserve stored records while showing only PYQs and eligible images', () => {
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url)));
  const fmge = JSON.parse(readFileSync(new URL('../data/fmge-question-bank.json', import.meta.url)));
  const library = { ...bank, fmgeSessions: fmge.sessions };
  const before = JSON.stringify(library);
  const visible = filterPracticeLibraryForUi(library);
  for (const [index, subject] of library.subjects.entries()) {
    const shown = visible.subjects[index];
    assert.deepEqual(shown.questions, subject.questions.filter(q => (!q.source || q.source === 'official')
      && !hasUnresolvedStatementAudit(q)
      && (subject.yearId !== 'final-year' || !hasQuestionImage(q) || q.imageReviewStatus === 'img1-visually-verified' || [...(q.imageUrls??[]),...(q.images??[])].some(url=>url.startsWith('/uploads/medicomm-img1-')))));
  }
  for (const [index, session] of library.fmgeSessions.entries()) {
    assert.deepEqual(visible.fmgeSessions[index].questions, session.questions.filter(q => !hasQuestionImage(q) || [...(q.imageUrls??[]),...(q.images??[])].some(url=>url.startsWith('/uploads/medicomm-img1-'))));
  }
  for (const key of ['subjects', 'fmgeSessions']) {
    const total = library[key].reduce((sum, set) => sum + set.questions.length, 0);
    const shown = visible[key].reduce((sum, set) => sum + set.questions.length, 0);
    console.log(`${key}: ${shown} visible, ${total - shown} hidden, ${total} stored`);
  }
  assert.equal(JSON.stringify(library), before);
});

test('all installed surgery replacements survive server normalization and UI filtering', () => {
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const start = source.indexOf('function normalizeQuestion(');
  const end = source.indexOf('\nfunction getOfficialPracticeQuestions', start);
  const normalize = vm.runInNewContext(`(${source.slice(start, end)})`);
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url)));
  const surgery = bank.subjects.find(s=>s.id==='general-surgery');
  const reviewed = surgery.questions.filter(q=>q.imageReviewStatus==='img1-visually-verified');
  assert.ok(reviewed.length > 0);
  const questions = reviewed.map(q=>normalize(q,surgery));
  assert(questions.every(q=>q.imageReviewStatus==='img1-visually-verified'));
  const library={subjects:[{...surgery,questions}]};
  const eligibleCount = questions.filter(q => !hasUnresolvedStatementAudit(q)).length;
  assert.equal(filterPracticeLibraryForUi(library).subjects[0].questions.length,eligibleCount);
  questions.forEach(q=>delete q.imageReviewStatus);
  assert.equal(filterPracticeLibraryForUi(library).subjects[0].questions.length,eligibleCount,'Older API responses must also show eligible installed assets');
});

test('all flagged PYQs stay stored but are hidden after API normalization', () => {
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url)));
  const before = JSON.stringify(bank);
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const start = source.indexOf('function normalizeQuestion(');
  const end = source.indexOf('\nfunction getOfficialPracticeQuestions', start);
  const normalize = vm.runInNewContext(`(${source.slice(start, end)})`);
  const normalized = { ...bank, subjects: bank.subjects.map(s => ({ ...s, questions: s.questions.map(q => normalize(q, s)) })) };
  for (const library of [bank, normalized]) {
    const visible = filterPracticeLibraryForUi(library);
    const shownIds = new Set(visible.subjects.flatMap(s => s.questions.map(q => q.id)));
    const flagged = library.subjects.flatMap(s => s.questions).filter(q => (!q.source || q.source === 'official') && hasUnresolvedStatementAudit(q));
    assert.equal(flagged.length, 322);
    for (const q of flagged) {
      assert.equal(shownIds.has(q.id), false, q.id);
      assert.equal(visible.hiddenQuestionIds.has(q.id), true, q.id);
    }
    assert.equal(visible.subjects.find(s => s.id === 'dermatology').questions.length, 39);
  }
  assert.equal(JSON.stringify(bank), before);
});
