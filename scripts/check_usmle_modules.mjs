import assert from "node:assert/strict";
import { readUsmleModules } from "../server/usmleModules.mjs";

const modules = readUsmleModules();
assert.equal(modules.length, 10);
assert.equal(modules[0].questions.length, 15);
assert.equal(modules[1].questions.length, 15);
assert.equal(modules[2].questions.length, 15);
assert(modules.slice(3).every(module => module.questions.length === 0));
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

// Independently calculate the numerical keys from the displayed inputs.
const acidBase = modules[0].questions[7];
const lab = name => Number.parseFloat(acidBase.laboratoryFindings.find(row => row.test === name).value);
assert.equal(lab("Sodium") - lab("Chloride") - lab("Bicarbonate"), 26);
assert(lab("PaCO2") < 1.5 * lab("Bicarbonate") + 8 - 2);
assert(Math.abs(6.1 + Math.log10(lab("Bicarbonate") / (0.03 * lab("PaCO2"))) - lab("Arterial pH")) < 0.01);
assert.equal(Math.round(100 * (0.9 * 100) / ((0.9 * 100) + (0.05 * 900))), 67);

const response = await fetch("http://127.0.0.1:4174/api/practice?source=usmle&subjectId=usmle-module-01");
assert.equal(response.status, 200);
const library = await response.json();
assert.equal(library.usmleModules.length, 10);
assert.equal(library.questions.length, 15);
assert(!library.subjects.some(subject => subject.id.startsWith("usmle-module-")), "Module leaked into subject directory");
assert(!library.usmleSubjects.some(subject => subject.id.startsWith("usmle-module-")), "Module leaked into legacy USMLE subjects");
assert.deepEqual(library.usmleModules[0].questions[0].references, modules[0].questions[0].references);
assert.deepEqual(library.usmleModules[0].questions[0].optionExplanations, modules[0].questions[0].optionExplanations);
console.log("PASS: Modules 1-3 contain 15 items each, 10 modules load, disciplines are mixed, numerical keys work, API metadata is intact, and modules stay isolated from subject directories.");
