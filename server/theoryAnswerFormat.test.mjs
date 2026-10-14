import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildTheoryAnswerFormat } from './theoryAnswerFormat.mjs';

test('all 19 PDF subjects select exactly their own LAQ, SAQ and placement rules', () => {
  const subjects = ['Anatomy', 'Physiology', 'Biochemistry', 'Pathology', 'Pharmacology',
    'Microbiology', 'Forensic Medicine and Toxicology', 'Community Medicine', 'General Medicine',
    'Pediatrics', 'Dermatology', 'Psychiatry', 'General Surgery', 'Orthopedics', 'ENT',
    'Ophthalmology', 'Obstetrics and Gynaecology', 'Anesthesiology', 'Radiology'];
  for (const [index, subject] of subjects.entries()) {
    const prompt = buildTheoryAnswerFormat(subject);
    assert.equal((prompt.match(/## \d+\./g) || []).length, 1, subject);
    assert(prompt.includes(`## ${index + 1}. `), subject);
    for (const rule of ['LAQ format:', 'SAQ format:', 'Diagram placement:', '[DIAGRAM TO DRAW:',
      'DO NOT generate or draw', 'practice score out of 10', '15 marks:']) assert(prompt.includes(rule), `${subject}: ${rule}`);
  }
});

test('all current theory-library titles resolve to a single subject format', () => {
  const bank = JSON.parse(readFileSync(new URL('../public/short-notes.json', import.meta.url), 'utf8'));
  for (const subject of bank.subjects) {
    assert.equal((buildTheoryAnswerFormat(subject.title).match(/## \d+\./g) || []).length, 1, subject.title);
  }
});
