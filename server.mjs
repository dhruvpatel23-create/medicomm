import { createServer } from "node:http";
import { randomBytes, pbkdf2Sync, timingSafeEqual } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync } from "node:fs";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveCollegeState } from "./collegeStateLookup.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const dataDir = path.join(__dirname, "data");
const runtimeDataDir = path.join(__dirname, "runtime-data");
const legacyUploadsDir = path.join(dataDir, "uploads");
const uploadsDir = path.join(runtimeDataDir, "uploads");
const legacyDatabasePath = path.join(dataDir, "users.json");
const databasePath = path.join(runtimeDataDir, "users.json");
const practiceQuestionBankPath = path.join(dataDir, "practice-question-bank.json");
const distDir = path.join(__dirname, "dist");
const host = process.env.HOST ?? "0.0.0.0";
const port = Number(process.env.PORT ?? 4174);
const supabaseUrl = (process.env.SUPABASE_URL ?? "").replace(/\/$/, "");
const supabaseServiceRoleKey =
  process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_SECRET_KEY ?? process.env.SUPABASE_SERVICE_KEY ?? "";
const supabaseStateTable = process.env.SUPABASE_STATE_TABLE ?? "app_state";
const supabaseStateKey = process.env.SUPABASE_STATE_KEY ?? "medicomm";
const isSupabaseEnabled = Boolean(supabaseUrl && supabaseServiceRoleKey);
const DEFAULT_USER_RATING = 1480;
const DEFAULT_USER_STREAK = 1;
const DEFAULT_CORRECT_ANSWERS = 0;
const DEFAULT_ATTEMPTED_QUESTIONS = 0;
const PASSWORD_HASH_ITERATIONS = 60000;
const LEGACY_PASSWORD_HASH_ITERATIONS = 120000;
const DUEL_DURATION_SECONDS = 180;
const DUEL_QUESTION_COUNT = 5;
const DUEL_ELO_K_FACTOR = 32;
const DUEL_FALLBACK_QUESTIONS = [
  {
    prompt: "Which cranial nerve is primarily responsible for lateral eye movement?",
    options: ["Oculomotor", "Trochlear", "Abducens", "Optic"],
    answer: "Abducens",
  },
  {
    prompt: "A patient with diabetic ketoacidosis is expected to have which acid-base disturbance?",
    options: ["Metabolic acidosis", "Metabolic alkalosis", "Respiratory acidosis", "Respiratory alkalosis"],
    answer: "Metabolic acidosis",
  },
  {
    prompt: "Which valve is most commonly affected in infective endocarditis among IV drug users?",
    options: ["Mitral", "Aortic", "Pulmonic", "Tricuspid"],
    answer: "Tricuspid",
  },
  {
    prompt: "The antidote for acetaminophen overdose is:",
    options: ["Naloxone", "Atropine", "N-acetylcysteine", "Flumazenil"],
    answer: "N-acetylcysteine",
  },
  {
    prompt: "Which nephron segment is primarily responsible for fine sodium regulation under aldosterone?",
    options: ["Proximal tubule", "Loop of Henle", "Distal convoluted tubule", "Collecting duct"],
    answer: "Collecting duct",
  },
];

ensureStorage();

const seedCommunityIds = new Set(["community-usmle-step-1", "community-emergency-medicine", "community-radiology-rounds"]);
let databaseCache = null;
let supabaseWriteChain = Promise.resolve();
const storageStatus = {
  mode: isSupabaseEnabled ? "supabase" : "local",
  table: supabaseStateTable,
  key: supabaseStateKey,
  loadedAt: null,
  lastWriteAt: null,
  lastWriteStatus: isSupabaseEnabled ? "pending" : "local-only",
  lastError: null,
};

function ensureStorage() {
  if (!existsSync(dataDir)) mkdirSync(dataDir, { recursive: true });
  if (!existsSync(runtimeDataDir)) mkdirSync(runtimeDataDir, { recursive: true });
  if (!existsSync(uploadsDir)) mkdirSync(uploadsDir, { recursive: true });
  if (!existsSync(databasePath)) {
    if (existsSync(legacyDatabasePath)) {
      writeFileSync(databasePath, readFileSync(legacyDatabasePath, "utf8"));
    } else {
      writeFileSync(databasePath, JSON.stringify({ users: [], sessions: {} }, null, 2));
    }
  }
}

function getEmptyDatabase() {
  return {
    users: [],
    sessions: {},
    communities: [],
    directConversations: [],
    duelQueue: [],
    duels: [],
    duelResults: [],
    questions: [],
    practiceResults: [],
  };
}

function normalizeDatabase(parsed = {}) {
  const communities = Array.isArray(parsed.communities)
    ? parsed.communities.filter((community) => !(seedCommunityIds.has(community.id) && !community.adminUserId))
    : [];
  const users = (parsed.users ?? []).map((user) => ({
    ...user,
    rating: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    streak: Number.isFinite(user.streak) ? user.streak : DEFAULT_USER_STREAK,
    correctAnswers: Number.isFinite(user.correctAnswers) ? user.correctAnswers : DEFAULT_CORRECT_ANSWERS,
    attemptedQuestions: Number.isFinite(user.attemptedQuestions) ? user.attemptedQuestions : DEFAULT_ATTEMPTED_QUESTIONS,
  }));
  return {
    users,
    sessions: parsed.sessions ?? {},
    communities,
    directConversations: Array.isArray(parsed.directConversations) ? parsed.directConversations : [],
    duelQueue: Array.isArray(parsed.duelQueue) ? parsed.duelQueue : [],
    duels: Array.isArray(parsed.duels) ? parsed.duels : [],
    duelResults: Array.isArray(parsed.duelResults) ? parsed.duelResults : [],
    questions: Array.isArray(parsed.questions) ? parsed.questions : [],
    practiceResults: Array.isArray(parsed.practiceResults) ? parsed.practiceResults : [],
  };
}

function readLocalDatabaseFile() {
  try {
    const raw = readFileSync(databasePath, "utf8");
    return normalizeDatabase(JSON.parse(raw));
  } catch {
    return getEmptyDatabase();
  }
}

async function requestSupabaseState(method, payload = null) {
  const url = `${supabaseUrl}/rest/v1/${encodeURIComponent(supabaseStateTable)}?key=eq.${encodeURIComponent(supabaseStateKey)}`;
  const response = await fetch(url, {
    method,
    headers: {
      apikey: supabaseServiceRoleKey,
      Authorization: `Bearer ${supabaseServiceRoleKey}`,
      "Content-Type": "application/json",
      ...(method === "GET" ? {} : { Prefer: "return=minimal" }),
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });

  if (!response.ok) {
    const message = await response.text().catch(() => "");
    throw new Error(`Supabase ${method} failed: ${message || response.statusText}`);
  }

  return response;
}

async function readSupabaseDatabase() {
  const response = await requestSupabaseState("GET");
  const rows = await response.json().catch(() => []);
  const row = Array.isArray(rows) ? rows[0] : null;
  return row?.data ? normalizeDatabase(row.data) : null;
}

async function writeSupabaseDatabase(data) {
  const payload = {
    key: supabaseStateKey,
    data,
    updated_at: new Date().toISOString(),
  };
  const url = `${supabaseUrl}/rest/v1/${encodeURIComponent(supabaseStateTable)}?on_conflict=key`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      apikey: supabaseServiceRoleKey,
      Authorization: `Bearer ${supabaseServiceRoleKey}`,
      "Content-Type": "application/json",
      Prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const message = await response.text().catch(() => "");
    throw new Error(`Supabase write failed: ${message || response.statusText}`);
  }

  storageStatus.lastWriteAt = new Date().toISOString();
  storageStatus.lastWriteStatus = "ok";
  storageStatus.lastError = null;
}

async function initializeDatabaseStore() {
  const localDatabase = readLocalDatabaseFile();

  if (!isSupabaseEnabled) {
    databaseCache = localDatabase;
    storageStatus.loadedAt = new Date().toISOString();
    console.log("Supabase is not configured; using local runtime-data/users.json.");
    return;
  }

  try {
    const remoteDatabase = await readSupabaseDatabase();
    if (remoteDatabase) {
      databaseCache = remoteDatabase;
      writeFileSync(databasePath, JSON.stringify(databaseCache, null, 2));
      storageStatus.loadedAt = new Date().toISOString();
      storageStatus.lastWriteStatus = "loaded";
      storageStatus.lastError = null;
      console.log(`Loaded MediComm database from Supabase table "${supabaseStateTable}".`);
      return;
    }

    databaseCache = localDatabase;
    await writeSupabaseDatabase(databaseCache);
    storageStatus.loadedAt = new Date().toISOString();
    console.log(`Seeded Supabase table "${supabaseStateTable}" from local database backup.`);
  } catch (error) {
    databaseCache = localDatabase;
    storageStatus.mode = "local-fallback";
    storageStatus.loadedAt = new Date().toISOString();
    storageStatus.lastWriteStatus = "error";
    storageStatus.lastError = error instanceof Error ? error.message : "Could not connect to Supabase.";
    console.warn(error instanceof Error ? error.message : "Could not connect to Supabase.");
    console.warn("Falling back to local runtime-data/users.json for this process.");
  }
}

