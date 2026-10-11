import assert from "node:assert/strict";
import { readUsmleModules } from "../server/usmleModules.mjs";

const modules = readUsmleModules();
assert.equal(modules.length, 10);
assert.equal(modules[0].questions.length, 15);
assert.equal(modules[1].questions.length, 15);
assert.equal(modules[2].questions.length, 15);
assert.equal(modules[3].questions.length, 15);
assert.equal(modules[4].questions.length, 15);
assert(modules.slice(5).every(module => module.questions.length === 0));
for (const question of modules[2].questions) {
  assert(question.prompt.trim().split(/\s+/).length >= 80, `Module 3 stem is too short: ${question.id}`);
  assert(question.laboratoryFindings.length > 0, `Module 3 item lacks structured findings: ${question.id}`);
}
const ids = new Set();
const disciplines = new Set();
for (const module of modules) {
  for (const question of module.questions) {
    assert(!ids.has(question.id), `Duplicate ID: ${question.id}`);
    ids.add(question.id);
    assert.equal(question.moduleId, module.id);
    assert.equal(question.subjectId, module.id);
    assert.equal(question.options.length, 5);
    assert.equal(new Set(question.options).size, 5);
    assert.equal(question.answer, question.options[question.answerIndex]);
    assert.equal(question.optionExplanations.length, 5);
    question.disciplines.forEach(discipline => disciplines.add(discipline));
    assert(question.references.every(reference => reference.book && reference.edition && reference.chapter && (reference.pdfPages || reference.url)));
  }
}
assert(disciplines.size >= 8);

for (const module of [modules[0], ...modules.slice(3, 5)]) {
  const keyCounts = Array(5).fill(0);
  for (const [index, question] of module.questions.entries()) {
    assert.equal(question.questionNumber, index + 1);
    const revision = module.contentRevision ? `-v${module.contentRevision}` : "";
    assert.equal(question.id, `${module.id}${revision}-q${String(index + 1).padStart(3, "0")}`);
    assert(question.references.length > 0, `Missing source: ${question.id}`);
    assert(question.sourceProposition?.trim(), `Missing tested proposition: ${question.id}`);
    assert(question.educationalObjective?.trim() && question.reasoningChain?.trim());
    assert(question.explanation?.trim() && question.optionExplanations.every(note => note.trim()));
    assert(!/\b(TBD|TODO)\b/.test(JSON.stringify(question)), `Unfinished item: ${question.id}`);
    assert(!/\b(EXCEPT|NOT)\b/.test(question.leadIn));
    assert(!question.options.some(option => /all of the above|none of the above/i.test(option)));
    assert.match(question.reviewStatus, /independent physician review pending/i);
    keyCounts[question.answerIndex] += 1;
  }
  assert.deepEqual(keyCounts, [3, 3, 3, 3, 3]);
  assert.equal(module.questions.filter(q => q.itemFamily === "communication").length, 1);
  assert.equal(module.questions.filter(q => q.itemFamily === "biostatistics").length, 1);
  assert.equal(module.questions.filter(q => q.itemFamily === "diagnosis").length, 1);
  assert.equal(module.questions.filter(q => q.laboratoryFindings.length > 0).length, 3);
}

// Independently derive the new statistical answers from the displayed study data.
const nnt = modules[3].questions.find(q => q.itemFamily === "biostatistics");
const eventRisks = nnt.laboratoryFindings.map(row => {
  const [events, total] = row.value.replaceAll(",", "").match(/\d+/g).map(Number);
  return events / total;
});
assert.equal(Number(nnt.answer), Math.round(1 / (eventRisks[0] - eventRisks[1])));
const oddsRatio = modules[4].questions.find(q => q.itemFamily === "biostatistics");
const [a, b, c, d] = oddsRatio.laboratoryFindings.map(row => Number(row.value));
assert.equal(Number(oddsRatio.answer), (a * d) / (b * c));

// The replacement block uses new IDs, so old saved progress cannot mark new items answered.
assert.equal(modules[0].contentRevision, 2);
assert(modules[0].questions.every(q => q.id.startsWith("usmle-module-01-v2-q")));
// Independently calculate the replacement block's numerical concepts from displayed inputs.
const acidBase = modules[0].questions[3];
const lab = name => Number.parseFloat(acidBase.laboratoryFindings.find(row => row.test === name).value);
assert.equal(lab("Sodium") - lab("Chloride") - lab("Bicarbonate"), 10);
assert(Math.abs(lab("PaCO2") - (1.5 * lab("Bicarbonate") + 8)) <= 2);
assert(Math.abs(6.1 + Math.log10(lab("Bicarbonate") / (0.03 * lab("PaCO2"))) - lab("Arterial pH")) < 0.01);
const riskRatio = modules[0].questions.find(q => q.itemFamily === "biostatistics");
const risks = riskRatio.laboratoryFindings.map(row => {
  const [events, total] = row.value.replaceAll(",", "").match(/\d+/g).map(Number);
  return events / total;
});
assert.equal(Number(riskRatio.answer), risks[0] / risks[1]);

const apiBase = process.env.USMLE_CHECK_API_BASE || "http://127.0.0.1:4174";
const apiHeaders = process.env.USMLE_CHECK_TOKEN ? { Authorization: `Bearer ${process.env.USMLE_CHECK_TOKEN}` } : {};
const response = await fetch(`${apiBase}/api/practice?source=usmle&subjectId=usmle-module-01`, { headers: apiHeaders });
assert.equal(response.status, 200);
const library = await response.json();
assert.equal(library.usmleModules.length, 10);
assert.equal(library.questions.length, 15);
assert(!library.subjects.some(subject => subject.id.startsWith("usmle-module-")), "Module leaked into subject directory");
assert(!library.usmleSubjects.some(subject => subject.id.startsWith("usmle-module-")), "Module leaked into legacy USMLE subjects");
assert.deepEqual(library.usmleModules[0].questions[0].references, modules[0].questions[0].references);
assert.deepEqual(library.usmleModules[0].questions[0].optionExplanations, modules[0].questions[0].optionExplanations);
for (const module of [modules[0], ...modules.slice(3, 5)]) {
  const result = await fetch(`${apiBase}/api/practice?source=usmle&subjectId=${module.id}`, { headers: apiHeaders });
  assert.equal(result.status, 200);
  const payload = await result.json();
  assert.equal(payload.questions.length, 15);
  for (const question of module.questions) {
    const actual = payload.questions.find(q => q.id === question.id);
    assert(actual, `Missing API question: ${question.id}`);
    for (const field of ["prompt", "leadIn", "answer", "answerIndex", "options", "optionExplanations", "references", "laboratoryFindings", "explanation", "educationalObjective", "reasoningChain"]) {
      assert.deepEqual(actual[field], question[field], `API changed ${field}: ${question.id}`);
    }
  }
}
console.log("PASS: Modules 1-5 contain 15 items each; new source metadata, balanced keys, NNT/odds-ratio calculations, live API content, and directory isolation verified.");
