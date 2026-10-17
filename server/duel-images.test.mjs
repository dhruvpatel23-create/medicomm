import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { getDuelImageUrls } from '../src/lib/duelImages.js';

const replacement = '/uploads/medicomm-img1-tick.png';
const original = '/uploads/yellowfool-tick.jpg';

test('battles display generated images without archived source references', () => {
  assert.deepEqual(getDuelImageUrls({ imageUrls: [replacement], images: [replacement], sourceImageUrls: [original], sourceImageUrl: original }), [replacement]);
  assert.deepEqual(getDuelImageUrls({ sourceImageUrls: [original], atlasImageTargetUrls: [replacement] }), []);
});

test('existing battle snapshots discard merged originals and retain multiple replacement panels', () => {
  const second = '/uploads/medicomm-atlas-tick-panel2.png?v=2';
  assert.deepEqual(getDuelImageUrls({ imageUrls: [replacement, original], images: [original, replacement, second] }), [replacement, second]);
  assert.deepEqual(getDuelImageUrls({ images: [' /uploads/panel1.png ', '/uploads/panel2.png'], image: '/uploads/panel1.png' }), ['/uploads/panel1.png', '/uploads/panel2.png']);
});

test('actual duel sanitizer excludes originals from both response image fields', () => {
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const functions = source.slice(source.indexOf('function collectQuestionImageUrls('), source.indexOf('let duelPoolBank'));
  const sanitize = new Function('getDuelImageUrls', `${functions}; return sanitizeDuelQuestionForClient;`)(getDuelImageUrls);
  const bank = JSON.parse(readFileSync(new URL('../data/practice-question-bank.json', import.meta.url), 'utf8'));
  const questions = bank.subjects.flatMap(subject => subject.questions).filter(q => q.sourceImageUrls?.length && q.imageUrls?.some(url => /medicomm-(img1|atlas)-/.test(url)));
  assert.ok(questions.length > 0);
  for (const question of questions) {
    const result = sanitize(question);
    assert.deepEqual(result.imageUrls, getDuelImageUrls(question));
    assert.deepEqual(result.images, result.imageUrls);
    assert.ok(result.imageUrls.every(url => !question.sourceImageUrls.includes(url)), question.id);
  }
});
