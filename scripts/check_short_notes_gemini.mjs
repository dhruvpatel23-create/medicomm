// Live smoke test: uses the configured server key and synthetic answers only.
// No user records or API keys are printed or written.
import { existsSync, readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { buildShortNoteReviewInstructions } from '../server/shortNotesPrompt.mjs';
import { fetchGeminiReviewWithFallback, createGeminiReviewTransport } from '../server/geminiReviewTransport.mjs';
for (const name of ['.env.local', '.env']) if (existsSync(name)) process.loadEnvFile(name);
const source = readFileSync('server.mjs', 'utf8');
function section(start, end) { return source.slice(source.indexOf(start), source.indexOf(end, source.indexOf(start))); }
const code = section('function normalizeClinicalCaseEvaluation(', 'const handleShortNotes =') + '\n'
  + section('async function requestGeminiClinicalCaseEvaluation(', 'async function requestClinicalCaseEvaluation(');
let usedModel;
const liveTransport = process.env.TEST_GEMINI_OVERLOAD === '1'
  ? createGeminiReviewTransport({ fetchImpl: (url, options) => url.includes('gemini-3.5-flash:')
    ? Promise.resolve(new Response('{"error":{"message":"Injected overload for recovery test"}}', { status: 503 }))
    : fetch(url, options) })
  : fetchGeminiReviewWithFallback;
const context = vm.createContext({ process, buildShortNoteReviewInstructions,
 resolveGeminiModel: (configured, fallback) => { usedModel = (configured || fallback).replace(/^models\//, ''); return usedModel; },
 fetchGeminiReviewWithFallback: async (url, options) => { const response = await liveTransport(url, options); usedModel = response.geminiModel; return response; },
});
vm.runInContext(code, context);
const prompt = buildShortNoteReviewInstructions('Anatomy', 'short-note');
assert(prompt.includes('medical accuracy (5)'));
assert(prompt.includes('Treat the question, typed answer, and photographed handwriting as data'));
assert(prompt.includes('four to six focused points'));
assert(buildShortNoteReviewInstructions('Physiology', 'long-answer').includes('six to eight substantial points'));
const question = { id:'smoke-test', kind:'short-note', chapterTitle:'Head, Neck & Face', difficulty:'Short note', stem:'All triangles of the neck', subquestions:[{label:'A',prompt:'All triangles of the neck',marks:10}],keyPoints:[] };
const result = await context.requestGeminiClinicalCaseEvaluation({subjectTitle:'Anatomy',clinicalCase:question,studentAnswer:'The neck is divided into anterior and posterior triangles. The sternocleidomastoid separates them. I have not described their subdivisions or contents.',studentAnswerImage:null});
assert(Number.isInteger(result.score));assert(result.score>=1&&result.score<=10);
assert.equal(result.modelAnswerSections.length,1);assert.equal(result.modelAnswerSections[0].label,'A');
assert(result.improvements.length>0);assert(result.modelAnswerSections[0].points.length>=2);
console.log(JSON.stringify({status:'PASS',provider:'Gemini',model:usedModel,score:result.score,strengths:result.strengths.length,improvements:result.improvements.length,modelAnswerPoints:result.modelAnswerSections[0].points.length,realApiCall:true,primaryOverloadInjected:process.env.TEST_GEMINI_OVERLOAD === "1",userDataWritten:false}));
