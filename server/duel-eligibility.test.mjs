import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { isDuelQuestionEligible } from './duelEligibility.mjs';
import { validDuelQuestion } from './duels.mjs';

test('only first-three-year PYQs and all topic-wise subjects are eligible', () => {
  const allowed = new Set(['anatomy', 'pathology', 'ent']);
  const final = new Set(['general-medicine', 'general-surgery']);
  for (const id of final) {
    for (const imageUrls of [[], ['/image.png']]) {
      assert.equal(isDuelQuestionEligible({ source: 'official', imageUrls }, { id }, allowed, final), false);
      assert.equal(isDuelQuestionEligible({ source: 'ai', imageUrls }, { id }, allowed, final), true);
    }
  }
  for (const id of allowed) {
    assert.equal(isDuelQuestionEligible({ source: 'official' }, { id }, allowed, final), true);
    assert.equal(isDuelQuestionEligible({}, { id }, allowed, final), true);
    assert.equal(isDuelQuestionEligible({ source: 'usmle' }, { id }, allowed, final), false);
  }
  assert.equal(isDuelQuestionEligible({}, { id: 'unknown' }, allowed, final), false);
});

test('actual 1v1 pool excludes every final-year PYQ and includes valid topic-wise questions', () => {
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url), 'utf8'));
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const poolSource = source.slice(source.indexOf('let duelPoolBank'), source.indexOf('function pickDuelQuestions('));
  const getPool = new Function('readPracticeQuestionBank', 'validDuelQuestion', 'sanitizeDuelQuestion', 'isDuelQuestionEligible', 'DUEL_QUESTION_COUNT', `${poolSource}; return getDuelQuestionPool;`)(() => bank, validDuelQuestion, q => q, isDuelQuestionEligible, 5);
  const pool = getPool();
  const ids = new Set(pool.map(q => q.id));
  const finalIds = new Set(bank.years.find(year => year.id === 'final-year').subjectIds);
  let excluded = 0, topicWise = 0;
  for (const subject of bank.subjects) for (const q of subject.questions) {
    if (q.source !== 'ai' && ['likely-missing-list', 'image-review-required'].includes(q.statementAudit?.status)) {
      assert.equal(ids.has(q.id), false, q.id);
    }
    if (finalIds.has(subject.id) && q.source !== 'ai') {
      assert.equal(ids.has(q.id), false, q.id);
      excluded++;
    }
    if (q.source === 'ai' && validDuelQuestion({ ...q, answerIndex: Number.isInteger(q.answerIndex) ? q.answerIndex : q.options?.indexOf(q.answer) })) {
      assert.ok(ids.has(q.id), q.id);
      topicWise++;
    }
  }
  assert.ok(excluded > 0);
  assert.ok(topicWise > 0);
  assert.strictEqual(getPool(), pool);
  console.log(`${excluded} final-year PYQs excluded; ${topicWise} topic-wise questions; ${pool.length} total eligible`);
});