function readDatabase() {
  if (!databaseCache) {
    databaseCache = readLocalDatabaseFile();
  }
  return structuredClone(databaseCache);
}

function writeDatabase(data) {
  databaseCache = normalizeDatabase(data);
  writeFileSync(databasePath, JSON.stringify(databaseCache, null, 2));

  if (!isSupabaseEnabled) return Promise.resolve();

  const databaseSnapshot = structuredClone(databaseCache);
  supabaseWriteChain = supabaseWriteChain.catch(() => undefined).then(() => writeSupabaseDatabase(databaseSnapshot));

  return supabaseWriteChain.catch((error) => {
    storageStatus.lastWriteStatus = "error";
    storageStatus.lastError = error instanceof Error ? error.message : "Could not write database to Supabase.";
    console.warn(storageStatus.lastError);
    throw error;
  });
}

function normalizeContactNumber(value) {
  return String(value ?? "").replace(/\D/g, "");
}

function readPracticeQuestionBank() {
  if (!existsSync(practiceQuestionBankPath)) {
    return {
      exam: {
        id: "neet-pg-2020",
        title: "NEET PG 2020 PYQs",
        year: 2020,
        questionCount: 0,
      },
      years: [],
      subjects: [],
    };
  }

  return JSON.parse(readFileSync(practiceQuestionBankPath, "utf8"));
}

function normalizeQuestion(question, subject, exam = {}) {
  const prompt = [question.subtopic, question.prompt].filter(Boolean).join(" ").trim();
  const options = Array.isArray(question.options) ? question.options.map((option) => String(option).trim()) : [];
  const answerIndex = Number.isInteger(question.answerIndex) ? question.answerIndex : options.indexOf(question.answer);
  const answer = options[answerIndex] ?? question.answer ?? "";

  return {
    id: String(question.id ?? randomBytes(8).toString("hex")),
    examId: String(question.examId ?? exam.id ?? "neet-pg-pyqs"),
    year: Number.isFinite(question.year) ? question.year : exam.year ?? null,
    subjectId: String(question.subjectId ?? subject?.id ?? ""),
    subjectTitle: String(subject?.title ?? question.subjectTitle ?? ""),
    topic: String(question.topic ?? "General").trim() || "General",
    prompt: prompt || String(question.prompt ?? "").trim(),
    options,
    answerIndex,
    answer: String(answer ?? ""),
    explanation: String(question.explanation ?? (answer ? `Correct answer: ${answer}` : "")).trim(),
    difficulty: String(question.difficulty ?? "exam").trim(),
    source: question.source === "ai" ? "ai" : "official",
    images: Array.isArray(question.images) ? question.images : [],
    createdAt: question.createdAt ?? null,
  };
}

function getOfficialPracticeQuestions(library) {
  const examsById = new Map((library.exams ?? []).map((exam) => [exam.id, exam]));
  return (library.subjects ?? []).flatMap((subject) =>
    (subject.questions ?? []).map((question) => {
      const exam = examsById.get(question.examId) ?? library.exam ?? {};
      return normalizeQuestion(question, subject, exam);
    }),
  );
}

function questionMatchesFilters(question, filters) {
  return (
    (!filters.examId || question.examId === filters.examId) &&
    (!filters.year || String(question.year ?? "") === filters.year) &&
    (!filters.subjectId || question.subjectId === filters.subjectId) &&
    (!filters.topic || question.topic.toLowerCase() === filters.topic.toLowerCase()) &&
    (!filters.source || question.source === filters.source)
  );
}

function applyPracticeFilters(questions, url) {
  const filters = {
    examId: String(url.searchParams.get("examId") ?? "").trim(),
    year: String(url.searchParams.get("year") ?? "").trim(),
    subjectId: String(url.searchParams.get("subjectId") ?? "").trim(),
    topic: String(url.searchParams.get("topic") ?? "").trim(),
    source: String(url.searchParams.get("source") ?? "").trim(),
  };

  return questions.filter((question) => questionMatchesFilters(question, filters));
}

function buildPracticeLibrary(library, storedQuestions = []) {
  const aiQuestions = storedQuestions.filter((question) => question.source === "ai").map((question) => normalizeQuestion(question));
  const questionsBySubjectId = new Map();

  for (const question of aiQuestions) {
    const bucket = questionsBySubjectId.get(question.subjectId) ?? [];
    bucket.push(question);
    questionsBySubjectId.set(question.subjectId, bucket);
  }

  return {
    ...library,
    subjects: (library.subjects ?? []).map((subject) => {
      return {
        ...subject,
        questions: (subject.questions ?? []).map((question) => normalizeQuestion(question, subject, library.exam)),
      };
    }),
    aiSubjects: (library.subjects ?? []).map((subject) => {
      const questions = questionsBySubjectId.get(subject.id) ?? [];
      return {
        id: subject.id,
        title: subject.title,
        questionCount: questions.length,
        questions,
      };
    }),
  };
}

function sanitizeDuelQuestion(question) {
  const options = Array.isArray(question.options) ? question.options.map((option) => String(option).trim()).filter(Boolean) : [];
  const answerIndex = Number.isInteger(question.answerIndex) ? question.answerIndex : options.indexOf(question.answer);
  return {
    id: String(question.id ?? randomBytes(8).toString("hex")),
    prompt: String(question.prompt ?? "").trim(),
    options,
    answerIndex,
    answer: String(options[answerIndex] ?? question.answer ?? ""),
    explanation: String(question.explanation ?? "").trim(),
    subjectId: String(question.subjectId ?? "").trim(),
    subjectTitle: String(question.subjectTitle ?? "").trim(),
    source: question.source === "ai" ? "ai" : "official",
  };
}

function sanitizeDuelQuestionForClient(question) {
  const sanitized = sanitizeDuelQuestion(question);
  return {
    id: sanitized.id,
    prompt: sanitized.prompt,
    options: sanitized.options,
    explanation: sanitized.explanation,
    subjectId: sanitized.subjectId,
    subjectTitle: sanitized.subjectTitle,
    source: sanitized.source,
  };
}

function getDuelQuestionPool() {
  const officialQuestions = getOfficialPracticeQuestions(readPracticeQuestionBank())
    .map((question) => sanitizeDuelQuestion(question))
    .filter(
      (question) =>
        question.prompt &&
        question.options.length === 4 &&
        question.answer &&
        question.answerIndex >= 0 &&
        question.answerIndex < question.options.length &&
        question.options.includes(question.answer),
    );

  if (officialQuestions.length >= DUEL_QUESTION_COUNT) return officialQuestions;
  return DUEL_FALLBACK_QUESTIONS.map((question, index) =>
    sanitizeDuelQuestion({
      ...question,
      id: `clinical-fallback-${index + 1}`,
      source: "official",
      subjectTitle: "Clinical basics",
    }),
  );
}

function pickDuelQuestions(count = DUEL_QUESTION_COUNT) {
  const pool = getDuelQuestionPool();
  const targetCount = Math.min(Math.max(1, count), pool.length);
  const shuffled = [...pool];

  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const swapIndex = randomBytes(4).readUInt32BE(0) % (index + 1);
    [shuffled[index], shuffled[swapIndex]] = [shuffled[swapIndex], shuffled[index]];
  }

  return shuffled.slice(0, targetCount);
}

function getQuestionAnswerMap(questionIds = []) {
  const pool = getDuelQuestionPool();
  const byId = new Map(pool.map((question) => [question.id, question]));
  return questionIds.map((questionId) => byId.get(String(questionId))).filter(Boolean);
}

function getValidSubjectIds(library) {
  return new Set((library.subjects ?? []).map((subject) => subject.id));
}

