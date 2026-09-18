import { readFileSync } from "node:fs";

// A separate integrated bank: module questions never enter the subject directories.
export function readUsmleModules() {
  const bank = JSON.parse(readFileSync(new URL("../data/usmle-module-bank.json", import.meta.url), "utf8"));
  return bank.modules.map((module) => ({ ...module, questionCount: module.questions.length }));
}
