import { readFileSync, statSync } from "node:fs";
import { cleanQuestionPrompt } from '../src/lib/questionText.js';

const bankUrl = new URL("../data/fmge-question-bank.json", import.meta.url);
let cachedBank;
let cachedMtime;

export function readFmgeSessions() {
  const modified = statSync(bankUrl).mtimeMs;
  if (!cachedBank || modified !== cachedMtime) {
    cachedBank = JSON.parse(readFileSync(bankUrl, "utf8"));
    for (const session of cachedBank.sessions) {
      for (const question of session.questions) question.prompt = cleanQuestionPrompt(question.prompt);
    }
    cachedMtime = modified;
  }
  return cachedBank.sessions;
}