function validateGeneratedQuestion(question, library) {
  const validSubjectIds = getValidSubjectIds(library);
  const prompt = String(question.prompt ?? "").trim();
  const explanation = String(question.explanation ?? "").trim();
  const options = Array.isArray(question.options) ? question.options.map((option) => String(option).trim()).filter(Boolean) : [];
  const answerIndex = Number(question.answerIndex);
  const subjectId = String(question.subjectId ?? "").trim();
  const topic = String(question.topic ?? "").trim();

  if (!prompt) return "Generated question must include a non-empty prompt.";
  if (options.length !== 4) return "Generated question must include exactly 4 options.";
  if (!Number.isInteger(answerIndex) || answerIndex < 0 || answerIndex > 3) {
    return "Generated question must include one correct answerIndex from 0 to 3.";
  }
  if (String(question.answer ?? "").trim() !== options[answerIndex]) {
    return "Generated question answer must match options[answerIndex].";
  }
  if (!explanation) return "Generated question must include a non-empty explanation.";
  if (!validSubjectIds.has(subjectId)) return "Generated question must use a valid subjectId from the PYQ bank.";
  if (!topic) return "Generated question must include a valid topic.";

  return null;
}

async function requestGeminiQuestion(payload, library) {
  const apiKey = process.env.GEMINI_API_KEY ?? process.env.GOOGLE_AI_STUDIO_API_KEY;
  if (!apiKey) {
    throw new Error("Set GEMINI_API_KEY to enable AI-generated supplemental practice.");
  }

  const model = process.env.GEMINI_MODEL ?? "gemini-2.5-flash";
  const subjectList = (library.subjects ?? []).map((subject) => `${subject.id}: ${subject.title}`).join(", ");
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "object",
            required: [
              "examId",
              "year",
              "subjectId",
              "topic",
              "prompt",
              "options",
              "answerIndex",
              "answer",
              "explanation",
              "difficulty",
            ],
            properties: {
              examId: { type: "string" },
              year: { type: "integer" },
              subjectId: { type: "string" },
              topic: { type: "string" },
              prompt: { type: "string" },
              options: {
                type: "array",
                minItems: 4,
                maxItems: 4,
                items: { type: "string" },
              },
              answerIndex: { type: "integer", minimum: 0, maximum: 3 },
              answer: { type: "string" },
              explanation: { type: "string" },
              difficulty: { type: "string" },
            },
          },
          temperature: 0.7,
        },
        contents: [
          {
            role: "user",
            parts: [
              {
                text:
                  "Create one supplemental medical MCQ. Return only JSON with keys examId, year, subjectId, topic, prompt, options, answerIndex, answer, explanation, difficulty. " +
                  `Valid subjectIds are: ${subjectList}. ` +
                  `Request: ${JSON.stringify(payload)}`,
              },
            ],
          },
        ],
      }),
    },
  );

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error?.message ?? "Gemini could not generate a question.");
  }

  const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) throw new Error("Gemini returned an empty response.");
  return JSON.parse(text);
}

async function requestGeminiQuestionBatch(payload, library, count) {
  const apiKey = process.env.GEMINI_API_KEY ?? process.env.GOOGLE_AI_STUDIO_API_KEY;
  if (!apiKey) {
    throw new Error("Set GEMINI_API_KEY to enable AI-generated supplemental practice.");
  }

  const model = process.env.GEMINI_MODEL ?? "gemini-2.5-flash";
  const subjectList = (library.subjects ?? []).map((subject) => `${subject.id}: ${subject.title}`).join(", ");
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "array",
            minItems: count,
            maxItems: count,
            items: {
              type: "object",
              required: [
                "examId",
                "year",
                "subjectId",
                "topic",
                "prompt",
                "options",
                "answerIndex",
                "answer",
                "explanation",
                "difficulty",
              ],
              properties: {
                examId: { type: "string" },
                year: { type: "integer" },
                subjectId: { type: "string" },
                topic: { type: "string" },
                prompt: { type: "string" },
                options: {
                  type: "array",
                  minItems: 4,
                  maxItems: 4,
                  items: { type: "string" },
                },
                answerIndex: { type: "integer", minimum: 0, maximum: 3 },
                answer: { type: "string" },
                explanation: { type: "string" },
                difficulty: { type: "string" },
              },
            },
          },
          temperature: 0.7,
        },
        contents: [
          {
            role: "user",
            parts: [
              {
                text:
                  `Create exactly ${count} supplemental medical MCQs. Return only a JSON array. ` +
                  "Every item must include examId, year, subjectId, topic, prompt, options, answerIndex, answer, explanation, difficulty. " +
                  "Use exactly 4 options per question and make answer equal to options[answerIndex]. " +
                  `Valid subjectIds are: ${subjectList}. ` +
                  `Request: ${JSON.stringify(payload)}`,
              },
            ],
          },
        ],
      }),
    },
  );

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error?.message ?? "Gemini could not generate questions.");
  }

  const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) throw new Error("Gemini returned an empty response.");
  const parsed = JSON.parse(text);
  if (!Array.isArray(parsed)) throw new Error("Gemini did not return a question array.");
  return parsed;
}

function countPracticeQuestions(library) {
  const countedFromSubjects = (library.subjects ?? []).reduce(
    (total, subject) => total + (subject.questions?.length ?? subject.questionCount ?? 0),
    0,
  );
  if (countedFromSubjects) return countedFromSubjects;
  if (Number.isFinite(library.exam?.questionCount)) return library.exam.questionCount;

  return (library.years ?? []).reduce(
    (total, year) =>
      total +
      (year.subjects ?? []).reduce((subjectTotal, subject) => subjectTotal + (subject.questions?.length ?? 0), 0),
    0,
  );
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  response.end(JSON.stringify(payload));
}

const staticMimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

async function serveStaticFile(response, requestPath) {
  if (!existsSync(distDir)) {
    sendJson(response, 404, { message: "Frontend build not found. Run npm run build before starting the server." });
    return;
  }

  const decodedPath = decodeURIComponent(requestPath);
  const normalizedPath = path.normalize(decodedPath).replace(/^(\.\.[/\\])+/, "");
  const requestedPath = path.join(distDir, normalizedPath);
  const resolvedPath = requestedPath.startsWith(distDir) ? requestedPath : path.join(distDir, "index.html");
  const filePath = existsSync(resolvedPath) ? resolvedPath : path.join(distDir, "index.html");

  try {
    const file = await fs.readFile(filePath);
    const extension = path.extname(filePath).toLowerCase();
    response.writeHead(200, {
      "Content-Type": staticMimeTypes[extension] ?? "application/octet-stream",
      "Cache-Control": filePath.endsWith("index.html") ? "no-cache" : "public, max-age=31536000, immutable",
    });
    response.end(file);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
}

function hashPassword(password, salt = randomBytes(16).toString("hex")) {
  const hash = pbkdf2Sync(password, salt, PASSWORD_HASH_ITERATIONS, 64, "sha512").toString("hex");
  return { salt, hash, iterations: PASSWORD_HASH_ITERATIONS };
}

function verifyPassword(password, salt, expectedHash, iterations = LEGACY_PASSWORD_HASH_ITERATIONS) {
  const attempt = pbkdf2Sync(password, salt, iterations, 64, "sha512");
  const stored = Buffer.from(expectedHash, "hex");
  return stored.length === attempt.length && timingSafeEqual(attempt, stored);
}

function sanitizeUser(user) {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    medicalCollege: user.medicalCollege,
    contactNumber: user.contactNumber,
    rating: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    streak: Number.isFinite(user.streak) ? user.streak : DEFAULT_USER_STREAK,
    correctAnswers: Number.isFinite(user.correctAnswers) ? user.correctAnswers : DEFAULT_CORRECT_ANSWERS,
    attemptedQuestions: Number.isFinite(user.attemptedQuestions) ? user.attemptedQuestions : DEFAULT_ATTEMPTED_QUESTIONS,
    profileImageUrl: user.profileImagePath ? `/uploads/${user.profileImagePath}` : null,
    createdAt: user.createdAt,
  };
}

function getLeaderboardRegion(medicalCollege) {
  const mappedState = resolveCollegeState(medicalCollege);
  if (mappedState) return mappedState;

  const normalized = String(medicalCollege ?? "").trim();
  if (!normalized) return "Registered users";

  const segments = normalized
    .split(",")
    .map((segment) => segment.trim())
    .filter(Boolean);

  if (segments.length < 2) return "Registered users";
  return segments.at(-1) ?? "Registered users";
}

function sanitizePublicUserProfile(user, currentUserId = null) {
  return {
    id: user.id,
    name: user.name,
    medicalCollege: user.medicalCollege,
    rating: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    streak: Number.isFinite(user.streak) ? user.streak : DEFAULT_USER_STREAK,
    correctAnswers: Number.isFinite(user.correctAnswers) ? user.correctAnswers : DEFAULT_CORRECT_ANSWERS,
    attemptedQuestions: Number.isFinite(user.attemptedQuestions) ? user.attemptedQuestions : DEFAULT_ATTEMPTED_QUESTIONS,
    profileImageUrl: user.profileImagePath ? `/uploads/${user.profileImagePath}` : null,
    state: getLeaderboardRegion(user.medicalCollege),
    createdAt: user.createdAt,
    isCurrentUser: currentUserId ? user.id === currentUserId : false,
  };
}

