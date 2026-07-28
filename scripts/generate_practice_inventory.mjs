import { readFileSync, writeFileSync } from "node:fs";

const DATA_PATHS = ["runtime-data/users.json", "data/users.json"];
const JSON_OUT = "docs/practice-question-inventory.json";
const MD_OUT = "docs/practice-question-inventory.md";

function readData(path) {
  return JSON.parse(readFileSync(path, "utf8").replace(/^\uFEFF/, ""));
}

function addCount(map, keys) {
  let cursor = map;
  for (const key of keys.slice(0, -1)) {
    cursor.set(key, cursor.get(key) ?? new Map());
    cursor = cursor.get(key);
  }
  const last = keys.at(-1);
  cursor.set(last, (cursor.get(last) ?? 0) + 1);
}

function buildInventory(data) {
  const tree = new Map();
  for (const question of data.questions ?? []) {
    const subject = question.subjectTitle || question.subjectId || "Unknown Subject";
    const chapter = question.chapterTitle || "Unknown Chapter";
    const topic = question.topicTitle || question.topic || "Unknown Topic";
    addCount(tree, [subject, chapter, topic]);
  }

  const subjects = [];
  let grandTotal = 0;
  for (const [subjectTitle, chaptersMap] of [...tree.entries()].sort()) {
    const chapters = [];
    let subjectTotal = 0;
    for (const [chapterTitle, topicsMap] of [...chaptersMap.entries()].sort()) {
      const topics = [...topicsMap.entries()]
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([topicTitle, count]) => ({ topicTitle, count }));
      const chapterTotal = topics.reduce((total, topic) => total + topic.count, 0);
      subjectTotal += chapterTotal;
      chapters.push({ chapterTitle, count: chapterTotal, topics });
    }
    grandTotal += subjectTotal;
    subjects.push({ subjectTitle, count: subjectTotal, chapters });
  }
  return { totalQuestions: grandTotal, subjects };
}

function flatten(inventory) {
  const rows = new Map();
  for (const subject of inventory.subjects) {
    for (const chapter of subject.chapters) {
      for (const topic of chapter.topics) {
        rows.set(`${subject.subjectTitle}\u0000${chapter.chapterTitle}\u0000${topic.topicTitle}`, topic.count);
      }
    }
  }
  return rows;
}

function compareInventories(primary, secondary) {
  const left = flatten(primary);
  const right = flatten(secondary);
  const keys = new Set([...left.keys(), ...right.keys()]);
  const mismatches = [];
  for (const key of [...keys].sort()) {
    const leftCount = left.get(key) ?? 0;
    const rightCount = right.get(key) ?? 0;
    if (leftCount === rightCount) continue;
    const [subjectTitle, chapterTitle, topicTitle] = key.split("\u0000");
    mismatches.push({ subjectTitle, chapterTitle, topicTitle, runtimeCount: leftCount, dataCount: rightCount });
  }
  return mismatches;
}

function markdown(inventory, mismatches) {
  const lines = [
    "# Practice Question Inventory",
    "",
    `Total questions: ${inventory.totalQuestions}`,
    "",
    "Source: `runtime-data/users.json`",
    "",
  ];

  if (mismatches.length) {
    lines.push("## Store Mismatches", "");
    lines.push("| Subject | Chapter | Topic | runtime-data | data |");
    lines.push("|---|---|---|---:|---:|");
    for (const mismatch of mismatches) {
      lines.push(`| ${mismatch.subjectTitle} | ${mismatch.chapterTitle} | ${mismatch.topicTitle} | ${mismatch.runtimeCount} | ${mismatch.dataCount} |`);
    }
    lines.push("");
  } else {
    lines.push("Store mismatch check: `runtime-data/users.json` and `data/users.json` match topic-wise.", "");
  }

  for (const subject of inventory.subjects) {
    lines.push(`## ${subject.subjectTitle} (${subject.count})`, "");
    for (const chapter of subject.chapters) {
      lines.push(`### ${chapter.chapterTitle} (${chapter.count})`, "");
      lines.push("| Topic | Questions |");
      lines.push("|---|---:|");
      for (const topic of chapter.topics) {
        lines.push(`| ${topic.topicTitle} | ${topic.count} |`);
      }
      lines.push("");
    }
  }
  return `${lines.join("\n")}\n`;
}

const runtimeInventory = buildInventory(readData(DATA_PATHS[0]));
const dataInventory = buildInventory(readData(DATA_PATHS[1]));
const mismatches = compareInventories(runtimeInventory, dataInventory);
const output = {
  generatedFrom: DATA_PATHS[0],
  comparedWith: DATA_PATHS[1],
  totalQuestions: runtimeInventory.totalQuestions,
  storeMismatches: mismatches,
  subjects: runtimeInventory.subjects,
};

writeFileSync(JSON_OUT, `${JSON.stringify(output, null, 2)}\n`, "utf8");
writeFileSync(MD_OUT, markdown(runtimeInventory, mismatches), "utf8");

console.log(`Wrote ${JSON_OUT}`);
console.log(`Wrote ${MD_OUT}`);
console.log(`Total questions: ${runtimeInventory.totalQuestions}`);
if (mismatches.length) {
  console.error(`Store mismatches: ${mismatches.length}`);
  process.exitCode = 1;
} else {
  console.log("Store mismatches: 0");
}
