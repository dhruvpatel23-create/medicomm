import { readFileSync } from 'node:fs';

// Saved prompt is also the live source of Gemini's formatting instructions.
const prompt = readFileSync(new URL('../docs/gemini-theory-answer-prompt.md', import.meta.url), 'utf8').replace(/\r\n/g, '\n');
const [rules, subjectText] = prompt.split('## Subject-specific formats');
export const theoryAnswerPresentation = rules.split('## Readable answer presentation')[1].split('## Marks and command words')[0].trim();
const formats = [...subjectText.matchAll(/## (\d+)\. ([^\n]+)\n([\s\S]*?)(?=\n## \d+\.|$)/g)];
const aliases = {
  'forensic medicine and toxicology': 7, 'forensic medicine': 7,
  'community medicine': 8, psm: 8, medicine: 9,
  dermatology: 11, surgery: 13, orthopaedics: 14, ent: 15,
  'obstetrics and gynaecology': 17, 'obstetrics and gynecology': 17, obg: 17,
  anesthesia: 18, anaesthesia: 18, anaesthesiology: 18, radiology: 19,
};

export function buildTheoryAnswerFormat(subjectTitle) {
  const key = String(subjectTitle).trim().toLowerCase();
  const selected = formats.find(match => Number(match[1]) === aliases[key]
    || match[2].toLowerCase() === key || match[2].toLowerCase().split(' (')[0] === key);
  return `${rules}\n\n## Required subject format\n${selected ? selected[0] : subjectText}\n\nBefore returning, check subject format, heading order, coverage, depth, and placement of named diagram markers. No generated diagrams are permitted.`;
}