function sanitizeLeaderboardUser(user, currentUserId = null) {
  return {
    id: user.id,
    name: user.name,
    state: getLeaderboardRegion(user.medicalCollege),
    college: user.medicalCollege || "Medical college",
    score: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    streak: Number.isFinite(user.streak) ? user.streak : DEFAULT_USER_STREAK,
    isCurrentUser: currentUserId ? user.id === currentUserId : false,
  };
}

function sanitizeSearchableUser(user, currentUserId = null) {
  return {
    id: user.id,
    name: user.name,
    medicalCollege: user.medicalCollege,
    profileImageUrl: user.profileImagePath ? `/uploads/${user.profileImagePath}` : null,
    state: getLeaderboardRegion(user.medicalCollege),
    rating: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    streak: Number.isFinite(user.streak) ? user.streak : DEFAULT_USER_STREAK,
    isCurrentUser: currentUserId ? user.id === currentUserId : false,
  };
}

function sanitizeDuelOpponent(user, currentUserId = null) {
  return {
    id: user.id,
    name: user.name,
    rating: Number.isFinite(user.rating) ? user.rating : DEFAULT_USER_RATING,
    specialty: getLeaderboardRegion(user.medicalCollege),
    profileImageUrl: user.profileImagePath ? `/uploads/${user.profileImagePath}` : null,
    isCurrentUser: currentUserId ? user.id === currentUserId : false,
  };
}

function sanitizeCommunity(community, users, currentUserId = null) {
  const members = community.memberIds
    .map((memberId) => users.find((user) => user.id === memberId))
    .filter(Boolean)
    .map((user) => ({
      id: user.id,
      name: user.name,
      medicalCollege: user.medicalCollege,
      profileImageUrl: user.profileImagePath ? `/uploads/${user.profileImagePath}` : null,
    }));

  return {
    id: community.id,
    name: community.name,
    description: community.description,
    topic: community.topic,
    createdAt: community.createdAt,
    adminUserId: community.adminUserId,
    adminName: users.find((user) => user.id === community.adminUserId)?.name ?? "MediComm",
    isAdmin: currentUserId ? community.adminUserId === currentUserId : false,
    isMember: currentUserId ? community.memberIds.includes(currentUserId) : false,
    memberCount: community.memberIds.length,
    members,
    messages: (community.messages ?? []).map((message) => ({
      id: message.id,
      userId: message.userId,
      userName: message.userName,
      text: message.text,
      createdAt: message.createdAt,
      isOwnMessage: currentUserId ? message.userId === currentUserId : false,
    })),
  };
}

function getDirectConversationWithUserMetadata(conversation, users, currentUserId) {
  const otherParticipantId = (conversation.participantIds ?? []).find((participantId) => participantId !== currentUserId) ?? null;
  const otherParticipant = users.find((user) => user.id === otherParticipantId) ?? null;
  return {
    otherParticipantId,
    otherParticipant,
  };
}

function sanitizeDirectConversation(conversation, users, currentUserId) {
  const { otherParticipantId, otherParticipant } = getDirectConversationWithUserMetadata(conversation, users, currentUserId);
  return {
    id: conversation.id,
    participantIds: conversation.participantIds ?? [],
    otherParticipantId,
    otherParticipant: otherParticipant
      ? sanitizeSearchableUser(otherParticipant, currentUserId)
      : {
          id: otherParticipantId,
          name: "Unknown user",
          medicalCollege: "",
          profileImageUrl: null,
          state: "Registered users",
          rating: DEFAULT_USER_RATING,
          streak: DEFAULT_USER_STREAK,
          isCurrentUser: false,
        },
    updatedAt: conversation.updatedAt ?? conversation.createdAt,
    createdAt: conversation.createdAt,
    messages: (conversation.messages ?? []).map((message) => ({
      id: message.id,
      userId: message.userId,
      userName: message.userName,
      text: message.text,
      type: message.type ?? "text",
      createdAt: message.createdAt,
      isOwnMessage: currentUserId ? message.userId === currentUserId : false,
    })),
  };
}

async function parseRequestBody(request) {
  const chunks = [];

  for await (const chunk of request) {
    chunks.push(chunk);
  }

  const rawBody = Buffer.concat(chunks).toString("utf8");
  if (!rawBody) return {};

  try {
    return JSON.parse(rawBody);
  } catch {
    throw new Error("Invalid JSON body.");
  }
}

function getTokenFromRequest(request) {
  const authorization = request.headers.authorization ?? "";
  if (!authorization.startsWith("Bearer ")) return null;
  return authorization.slice("Bearer ".length).trim();
}

function getSessionUser(request, database) {
  const token = getTokenFromRequest(request);
  if (!token) return null;

  const userId = database.sessions[token];
  if (!userId) return null;

  return database.users.find((user) => user.id === userId) ?? null;
}

function validateSignupPayload(payload) {
  const requiredFields = [
    ["name", "Name"],
    ["email", "Email"],
    ["medicalCollege", "Medical college"],
    ["contactNumber", "Contact number"],
    ["password", "Password"],
  ];

  for (const [field, label] of requiredFields) {
    if (!String(payload[field] ?? "").trim()) {
      return `${label} is required.`;
    }
  }

  if (!/^\S+@\S+\.\S+$/.test(payload.email)) return "Enter a valid email address.";
  if (normalizeContactNumber(payload.contactNumber).length < 8) return "Enter a valid mobile number.";
  if (String(payload.password).length < 6) return "Password must be at least 6 characters.";
  return null;
}

async function saveProfileImage(userId, dataUrl, existingFileName) {
  const matches = String(dataUrl).match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,(.+)$/);
  if (!matches) throw new Error("Profile photo must be a valid image.");

  const mimeType = matches[1];
  const base64Payload = matches[2];
  const supportedTypes = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
  };

  const extension = supportedTypes[mimeType];
  if (!extension) throw new Error("Only PNG, JPG, WEBP, or GIF profile pictures are supported.");

  const fileName = `${userId}-${Date.now()}.${extension}`;
  const filePath = path.join(uploadsDir, fileName);
  await fs.writeFile(filePath, Buffer.from(base64Payload, "base64"));

  if (existingFileName) {
    const existingPath = path.join(uploadsDir, existingFileName);
    if (existsSync(existingPath)) unlinkSync(existingPath);
  }

  return fileName;
}

async function handlePublicUserProfile(request, response, userId) {
  const database = readDatabase();
  const sessionUser = getSessionUser(request, database);
  if (!sessionUser) {
    sendJson(response, 401, { error: "Please log in to view profiles." });
    return;
  }

  const targetUser = database.users.find((user) => user.id === userId);
  if (!targetUser) {
    sendJson(response, 404, { error: "User profile not found." });
    return;
  }

  sendJson(response, 200, { user: sanitizePublicUserProfile(targetUser, sessionUser.id) });
}

async function handleSignup(request, response) {
  const database = readDatabase();
  const payload = await parseRequestBody(request);
  const validationMessage = validateSignupPayload(payload);

  if (validationMessage) {
    return sendJson(response, 400, { message: validationMessage });
  }

  const email = String(payload.email).trim().toLowerCase();
  const contactNumber = normalizeContactNumber(payload.contactNumber);
  if (database.users.some((user) => user.email.toLowerCase() === email)) {
    return sendJson(response, 409, { message: "An account with this email already exists." });
  }
  if (database.users.some((user) => normalizeContactNumber(user.contactNumber) === contactNumber)) {
    return sendJson(response, 409, { message: "An account with this mobile number already exists." });
  }

  const { hash, salt, iterations } = hashPassword(String(payload.password));
  const user = {
    id: randomBytes(12).toString("hex"),
    name: String(payload.name).trim(),
    email,
    medicalCollege: String(payload.medicalCollege).trim(),
    contactNumber,
    rating: DEFAULT_USER_RATING,
    streak: DEFAULT_USER_STREAK,
    correctAnswers: DEFAULT_CORRECT_ANSWERS,
    attemptedQuestions: DEFAULT_ATTEMPTED_QUESTIONS,
    passwordHash: hash,
    passwordSalt: salt,
    passwordIterations: iterations,
    profileImagePath: null,
    createdAt: new Date().toISOString(),
  };

  const token = randomBytes(24).toString("hex");
  database.users.push(user);
  database.sessions[token] = user.id;
  await writeDatabase(database);

  return sendJson(response, 201, {
    token,
    user: sanitizeUser(user),
  });
}

