import { ABROAD_STATE, medicalCollegesByState } from "./src/data/medicalColleges.js";

function normalizeCollegeName(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/\bnmc sl \d+\b/g, " ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const collegeStateEntries = Object.entries(medicalCollegesByState).flatMap(([state, colleges]) =>
  colleges.map((college) => [normalizeCollegeName(college), state]),
);

const legacyCollegeAliases = [
  ["aiims delhi", "Delhi"],
  ["armed forces medical college pune", "Maharashtra"],
  ["b j medical college ahmedabad", "Gujarat"],
  ["bj medical college ahmedabad", "Gujarat"],
  ["bangalore medical college", "Karnataka"],
  ["christian medical college vellore", "Tamil Nadu"],
  ["government medical college amritsar", "Punjab"],
  ["government medical college srinagar", "Jammu and Kashmir"],
  ["grant medical college mumbai", "Maharashtra"],
  ["jipmer puducherry", "Puducherry"],
  ["king georges medical university lucknow", "Uttar Pradesh"],
  ["kgmu lucknow", "Uttar Pradesh"],
  ["lady hardinge medical college new delhi", "Delhi"],
  ["madras medical college chennai", "Tamil Nadu"],
  ["maulana azad medical college new delhi", "Delhi"],
  ["osmania medical college hyderabad", "Telangana"],
  ["sms medical college jaipur", "Rajasthan"],
  ["vmmc and safdarjung hospital new delhi", "Delhi"],
];

const collegeStateLookup = new Map([
  ...collegeStateEntries,
  ...legacyCollegeAliases.map(([college, state]) => [normalizeCollegeName(college), state]),
]);

function resolveCollegeState(collegeName) {
  const normalized = normalizeCollegeName(collegeName);
  if (!normalized) return null;
  if (normalized === normalizeCollegeName(ABROAD_STATE)) return ABROAD_STATE;

  if (collegeStateLookup.has(normalized)) {
    return collegeStateLookup.get(normalized);
  }

  for (const [key, state] of collegeStateLookup.entries()) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return state;
    }
  }

  return null;
}

export { normalizeCollegeName, resolveCollegeState };
