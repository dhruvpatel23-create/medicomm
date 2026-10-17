import test from 'node:test';
import assert from 'node:assert/strict';
import { cleanQuestionPrompt } from '../src/lib/questionText.js';
import { fmgeAttemptView } from './fmgeTests.mjs';

test('removes source question labels without stripping clinical numbers', () => {
  assert.equal(cleanQuestionPrompt('4. A young male patient was brought to the emergency department.'), 'A young male patient was brought to the emergency department.');
  assert.equal(cleanQuestionPrompt('12. Which drug is indicated?'), 'Which drug is indicated?');
  assert.equal(cleanQuestionPrompt('19. HCO3 = 28. What is the diagnosis?'), 'HCO3 = 28. What is the diagnosis?');
  assert.equal(cleanQuestionPrompt('Q. 12) A 7-year-old child presents with fever.'), 'A 7-year-old child presents with fever.');
  for (const text of ['43-year-old presents with fever.', '4-8 speakers talk about a topic.', '2-3 BPG binds to?', '5-Fluorouracil inhibits which enzyme?', '0.5 mg is administered.', '1.5 L of fluid was given.', '1. First statement. 2. Second statement. Which is correct?']) {
    assert.equal(cleanQuestionPrompt(text), text);
  }
});

test('saved attempts and completed reviews display cleaned stems without mutating their snapshots', () => {
  const q = { id: 'source-q', prompt: '4. A young male patient presents.', options: ['A','B','C','D'], answerIndex: 0, explanation: 'Explanation', subjectId: 'medicine', subjectTitle: 'Medicine' };
  const attempt = { id: 'attempt', testId: 'test', status: 'active', part: 1, questions: [q], answers: {}, marked: {}, currentIndex: 0, revision: 0 };
  assert.equal(fmgeAttemptView(attempt, 0).questions[0].prompt, 'A young male patient presents.');
  attempt.status = 'completed';
  assert.equal(fmgeAttemptView(attempt, 0).questions[0].prompt, 'A young male patient presents.');
  assert.equal(q.prompt, '4. A young male patient presents.');
});