async function handleLogin(request, response) {
  const database = readDatabase();
  const payload = await parseRequestBody(request);
  const email = String(payload.email ?? "").trim().toLowerCase();
  const password = String(payload.password ?? "");

  if (!email || !password) {
    return sendJson(response, 400, { message: "Email and password are required." });
  }

  const user = database.users.find((entry) => entry.email.toLowerCase() === email);
  const passwordIterations = Number.isFinite(user?.passwordIterations)
    ? user.passwordIterations
    : LEGACY_PASSWORD_HASH_ITERATIONS;

  if (!user || !verifyPassword(password, user.passwordSalt, user.passwordHash, passwordIterations)) {
    return sendJson(response, 401, { message: "Invalid email or password." });
  }

  if (passwordIterations !== PASSWORD_HASH_ITERATIONS) {
    const { hash, salt, iterations } = hashPassword(password);
    user.passwordHash = hash;
    user.passwordSalt = salt;
    user.passwordIterations = iterations;
  }

  const token = randomBytes(24).toString("hex");
  database.sessions[token] = user.id;
  await writeDatabase(database);

  return sendJson(response, 200, {
    token,
    user: sanitizeUser(user),
  });
}

function handleSession(request, response) {
  const database = readDatabase();
  const user = getSessionUser(request, database);

  if (!user) {
    return sendJson(response, 401, { message: "Session expired. Please sign in again." });
  }

  return sendJson(response, 200, { user: sanitizeUser(user) });
}

async function handleLogout(request, response) {
  const database = readDatabase();
  const token = getTokenFromRequest(request);

  if (token && database.sessions[token]) {
    delete database.sessions[token];
    await writeDatabase(database);
  }

  return sendJson(response, 200, { success: true });
}

async function handleProfileUpdate(request, response) {
  const database = readDatabase();
  const token = getTokenFromRequest(request);
  const sessionUser = getSessionUser(request, database);

  if (!token || !sessionUser) {
    return sendJson(response, 401, { message: "Please log in to update your profile." });
  }

  const payload = await parseRequestBody(request);
  const name = String(payload.name ?? "").trim();
  const medicalCollege = String(payload.medicalCollege ?? "").trim();
  const contactNumber = String(payload.contactNumber ?? "").trim();
  const normalizedContactNumber = normalizeContactNumber(contactNumber);

  if (!name || !medicalCollege || !normalizedContactNumber) {
    return sendJson(response, 400, { message: "Name, medical college, and contact number are required." });
  }
  if (normalizedContactNumber.length < 8) {
    return sendJson(response, 400, { message: "Enter a valid mobile number." });
  }

  const userIndex = database.users.findIndex((user) => user.id === sessionUser.id);
  if (
    database.users.some(
      (user) => user.id !== sessionUser.id && normalizeContactNumber(user.contactNumber) === normalizedContactNumber,
    )
  ) {
    return sendJson(response, 409, { message: "Another account already uses this mobile number." });
  }
  const updatedUser = {
    ...database.users[userIndex],
    name,
    medicalCollege,
    contactNumber: normalizedContactNumber,
  };

  if (payload.profileImageDataUrl) {
    updatedUser.profileImagePath = await saveProfileImage(
      updatedUser.id,
      payload.profileImageDataUrl,
      updatedUser.profileImagePath,
    );
  }

  database.users[userIndex] = updatedUser;
  await writeDatabase(database);

  return sendJson(response, 200, { user: sanitizeUser(updatedUser) });
}

async function handleProfileStatsUpdate(request, response) {
  const database = readDatabase();
  const token = getTokenFromRequest(request);
  const sessionUser = getSessionUser(request, database);

  if (!token || !sessionUser) {
    return sendJson(response, 401, { message: "Please log in to update your stats." });
  }

  const payload = await parseRequestBody(request);
  const userIndex = database.users.findIndex((user) => user.id === sessionUser.id);

  if (userIndex === -1) {
    return sendJson(response, 404, { message: "User not found." });
  }

  const nextRating = Number.isFinite(database.users[userIndex].rating)
    ? database.users[userIndex].rating
    : DEFAULT_USER_RATING;
  const nextStreak = Number.isFinite(payload.streak)
    ? Math.max(1, Math.round(payload.streak))
    : database.users[userIndex].streak;
  const nextCorrectAnswers = Number.isFinite(payload.correctAnswers)
    ? Math.max(0, Math.round(payload.correctAnswers))
    : database.users[userIndex].correctAnswers;
  const nextAttemptedQuestions = Number.isFinite(payload.attemptedQuestions)
    ? Math.max(0, Math.round(payload.attemptedQuestions))
    : database.users[userIndex].attemptedQuestions;

  const updatedUser = {
    ...database.users[userIndex],
    rating: nextRating,
    streak: nextStreak,
    correctAnswers: nextCorrectAnswers,
    attemptedQuestions: nextAttemptedQuestions,
  };

  database.users[userIndex] = updatedUser;
  await writeDatabase(database);

  return sendJson(response, 200, { user: sanitizeUser(updatedUser) });
}

function requireSessionUser(request, response, database) {
  const token = getTokenFromRequest(request);
  const user = getSessionUser(request, database);

  if (!token || !user) {
    sendJson(response, 401, { message: "Please log in to continue." });
    return null;
  }

  return user;
}

function handleCommunitiesList(request, response) {
  const database = readDatabase();
  const currentUser = getSessionUser(request, database);
  const communities = database.communities.map((community) =>
    sanitizeCommunity(community, database.users, currentUser?.id ?? null),
  );

  return sendJson(response, 200, { communities });
}

function handleUserSearch(request, response, url) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const query = String(url.searchParams.get("q") ?? "")
    .trim()
    .toLowerCase();

  if (!query) {
    return sendJson(response, 200, { users: [] });
  }

  const users = database.users
    .filter((user) => user.id !== currentUser.id)
    .filter((user) => {
      const haystack = [user.name, user.medicalCollege, getLeaderboardRegion(user.medicalCollege)]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    })
    .sort((left, right) => left.name.localeCompare(right.name))
    .slice(0, 12)
    .map((user) => sanitizeSearchableUser(user, currentUser.id));

  return sendJson(response, 200, { users });
}

function handleDirectConversationsList(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const conversations = database.directConversations
    .filter((conversation) => (conversation.participantIds ?? []).includes(currentUser.id))
    .sort(
      (left, right) =>
        new Date(right.updatedAt ?? right.createdAt).getTime() - new Date(left.updatedAt ?? left.createdAt).getTime(),
    )
    .map((conversation) => sanitizeDirectConversation(conversation, database.users, currentUser.id));

  return sendJson(response, 200, { conversations });
}

async function handleOpenDirectConversation(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const payload = await parseRequestBody(request);
  const targetUserId = String(payload.targetUserId ?? "").trim();

  if (!targetUserId || targetUserId === currentUser.id) {
    return sendJson(response, 400, { message: "Choose a valid user to start a private chat." });
  }

  const targetUser = database.users.find((user) => user.id === targetUserId);
  if (!targetUser) {
    return sendJson(response, 404, { message: "That user could not be found." });
  }

  let conversation =
    database.directConversations.find((entry) => {
      const participants = entry.participantIds ?? [];
      return participants.length === 2 && participants.includes(currentUser.id) && participants.includes(targetUserId);
    }) ?? null;

  if (!conversation) {
    const createdAt = new Date().toISOString();
    conversation = {
      id: randomBytes(10).toString("hex"),
      participantIds: [currentUser.id, targetUserId],
      createdAt,
      updatedAt: createdAt,
      messages: [
        {
          id: randomBytes(8).toString("hex"),
          userId: null,
          userName: "MediComm Bot",
          text: `Private chat opened between ${currentUser.name} and ${targetUser.name}.`,
          type: "system",
          createdAt,
        },
      ],
    };
    database.directConversations.unshift(conversation);
    await writeDatabase(database);
  }

  return sendJson(response, 200, {
    conversation: sanitizeDirectConversation(conversation, database.users, currentUser.id),
  });
}

async function handleSendDirectMessage(request, response, conversationId) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const conversationIndex = database.directConversations.findIndex((conversation) => conversation.id === conversationId);
  if (conversationIndex === -1) {
    return sendJson(response, 404, { message: "Conversation not found." });
  }

  const conversation = database.directConversations[conversationIndex];
  if (!(conversation.participantIds ?? []).includes(currentUser.id)) {
    return sendJson(response, 403, { message: "You are not part of this conversation." });
  }

  const payload = await parseRequestBody(request);
  const text = String(payload.text ?? "").trim();
  const type = String(payload.type ?? "text").trim();

  if (!text) {
    return sendJson(response, 400, { message: "Message cannot be empty." });
  }

  if (!["text", "challenge"].includes(type)) {
    return sendJson(response, 400, { message: "Unsupported message type." });
  }

  const createdAt = new Date().toISOString();
  conversation.messages.push({
    id: randomBytes(8).toString("hex"),
    userId: currentUser.id,
    userName: currentUser.name,
    text,
    type,
    createdAt,
  });
  conversation.updatedAt = createdAt;

  database.directConversations[conversationIndex] = conversation;
  await writeDatabase(database);

  return sendJson(response, 200, {
    conversation: sanitizeDirectConversation(conversation, database.users, currentUser.id),
  });
}

