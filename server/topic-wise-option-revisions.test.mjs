import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { reviseTopicWiseOptions } from './topicWiseOptionRevisions.mjs';

const manifest = JSON.parse(readFileSync(new URL('../data/topic-wise-option-revisions.json', import.meta.url)));
const cleanup = JSON.parse(readFileSync(new URL('../data/topic-wise-correct-option-cleanup.json', import.meta.url)));
const userEdits = JSON.parse(readFileSync(new URL('../data/topic-wise-user-option-edits.json', import.meta.url)));

test('user option edits apply exactly to old copies without changing the key or other fields', () => {
  for (const r of userEdits.questions) {
    const old = { id: r.id, source: 'ai', prompt: r.prompt, options: [...r.beforeOptions],
      answer: r.beforeAnswer, answerIndex: r.answerIndex, explanation: 'preserve', tags: ['keep'] };
    const updated = reviseTopicWiseOptions(old);
    assert.deepEqual(updated, { ...old, options: r.options, answer: r.options[r.answerIndex] }, r.id);
    assert.deepEqual(old.options, r.beforeOptions);
    assert.strictEqual(reviseTopicWiseOptions(updated), updated);
    const conflict = { ...old, prompt: 'A newer stem' };
    assert.strictEqual(reviseTopicWiseOptions(conflict), conflict);
  }
});

test('correct-option cleanup preserves every distractor, stem and answer position', () => {
  assert.equal(new Set(cleanup.scopeQuestionIds).size, 7522);
  const scope = new Set(cleanup.scopeQuestionIds);
  for (const r of cleanup.questions) {
    assert.ok(scope.has(r.id), r.id);
    assert.deepEqual(r.beforeOptions.flatMap((option, i) => option !== r.options[i] ? [i] : []), [r.answerIndex], r.id);
    assert.ok(r.options[r.answerIndex].length < r.beforeAnswer.length, r.id);
    assert.equal(new Set(r.options.map(o => o.toLowerCase().trim())).size, 4, r.id);
    const old = { id: r.id, source: 'ai', prompt: r.prompt, options: [...r.beforeOptions],
      answerIndex: r.answerIndex, answer: r.beforeAnswer, explanation: 'Keep existing teaching notes', tags: ['original'] };
    const result = reviseTopicWiseOptions(old);
    assert.deepEqual(result, { ...old, options: r.options, answer: r.options[r.answerIndex] }, r.id);
    assert.deepEqual(old.options, r.beforeOptions);
    assert.strictEqual(reviseTopicWiseOptions(result), result);
    for (const changed of [{ ...old, source: 'official' }, { ...old, prompt: 'Changed stem' },
      { ...old, answerIndex: (r.answerIndex + 1) % 4 }, { ...old, options: ['New', 'Option', 'Set', 'Here'] }]) {
      assert.strictEqual(reviseTopicWiseOptions(changed), changed);
    }
  }
});

test('reviewed edits preserve stems, answer positions and explanations in old stored copies', () => {
  for (const r of manifest.questions) {
    const original = { id: r.id, source: 'ai', prompt: r.prompt, options: r.beforeOptions,
      answer: r.beforeAnswer, answerIndex: r.answerIndex, explanation: 'Original explanation' };
    const before = JSON.stringify(original);
    const result = reviseTopicWiseOptions(original);
    assert.equal(result.prompt, original.prompt);
    assert.equal(result.explanation, original.explanation);
    assert.equal(result.answerIndex, original.answerIndex);
    assert.deepEqual(result.options, r.options);
    assert.equal(result.answer, result.options[result.answerIndex]);
    assert.equal(new Set(result.options.map(o => o.toLowerCase())).size, 4);
    const wrongLengths = result.options.filter((_, i) => i !== result.answerIndex).map(o => o.length);
    assert.ok(result.answer.length / Math.max(...wrongLengths) <= 1.35, r.id);
    assert.equal(JSON.stringify(original), before);
    assert.strictEqual(reviseTopicWiseOptions(result), result);
    for (const changed of [{ ...original, source: 'official' }, { ...original, prompt: 'Changed stem' },
      { ...original, answerIndex: (r.answerIndex + 1) % 4 }, { ...original, options: ['New', 'Option', 'Set', 'Here'] }]) {
      assert.strictEqual(reviseTopicWiseOptions(changed), changed);
    }
  }
});

test('canonical banks agree on every reviewed option set', () => {
  for (const path of ['data/users.json', 'data/practice-question-bank.json', 'public/practice-question-bank.json']) {
    const bank = JSON.parse(readFileSync(new URL(`../${path}`, import.meta.url)));
    const questions = new Map((bank.questions ?? bank.subjects.flatMap(s => s.questions)).map(q => [q.id, q]));
    for (const revision of [...manifest.questions, ...cleanup.questions, ...userEdits.questions]) {
      const q = questions.get(revision.id);
      assert.equal(q.prompt, revision.prompt, revision.id);
      assert.deepEqual(q.options, revision.options, revision.id);
      assert.equal(q.answer, q.options[revision.answerIndex], revision.id);
    }
  }
});
