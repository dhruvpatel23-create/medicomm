import { readFileSync, statSync } from "node:fs";

const bankUrl = new URL("../data/fmge-question-bank.json", import.meta.url);
let cachedBank;
let cachedMtime;

export function readFmgeSessions() {
  const modified = statSync(bankUrl).mtimeMs;
  if (!cachedBank || modified !== cachedMtime) {
    cachedBank = JSON.parse(readFileSync(bankUrl, "utf8"));
    cachedMtime = modified;
  }
  return cachedBank.sessions;
}