function handleLeaderboard(request, response) {
  const database = readDatabase();
  const currentUser = getSessionUser(request, database);
  const players = database.users
    .map((user) => sanitizeLeaderboardUser(user, currentUser?.id ?? null))
    .sort((left, right) => right.score - left.score || right.streak - left.streak || left.name.localeCompare(right.name));

  return sendJson(response, 200, { players });
}

function findActiveRatedDuel(database, userId) {
  return (database.duels ?? []).find((duel) => duel.status === "matched" && (duel.playerIds ?? []).includes(userId)) ?? null;
}

function buildRatedDuelPayload(duel, currentUser, database) {
  const opponentId = (duel.playerIds ?? []).find((playerId) => playerId !== currentUser.id);
  const opponent = database.users.find((user) => user.id === opponentId) ?? null;

  return {
    status: "matched",
    duel: {
      id: duel.id,
      createdAt: duel.createdAt,
      startedAt: duel.startedAt,
      playerIds: duel.playerIds,
    },
    opponent: opponent ? sanitizeDuelOpponent(opponent, currentUser.id) : null,
  };
}

function calculateExpectedScore(playerRating, opponentRating) {
  return 1 / (1 + 10 ** ((opponentRating - playerRating) / 400));
}

function calculateEloDelta(playerRating, opponentRating, actualScore) {
  const expectedScore = calculateExpectedScore(playerRating, opponentRating);
  return Math.round(DUEL_ELO_K_FACTOR * (actualScore - expectedScore));
}

function getActualScore(userScore, opponentScore) {
  if (userScore > opponentScore) return { actualScore: 1, verdict: "win" };
  if (userScore < opponentScore) return { actualScore: 0, verdict: "loss" };
  return { actualScore: 0.5, verdict: "draw" };
}

function scoreDuelAnswers(payload) {
  const answers = payload.answers && typeof payload.answers === "object" ? payload.answers : {};
  const questionIds = Array.isArray(payload.questionIds) ? payload.questionIds.map((id) => String(id)) : [];
  const questions = getQuestionAnswerMap(questionIds);

  if (!questions.length || questions.length !== questionIds.length) {
    return { error: "Duel questions could not be verified. Start a fresh duel and try again." };
  }

  const correct = questions.reduce((total, question) => {
    const selected = String(answers[question.id] ?? "").trim();
    return total + (selected && selected === question.answer ? 1 : 0);
  }, 0);

  return {
    questions,
    correct,
    attempted: questions.length,
  };
}

function sanitizeDuelResult(result) {
  return {
    id: result.id,
    duelId: result.duelId,
    mode: result.mode,
    verdict: result.verdict,
    delta: result.delta,
    previousRating: result.previousRating,
    nextRating: result.nextRating,
    userScore: result.userScore,
    opponentScore: result.opponentScore,
    attemptedQuestions: result.attemptedQuestions,
    correctAnswers: result.correctAnswers,
    ratingAffected: result.ratingAffected,
    forfeited: Boolean(result.forfeited),
    completedAt: result.completedAt,
  };
}

function handleDuelQuestions(request, response, url) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return null;

  const count = Number(url.searchParams.get("count") ?? DUEL_QUESTION_COUNT);
  const questions = pickDuelQuestions(Number.isFinite(count) ? Math.round(count) : DUEL_QUESTION_COUNT).map(
    sanitizeDuelQuestionForClient,
  );
  return sendJson(response, 200, {
    durationSeconds: DUEL_DURATION_SECONDS,
    questions,
  });
}

async function handleCompleteDuel(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return null;

  const payload = await parseRequestBody(request);
  const mode = payload.mode === "bot" ? "bot" : "rated";
  const forfeited = Boolean(payload.forfeit);
  const duelId = String(payload.duelId ?? "").trim() || (mode === "bot" ? `bot-${currentUser.id}-${String(payload.sessionId ?? "")}` : "");
  const resultKey = duelId ? `${duelId}:${currentUser.id}` : "";

  if (resultKey) {
    const previousResult = (database.duelResults ?? []).find((result) => result.resultKey === resultKey);
    if (previousResult) {
      return sendJson(response, 200, { result: sanitizeDuelResult(previousResult), user: sanitizeUser(currentUser) });
    }
  }

  const scored = scoreDuelAnswers(payload);
  if (scored.error) {
    return sendJson(response, 422, { message: scored.error });
  }

  const userIndex = database.users.findIndex((user) => user.id === currentUser.id);
  if (userIndex === -1) {
    return sendJson(response, 404, { message: "User not found." });
  }

  const submittedOpponentScore = Math.max(0, Math.min(scored.attempted, Math.round(Number(payload.opponentScore ?? 0))));
  const opponentScore = forfeited ? Math.min(scored.attempted, Math.max(submittedOpponentScore, scored.correct + 1)) : submittedOpponentScore;
  const scoredOutcome = getActualScore(scored.correct, opponentScore);
  const actualScore = forfeited ? 0 : scoredOutcome.actualScore;
  const verdict = forfeited ? "loss" : scoredOutcome.verdict;
  const previousRating = Number.isFinite(database.users[userIndex].rating)
    ? database.users[userIndex].rating
    : DEFAULT_USER_RATING;
  const opponentRating = Number.isFinite(payload.opponentRating) ? Math.max(0, Math.round(payload.opponentRating)) : previousRating;
  const delta = mode === "bot" ? 0 : calculateEloDelta(previousRating, opponentRating, actualScore);
  const nextRating = Math.max(0, previousRating + delta);

  const updatedUser = {
    ...database.users[userIndex],
    rating: nextRating,
    correctAnswers: Math.max(
      0,
      Math.round((database.users[userIndex].correctAnswers ?? DEFAULT_CORRECT_ANSWERS) + scored.correct),
    ),
    attemptedQuestions: Math.max(
      0,
      Math.round((database.users[userIndex].attemptedQuestions ?? DEFAULT_ATTEMPTED_QUESTIONS) + scored.attempted),
    ),
  };

  const completedAt = new Date().toISOString();
  const result = {
    id: randomBytes(10).toString("hex"),
    resultKey,
    duelId: duelId || null,
    mode,
    userId: currentUser.id,
    opponentId: mode === "bot" ? null : String(payload.opponentId ?? "").trim() || null,
    verdict,
    delta,
    previousRating,
    nextRating,
    userScore: scored.correct,
    opponentScore,
    attemptedQuestions: scored.attempted,
    correctAnswers: scored.correct,
    ratingAffected: mode !== "bot",
    forfeited,
    completedAt,
  };

  database.users[userIndex] = updatedUser;
  database.duelResults = [result, ...(database.duelResults ?? []).slice(0, 499)];

  const duelIndex = (database.duels ?? []).findIndex((duel) => duel.id === duelId);
  if (duelIndex !== -1) {
    const duel = database.duels[duelIndex];
    const completedBy = new Set([...(duel.completedBy ?? []), currentUser.id]);
    database.duels[duelIndex] = {
      ...duel,
      completedBy: [...completedBy],
      lastCompletedAt: completedAt,
      status: completedBy.size >= (duel.playerIds ?? []).length ? "completed" : duel.status,
    };
  }

  await writeDatabase(database);
  return sendJson(response, 200, { result: sanitizeDuelResult(result), user: sanitizeUser(updatedUser) });
}

