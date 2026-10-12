import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCustomModuleCatalog, customModulePool, customModuleResult, sampleCustomModule, readCustomModuleSession } from '../src/lib/customModules.js';

const questions = Array.from({ length: 40 }, (_, index) => ({ id: `q-${index}`, prompt: `Question ${index}`, options: ['A', 'B'], answerIndex: 0, chapterTitle: index < 20 ? 'Shared title' : 'Second chapter' }));
const subjects = [{ id: 'anatomy', title: 'Anatomy', questions }, { id: 'physiology', title: 'Physiology', questions: [{ ...questions[0], id: 'physiology-q' }] }, { id: 'empty', title: 'Coming soon', questions: [] }];

test('chapter filters are scoped by subject and combine without duplicate questions', () => {
  const before = JSON.stringify(subjects);
  const catalog = buildCustomModuleCatalog(subjects);
  assert.equal(catalog[2].chapters.length, 0);
  const anatomy = catalog[0].chapters.find(c => c.title === 'Shared title');
  const physiology = catalog[1].chapters[0];
  assert.notEqual(anatomy.key, physiology.key);
  assert.equal(customModulePool(catalog, []).length, 0);
  assert.equal(customModulePool(catalog, [anatomy.key, anatomy.key]).length, 20);
  assert.equal(customModulePool(catalog, [anatomy.key, physiology.key]).length, 21);
  assert.equal(JSON.stringify(subjects), before);
});

test('tests have exactly 10, 20 or 30 unique questions from the chosen pool', () => {
  const before = structuredClone(questions);
  for (const size of [10, 20, 30]) {
    const sampled = sampleCustomModule([...questions, questions[0]], size, () => .3);
    assert.equal(sampled.length, size);
    assert.equal(new Set(sampled.map(q => q.id)).size, size);
    assert(sampled.every(q => questions.includes(q)));
  }
  assert.throws(() => sampleCustomModule(questions.slice(0, 9), 10));
  assert.throws(() => sampleCustomModule(questions, 15));
  assert.deepEqual(questions, before);
});

test('result distinguishes correct, incorrect and unanswered questions', () => {
  assert.deepEqual(customModuleResult({ questions: questions.slice(0, 10), answers: { 'q-0': 0, 'q-1': 1 } }), { correct: 1, incorrect: 1, skipped: 8, total: 10 });
});

test('resuming preserves the timer and answers and rejects malformed storage', () => {
  const previous = globalThis.sessionStorage;
  const session = { version: 1, id: 'session', status: 'active', startedAt: 1000, questions: questions.slice(0, 10), answers: { 'q-0': 0 }, flags: ['q-1'], index: 1 };
  try {
    globalThis.sessionStorage = { getItem: () => JSON.stringify(session) };
    assert.deepEqual(readCustomModuleSession('test'), session);
    globalThis.sessionStorage = { getItem: () => '{bad' };
    assert.equal(readCustomModuleSession('test'), null);
    globalThis.sessionStorage = { getItem: () => JSON.stringify({ ...session, index: 11 }) };
    assert.equal(readCustomModuleSession('test'), null);
  } finally { globalThis.sessionStorage = previous; }
});
