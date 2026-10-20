import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { shuffleQuestionOptions } from "../src/lib/shuffleQuestionOptions.js";

test("shuffling preserves grading and explanation alignment without mutating the question", () => {
  const question = {
    options: ["correct", "second", "third", "fourth"],
    answer: "correct",
    answerIndex: 0,
    optionExplanations: ["why correct", "why second", "why third", "why fourth"],
  };
  const before = structuredClone(question);
  const shuffled = shuffleQuestionOptions(question, () => 0);
  assert.deepEqual(shuffled.options, ["second", "third", "fourth", "correct"]);
  assert.equal(shuffled.options[shuffled.answerIndex], question.answer);
  assert.deepEqual(shuffled.optionExplanations, ["why second", "why third", "why fourth", "why correct"]);
  assert.deepEqual(question, before);
});

test("every topic-wise subject can shuffle while retaining its correct answer", () => {
  const bank = JSON.parse(readFileSync(new URL("../data/users.json", import.meta.url), "utf8").replace(/^\uFEFF/, ""));
  const subjects = new Map();
  for (const question of bank.questions.filter(question => question.source === "ai")) {
    const shuffled = shuffleQuestionOptions(question, () => 0);
    assert.deepEqual([...shuffled.options].sort(), [...question.options].sort(), question.id);
    assert.equal(shuffled.answer, question.answer, question.id);
    assert.equal(shuffled.options[shuffled.answerIndex], question.options[question.answerIndex], question.id);
    assert.notDeepEqual(shuffled.options, question.options, question.id);
    subjects.set(question.subjectId, (subjects.get(question.subjectId) ?? 0) + 1);
  }
  assert.ok(subjects.has("ent"));
  assert.ok(subjects.size > 0);
  console.log("Verified topic-wise subjects:", Object.fromEntries(subjects));
});