async function handleJoinRatedDuelQueue(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return null;

  const activeDuel = findActiveRatedDuel(database, currentUser.id);
  if (activeDuel) {
    return sendJson(response, 200, buildRatedDuelPayload(activeDuel, currentUser, database));
  }

  const existingQueueEntry = (database.duelQueue ?? []).find((entry) => entry.userId === currentUser.id);
  if (existingQueueEntry) {
    return sendJson(response, 200, {
      status: "waiting",
      ticketId: existingQueueEntry.id,
      queuedAt: existingQueueEntry.createdAt,
      waitingCount: database.duelQueue.length,
    });
  }

  const queuedOpponent = (database.duelQueue ?? [])
    .map((entry) => ({
      entry,
      user: database.users.find((user) => user.id === entry.userId),
    }))
    .filter(({ user }) => user && user.id !== currentUser.id)
    .sort(
      (left, right) =>
        Math.abs((left.user.rating ?? DEFAULT_USER_RATING) - (currentUser.rating ?? DEFAULT_USER_RATING)) -
        Math.abs((right.user.rating ?? DEFAULT_USER_RATING) - (currentUser.rating ?? DEFAULT_USER_RATING)),
    )[0];

  if (queuedOpponent?.user) {
    const now = new Date().toISOString();
    const duel = {
      id: randomBytes(10).toString("hex"),
      type: "rated",
      status: "matched",
      playerIds: [queuedOpponent.user.id, currentUser.id],
      createdAt: now,
      startedAt: now,
    };
    database.duelQueue = (database.duelQueue ?? []).filter((entry) => entry.id !== queuedOpponent.entry.id);
    database.duels = [duel, ...(database.duels ?? []).slice(0, 99)];
    await writeDatabase(database);
    return sendJson(response, 201, buildRatedDuelPayload(duel, currentUser, database));
  }

  const now = new Date().toISOString();
  const ticket = {
    id: randomBytes(10).toString("hex"),
    userId: currentUser.id,
    rating: Number.isFinite(currentUser.rating) ? currentUser.rating : DEFAULT_USER_RATING,
    createdAt: now,
  };
  database.duelQueue = [ticket, ...(database.duelQueue ?? [])];
  await writeDatabase(database);

  return sendJson(response, 202, {
    status: "waiting",
    ticketId: ticket.id,
    queuedAt: ticket.createdAt,
    waitingCount: database.duelQueue.length,
  });
}

function handleRatedDuelQueueStatus(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return null;

  const activeDuel = findActiveRatedDuel(database, currentUser.id);
  if (activeDuel) {
    return sendJson(response, 200, buildRatedDuelPayload(activeDuel, currentUser, database));
  }

  const queuedEntry = (database.duelQueue ?? []).find((entry) => entry.userId === currentUser.id);
  return sendJson(response, 200, {
    status: queuedEntry ? "waiting" : "idle",
    ticketId: queuedEntry?.id ?? null,
    queuedAt: queuedEntry?.createdAt ?? null,
    waitingCount: database.duelQueue?.length ?? 0,
  });
}

async function handleLeaveRatedDuelQueue(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return null;

  const previousLength = database.duelQueue?.length ?? 0;
  const previousDuelLength = database.duels?.length ?? 0;
  database.duelQueue = (database.duelQueue ?? []).filter((entry) => entry.userId !== currentUser.id);
  database.duels = (database.duels ?? []).filter(
    (duel) => duel.status !== "matched" || !(duel.playerIds ?? []).includes(currentUser.id),
  );
  if (database.duelQueue.length !== previousLength || database.duels.length !== previousDuelLength) {
    await writeDatabase(database);
  }

  return sendJson(response, 200, { success: true });
}

function handleSummary(response) {
  const database = readDatabase();
  const practiceLibrary = readPracticeQuestionBank();
  const attemptedQuestions = database.users.reduce(
    (total, user) => total + (Number.isFinite(user.attemptedQuestions) ? user.attemptedQuestions : 0),
    0,
  );
  const correctAnswers = database.users.reduce(
    (total, user) => total + (Number.isFinite(user.correctAnswers) ? user.correctAnswers : 0),
    0,
  );

  return sendJson(response, 200, {
    users: database.users.length,
    communities: database.communities.length,
    practiceQuestions: countPracticeQuestions(practiceLibrary),
    attemptedQuestions,
    correctAnswers,
  });
}

function handleStorageStatus(response) {
  const database = readDatabase();
  return sendJson(response, 200, {
    ...storageStatus,
    supabaseConfigured: isSupabaseEnabled,
    users: database.users.length,
    communities: database.communities.length,
    questions: database.questions.length,
  });
}

function handlePracticeQuestionBank(request, response, url) {
  const database = readDatabase();
  const library = buildPracticeLibrary(readPracticeQuestionBank(), database.questions);
  const allQuestions = [
    ...getOfficialPracticeQuestions(readPracticeQuestionBank()),
    ...database.questions.filter((question) => question.source === "ai").map((question) => normalizeQuestion(question)),
  ];

  return sendJson(response, 200, {
    ...library,
    filters: {
      exams: library.exams ?? [],
      subjects: (library.subjects ?? []).map((subject) => ({ id: subject.id, title: subject.title })),
      topics: [...new Set(allQuestions.map((question) => question.topic).filter(Boolean))].sort(),
      sources: ["official", "ai"],
    },
    questions: applyPracticeFilters(allQuestions, url),
  });
}

async function handleGenerateQuestion(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const library = readPracticeQuestionBank();
  const payload = await parseRequestBody(request);
  const generated = await requestGeminiQuestion(payload, library);
  const validationMessage = validateGeneratedQuestion(generated, library);

  if (validationMessage) {
    return sendJson(response, 422, { message: validationMessage });
  }

  const question = normalizeQuestion(
    {
      ...generated,
      id: randomBytes(12).toString("hex"),
      source: "ai",
      answer: generated.options[generated.answerIndex],
      createdAt: new Date().toISOString(),
      createdByUserId: currentUser.id,
    },
    (library.subjects ?? []).find((subject) => subject.id === generated.subjectId),
    { id: generated.examId ?? library.exam?.id ?? "neet-pg-pyqs", year: Number(generated.year) || null },
  );

  database.questions.unshift(question);
  await writeDatabase(database);

  return sendJson(response, 201, {
    question,
    message: "Supplemental AI practice question generated and stored separately from official PYQs.",
  });
}

async function handleGenerateQuestionBatch(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const library = readPracticeQuestionBank();
  const payload = await parseRequestBody(request);
  const subjectId = String(payload.subjectId ?? "").trim();
  const subject = (library.subjects ?? []).find((entry) => entry.id === subjectId);

  if (!subject) {
    return sendJson(response, 400, { message: "Choose a valid subject for AI practice." });
  }

  const targetCount = Math.min(20, Math.max(1, Math.round(Number(payload.count) || 20)));
  const existingQuestions = database.questions
    .filter((question) => question.source === "ai" && question.subjectId === subjectId)
    .map((question) => normalizeQuestion(question, subject, library.exam));

  if (existingQuestions.length >= targetCount) {
    return sendJson(response, 200, {
      questions: existingQuestions.slice(0, targetCount),
      message: `${subject.title} already has ${targetCount} supplemental AI questions.`,
    });
  }

  const neededCount = targetCount - existingQuestions.length;
  const generatedQuestions = await requestGeminiQuestionBatch(
    {
      examId: payload.examId ?? library.exam?.id ?? "neet-pg-pyqs",
      subjectId,
      subjectTitle: subject.title,
      count: neededCount,
      difficulty: payload.difficulty ?? "exam",
      topic: payload.topic ?? "High-yield review",
    },
    library,
    neededCount,
  );

  const now = new Date().toISOString();
  const normalizedQuestions = [];
  for (const generated of generatedQuestions) {
    if (String(generated.subjectId ?? "").trim() !== subjectId) {
      return sendJson(response, 422, { message: `Generated question must stay within ${subject.title}.` });
    }

    const validationMessage = validateGeneratedQuestion(generated, library);
    if (validationMessage) {
      return sendJson(response, 422, { message: validationMessage });
    }

    normalizedQuestions.push(
      normalizeQuestion(
        {
          ...generated,
          id: randomBytes(12).toString("hex"),
          source: "ai",
          answer: generated.options[generated.answerIndex],
          createdAt: now,
          createdByUserId: currentUser.id,
        },
        subject,
        { id: generated.examId ?? library.exam?.id ?? "neet-pg-pyqs", year: Number(generated.year) || null },
      ),
    );
  }

  database.questions.unshift(...normalizedQuestions);
  await writeDatabase(database);

  return sendJson(response, 201, {
    questions: [...existingQuestions, ...normalizedQuestions].slice(0, targetCount),
    message: `${subject.title} AI practice now has ${targetCount} supplemental questions.`,
  });
}

