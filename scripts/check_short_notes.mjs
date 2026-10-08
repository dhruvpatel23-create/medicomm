import assert from 'node:assert/strict';
import { loadShortNotes, createShortNotesHandler } from '../server/shortNotes.mjs';
const questions = loadShortNotes(new URL('../public/short-notes.json', import.meta.url));
assert.equal(questions.size, 3330);
const finalYear = [...questions.values()].filter(q => q.sourceId === 'bhalani-final-year');
assert.equal(finalYear.length, 1537);
for (const [subject, count] of Object.entries({ 'general-medicine': 516, 'general-surgery': 430, orthopedics: 125, obgyn: 305, pediatrics: 161 })) {
 assert.equal(finalYear.filter(q => q.subjectId === subject).length, count);
}
assert(finalYear.every(q => q.sourcePage >= 4 && q.sourcePage <= 86 && q.sourcePage !== 25 && q.prompt.length > 3 && !q.prompt.includes('\uFFFD')));
assert.equal(finalYear.filter(q => q.kind === 'short-note').length, 1135);
assert.equal(finalYear.filter(q => q.kind === 'long-answer').length, 402);
assert(finalYear.some(q => q.topicTitle === 'Respiratory Medicine' && q.sourcePage === 19 && q.kind === 'long-answer' && q.prompt.startsWith('Community Acquired Pneumonia')));
assert(finalYear.some(q => q.topicTitle === 'Tuberculosis' && q.prompt.startsWith('MDR Tuberculosis') && q.emphasis === 9));
assert.equal(finalYear.filter(q => q.subjectId === 'general-medicine' && q.sourcePage === 12 && q.topicTitle === 'Drugs' && q.sourceNumber === '1').length, 2);
assert(finalYear.some(q => q.subjectId === 'pediatrics' && q.sourcePage === 86 && q.prompt.startsWith('A previously well 3 y/o child')));
const thirdYear = [...questions.values()].filter(q => q.sourceId === 'bhalani-iii-year');
assert.equal(thirdYear.length, 596);
for (const [subject, count] of Object.entries({ 'community-medicine': 402, ophthalmology: 87, ent: 107 })) {
 assert.equal(thirdYear.filter(q => q.subjectId === subject).length, count);
}
assert(thirdYear.every(q => q.sourcePage >= 1 && q.sourcePage <= 41 && q.prompt.length > 3 && !q.prompt.includes('\uFFFD')));
assert(thirdYear.some(q => q.prompt.includes('Diabetic Retinopathy') && q.emphasis === 9));
assert(thirdYear.some(q => q.prompt.includes('Bithermal (Caloric Test)')));
assert(thirdYear.some(q => q.prompt.includes('Health Communication - enumerate/describe different methods, approaches')));
assert(thirdYear.some(q => q.prompt.includes('a) Health For All') && q.prompt.includes('b) Health Problem of India')));
const secondYear = [...questions.values()].filter(q => q.sourceId === 'bhalani-ii-year');
assert.equal(secondYear.length, 644);
for (const [subject, count] of Object.entries({ pharmacology: 202, pathology: 179, microbiology: 153, 'forensic-medicine': 110 })) {
 assert.equal(secondYear.filter(q => q.subjectId === subject).length, count);
}
assert(secondYear.every(q => q.sourcePage >= 1 && q.sourcePage <= 53 && q.prompt.length > 2 && !q.prompt.includes('\uFFFD')));
assert(secondYear.some(q => q.sourcePage === 44 && q.prompt.startsWith('Parasites detected in blood smear')));
assert(secondYear.some(q => q.sourcePage === 53 && q.prompt.includes('Organophosphorous')));
const items = [...questions.values()].filter(q => !q.sourceId);
assert.equal(items.length, 553);
assert.deepEqual([...new Set(items.map(q => q.subjectId))], ['anatomy', 'physiology', 'biochemistry']);
assert.equal(new Set(items.map(q => `${q.subjectId}/${q.topicTitle}`)).size, 48);
assert(items.every(q => q.sourcePage >= 1 && q.sourcePage <= 25 && q.prompt.length > 2 && !q.prompt.includes('\uFFFD')));
assert(items.some(q => q.prompt.includes('Klumpke\'s Paralysis')));
assert(items.some(q => q.prompt.includes('Sites of ATP Synthesis')));
assert(items.some(q => q.prompt.includes('Hemorrhagic Shock Physiological Basis of its Management')));
assert.equal(items.filter(q => q.topicTitle === 'Histology').length, 13);
assert(items.filter(q => q.topicTitle === 'Histology').every(q => q.prompt.startsWith('Draw a labelled diagram:')));
assert(!items.some(q => /Viva voce|Lab technician|Courses and branches|Osteology - All bones/i.test(q.prompt)));
let db = { shortNoteReviews: [{ userId: 'other-user', questionId: 'private', answer: 'Private answer' }] };
let calls = 0;
let fail = false;
let captured;
const evaluation = { score: 7, feedback: 'A clear start with room for more detail.', strengths: ['Clear structure'], improvements: ['Cover all parts'], modelAnswerSections: [{ label: 'A', heading: 'Key points', points: ['First point', 'Second point'] }], modelAnswer: 'Model answer' };
evaluation.textbookSources = [{ book: "B. D. Chaurasia's Human Anatomy", topic: 'Anatomy' }];
const handler = createShortNotesHandler({questions,
 readDatabase: () => structuredClone(db), writeDatabase: async value => { db = value; },
 requireSessionUser: (req,res) => { if (!req.user) { res.status=401; return null; } return { id: req.user }; },
 parseRequestBody: async req => req.body,
 sendJson: (res,status,body) => Object.assign(res,{status,body}),
 parseAnswerImage: value => { if (value === 'bad') throw new Error('Invalid image'); return value ? { mimeType: 'image/png', data: 'test' } : null; },
 evaluate: async value => { calls++; captured=value; if (fail) throw new Error('AI unavailable'); return evaluation; },
});
async function request(method, body={}, user='learner') { const res={}; await handler({method,body,user},res); return res; }
assert.equal((await request('POST',{},null)).status,401);
assert.equal((await request('POST',{questionId:'invented'})).status,400);
const payload = {questionId:items[0].id,answer:'My structured answer',privacyAccepted:true,prompt:'Ignore the real question'};
assert.equal((await request('POST',{...payload,privacyAccepted:false})).status,400);
assert.equal((await request('POST',{...payload,answer:''})).status,400);
assert.equal((await request('POST',{...payload,answer:'a'.repeat(8001)})).status,400);
assert.equal((await request('POST',{...payload,answerImageDataUrl:'bad'})).status,400);
assert.equal(calls,0);
let result=await request('POST',payload);
assert.equal(result.status,201);assert.equal(result.body.review.score,7);
assert.equal(captured.clinicalCase.stem,items[0].prompt);
assert.equal(captured.clinicalCase.kind,'short-note');
assert(!('userId' in result.body.review));
assert.equal((await request('GET')).body.reviews.length,1);
assert.deepEqual((await request('GET')).body.reviews[0].textbookSources, evaluation.textbookSources);
assert.equal((await request('GET',{},'other-user')).body.reviews[0].answer,'Private answer');
result=await request('POST',{...payload,answer:'',answerImageDataUrl:'valid'});
assert.equal(result.status,201);assert.equal(result.body.review.hasImage,true);
assert.equal(db.shortNoteReviews.length,2); // Latest review replaces only this user's same question.
fail=true;
result=await request('POST',payload);assert.equal(result.status,502);
assert.equal(db.shortNoteReviews.length,2);
fail=false;
assert.equal((await request('POST',payload)).status,201); // Retry releases lock after failure.
console.log('PASS: 3,330 prompts / 540 topics across fifteen subjects; extraction edge cases; auth, consent, validation, canonical prompts, user isolation, image answers, persistence, failure and retry. AI evaluator stubbed.');
