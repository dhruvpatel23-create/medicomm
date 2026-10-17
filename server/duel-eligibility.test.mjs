import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { isDuelImageEligible } from './duelEligibility.mjs';
import { hasQuestionImage } from '../src/lib/practiceImageVisibility.js';
import { validDuelQuestion } from './duels.mjs';

test('final-year image questions are excluded except General Surgery', () => {
  const ids = new Set(['general-medicine', 'general-surgery']);
  for (const imageFields of [{ imageUrls: ['/image.png'] }, { images: ['/image.png'] }, { imageUrl: '/image.png' }, { image: '/image.png' }, { explanationImageUrls: ['/image.png'] }]) {
    assert.equal(isDuelImageEligible(imageFields, { id: 'general-medicine' }, ids), false);
    assert.equal(isDuelImageEligible(imageFields, { id: 'obgyn', yearId: 'final-year' }, ids), false);
    assert.equal(isDuelImageEligible(imageFields, { id: 'general-surgery', yearId: 'final-year' }, ids), true);
    assert.equal(isDuelImageEligible(imageFields, { id: 'anatomy', yearId: 'first-year' }, ids), true);
  }
  assert.equal(isDuelImageEligible({ prompt: 'Text only' }, { id: 'general-medicine' }, ids), true);
});

test('actual 1v1 pool excludes restricted images and retains surgery and text questions', () => {
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url), 'utf8'));
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const poolSource = source.slice(source.indexOf('let duelPoolBank'), source.indexOf('function pickDuelQuestions('));
  const getPool = new Function('readPracticeQuestionBank', 'validDuelQuestion', 'sanitizeDuelQuestion', 'isDuelImageEligible', 'DUEL_QUESTION_COUNT', `${poolSource}; return getDuelQuestionPool;`)(() => bank, validDuelQuestion, q => q, isDuelImageEligible, 5);
  const pool = getPool();
  const poolIds = new Set(pool.map(q => q.id));
  const finalIds = new Set(bank.years.find(year => year.id === 'final-year').subjectIds);
  let excluded = 0;
  for (const subject of bank.subjects) {
    if (!finalIds.has(subject.id) || subject.id === 'general-surgery') continue;
    for (const q of subject.questions.filter(hasQuestionImage)) {
      assert.equal(poolIds.has(q.id), false, q.id);
      excluded++;
    }
    assert.ok(subject.questions.some(q => !hasQuestionImage(q) && poolIds.has(q.id)), `${subject.id}: text questions remain eligible`);
  }
  assert.ok(excluded > 0);
  assert.ok(bank.subjects.find(s => s.id === 'general-surgery').questions.some(q => hasQuestionImage(q) && poolIds.has(q.id)));
  assert.strictEqual(getPool(), pool, 'cached pool retains the same filtering');
  console.log(`${excluded} final-year image questions excluded; ${pool.length} questions eligible for 1v1`);
});