async function handleCreateCommunity(request, response) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const payload = await parseRequestBody(request);
  const name = String(payload.name ?? "").trim();
  const description = String(payload.description ?? "").trim();
  const topic = String(payload.topic ?? "").trim();

  if (!name || !description || !topic) {
    return sendJson(response, 400, { message: "Community name, topic, and description are required." });
  }

  if (database.communities.some((community) => community.name.toLowerCase() === name.toLowerCase())) {
    return sendJson(response, 409, { message: "A community with that name already exists." });
  }

  const community = {
    id: randomBytes(10).toString("hex"),
    name,
    description,
    topic,
    adminUserId: currentUser.id,
    memberIds: [currentUser.id],
    messages: [
      {
        id: randomBytes(8).toString("hex"),
        userId: null,
        userName: "MediComm Bot",
        text: `${currentUser.name} created this community. Introduce yourself and start the discussion.`,
        createdAt: new Date().toISOString(),
      },
    ],
    createdAt: new Date().toISOString(),
  };

  database.communities.unshift(community);
  await writeDatabase(database);

  return sendJson(response, 201, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

async function handleJoinCommunity(request, response, communityId) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const communityIndex = database.communities.findIndex((community) => community.id === communityId);
  if (communityIndex === -1) {
    return sendJson(response, 404, { message: "Community not found." });
  }

  const community = database.communities[communityIndex];
  if (!community.memberIds.includes(currentUser.id)) {
    community.memberIds.push(currentUser.id);
    community.messages.push({
      id: randomBytes(8).toString("hex"),
      userId: null,
      userName: "MediComm Bot",
      text: `${currentUser.name} joined the community.`,
      createdAt: new Date().toISOString(),
    });
    database.communities[communityIndex] = community;
    await writeDatabase(database);
  }

  return sendJson(response, 200, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

async function handleSendCommunityMessage(request, response, communityId) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const communityIndex = database.communities.findIndex((community) => community.id === communityId);
  if (communityIndex === -1) {
    return sendJson(response, 404, { message: "Community not found." });
  }

  const community = database.communities[communityIndex];
  if (!community.memberIds.includes(currentUser.id)) {
    return sendJson(response, 403, { message: "Join the community before sending messages." });
  }

  const payload = await parseRequestBody(request);
  const text = String(payload.text ?? "").trim();
  if (!text) {
    return sendJson(response, 400, { message: "Message cannot be empty." });
  }

  community.messages.push({
    id: randomBytes(8).toString("hex"),
    userId: currentUser.id,
    userName: currentUser.name,
    text,
    createdAt: new Date().toISOString(),
  });

  database.communities[communityIndex] = community;
  await writeDatabase(database);

  return sendJson(response, 200, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

async function handleRemoveCommunityMember(request, response, communityId, memberId) {
  const database = readDatabase();
  const currentUser = requireSessionUser(request, response, database);
  if (!currentUser) return;

  const communityIndex = database.communities.findIndex((community) => community.id === communityId);
  if (communityIndex === -1) {
    return sendJson(response, 404, { message: "Community not found." });
  }

  const community = database.communities[communityIndex];
  if (community.adminUserId !== currentUser.id) {
    return sendJson(response, 403, { message: "Only the community admin can remove members." });
  }

  if (memberId === currentUser.id) {
    return sendJson(response, 400, { message: "The admin cannot remove themselves from the community." });
  }

  if (!community.memberIds.includes(memberId)) {
    return sendJson(response, 404, { message: "That member is not in this community." });
  }

  community.memberIds = community.memberIds.filter((id) => id !== memberId);
  const removedUser = database.users.find((user) => user.id === memberId);
  community.messages.push({
    id: randomBytes(8).toString("hex"),
    userId: null,
    userName: "MediComm Bot",
    text: `${removedUser?.name ?? "A member"} was removed by the admin.`,
    createdAt: new Date().toISOString(),
  });
  database.communities[communityIndex] = community;
  await writeDatabase(database);

  return sendJson(response, 200, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

async function handleRequest(request, response) {
  response.setHeader("Access-Control-Allow-Origin", "*");
  response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  response.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS");

  if (request.method === "OPTIONS") {
    response.writeHead(204);
    response.end();
    return;
  }

  const requestHost = request.headers.host ?? `${host}:${port}`;
  const url = new URL(request.url, `http://${requestHost}`);

  if (request.method === "GET" && url.pathname.startsWith("/uploads/")) {
    const requestedFile = path.basename(url.pathname);
    const filePath = path.join(uploadsDir, requestedFile);

    if (!existsSync(filePath)) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    const extension = path.extname(filePath).toLowerCase();
    const mimeType =
      extension === ".png"
        ? "image/png"
        : extension === ".jpg" || extension === ".jpeg"
          ? "image/jpeg"
          : extension === ".webp"
            ? "image/webp"
            : extension === ".gif"
              ? "image/gif"
              : "application/octet-stream";

    response.writeHead(200, { "Content-Type": mimeType });
    response.end(readFileSync(filePath));
    return;
  }

  try {
    if (request.method === "POST" && url.pathname === "/api/auth/signup") return await handleSignup(request, response);
    if (request.method === "POST" && url.pathname === "/api/auth/login") return await handleLogin(request, response);
    if (request.method === "GET" && url.pathname === "/api/auth/session") return handleSession(request, response);
    if (request.method === "POST" && url.pathname === "/api/auth/logout") return handleLogout(request, response);
    if (request.method === "PATCH" && url.pathname === "/api/profile") return await handleProfileUpdate(request, response);
    if (request.method === "PATCH" && url.pathname === "/api/profile/stats") return await handleProfileStatsUpdate(request, response);
    if (request.method === "GET" && url.pathname === "/api/leaderboard") return handleLeaderboard(request, response);
    if (request.method === "GET" && url.pathname === "/api/duels/questions") return handleDuelQuestions(request, response, url);
    if (request.method === "POST" && url.pathname === "/api/duels/complete") return await handleCompleteDuel(request, response);
    if (request.method === "POST" && url.pathname === "/api/duels/rated/queue") return await handleJoinRatedDuelQueue(request, response);
    if (request.method === "GET" && url.pathname === "/api/duels/rated/queue") return handleRatedDuelQueueStatus(request, response);
    if (request.method === "DELETE" && url.pathname === "/api/duels/rated/queue") return await handleLeaveRatedDuelQueue(request, response);
    if (request.method === "GET" && url.pathname === "/api/summary") return handleSummary(response);
    if (request.method === "GET" && url.pathname === "/api/storage/status") return handleStorageStatus(response);
    if (request.method === "GET" && url.pathname === "/api/practice") return handlePracticeQuestionBank(request, response, url);
    if (request.method === "POST" && url.pathname === "/api/generate-question") return await handleGenerateQuestion(request, response);
    if (request.method === "POST" && url.pathname === "/api/generate-questions") return await handleGenerateQuestionBatch(request, response);
    if (request.method === "GET" && url.pathname === "/api/users/search") return handleUserSearch(request, response, url);
    if (request.method === "GET" && url.pathname === "/api/direct-messages") return handleDirectConversationsList(request, response);
    if (request.method === "POST" && url.pathname === "/api/direct-messages/open")
      return await handleOpenDirectConversation(request, response);

    const publicUserMatch = url.pathname.match(/^\/api\/users\/([^/]+)$/);
    if (request.method === "GET" && publicUserMatch) {
      return await handlePublicUserProfile(request, response, publicUserMatch[1]);
    }
    if (request.method === "GET" && url.pathname === "/api/communities") return handleCommunitiesList(request, response);
    if (request.method === "POST" && url.pathname === "/api/communities") return await handleCreateCommunity(request, response);

    const joinMatch = url.pathname.match(/^\/api\/communities\/([^/]+)\/join$/);
    if (request.method === "POST" && joinMatch) {
      return handleJoinCommunity(request, response, joinMatch[1]);
    }

    const messagesMatch = url.pathname.match(/^\/api\/communities\/([^/]+)\/messages$/);
    if (request.method === "POST" && messagesMatch) {
      return await handleSendCommunityMessage(request, response, messagesMatch[1]);
    }

    const removeMemberMatch = url.pathname.match(/^\/api\/communities\/([^/]+)\/members\/([^/]+)$/);
    if (request.method === "DELETE" && removeMemberMatch) {
      return handleRemoveCommunityMember(request, response, removeMemberMatch[1], removeMemberMatch[2]);
    }

    const directMessageMatch = url.pathname.match(/^\/api\/direct-messages\/([^/]+)\/messages$/);
    if (request.method === "POST" && directMessageMatch) {
      return await handleSendDirectMessage(request, response, directMessageMatch[1]);
    }

    if (url.pathname.startsWith("/api/")) {
      sendJson(response, 404, { message: "Route not found." });
      return;
    }

    if (request.method === "GET" || request.method === "HEAD") {
      return await serveStaticFile(response, url.pathname === "/" ? "/index.html" : url.pathname);
    }

    sendJson(response, 404, { message: "Route not found." });
  } catch (error) {
    sendJson(response, 500, { message: error instanceof Error ? error.message : "Unexpected server error." });
  }
}

await initializeDatabaseStore();

createServer(handleRequest).listen(port, host, () => {
  console.log(`MediComm listening on http://${host}:${port}`);
});
