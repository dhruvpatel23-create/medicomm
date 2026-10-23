import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { reviseTopicWiseOptions } from './topicWiseOptionRevisions.mjs';

const manifest = JSON.parse(readFileSync(new URL('../data/topic-wise-option-revisions.json', import.meta.url)));

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
    for (const revision of manifest.questions) {
      const q = questions.get(revision.id);
      assert.equal(q.prompt, revision.prompt, revision.id);
      assert.deepEqual(q.options, revision.options, revision.id);
      assert.equal(q.answer, q.options[revision.answerIndex], revision.id);
    }
  }
});
