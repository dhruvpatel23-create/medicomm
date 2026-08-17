import { copyFileSync, readFileSync, writeFileSync } from "node:fs";

const SOURCE_DATA = "data/users.json";
const DATA_BANK = "data/practice-question-bank.json";
const PUBLIC_BANK = "public/practice-question-bank.json";
const DIST_BANK = "dist/practice-question-bank.json";
const SYNC_SUBJECT_IDS = new Set(["general-medicine", "ophthalmology"]);

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8").replace(/^\uFEFF/, ""));
}

function normalizeAiQuestion(question) {
  return {
    ...question,
    subject: question.subjectTitle ?? question.subject ?? "",
    yearId: question.yearId ?? "third-year",
    examId: question.examId ?? "ai-generated",
    examTitle: question.examTitle ?? "AI Topic-wise Questions",
    year: Number.isFinite(question.year) ? question.year : null,
    questionNumber: Number.isFinite(question.questionNumber) ? question.questionNumber : null,
    source: "ai",
  };
}

const data = readJson(SOURCE_DATA);
const aiQuestions = (data.questions ?? [])
  .filter((question) => question.source === "ai" && SYNC_SUBJECT_IDS.has(question.subjectId))
  .map(normalizeAiQuestion);

function syncBank(path) {
  const bank = readJson(path);
  const aiIds = new Set(aiQuestions.map((question) => question.id));
  const questionsBySubject = new Map();

  for (const question of aiQuestions) {
    const subjectId = question.subjectId;
    if (!subjectId) continue;
    const bucket = questionsBySubject.get(subjectId) ?? [];
    bucket.push(question);
    questionsBySubject.set(subjectId, bucket);
  }

  const yearSubjectIds = new Set((bank.years ?? []).flatMap((year) => year.subjectIds ?? []));
  bank.subjects = (bank.subjects ?? []).map((subject) => {
    const subjectAiQuestions = questionsBySubject.get(subject.id) ?? [];
    const officialQuestions = (subject.questions ?? []).filter((question) => !aiIds.has(question.id) && question.source !== "ai");
    const questions = [...officialQuestions, ...subjectAiQuestions];
    return {
      ...subject,
      questionCount: questions.length,
      questions,
    };
  }).filter((subject) => (subject.questions?.length ?? 0) > 0 || yearSubjectIds.has(subject.id));

  for (const [subjectId, subjectQuestions] of questionsBySubject.entries()) {
    if ((bank.subjects ?? []).some((subject) => subject.id === subjectId)) continue;
    const title = subjectQuestions[0]?.subjectTitle ?? subjectQuestions[0]?.subject ?? subjectId;
    bank.subjects.push({
      id: subjectId,
      title,
      yearId: subjectQuestions[0]?.yearId ?? "third-year",
      questionCount: subjectQuestions.length,
      questions: subjectQuestions,
    });
  }

  bank.exam = {
    ...(bank.exam ?? {}),
    questionCount: (bank.subjects ?? []).reduce((total, subject) => total + (subject.questions?.length ?? 0), 0),
  };

  writeFileSync(path, `${JSON.stringify(bank, null, 2)}\n`, "utf8");
}

syncBank(DATA_BANK);
syncBank(PUBLIC_BANK);
copyFileSync(PUBLIC_BANK, DIST_BANK);

console.log(`Synced ${aiQuestions.length} AI questions into ${DATA_BANK}, ${PUBLIC_BANK}, and ${DIST_BANK}.`);
