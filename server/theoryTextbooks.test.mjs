import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { buildShortNoteReviewInstructions } from './shortNotesPrompt.mjs';
import { theoryTextbooks, buildTheoryTextbookInstructions, textbookSourceSchema, normalizeTextbookSources } from './theoryTextbooks.mjs';

test('all theory-library subjects have a textbook reference list', () => {
  const bank = JSON.parse(readFileSync(new URL('../public/short-notes.json', import.meta.url), 'utf8'));
  for (const subject of bank.subjects) assert(theoryTextbooks(subject.title).length, subject.title);
});

test('references reject absent, invented, duplicate, or wrong-subject books', () => {
  const reference = { book: theoryTextbooks('Anatomy')[0], topic: 'Triangles of the neck' };
  assert.deepEqual(normalizeTextbookSources([reference], 'Anatomy'), [reference]);
  for (const invalid of [undefined, [], [reference, reference], [{ ...reference, book: 'Invented book' }], [{ ...reference, topic: '' }]]) {
    assert.throws(() => normalizeTextbookSources(invalid, 'Anatomy'));
  }
  assert.throws(() => normalizeTextbookSources([reference], 'Physiology'));
});

test('Gemini request requires sources and returns validated sources with the model answer', async () => {
  const source = readFileSync(new URL('../server.mjs', import.meta.url), 'utf8');
  const section = (start, end) => source.slice(source.indexOf(start), source.indexOf(end, source.indexOf(start)));
  const code = section('function normalizeClinicalCaseEvaluation(', 'const handleShortNotes =') + '\n'
    + section('async function requestGeminiClinicalCaseEvaluation(', 'async function requestClinicalCaseEvaluation(');
  const reference = { book: theoryTextbooks('Anatomy')[0], topic: 'Triangles of the neck' };
  let requestBody;
  const response = { score: 7, feedback: 'The main divisions are correct; include their boundaries and contents.', strengths: ['Identifies the main divisions.'], improvements: ['Describe the boundaries.'],
    modelAnswerSections: [{ label: 'A', heading: 'Triangles of the neck', points: [
      'Introduction: The sternocleidomastoid divides each side of the neck into anterior and posterior triangles.',
      'Boundaries: Describe the anatomical boundaries and subdivisions of each triangle under separate headings.',
    ] }], textbookSources: [reference] };
  const context = vm.createContext({ process: { env: { GEMINI_API_KEY: 'test-only' } }, buildShortNoteReviewInstructions,
    buildTheoryTextbookInstructions, textbookSourceSchema, normalizeTextbookSources,
    resolveGeminiModel: (_configured, fallback) => fallback,
    fetchGeminiReviewWithFallback: async (_url, options) => {
      requestBody = JSON.parse(options.body);
      return { ok: true, json: async () => ({ candidates: [{ content: { parts: [{ text: JSON.stringify(response) }] } }] }) };
    },
  });
  vm.runInContext(code, context);
  const clinicalCase = { kind: 'short-note', stem: 'Triangles of the neck', subquestions: [{ label: 'A', prompt: 'Triangles of the neck', marks: 10 }], keyPoints: [] };
  for (const kind of ['short-note', 'long-answer', 'clinical-case']) {
    const result = await context.requestGeminiClinicalCaseEvaluation({ subjectTitle: 'Anatomy', clinicalCase: { ...clinicalCase, kind }, studentAnswer: 'My answer' });
    assert.deepEqual(JSON.parse(JSON.stringify(result.textbookSources)), [reference]);
    assert(requestBody.generationConfig.responseSchema.required.includes('textbookSources'));
    assert.deepEqual(requestBody.generationConfig.responseSchema.properties.textbookSources.items.properties.book.enum, theoryTextbooks('Anatomy'));
    const instructions = requestBody.systemInstruction.parts[0].text;
    assert(instructions.includes('Indian university/professional examination answer format only'));
    assert(instructions.includes('no full textbook has been supplied or retrieved'));
    assert(instructions.includes('Do not claim you consulted a book'));
  }
  delete response.textbookSources;
  await assert.rejects(context.requestGeminiClinicalCaseEvaluation({ subjectTitle: 'Anatomy', clinicalCase, studentAnswer: 'My answer' }), /textbook references/);
});
