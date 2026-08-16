import { useEffect, useMemo, useState } from "react";
import { AppShell } from "./components/AppShellV2";
import { apiRequest } from "./lib/api";
import { SESSION_TOKEN_KEY, THEME_STORAGE_KEY } from "./lib/clientStorage";

const PRACTICE_LIBRARY_URL = "/api/practice";
const PRACTICE_LIBRARY_CACHE_KEY = "medicomm-practice-library-cache";
const PRACTICE_PROGRESS_STORAGE_KEY = "medicomm-practice-progress";
const ANALYTICS_EVENTS_STORAGE_KEY = "medicomm-analytics-events";
const COMMUNITY_THREAD_WORD_LIMIT = 300;
const COMMUNITY_THREAD_IMAGE_LIMIT_BYTES = 5 * 1024 * 1024;
// Atlas artwork was replaced in place, so use a versioned URL to ensure clients
// don't keep showing a previously cached source image.
const ATLAS_IMAGE_VERSION = "20260626";

const directoryOrder = (value) => Number.isFinite(Number(value)) ? Number(value) : Number.MAX_SAFE_INTEGER;

const PATHOLOGY_CHAPTER_ORDER = new Map([
  "The Cell as a Unit of Health and Disease",
  "Cell Injury, Cell Death, and Adaptations",
  "Inflammation and Repair",
  "Hemodynamic Disorders, Thromboembolic Disease, and Shock",
  "Genetic Disorders",
  "Diseases of the Immune System",
  "Neoplasia",
  "Infectious Diseases",
  "Environmental and Nutritional Diseases",
  "Diseases of Infancy and Childhood",
  "Blood Vessels",
  "The Heart",
  "Diseases of White Blood Cells, Lymph Nodes, Spleen, and Thymus",
  "Red Blood Cell and Bleeding Disorders",
  "The Lung",
  "Head and Neck",
  "The Gastrointestinal Tract",
  "Liver and Gallbladder",
  "The Pancreas",
  "The Kidney",
  "The Lower Urinary Tract and Male Genital System",
  "The Female Genital Tract",
  "The Breast",
  "The Endocrine System",
  "The Skin",
  "Bones, Joints, and Soft Tissue Tumors",
  "Peripheral Nerves and Skeletal Muscles",
  "The Central Nervous System",
  "The Eye",
].map((title, index) => [title, index + 1]));

function getPracticeChapterOrder(question, subjectId) {
  if (subjectId === "pathology") {
    return PATHOLOGY_CHAPTER_ORDER.get(question.chapterTitle) ?? directoryOrder(question.chapterOrder);
  }
  return directoryOrder(question.chapterOrder);
}

const comparePracticeDirectoryEntries = (left, right) => {
  const orderDifference = directoryOrder(left.order) - directoryOrder(right.order);
  if (orderDifference !== 0) return orderDifference;
  return String(left.title ?? left.topic ?? "").localeCompare(String(right.title ?? right.topic ?? ""));
};

const features = [
  {
    icon: "STK",
    title: "Streak-Based Learning",
    text: "Build daily habits and maintain your learning streak. The longer your streak, the more you learn and earn.",
    tint: "blue",
  },
  {
    icon: "LDB",
    title: "Competitive Leaderboards",
    text: "Compete with peers globally and locally. See where you stand and push yourself to the top.",
    tint: "green",
  },
  {
    icon: "COM",
    title: "Join Communities",
    text: "Connect with specialists in your field. Share knowledge and learn from the best.",
    tint: "purple",
  },
  {
    icon: "AIM",
    title: "Targeted Practice",
    text: "Focus on specific medical specialties or weak areas. Our AI adapts to your learning needs.",
    tint: "orange",
  },
  {
    icon: "TRK",
    title: "Track Progress",
    text: "Detailed analytics on your performance. Know your strengths and areas for improvement.",
    tint: "pink",
  },
  {
    icon: "CRT",
    title: "Expert-Curated Content",
    text: "Questions reviewed by medical professionals. Always accurate, relevant, and up-to-date.",
    tint: "cyan",
  },
];

const navItems = ["Home", "Dashboard", "Practice", "Analytics", "Leaderboard", "Communities", "Compete", "Pricing", "Profile", "Settings"];

const medicalCollegeSuggestions = [
  "AIIMS Delhi",
  "Armed Forces Medical College, Pune",
  "B. J. Medical College, Ahmedabad",
  "Bangalore Medical College and Research Institute",
  "Banaras Hindu University Institute of Medical Sciences",
  "Christian Medical College, Vellore",
  "Government Medical College, Amritsar",
  "Government Medical College, Srinagar",
  "Grant Medical College, Mumbai",
  "Indira Gandhi Medical College, Shimla",
  "Jawaharlal Institute of Postgraduate Medical Education and Research",
  "JNIMS, Imphal",
  "King George's Medical University, Lucknow",
  "Lady Hardinge Medical College, New Delhi",
  "Madras Medical College, Chennai",
  "Maulana Azad Medical College, New Delhi",
  "Mysore Medical College and Research Institute",
  "NEIGRIHMS, Shillong",
  "Osmania Medical College, Hyderabad",
  "Patna Medical College",
  "Pt. B. D. Sharma PGIMS, Rohtak",
  "RIMS, Ranchi",
  "SCB Medical College, Cuttack",
  "SMS Medical College, Jaipur",
  "Sikkim Manipal Institute of Medical Sciences",
  "Stanley Medical College, Chennai",
  "Topiwala National Medical College, Mumbai",
  "VMMC and Safdarjung Hospital, New Delhi",
].sort((left, right) => left.localeCompare(right));

const duelOpponents = [
  { name: "Ava Patel", rating: 1538, specialty: "Cardiology" },
  { name: "Noah Chen", rating: 1464, specialty: "Emergency Medicine" },
  { name: "Maya Singh", rating: 1506, specialty: "Neurology" },
  { name: "Liam Carter", rating: 1588, specialty: "Surgery" },
];

const emptyPracticeLibrary = {
  exam: {
    id: "neet-pg-pyqs",
    title: "NEET PG PYQs",
    questionCount: 0,
  },
  years: [],
  subjects: [],
};

function normalizePracticeLibrary(data) {
  return {
    exam: data?.exam ?? emptyPracticeLibrary.exam,
    years: data?.years ?? [],
    subjects: data?.subjects ?? [],
    aiSubjects: data?.aiSubjects ?? [],
  };
}

function readCachedPracticeLibrary() {
  if (typeof window === "undefined") return null;
  try {
    const cached = JSON.parse(localStorage.getItem(PRACTICE_LIBRARY_CACHE_KEY) || "null");
    if (!cached || !Array.isArray(cached.subjects)) return null;
    return normalizePracticeLibrary(cached);
  } catch {
    return null;
  }
}

function writeCachedPracticeLibrary(library) {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(PRACTICE_LIBRARY_CACHE_KEY, JSON.stringify(library));
  } catch {
    // The live response is still usable when browser storage is full or unavailable.
  }
}

const fallbackDuelQuestions = [
  {
    id: "clinical-fallback-1",
    prompt: "Which cranial nerve is primarily responsible for lateral eye movement?",
    options: ["Oculomotor", "Trochlear", "Abducens", "Optic"],
  },
  {
    id: "clinical-fallback-2",
    prompt: "A patient with diabetic ketoacidosis is expected to have which acid-base disturbance?",
    options: ["Metabolic acidosis", "Metabolic alkalosis", "Respiratory acidosis", "Respiratory alkalosis"],
  },
  {
    id: "clinical-fallback-3",
    prompt: "Which valve is most commonly affected in infective endocarditis among IV drug users?",
    options: ["Mitral", "Aortic", "Pulmonic", "Tricuspid"],
  },
  {
    id: "clinical-fallback-4",
    prompt: "The antidote for acetaminophen overdose is:",
    options: ["Naloxone", "Atropine", "N-acetylcysteine", "Flumazenil"],
  },
  {
    id: "clinical-fallback-5",
    prompt: "Which nephron segment is primarily responsible for fine sodium regulation under aldosterone?",
    options: ["Proximal tubule", "Loop of Henle", "Distal convoluted tubule", "Collecting duct"],
  },
];

const DUEL_DURATION_SECONDS = 180;

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function createOpponentTimeline(opponentRating, questions = fallbackDuelQuestions) {
  return questions.map((question, index) => {
    const progressSeconds = 24 + index * 26 + (opponentRating % 11);
    const skillGate = (opponentRating + index * 37) % 100;
    const targetAccuracy = Math.min(86, Math.max(52, 58 + Math.round((opponentRating - 1400) / 6)));
    return {
      revealAt: Math.min(progressSeconds, DUEL_DURATION_SECONDS - 6),
      correct: skillGate < targetAccuracy,
      answer: question.answer,
    };
  });
}

function normalizeAnswerValue(value) {
  return String(value ?? "").trim().replace(/\s+/g, " ").toLowerCase();
}

function isAnswerCorrect(question, selectedAnswer) {
  if (!question || !selectedAnswer) return false;
  const selected = normalizeAnswerValue(selectedAnswer);
  const answer = normalizeAnswerValue(question.answer);
  if (selected && answer && selected === answer) return true;

  const answerIndex = Number(question.answerIndex);
  if (Number.isInteger(answerIndex) && answerIndex >= 0) {
    return selected === normalizeAnswerValue(question.options?.[answerIndex]);
  }

  return false;
}

function getDuelOpponentSnapshot(timeline, elapsedSeconds) {
  const answeredSteps = timeline.filter((step) => step.revealAt <= elapsedSeconds);
  return {
    answered: answeredSteps.length,
    correct: answeredSteps.filter((step) => step.correct).length,
  };
}

function getPracticeImageUrl(imageUrl) {
  if (!imageUrl?.includes("/medicomm-atlas-")) return imageUrl;
  const separator = imageUrl.includes("?") ? "&" : "?";
  return `${imageUrl}${separator}v=${ATLAS_IMAGE_VERSION}`;
}

function getQuestionImageUrls(question) {
  return [
    ...(Array.isArray(question?.imageUrls) ? question.imageUrls : []),
    ...(Array.isArray(question?.images) ? question.images : []),
    question?.imageUrl,
    question?.image,
  ]
    .map((imageUrl) => String(imageUrl ?? "").trim())
    .filter(Boolean)
    .filter((imageUrl, index, list) => list.indexOf(imageUrl) === index);
}

function getSeededClientRank(value) {
  let hash = 2166136261;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function formatDuration(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function pickOpponent(playerRating) {
  return [...duelOpponents].sort(
    (left, right) => Math.abs(left.rating - playerRating) - Math.abs(right.rating - playerRating),
  )[0];
}

function getInitials(name) {
  return String(name ?? "")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("") || "MQ";
}

function createProfileState(user) {
  return {
    name: user?.name ?? "",
    medicalCollege: user?.medicalCollege ?? "",
    contactNumber: user?.contactNumber ?? "",
    profileImageDataUrl: "",
  };
}

function calculateAccuracy(correctAnswers, attemptedQuestions) {
  if (!attemptedQuestions) return 0;
  return Math.round((correctAnswers / attemptedQuestions) * 100);
}

function countWords(value) {
  const normalized = String(value ?? "").trim();
  return normalized ? normalized.split(/\s+/).length : 0;
}

function formatStatValue(value) {
  return Number.isFinite(value) ? value.toLocaleString("en-IN") : "0";
}

function getPracticeProgressStorageKey(user) {
  const userKey = user?.id ?? user?.email ?? "guest";
  return `${PRACTICE_PROGRESS_STORAGE_KEY}:${userKey}`;
}

function readPracticeProgress(user) {
  if (typeof window === "undefined") return {};

  try {
    const rawProgress = localStorage.getItem(getPracticeProgressStorageKey(user));
    const parsedProgress = rawProgress ? JSON.parse(rawProgress) : {};
    return parsedProgress && typeof parsedProgress === "object" && !Array.isArray(parsedProgress) ? parsedProgress : {};
  } catch {
    return {};
  }
}

function writePracticeProgress(user, progress) {
  if (typeof window === "undefined") return;
  localStorage.setItem(getPracticeProgressStorageKey(user), JSON.stringify(progress));
}

function scrollPracticeViewToTop() {
  if (typeof window === "undefined") return;
  window.requestAnimationFrame(() => {
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
    document.getElementById("main-content")?.scrollTo?.({ top: 0, left: 0, behavior: "auto" });
  });
}

function getAnalyticsStorageKey(user) {
  const userKey = user?.id ?? user?.email ?? "guest";
  return `${ANALYTICS_EVENTS_STORAGE_KEY}:${userKey}`;
}

function readAnalyticsEvents(user, progress = {}) {
  if (typeof window === "undefined") return [];
  try {
    const parsed = JSON.parse(localStorage.getItem(getAnalyticsStorageKey(user)) || "[]");
    if (Array.isArray(parsed) && parsed.length) return parsed;
  } catch {
    // Fall through to the legacy progress migration below.
  }
  return Object.entries(progress).map(([questionId, item]) => ({
    id: `legacy-${questionId}`,
    questionId,
    answeredAt: item.answeredAt,
    correct: item.correct === true,
    subjectId: item.subjectId || "unknown",
    topic: "General review",
    activity: "pyq",
    durationSeconds: 0,
  }));
}

function writeAnalyticsEvents(user, events) {
  if (typeof window === "undefined") return;
  localStorage.setItem(getAnalyticsStorageKey(user), JSON.stringify(events.slice(-2000)));
}

function getQuestionYearKey(question) {
  return Number.isFinite(question?.year) ? String(question.year) : "unknown";
}

function getYearSetTitle(yearKey) {
  return yearKey === "unknown" ? "Unsorted PYQs" : `${yearKey} PYQs`;
}

function formatExplanationText(value) {
  const text = String(value ?? "").trim();
  if (!text) return "";

  const letters = text.match(/[A-Za-z]/g) ?? [];
  if (!letters.length) return text;

  const uppercaseLetters = letters.filter((letter) => letter === letter.toUpperCase()).length;
  if (uppercaseLetters / letters.length < 0.82) return text;

  return text
    .toLowerCase()
    .replace(/(^|[.!?]\s+)([a-z])/g, (match, prefix, letter) => `${prefix}${letter.toUpperCase()}`)
    .replace(/\b(mcq|neet|pg|aiims|inicet|ini-cet|dna|rna|ct|mri|ecg|hiv|hbv|hcv|tb|cns|csf|iv|im|igg|igm|ige|iga)\b/gi, (match) =>
      match.toUpperCase(),
    );
}

function buildSubjectYearSets(subject, progress = {}) {
  const groups = new Map();

  for (const question of subject?.questions ?? []) {
    const yearKey = getQuestionYearKey(question);
    const group = groups.get(yearKey) ?? {
      id: yearKey,
      year: Number.isFinite(question.year) ? question.year : null,
      title: getYearSetTitle(yearKey),
      examTitles: new Set(),
      questions: [],
    };
    if (question.examTitle) group.examTitles.add(question.examTitle);
    group.questions.push(question);
    groups.set(yearKey, group);
  }

  return [...groups.values()]
    .map((group) => {
      const answered = group.questions.filter((question) => progress[question.id]).length;
      const total = group.questions.length;
      return {
        ...group,
        examTitles: [...group.examTitles],
        answered,
        total,
        progressPercent: total ? Math.round((answered / total) * 100) : 0,
      };
    })
    .sort((left, right) => {
      if (left.year === null && right.year === null) return left.title.localeCompare(right.title);
      if (left.year === null) return 1;
      if (right.year === null) return -1;
      return right.year - left.year;
    });
}

function getCommunityInviteUrl(communityId) {
  if (typeof window === "undefined" || !communityId) return "";
  const url = new URL(window.location.origin);
  url.searchParams.set("community", communityId);
  return url.toString();
}

function mergeUserPerformance(user) {
  return user;
}

function formatCommunityTimestamp(value) {
  if (!value) return "";

  return new Date(value).toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function getInitialTheme() {
  if (typeof window === "undefined") return "light";

  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function App() {
  const [theme, setTheme] = useState(getInitialTheme);
  const [activeView, setActiveView] = useState("Home");
  const [selectedOption, setSelectedOption] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [answerConfidence, setAnswerConfidence] = useState("");
  const [flaggedQuestions, setFlaggedQuestions] = useState({});
  const [practiceLibrary, setPracticeLibrary] = useState(emptyPracticeLibrary);
  const [practiceLibraryStatus, setPracticeLibraryStatus] = useState("idle");
  const [practiceLibraryMessage, setPracticeLibraryMessage] = useState("");
  const [aiPracticeBusy, setAiPracticeBusy] = useState(false);
  const [aiPracticeMessage, setAiPracticeMessage] = useState("");
  const [selectedPracticeSubjectId, setSelectedPracticeSubjectId] = useState("");
  const [selectedPracticeMode, setSelectedPracticeMode] = useState("pyq");
  const [selectedPracticeExamYear, setSelectedPracticeExamYear] = useState("");
  const [selectedPracticeTopic, setSelectedPracticeTopic] = useState("");
  const [selectedPracticeChapter, setSelectedPracticeChapter] = useState("");
  const [practiceChoiceSubjectId, setPracticeChoiceSubjectId] = useState("");
  const [practiceQuestionIndex, setPracticeQuestionIndex] = useState(0);
  const [practiceStage, setPracticeStage] = useState("catalog");
  const [practiceProgress, setPracticeProgress] = useState({});
  const [analyticsEvents, setAnalyticsEvents] = useState([]);
  const [analyticsPeriod, setAnalyticsPeriod] = useState(30);
  const [practiceQuestionStartedAt, setPracticeQuestionStartedAt] = useState(Date.now());
  const [userRating, setUserRating] = useState(1480);
  const [duelStatus, setDuelStatus] = useState("idle");
  const [duelQuestions, setDuelQuestions] = useState(fallbackDuelQuestions);
  const [duelMode, setDuelMode] = useState("rated");
  const [duelSessionId, setDuelSessionId] = useState("");
  const [duelOpponent, setDuelOpponent] = useState(null);
  const [duelTimeLeft, setDuelTimeLeft] = useState(DUEL_DURATION_SECONDS);
  const [duelIndex, setDuelIndex] = useState(0);
  const [duelSelections, setDuelSelections] = useState({});
  const [duelSubmitted, setDuelSubmitted] = useState({});
  const [duelOpponentTimeline, setDuelOpponentTimeline] = useState([]);
  const [duelOpponentProgress, setDuelOpponentProgress] = useState({ answered: 0, correct: 0 });
  const [duelResult, setDuelResult] = useState(null);
  const [duelQueueInfo, setDuelQueueInfo] = useState(null);
  const [duelMessage, setDuelMessage] = useState("");
  const [duelForfeited, setDuelForfeited] = useState(false);
  const [selectedLeaderboardState, setSelectedLeaderboardState] = useState("");
  const [stateSearchTerm, setStateSearchTerm] = useState("");
  const [authStatus, setAuthStatus] = useState("loading");
  const [authMode, setAuthMode] = useState("login");
  const [authBusy, setAuthBusy] = useState(false);
  const [authMessage, setAuthMessage] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [user, setUser] = useState(null);
  const [profileState, setProfileState] = useState(createProfileState(null));
  const [profileBusy, setProfileBusy] = useState(false);
  const [profileMessage, setProfileMessage] = useState("");
  const [publicProfile, setPublicProfile] = useState(null);
  const [publicProfileBusy, setPublicProfileBusy] = useState(false);
  const [publicProfileMessage, setPublicProfileMessage] = useState("");
  const [publicProfileReturnView, setPublicProfileReturnView] = useState("Communities");
  const [leaderboardPlayers, setLeaderboardPlayers] = useState([]);
  const [platformSummary, setPlatformSummary] = useState({
    users: 0,
    communities: 0,
    practiceQuestions: 0,
    attemptedQuestions: 0,
    correctAnswers: 0,
  });
  const [communities, setCommunities] = useState([]);
  const [communitiesBusy, setCommunitiesBusy] = useState(false);
  const [communitiesMessage, setCommunitiesMessage] = useState("");
  const [selectedCommunityId, setSelectedCommunityId] = useState("");
  const [communityStage, setCommunityStage] = useState("hub");
  const [communityMessageDraft, setCommunityMessageDraft] = useState("");
  const [communityThreadImage, setCommunityThreadImage] = useState(null);
  const [communityReplyDrafts, setCommunityReplyDrafts] = useState({});
  const [expandedCommunityThreads, setExpandedCommunityThreads] = useState({});
  const [directConversations, setDirectConversations] = useState([]);
  const [directMessagesBusy, setDirectMessagesBusy] = useState(false);
  const [directMessagesMessage, setDirectMessagesMessage] = useState("");
  const [selectedDirectConversationId, setSelectedDirectConversationId] = useState("");
  const [directMessageDraft, setDirectMessageDraft] = useState("");
  const [directSearchTerm, setDirectSearchTerm] = useState("");
  const [directSearchResults, setDirectSearchResults] = useState([]);
  const [directSearchBusy, setDirectSearchBusy] = useState(false);
  const [createCommunityForm, setCreateCommunityForm] = useState({
    name: "",
    topic: "",
    description: "",
  });
  const [authForm, setAuthForm] = useState({
    name: "",
    email: "",
    medicalCollege: "",
    contactNumber: "",
    password: "",
  });

  const practiceSubjects = practiceLibrary.subjects ?? [];
  const aiPracticeSubjects = practiceLibrary.aiSubjects ?? [];
  const aiPracticeQuestionCountsBySubject = useMemo(
    () =>
      Object.fromEntries(
        aiPracticeSubjects.map((subject) => [subject.id, subject.questions?.length ?? 0]),
      ),
    [aiPracticeSubjects],
  );
  const practiceYears = practiceLibrary.years ?? [];
  const activePracticeSubjects = selectedPracticeMode === "ai" ? aiPracticeSubjects : practiceSubjects;
  const currentPracticeSubject =
    activePracticeSubjects.find((subject) => subject.id === selectedPracticeSubjectId) ??
    activePracticeSubjects[0] ??
    null;
  const currentPracticeYearSets = useMemo(
    () => buildSubjectYearSets(currentPracticeSubject, practiceProgress),
    [currentPracticeSubject, practiceProgress],
  );
  const currentPracticeQuestionSet =
    selectedPracticeMode === "pyq" && selectedPracticeExamYear
      ? currentPracticeYearSets.find((yearSet) => yearSet.id === selectedPracticeExamYear) ?? null
      : null;
  const currentPracticeQuestions =
    selectedPracticeMode === "ai" && selectedPracticeTopic
      ? (currentPracticeSubject?.questions ?? []).filter((question) => question.topic === selectedPracticeTopic)
      : currentPracticeQuestionSet?.questions ?? currentPracticeSubject?.questions ?? [];
  const currentPracticeQuestion = currentPracticeQuestions[practiceQuestionIndex] ?? null;
  const practiceChoiceSubject =
    practiceSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    null;
  const practiceChoiceYearSets = useMemo(
    () => buildSubjectYearSets(practiceChoiceSubject, practiceProgress),
    [practiceChoiceSubject, practiceProgress],
  );
  const currentAiPracticeSubject = aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ?? null;
  const practiceChoiceAiQuestionCount = currentAiPracticeSubject?.questions?.length ?? 0;
  const groupedPracticeYears = practiceYears.map((year) => ({
    ...year,
    subjects: year.subjectIds
      .map((subjectId) => practiceSubjects.find((subject) => subject.id === subjectId))
      .filter(Boolean),
  }));
  const groupedPracticeSubjectIds = new Set(groupedPracticeYears.flatMap((year) => year.subjects.map((subject) => subject.id)));
  const supplementalAiPracticeSubjects = aiPracticeSubjects
    .filter((subject) => !groupedPracticeSubjectIds.has(subject.id))
    .sort((a, b) => a.title.localeCompare(b.title));
  const activePracticeYear =
    groupedPracticeYears.find((year) => year.subjects.some((subject) => subject.id === selectedPracticeSubjectId)) ?? null;
  const isCorrect = submitted && currentPracticeQuestion ? selectedOption === currentPracticeQuestion.answer : false;
  const currentDuelQuestion = duelQuestions[duelIndex];
  const currentDuelSelection = duelSelections[duelIndex] ?? "";
  const currentDuelSubmitted = Boolean(duelSubmitted[duelIndex]);
  const isDarkMode = theme === "dark";

  const userDuelScore = useMemo(
    () =>
      duelQuestions.reduce((total, question, index) => {
        if (!duelSubmitted[index]) return total;
        return total + (isAnswerCorrect(question, duelSelections[index]) ? 1 : 0);
      }, 0),
    [duelQuestions, duelSelections, duelSubmitted],
  );
  const userDuelAnswered = Object.keys(duelSubmitted).length;

  const attemptedQuestions = user?.attemptedQuestions ?? 0;
  const correctAnswers = user?.correctAnswers ?? 0;
  const accuracyRate = calculateAccuracy(correctAnswers, attemptedQuestions);

  const quickStats = useMemo(
    () => ({
      questionsToday: attemptedQuestions,
      timeSpent: "1h 18m",
      weakArea: `${correctAnswers} correct overall`,
    }),
    [attemptedQuestions, correctAnswers],
  );

  const homeStats = useMemo(
    () => [
      { icon: "MCQ", value: formatStatValue(platformSummary.practiceQuestions), label: "Medical MCQs", tint: "blue" },
      { icon: "ACT", value: formatStatValue(platformSummary.users), label: "Registered learners", tint: "green" },
      { icon: "HUB", value: formatStatValue(platformSummary.communities), label: "Communities", tint: "purple" },
    ],
    [platformSummary],
  );

  const activityFeed = useMemo(
    () => [
      {
        title: "Questions attempted",
        detail: `${formatStatValue(platformSummary.attemptedQuestions)} total attempts across learners`,
        time: "Live",
      },
      {
        title: "Correct answers",
        detail: `${formatStatValue(platformSummary.correctAnswers)} answers solved correctly`,
        time: "Live",
      },
      {
        title: "Community rooms",
        detail: `${formatStatValue(platformSummary.communities)} active user-created groups`,
        time: "Live",
      },
    ],
    [platformSummary],
  );

  const liveLeaderboard = useMemo(() => {
    return [...leaderboardPlayers]
      .sort((left, right) => right.score - left.score)
      .map((player, index) => ({ ...player, rank: index + 1 }));
  }, [leaderboardPlayers]);

  const stateLeaderboard = useMemo(() => {
    const grouped = liveLeaderboard.reduce((accumulator, player) => {
      const existing = accumulator[player.state] ?? [];
      accumulator[player.state] = [...existing, player];
      return accumulator;
    }, {});

    return Object.entries(grouped)
      .map(([state, players]) => ({
        state,
        players: players.sort((left, right) => right.score - left.score),
      }))
      .sort((left, right) => right.players[0].score - left.players[0].score);
  }, [liveLeaderboard]);

  const selectedStateEntry =
    stateLeaderboard.find((entry) => entry.state === selectedLeaderboardState) ?? stateLeaderboard[0];

  const filteredStateLeaderboard = useMemo(() => {
    const normalizedQuery = stateSearchTerm.trim().toLowerCase();
    if (!normalizedQuery) return stateLeaderboard;
    return stateLeaderboard.filter((entry) => entry.state.toLowerCase().includes(normalizedQuery));
  }, [stateLeaderboard, stateSearchTerm]);

  const currentUserLeaderboardEntry = useMemo(
    () => liveLeaderboard.find((entry) => entry.isCurrentUser) ?? null,
    [liveLeaderboard],
  );

  const currentUserStateEntry = useMemo(() => {
    if (!currentUserLeaderboardEntry) return null;
    return stateLeaderboard.find((entry) => entry.state === currentUserLeaderboardEntry.state) ?? null;
  }, [currentUserLeaderboardEntry, stateLeaderboard]);

  const currentUserStateRank = useMemo(() => {
    if (!currentUserStateEntry || !currentUserLeaderboardEntry) return null;
    return currentUserStateEntry.players.findIndex((player) => player.id === currentUserLeaderboardEntry.id) + 1;
  }, [currentUserStateEntry, currentUserLeaderboardEntry]);

  const summaryCards = useMemo(
    () => [
      { label: "Current streak", value: `${user?.streak ?? 1} days`, accent: "blue" },
      { label: "Accuracy rate", value: `${accuracyRate}%`, accent: "green" },
      { label: "Attempted questions", value: attemptedQuestions, accent: "cyan" },
      { label: "Correct answers", value: correctAnswers, accent: "orange" },
      {
        label: "Rank this week",
        value: `#${currentUserLeaderboardEntry?.rank ?? "-"}`,
        accent: "purple",
      },
    ],
    [accuracyRate, attemptedQuestions, correctAnswers, currentUserLeaderboardEntry, user],
  );

  const selectedCommunity =
    communities.find((community) => community.id === selectedCommunityId) ?? communities[0] ?? null;
  const selectedDirectConversation =
    directConversations.find((conversation) => conversation.id === selectedDirectConversationId) ??
    directConversations[0] ??
    null;

  async function fetchLeaderboard() {
    try {
      const data = await apiRequest("/api/leaderboard");
      setLeaderboardPlayers(data.players ?? []);
    } catch {
      setLeaderboardPlayers([]);
    }
  }

  async function fetchPlatformSummary() {
    try {
      const data = await apiRequest("/api/summary");
      setPlatformSummary({
        users: data.users ?? 0,
        communities: data.communities ?? 0,
        practiceQuestions: data.practiceQuestions ?? 0,
        attemptedQuestions: data.attemptedQuestions ?? 0,
        correctAnswers: data.correctAnswers ?? 0,
      });
    } catch {
      setPlatformSummary((current) => current);
    }
  }

async function fetchPracticeLibrary() {
  const cachedLibrary = readCachedPracticeLibrary();
  if (cachedLibrary?.subjects?.length) {
    setPracticeLibrary(cachedLibrary);
    setSelectedPracticeSubjectId((current) => {
      const hasCurrentSubject = [...cachedLibrary.subjects, ...(cachedLibrary.aiSubjects ?? [])].some((subject) => subject.id === current);
      return hasCurrentSubject ? current : cachedLibrary.subjects[0]?.id ?? cachedLibrary.aiSubjects?.[0]?.id ?? "";
    });
    setPracticeLibraryStatus("ready");
    setPracticeLibraryMessage("Showing saved questions while refreshing the library.");
  } else {
    setPracticeLibraryStatus("loading");
  }

  let lastError = null;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 45000);
    try {
      if (attempt > 0) {
        await new Promise((resolve) => window.setTimeout(resolve, 900 * attempt));
      }

      const response = await fetch(PRACTICE_LIBRARY_URL, {
        cache: "default",
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error("Could not load practice questions.");
      }

      const nextLibrary = normalizePracticeLibrary(await response.json());
      setPracticeLibrary(nextLibrary);
      writeCachedPracticeLibrary(nextLibrary);
      setSelectedPracticeSubjectId((current) => {
        const hasCurrentSubject = [...nextLibrary.subjects, ...(nextLibrary.aiSubjects ?? [])].some((subject) => subject.id === current);
        if (hasCurrentSubject) return current;
        return nextLibrary.subjects[0]?.id ?? nextLibrary.aiSubjects?.[0]?.id ?? "";
      });
      setPracticeLibraryMessage("");
      setPracticeLibraryStatus("ready");
      window.clearTimeout(timeoutId);
      return;
    } catch (error) {
      lastError = error;
    } finally {
      window.clearTimeout(timeoutId);
    }
  }

  if (cachedLibrary?.subjects?.length) {
    setPracticeLibraryMessage("You are offline or the connection is slow. Saved questions are available.");
    setPracticeLibraryStatus("ready");
    return;
  }

  setPracticeLibrary(emptyPracticeLibrary);
  setSelectedPracticeSubjectId("");
  setPracticeLibraryMessage(lastError instanceof Error ? lastError.message : "Could not load practice questions.");
  setPracticeLibraryStatus("error");
}

  useEffect(() => {
    const token = localStorage.getItem(SESSION_TOKEN_KEY);
    let isActive = true;

    if (!token) {
      setAuthStatus("unauthenticated");
      return undefined;
    }

    apiRequest("/api/auth/session", { timeoutMs: 3000 })
      .then((data) => {
        if (!isActive) return;
        const mergedUser = mergeUserPerformance(data.user);
        setUser(mergedUser);
        setUserRating(mergedUser.rating ?? 1480);
        setProfileState(createProfileState(mergedUser));
        setAuthStatus("authenticated");
      })
      .catch(() => {
        if (!isActive) return;
        localStorage.removeItem(SESSION_TOKEN_KEY);
        setAuthStatus("unauthenticated");
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  useEffect(() => {
    if (!practiceChoiceSubject) return undefined;

    const previousBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = previousBodyOverflow;
    };
  }, [practiceChoiceSubject]);

  useEffect(() => {
    const nextProgress = readPracticeProgress(user);
    setPracticeProgress(nextProgress);
    setAnalyticsEvents(readAnalyticsEvents(user, nextProgress));
  }, [user?.id, user?.email]);

  useEffect(() => {
    fetchLeaderboard();
    fetchPlatformSummary();
  }, [authStatus]);

  useEffect(() => {
    if (activeView !== "Practice" || practiceLibraryStatus !== "idle") return;
    fetchPracticeLibrary();
  }, [activeView, practiceLibraryStatus]);

  useEffect(() => {
    if (activeView !== "Practice" || practiceStage !== "subject") return undefined;
    const handlePracticeKeyboard = (event) => {
      if (["INPUT", "TEXTAREA", "SELECT"].includes(event.target?.tagName)) return;
      const optionIndex = Number(event.key) - 1;
      if (optionIndex >= 0 && optionIndex < (currentPracticeQuestion?.options?.length ?? 0) && !submitted) {
        setSelectedOption(currentPracticeQuestion.options[optionIndex]);
      }
      if (event.key.toLowerCase() === "f" && currentPracticeQuestion) {
        setFlaggedQuestions((current) => ({ ...current, [currentPracticeQuestion.id]: !current[currentPracticeQuestion.id] }));
      }
      if (event.key === "Enter") {
        event.preventDefault();
        if (submitted) handleNextPracticeQuestion();
        else if (selectedOption) handleSubmitAnswer();
      }
    };
    window.addEventListener("keydown", handlePracticeKeyboard);
    return () => window.removeEventListener("keydown", handlePracticeKeyboard);
  }, [activeView, currentPracticeQuestion, practiceStage, selectedOption, submitted]);

  async function fetchCommunities({ silent = false } = {}) {
    if (authStatus !== "authenticated") return;

    try {
      if (!silent) setCommunitiesBusy(true);
      const data = await apiRequest("/api/communities");
      setCommunities(data.communities);
      setSelectedCommunityId((current) => {
        if (current && data.communities.some((community) => community.id === current)) return current;
        return data.communities[0]?.id ?? "";
      });
      setCommunitiesMessage("");
      await fetchPlatformSummary();
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not load communities.");
    } finally {
      if (!silent) setCommunitiesBusy(false);
    }
  }

  async function fetchDirectConversations({ silent = false } = {}) {
    if (authStatus !== "authenticated") return;

    try {
      if (!silent) setDirectMessagesBusy(true);
      const data = await apiRequest("/api/direct-messages");
      setDirectConversations(data.conversations ?? []);
      setSelectedDirectConversationId((current) => {
        if (current && (data.conversations ?? []).some((conversation) => conversation.id === current)) return current;
        return data.conversations?.[0]?.id ?? "";
      });
      setDirectMessagesMessage("");
    } catch (error) {
      setDirectMessagesMessage(error instanceof Error ? error.message : "Could not load messages.");
    } finally {
      if (!silent) setDirectMessagesBusy(false);
    }
  }

  useEffect(() => {
    if (authStatus !== "authenticated") return undefined;
    fetchCommunities();
    fetchDirectConversations();
    const messageInterval = window.setInterval(() => fetchDirectConversations({ silent: true }), 15000);
    return () => window.clearInterval(messageInterval);
  }, [authStatus]);

  useEffect(() => {
    if (authStatus !== "authenticated") return;
    const communityId = new URLSearchParams(window.location.search).get("community");
    if (!communityId) return;
    setSelectedCommunityId(communityId);
    setCommunityStage("detail");
    setActiveView("Communities");
  }, [authStatus]);

  useEffect(() => {
    if (authStatus !== "authenticated" || activeView !== "Communities") return undefined;

    fetchCommunities({ silent: true });

    const interval = window.setInterval(() => {
      fetchCommunities({ silent: true });
    }, 5000);

    return () => window.clearInterval(interval);
  }, [authStatus, activeView]);

  useEffect(() => {
    if (authStatus !== "authenticated" || activeView !== "Communities") return undefined;

    const query = directSearchTerm.trim();
    if (query.length < 2) {
      setDirectSearchResults([]);
      setDirectSearchBusy(false);
      return undefined;
    }

    let cancelled = false;
    const timeoutId = window.setTimeout(async () => {
      try {
        setDirectSearchBusy(true);
        const data = await apiRequest(`/api/users/search?q=${encodeURIComponent(query)}`);
        if (!cancelled) {
          setDirectSearchResults(data.users ?? []);
        }
      } catch (error) {
        if (!cancelled) {
          setDirectMessagesMessage(error instanceof Error ? error.message : "Could not search users.");
        }
      } finally {
        if (!cancelled) {
          setDirectSearchBusy(false);
        }
      }
    }, 250);

    return () => {
      cancelled = true;
      window.clearTimeout(timeoutId);
    };
  }, [activeView, authStatus, directSearchTerm]);

  useEffect(() => {
    if (!stateSearchTerm.trim()) return;
    if (filteredStateLeaderboard.length === 1) {
      setSelectedLeaderboardState(filteredStateLeaderboard[0].state);
    }
  }, [filteredStateLeaderboard, stateSearchTerm]);

  useEffect(() => {
    if (!selectedStateEntry && filteredStateLeaderboard.length) {
      setSelectedLeaderboardState(filteredStateLeaderboard[0].state);
      return;
    }

    if (!selectedLeaderboardState && currentUserLeaderboardEntry?.state) {
      setSelectedLeaderboardState(currentUserLeaderboardEntry.state);
    }
  }, [currentUserLeaderboardEntry, filteredStateLeaderboard, selectedLeaderboardState, selectedStateEntry]);

  useEffect(() => {
    if (duelStatus !== "live") return undefined;

    const timer = window.setInterval(() => {
      setDuelTimeLeft((current) => {
        if (current <= 1) {
          window.clearInterval(timer);
          setDuelStatus("finished");
          return 0;
        }
        return current - 1;
      });
    }, 1000);

    return () => window.clearInterval(timer);
  }, [duelStatus]);

  useEffect(() => {
    if (duelStatus !== "matchmaking" || !duelQueueInfo?.ticketId) return undefined;

    let cancelled = false;
    const pollQueue = async () => {
      try {
        const data = await apiRequest("/api/duels/rated/queue");
        if (cancelled) return;

        if (data.status === "matched" && data.opponent) {
          const sessionId = data.duel?.id ?? createDuelSessionId("rated");
          const questions = await loadDuelQuestions(sessionId);
          beginLiveDuel(data.opponent, {
            mode: "rated",
            questions,
            sessionId,
          });
          return;
        }

        if (data.status === "idle") {
          setDuelStatus("idle");
          setDuelQueueInfo(null);
          setDuelMessage("You are no longer in the rated duel queue.");
          return;
        }

        setDuelQueueInfo({
          ticketId: data.ticketId,
          queuedAt: data.queuedAt,
          waitingCount: data.waitingCount ?? 1,
        });
      } catch (error) {
        if (!cancelled) {
          setDuelMessage(error instanceof Error ? error.message : "Could not check the duel queue.");
        }
      }
    };

    const intervalId = window.setInterval(pollQueue, 2500);
    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, [duelQueueInfo?.ticketId, duelQuestions, duelStatus]);

  useEffect(() => {
    if (duelStatus !== "live") return;

    const elapsed = DUEL_DURATION_SECONDS - duelTimeLeft;
    setDuelOpponentProgress(getDuelOpponentSnapshot(duelOpponentTimeline, elapsed));
  }, [duelStatus, duelTimeLeft, duelOpponentTimeline]);

  useEffect(() => {
    if (duelStatus !== "finished" || !duelOpponent || duelResult) return;

    const elapsed = DUEL_DURATION_SECONDS - duelTimeLeft;
    const opponentSnapshot = getDuelOpponentSnapshot(duelOpponentTimeline, elapsed);
    const opponentCorrect = opponentSnapshot.correct;
    const opponentAnswered = opponentSnapshot.answered;
    const userAnswered = Object.keys(duelSubmitted).length;
    const userCompletedEarlier = userAnswered === duelQuestions.length && duelTimeLeft > 0;
    const opponentCompletedEarlier =
      opponentAnswered === duelQuestions.length &&
      duelOpponentTimeline.every((step) => step.revealAt <= elapsed);

    let verdict = duelForfeited ? "loss" : "draw";

    if (!duelForfeited && userDuelScore > opponentCorrect) {
      verdict = "win";
    } else if (!duelForfeited && userDuelScore < opponentCorrect) {
      verdict = "loss";
    } else if (!duelForfeited && userCompletedEarlier && !opponentCompletedEarlier) {
      verdict = "win";
    } else if (!duelForfeited && !userCompletedEarlier && opponentCompletedEarlier) {
      verdict = "loss";
    }

    setDuelOpponentProgress(opponentSnapshot);

    const completeDuel = async () => {
      try {
        const data = await apiRequest("/api/duels/complete", {
          method: "POST",
          body: JSON.stringify({
            mode: duelMode,
            duelId: duelMode === "rated" ? duelSessionId : "",
            sessionId: duelSessionId,
            opponentId: duelOpponent.id,
            opponentRating: duelOpponent.rating,
            opponentScore: opponentCorrect,
            forfeit: duelForfeited,
            questionIds: duelQuestions.map((question) => question.id),
            answers: duelQuestions.reduce(
              (answers, question, index) => ({
                ...answers,
                [question.id]: duelSelections[index] ?? "",
              }),
              {},
            ),
          }),
        });

        const result = data.result ?? {};
        const mergedUser = mergeUserPerformance(data.user);
        const nextRating = mergedUser.rating ?? result.nextRating ?? userRating;
        setUser(mergedUser);
        setUserRating(nextRating);
        setAnalyticsEvents((current) => {
          const completedAt = new Date().toISOString();
          const secondsPerAnswer = userAnswered ? Math.max(1, Math.round((DUEL_DURATION_SECONDS - duelTimeLeft) / userAnswered)) : 0;
          const duelEvents = duelQuestions.flatMap((question, index) => duelSubmitted[index] ? [{
            id: `${duelSessionId || completedAt}-${question.id}`,
            questionId: question.id,
            answeredAt: completedAt,
            correct: isAnswerCorrect(question, duelSelections[index]),
            subjectId: question.subjectId || "mixed-duel",
            subject: question.subject || "Mixed battle",
            topic: question.topic || "Battle review",
            activity: "battle",
            durationSeconds: secondsPerAnswer,
          }] : []);
          const nextEvents = [...current, ...duelEvents];
          writeAnalyticsEvents(user, nextEvents);
          return nextEvents;
        });
        setLeaderboardPlayers((current) =>
          current.map((player) =>
            player.id === user?.id
              ? {
                  ...player,
                  score: nextRating,
                  isCurrentUser: true,
                }
              : player,
          ),
        );
        setDuelResult({
          verdict: result.verdict ?? verdict,
          delta: result.delta ?? 0,
          previousRating: result.previousRating ?? userRating,
          nextRating,
          userScore: result.userScore ?? userDuelScore,
          opponentScore: result.opponentScore ?? opponentCorrect,
          userAnswered,
          opponentAnswered,
          ratingAffected: result.ratingAffected ?? duelMode !== "bot",
          forfeited: result.forfeited ?? duelForfeited,
        });
        await fetchLeaderboard();
        await fetchPlatformSummary();
      } catch (error) {
        setDuelMessage(error instanceof Error ? error.message : "Could not save the duel result.");
        setDuelResult({
          verdict,
          delta: 0,
          previousRating: userRating,
          nextRating: userRating,
          userScore: userDuelScore,
          opponentScore: opponentCorrect,
          userAnswered,
          opponentAnswered,
          ratingAffected: false,
          forfeited: duelForfeited,
        });
      }
    };

    void completeDuel();
  }, [
    duelMode,
    duelOpponent,
    duelOpponentTimeline,
    duelForfeited,
    duelQuestions,
    duelResult,
    duelSelections,
    duelSessionId,
    duelStatus,
    duelSubmitted,
    duelTimeLeft,
    fetchLeaderboard,
    fetchPlatformSummary,
    user,
    userDuelScore,
    userRating,
  ]);

  function handleSubmitAnswer() {
    if (!selectedOption || submitted || !currentPracticeQuestion || !user) return;

    const wasCorrect = selectedOption === currentPracticeQuestion.answer;
    const nextCorrectAnswers = (user.correctAnswers ?? 0) + (wasCorrect ? 1 : 0);
    const nextAttemptedQuestions = (user.attemptedQuestions ?? 0) + 1;

    setUser((current) =>
      current
        ? {
            ...current,
            correctAnswers: nextCorrectAnswers,
            attemptedQuestions: nextAttemptedQuestions,
          }
        : current,
    );
    setSubmitted(true);
    setAnalyticsEvents((current) => {
      const nextEvents = [...current, {
        id: `${Date.now()}-${currentPracticeQuestion.id}`,
        questionId: currentPracticeQuestion.id,
        answeredAt: new Date().toISOString(),
        correct: wasCorrect,
        subjectId: currentPracticeQuestion.subjectId || currentPracticeSubject?.id || "unknown",
        subject: currentPracticeSubject?.title || "Other",
        topic: currentPracticeQuestion.topic || currentPracticeQuestion.subtopic || "General review",
        activity: selectedPracticeMode === "ai" ? "revision" : "pyq",
        durationSeconds: Math.max(1, Math.min(1800, Math.round((Date.now() - practiceQuestionStartedAt) / 1000))),
      }];
      writeAnalyticsEvents(user, nextEvents);
      return nextEvents;
    });
    setPracticeProgress((current) => {
      const nextProgress = {
        ...current,
        [currentPracticeQuestion.id]: {
          answeredAt: new Date().toISOString(),
          correct: wasCorrect,
          subjectId: currentPracticeQuestion.subjectId,
          year: currentPracticeQuestion.year,
        },
      };
      writePracticeProgress(user, nextProgress);
      return nextProgress;
    });
    void saveUserStats(userRating, user?.streak ?? 1, {
      correctAnswers: nextCorrectAnswers,
      attemptedQuestions: nextAttemptedQuestions,
    });
  }

  function handleSelectPracticeSubject(subjectId) {
    setPracticeChoiceSubjectId(subjectId);
  }

  function closePracticeChoice() {
    setPracticeChoiceSubjectId("");
  }

  function startPracticeSession(subjectId, mode, examYear = "") {
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode(mode);
    setSelectedPracticeExamYear(mode === "pyq" ? examYear : "");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setPracticeStage("subject");
    setPracticeQuestionStartedAt(Date.now());
    setPracticeChoiceSubjectId("");
  }

  function handleBackToPracticeDirectory() {
    setPracticeStage("catalog");
    setSelectedPracticeMode("pyq");
    setSelectedPracticeExamYear("");
    setSelectedOption("");
    setSubmitted(false);
  }

  function openCommunityChat(communityId) {
    setSelectedCommunityId(communityId);
    setCommunityStage("detail");
  }

  function openDirectConversation(conversationId) {
    setSelectedDirectConversationId(conversationId);
    setCommunityStage("direct");
    setDirectMessageDraft("");
  }

  function handleBackToCommunityHub() {
    setCommunityStage("hub");
    setCommunityMessageDraft("");
    setCommunityThreadImage(null);
    setDirectMessageDraft("");
  }

  function handleNextPracticeQuestion() {
    if (!currentPracticeSubject) return;
    if (practiceQuestionIndex >= currentPracticeQuestions.length - 1) return;
    setPracticeQuestionIndex((current) => current + 1);
    setSelectedOption("");
    setSubmitted(false);
    setAnswerConfidence("");
    setPracticeQuestionStartedAt(Date.now());
  }

  function handleStartAiPractice(subjectId) {
    const subject = practiceSubjects.find((entry) => entry.id === subjectId);
    if (!subject) return;

    setAiPracticeMessage("");
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode("ai");
    setSelectedPracticeExamYear("");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setPracticeStage("chapters");
    setPracticeChoiceSubjectId("");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    scrollPracticeViewToTop();
  }

  function openPracticeChapter(chapterTitle) {
    setSelectedPracticeChapter(chapterTitle);
    setPracticeStage("topics");
    scrollPracticeViewToTop();
  }
  function startTopicPractice(topic) {
    setSelectedPracticeTopic(topic);
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setPracticeStage("subject");
    setPracticeQuestionStartedAt(Date.now());
    scrollPracticeViewToTop();
  }
  async function handleCreateCommunity(event) {
    event.preventDefault();
    setCommunitiesMessage("");

    try {
      const data = await apiRequest("/api/communities", {
        method: "POST",
        body: JSON.stringify(createCommunityForm),
      });
      setCreateCommunityForm({ name: "", topic: "", description: "" });
      setCommunities((current) => [data.community, ...current]);
      setSelectedCommunityId(data.community.id);
      setCommunityStage("detail");
      setCommunitiesMessage("Community created. You are the admin and can share the invite link.");
      await fetchPlatformSummary();
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not create community.");
    }
  }

  async function handleJoinCommunity(communityId) {
    setCommunitiesMessage("");

    try {
      const data = await apiRequest(`/api/communities/${communityId}/join`, {
        method: "POST",
      });
      setCommunities((current) =>
        current.map((community) => (community.id === communityId ? data.community : community)),
      );
      setSelectedCommunityId(communityId);
      setCommunityStage("detail");
      setCommunitiesMessage("Joined community successfully.");
      await fetchPlatformSummary();
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not join community.");
    }
  }

  async function handleSendCommunityMessage(event, parentMessageId = null) {
    event.preventDefault();
    const draft = parentMessageId ? communityReplyDrafts[parentMessageId] ?? "" : communityMessageDraft;
    const imageDataUrl = parentMessageId ? null : communityThreadImage?.dataUrl ?? null;
    if (!selectedCommunity || (!draft.trim() && !imageDataUrl)) return;
    if (countWords(draft) > COMMUNITY_THREAD_WORD_LIMIT) {
      setCommunitiesMessage("Threads can contain at most " + COMMUNITY_THREAD_WORD_LIMIT + " words.");
      return;
    }

    setCommunitiesMessage("");

    try {
      const data = await apiRequest(`/api/communities/${selectedCommunity.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ text: draft, parentMessageId, imageDataUrl }),
      });
      setCommunities((current) =>
        current.map((community) => (community.id === selectedCommunity.id ? data.community : community)),
      );
      if (parentMessageId) {
        setCommunityReplyDrafts((current) => ({ ...current, [parentMessageId]: "" }));
        setExpandedCommunityThreads((current) => ({ ...current, [parentMessageId]: true }));
      } else {
        setCommunityMessageDraft("");
        setCommunityThreadImage(null);
      }
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not publish your post.");
    }
  }

  async function handleCommunityThreadImageChange(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    if (!(["image/jpeg", "image/png", "image/webp", "image/gif"].includes(file.type))) {
      setCommunitiesMessage("Choose a PNG, JPG, WEBP, or GIF image.");
      return;
    }
    if (file.size > COMMUNITY_THREAD_IMAGE_LIMIT_BYTES) {
      setCommunitiesMessage("Thread images must be 5 MB or smaller.");
      return;
    }

    try {
      const dataUrl = await convertFileToDataUrl(file);
      setCommunityThreadImage({ dataUrl, name: file.name });
      setCommunitiesMessage("");
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not load that image.");
    }
  }

  function toggleCommunityThread(messageId, forceOpen = false) {
    setExpandedCommunityThreads((current) => ({
      ...current,
      [messageId]: forceOpen ? true : !current[messageId],
    }));
  }

  async function handleRemoveCommunityMember(communityId, memberId) {
    setCommunitiesMessage("");

    try {
      const data = await apiRequest(`/api/communities/${communityId}/members/${memberId}`, {
        method: "DELETE",
      });
      setCommunities((current) =>
        current.map((community) => (community.id === communityId ? data.community : community)),
      );
      setSelectedCommunityId(communityId);
      setCommunitiesMessage("Member removed from community.");
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not remove member.");
    }
  }

  async function handleOpenDirectChat(targetUserId) {
    if (!targetUserId) return;

    setDirectMessagesMessage("");

    try {
      const data = await apiRequest("/api/direct-messages/open", {
        method: "POST",
        body: JSON.stringify({ targetUserId }),
      });
      setDirectConversations((current) => {
        const filtered = current.filter((conversation) => conversation.id !== data.conversation.id);
        return [data.conversation, ...filtered];
      });
      setSelectedDirectConversationId(data.conversation.id);
      setCommunityStage("direct");
      setDirectSearchTerm("");
      setDirectSearchResults([]);
    } catch (error) {
      setDirectMessagesMessage(error instanceof Error ? error.message : "Could not open private chat.");
    }
  }

  async function handleCopyCommunityInvite(communityId) {
    const inviteUrl = getCommunityInviteUrl(communityId);
    if (!inviteUrl) return;

    try {
      await navigator.clipboard.writeText(inviteUrl);
      setCommunitiesMessage("Invite link copied. Share it with learners you want in this community.");
    } catch {
      setCommunitiesMessage(inviteUrl);
    }
  }

  async function handleSendDirectMessage(event) {
    event.preventDefault();
    if (!selectedDirectConversation || !directMessageDraft.trim()) return;

    setDirectMessagesMessage("");

    try {
      const data = await apiRequest(`/api/direct-messages/${selectedDirectConversation.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ text: directMessageDraft }),
      });
      setDirectConversations((current) => {
        const filtered = current.filter((conversation) => conversation.id !== data.conversation.id);
        return [data.conversation, ...filtered];
      });
      setSelectedDirectConversationId(data.conversation.id);
      setDirectMessageDraft("");
    } catch (error) {
      setDirectMessagesMessage(error instanceof Error ? error.message : "Could not send private message.");
    }
  }

  async function handleDirectChallenge() {
    if (!selectedDirectConversation?.otherParticipant) return;

    const opponentProfile = selectedDirectConversation.otherParticipant;
    const challengeText = `I have challenged you to a 1v1 duel. Join me in Compete and prove your rank.`;

    try {
      const data = await apiRequest(`/api/direct-messages/${selectedDirectConversation.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ text: challengeText, type: "challenge" }),
      });
      setDirectConversations((current) => {
        const filtered = current.filter((conversation) => conversation.id !== data.conversation.id);
        return [data.conversation, ...filtered];
      });
      setSelectedDirectConversationId(data.conversation.id);
    } catch (error) {
      setDirectMessagesMessage(error instanceof Error ? error.message : "Could not send duel challenge.");
    }

    startDuel({
      id: opponentProfile.id,
      name: opponentProfile.name,
      rating: opponentProfile.rating ?? userRating,
      specialty: opponentProfile.state || "Medical challenger",
    });
  }

  function createDuelSessionId(prefix = "duel") {
    const randomId =
      typeof crypto !== "undefined" && typeof crypto.randomUUID === "function"
        ? crypto.randomUUID()
        : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    return `${prefix}-${randomId}`;
  }

  async function loadDuelQuestions(sessionId) {
    let data;

    try {
      data = await apiRequest(`/api/duels/questions?count=${fallbackDuelQuestions.length}&session=${encodeURIComponent(sessionId)}`, {
        cache: "no-store",
      });
    } catch (error) {
      if (!(error instanceof Error) || !/route not found/i.test(error.message)) {
        throw error;
      }

      const practiceData = await apiRequest(`/api/practice?source=official&session=${encodeURIComponent(sessionId)}`, {
        cache: "no-store",
      });
      const practiceQuestions = Array.isArray(practiceData.questions) ? practiceData.questions : [];
      data = {
        questions: practiceQuestions
          .filter((question) => question?.id && question?.prompt && Array.isArray(question.options) && question.options.length === 4)
          .sort(
            (left, right) =>
              getSeededClientRank(`${sessionId}:${left.id}`) - getSeededClientRank(`${sessionId}:${right.id}`),
          )
          .slice(0, fallbackDuelQuestions.length),
      };
    }

    if (!Array.isArray(data.questions) || !data.questions.length) {
      throw new Error("Could not load fresh compete questions.");
    }

    return data.questions;
  }

  function beginLiveDuel(opponent, options = {}) {
    const questions = Array.isArray(options.questions) && options.questions.length ? options.questions : fallbackDuelQuestions;
    setActiveView("Compete");
    setDuelQuestions(questions);
    setDuelMode(options.mode ?? "rated");
    setDuelSessionId(options.sessionId ?? "");
    setDuelOpponent(opponent);
    setDuelOpponentTimeline(createOpponentTimeline(opponent.rating ?? userRating, questions));
    setDuelTimeLeft(DUEL_DURATION_SECONDS);
    setDuelIndex(0);
    setDuelSelections({});
    setDuelSubmitted({});
    setDuelOpponentProgress({ answered: 0, correct: 0 });
    setDuelResult(null);
    setDuelQueueInfo(null);
    setDuelMessage("");
    setDuelForfeited(false);
    setDuelStatus("live");
  }

  async function startDuel(preferredOpponent = null) {
    if (preferredOpponent) {
      try {
        const sessionId = createDuelSessionId("challenge");
        const questions = await loadDuelQuestions(sessionId);
        beginLiveDuel(preferredOpponent, {
          mode: "rated",
          questions,
          sessionId,
        });
      } catch (error) {
        setActiveView("Compete");
        setDuelStatus("idle");
        setDuelMessage(error instanceof Error ? error.message : "Could not load fresh duel questions.");
      }
      return;
    }

    if (!user) {
      setAuthMode("login");
      setActiveView("Profile");
      return;
    }

    setActiveView("Compete");
    setDuelOpponent(null);
    setDuelOpponentTimeline([]);
    setDuelTimeLeft(DUEL_DURATION_SECONDS);
    setDuelIndex(0);
    setDuelSelections({});
    setDuelSubmitted({});
    setDuelOpponentProgress({ answered: 0, correct: 0 });
    setDuelResult(null);
    setDuelMessage("");
    setDuelStatus("matchmaking");

    try {
      const data = await apiRequest("/api/duels/rated/queue", {
        method: "POST",
      });

      if (data.status === "matched" && data.opponent) {
        const sessionId = data.duel?.id ?? createDuelSessionId("rated");
        const questions = await loadDuelQuestions(sessionId);
        beginLiveDuel(data.opponent, {
          mode: "rated",
          questions,
          sessionId,
        });
        return;
      }

      setDuelQueueInfo({
        ticketId: data.ticketId,
        queuedAt: data.queuedAt,
        waitingCount: data.waitingCount ?? 1,
      });
    } catch (error) {
      setDuelStatus("idle");
      setDuelMessage(error instanceof Error ? error.message : "Could not join the rated duel queue.");
    }
  }

  async function startBotDuel() {
    if (!user) {
      setAuthMode("login");
      setActiveView("Profile");
      return;
    }

    setActiveView("Compete");
    setDuelMessage("");
    try {
      const sessionId = createDuelSessionId("bot");
      const questions = await loadDuelQuestions(sessionId);
      beginLiveDuel(
        {
          id: "medicomm-clinical-bot",
          name: "Clinical Bot",
          rating: userRating,
          specialty: "Ratingless PYQ sparring",
          ratingless: true,
        },
        {
          mode: "bot",
          questions,
          sessionId,
        },
      );
    } catch (error) {
      setDuelStatus("idle");
      setDuelMessage(error instanceof Error ? error.message : "Could not load fresh bot questions.");
    }
  }

  async function leaveDuelQueue() {
    try {
      await apiRequest("/api/duels/rated/queue", {
        method: "DELETE",
      });
    } catch (error) {
      setDuelMessage(error instanceof Error ? error.message : "Could not leave the duel queue.");
    } finally {
      resetDuel(false);
    }
  }

  function submitDuelAnswer() {
    if (!currentDuelSelection || currentDuelSubmitted || !currentDuelQuestion || !user) return;
    setDuelSubmitted((current) => ({ ...current, [duelIndex]: true }));
  }

  function nextDuelQuestion() {
    if (duelIndex === duelQuestions.length - 1) {
      setDuelStatus("finished");
      return;
    }
    setDuelIndex((current) => current + 1);
  }

  function forfeitDuel() {
    if (duelStatus !== "live") return;
    setDuelForfeited(true);
    setDuelStatus("finished");
  }

  function resetDuel(syncServer = true) {
    if (syncServer && (duelStatus === "matchmaking" || duelStatus === "live" || duelStatus === "finished")) {
      void apiRequest("/api/duels/rated/queue", {
        method: "DELETE",
      }).catch(() => undefined);
    }
    setDuelStatus("idle");
    setDuelQuestions(fallbackDuelQuestions);
    setDuelMode("rated");
    setDuelSessionId("");
    setDuelOpponent(null);
    setDuelTimeLeft(DUEL_DURATION_SECONDS);
    setDuelIndex(0);
    setDuelSelections({});
    setDuelSubmitted({});
    setDuelOpponentTimeline([]);
    setDuelOpponentProgress({ answered: 0, correct: 0 });
    setDuelResult(null);
    setDuelQueueInfo(null);
    setDuelMessage("");
    setDuelForfeited(false);
  }

  function updateAuthField(field, value) {
    setAuthForm((current) => ({ ...current, [field]: value }));
  }

  function updateProfileField(field, value) {
    setProfileState((current) => ({ ...current, [field]: value }));
  }

  function updateCreateCommunityField(field, value) {
    setCreateCommunityForm((current) => ({ ...current, [field]: value }));
  }

  async function openPublicProfile(userId, returnView = activeView) {
    if (!userId) return;
    if (userId === user?.id) {
      setActiveView("Profile");
      return;
    }

    setPublicProfileBusy(true);
    setPublicProfileMessage("");
    setPublicProfileReturnView(returnView);

    try {
      const data = await apiRequest(`/api/users/${userId}`);
      setPublicProfile(mergeUserPerformance(data.user));
      setActiveView("PublicProfile");
    } catch (error) {
      setPublicProfileMessage(error instanceof Error ? error.message : "Could not load that profile.");
    } finally {
      setPublicProfileBusy(false);
    }
  }

  function closePublicProfile() {
    setActiveView(publicProfileReturnView || "Communities");
  }

  async function convertFileToDataUrl(file) {
    return await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result));
      reader.onerror = () => reject(new Error("Unable to read that image file."));
      reader.readAsDataURL(file);
    });
  }

  async function handleProfilePhotoChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const dataUrl = await convertFileToDataUrl(file);
      updateProfileField("profileImageDataUrl", dataUrl);
      setProfileMessage("New profile picture selected. Save profile to apply it.");
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "Could not load that image.");
    }
  }

  async function saveUserStats(nextRating, nextStreak = user?.streak ?? 1, nextStats = {}) {
    try {
      const data = await apiRequest("/api/profile/stats", {
        method: "PATCH",
        body: JSON.stringify({
          rating: nextRating,
          streak: nextStreak,
          correctAnswers: nextStats.correctAnswers,
          attemptedQuestions: nextStats.attemptedQuestions,
        }),
      });

      const mergedUser = mergeUserPerformance(data.user);
      setUser(mergedUser);
      setUserRating(mergedUser.rating ?? nextRating);
      await fetchLeaderboard();
      await fetchPlatformSummary();
    } catch {
      // Keep the local score even if persistence fails.
    }
  }

  async function handleAuthSubmit(event) {
    event.preventDefault();
    setAuthBusy(true);
    setAuthMessage("");

    const endpoint = authMode === "signup" ? "/api/auth/signup" : "/api/auth/login";
    const payload =
      authMode === "signup"
        ? authForm
        : {
            email: authForm.email,
            password: authForm.password,
          };

    try {
      const data = await apiRequest(endpoint, {
        method: "POST",
        body: JSON.stringify(payload),
        timeoutMs: 20000,
      });

      localStorage.setItem(SESSION_TOKEN_KEY, data.token);
      const mergedUser = mergeUserPerformance(data.user);
      setUser(mergedUser);
      setUserRating(mergedUser.rating ?? 1480);
      setProfileState(createProfileState(mergedUser));
      setAuthStatus("authenticated");
      setActiveView("Dashboard");
      await fetchLeaderboard();
      setAuthForm({
        name: "",
        email: "",
        medicalCollege: "",
        contactNumber: "",
        password: "",
      });
    } catch (error) {
      setAuthMessage(error instanceof Error ? error.message : "Authentication failed.");
    } finally {
      setAuthBusy(false);
    }
  }

  function handleGuestLogin() {
    const guestUser = {
      id: "guest",
      name: "Guest learner",
      email: "guest@medicomm.local",
      medicalCollege: "Explore mode",
      contactNumber: "",
      rating: 1200,
      streak: 1,
      attemptedQuestions: 0,
      correctAnswers: 0,
    };
    setUser(guestUser);
    setUserRating(1200);
    setProfileState(createProfileState(guestUser));
    setAuthStatus("guest");
    setActiveView("Dashboard");
    setAuthMessage("");
  }

  async function handleLogout() {
    try {
      await apiRequest("/api/auth/logout", { method: "POST" });
    } catch {
      // Best-effort logout.
    } finally {
      localStorage.removeItem(SESSION_TOKEN_KEY);
      setAuthStatus("unauthenticated");
      setUser(null);
      setUserRating(1480);
      setProfileState(createProfileState(null));
      setAuthMode("login");
      setAuthMessage("");
    }
  }

  async function handleProfileSave(event) {
    event.preventDefault();
    if (authStatus === "guest") {
      setProfileMessage("Create a free account to save profile changes across devices.");
      return;
    }
    setProfileBusy(true);
    setProfileMessage("");

    try {
      const data = await apiRequest("/api/profile", {
        method: "PATCH",
        body: JSON.stringify(profileState),
      });

      const mergedUser = mergeUserPerformance(data.user);
      setUser(mergedUser);
      setUserRating(mergedUser.rating ?? userRating);
      setProfileState(createProfileState(mergedUser));
      await fetchLeaderboard();
      setProfileMessage("Profile updated successfully.");
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "Profile update failed.");
    } finally {
      setProfileBusy(false);
    }
  }

  function renderAvatar() {
    if (user?.profileImageUrl) {
      return <img className="avatar-image" src={user.profileImageUrl} alt={`${user.name} profile`} />;
    }

    return <span>{getInitials(user?.name)}</span>;
  }

  function renderAuthPage() {
    const isSignup = authMode === "signup";

    return (
      <div className="auth-shell">
        <section className="auth-hero">
          <div className="auth-brand"><span className="brand-mark">M</span><strong><span className="brand-medi">Medi</span><span className="brand-comm">Comm</span></strong></div>
          <p className="eyebrow">Built for serious medical preparation</p>
          <h1>Study with clarity.<br /><span>Perform with confidence.</span></h1>
          <p>
            A focused workspace for PYQs, intelligent revision, performance analytics, and peer learning—designed around the way MBBS students actually study.
          </p>
          <div className="auth-proof-grid">
            <div><strong>{formatStatValue(platformSummary.practiceQuestions) || "5,000+"}</strong><span>curated questions</span></div>
            <div><strong>19</strong><span>medical subjects</span></div>
            <div><strong>24/7</strong><span>focused practice</span></div>
          </div>
          <div className="auth-preview-card" aria-hidden="true">
            <div className="auth-preview-header"><span>Today&apos;s focus</span><strong>72% complete</strong></div>
            <div className="auth-preview-track"><span /></div>
            <div className="auth-preview-row"><span>Pathology · PYQs</span><strong>Continue →</strong></div>
          </div>
        </section>

        <section className="card auth-card">
          <div className="auth-card-heading">
            <p className="eyebrow">Welcome to MediComm</p>
            <h2>{isSignup ? "Create your study account" : "Continue your learning"}</h2>
            <p>{isSignup ? "Set up your profile in under a minute." : "Sign in to sync progress across devices."}</p>
          </div>
          <div className="auth-tabs" role="tablist" aria-label="Authentication mode">
            <button
              className={`auth-tab${authMode === "login" ? " auth-tab-active" : ""}`}
              type="button"
              onClick={() => {
                setAuthMode("login");
                setAuthMessage("");
              }}
            >
              Login
            </button>
            <button
              className={`auth-tab${authMode === "signup" ? " auth-tab-active" : ""}`}
              type="button"
              onClick={() => {
                setAuthMode("signup");
                setAuthMessage("");
              }}
            >
              Sign up
            </button>
          </div>

          <form className="auth-form" onSubmit={handleAuthSubmit} autoComplete="off">
            {isSignup ? (
              <>
                <label className="field">
                  <span>Name</span>
                  <input
                    type="text"
                    autoComplete="off"
                    value={authForm.name}
                    onChange={(event) => updateAuthField("name", event.target.value)}
                    placeholder="Enter your full name"
                  />
                </label>
                <label className="field">
                  <span>Medical college</span>
                  <div className="college-search">
                    <input
                      type="text"
                      autoComplete="off"
                      list="medical-college-options"
                      value={authForm.medicalCollege}
                      onChange={(event) => updateAuthField("medicalCollege", event.target.value)}
                      placeholder="Type your college name or initials like AIIMS, MAMC, SMS"
                    />
                    <datalist id="medical-college-options">
                      {medicalCollegeSuggestions.map((college) => (
                        <option key={college} value={college} />
                      ))}
                    </datalist>
                  </div>
                </label>
                <label className="field">
                  <span>Contact number</span>
                  <input
                    type="tel"
                    autoComplete="off"
                    value={authForm.contactNumber}
                    onChange={(event) => updateAuthField("contactNumber", event.target.value)}
                    placeholder="Your contact number"
                  />
                </label>
              </>
            ) : null}

            <label className="field">
              <span>Email</span>
              <input
                type="email"
                autoComplete="off"
                value={authForm.email}
                onChange={(event) => updateAuthField("email", event.target.value)}
                placeholder="you@example.com"
              />
            </label>

            <label className="field">
              <span>Password</span>
              <div className="password-input-wrap">
                <input
                  type={passwordVisible ? "text" : "password"}
                  autoComplete={isSignup ? "new-password" : "current-password"}
                  value={authForm.password}
                  onChange={(event) => updateAuthField("password", event.target.value)}
                  placeholder="At least 6 characters"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setPasswordVisible((current) => !current)}
                  aria-label={passwordVisible ? "Hide password" : "Show password"}
                  title={passwordVisible ? "Hide password" : "Show password"}
                >
                  {passwordVisible ? "Hide" : "Show"}
                </button>
              </div>
            </label>

            {authMessage ? <p className="form-message" role="alert">{authMessage}</p> : null}

            <button className="button button-primary auth-submit" type="submit" disabled={authBusy}>
              {authBusy ? "Please wait..." : isSignup ? "Create account" : "Login"}
            </button>
          </form>
          <div className="auth-divider"><span>or</span></div>
          <button className="button button-secondary guest-button" type="button" onClick={handleGuestLogin}>
            Explore as guest
          </button>
          <p className="auth-fine-print">Guest progress stays on this device. Create an account anytime to sync it.</p>
        </section>
      </div>
    );
  }

  function renderHome() {
    return (
      <>
        <section className="hero">
          <h1>
            Master Medical Concepts with
            <span>Gamified Learning</span>
          </h1>
          <p>
            Practice medical MCQs, build your streak, compete with real registered learners, and
            track progress from live account and practice activity.
          </p>
          <div className="hero-actions">
            <button className="button button-primary" onClick={() => setActiveView("Practice")}>
              Start Practicing
            </button>
            <button className="button button-secondary" onClick={() => setActiveView("Profile")}>
              Open Profile
            </button>
          </div>
        </section>

        <section className="stats">
          {homeStats.map((stat) => (
            <article className="card stat-card" key={stat.label}>
              <div className={`icon-badge ${stat.tint}`}>{stat.icon}</div>
              <strong>{stat.value}</strong>
              <span>{stat.label}</span>
            </article>
          ))}
        </section>

        <section className="practice-upgrade-band">
          <article className="card panel practice-upgrade-panel">
            <div>
              <p className="eyebrow">Practice engine</p>
              <h2>Official PYQs and topic-wise questions, together.</h2>
              <p className="panel-copy">
                The practice library now loads from the backend, keeps NEET PG PYQs as the core bank, and labels
                Gemini-generated MCQs separately so they never look like official exam material.
              </p>
            </div>
            <div className="practice-upgrade-actions">
              <span className="rank-pill source-official">Official PYQ bank</span>
              <span className="rank-pill source-ai">Topic Wise Questions</span>
              <button className="button button-primary" onClick={() => setActiveView("Practice")}>
                Open practice library
              </button>
            </div>
          </article>
        </section>

        <section className="features-section">
          <div className="section-heading">
            <h2>Why Choose MediComm?</h2>
            <p>Everything you need to excel in medical knowledge</p>
          </div>

          <div className="features-grid">
            {features.map((feature) => (
              <article className="card feature-card" key={feature.title}>
                <div className={`icon-badge ${feature.tint}`}>{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="cta-banner">
          <h2>Ready to Level Up Your Medical Knowledge?</h2>
          <p>Join the current live learner base and help grow the community from real usage.</p>
          <button className="button cta-button" onClick={() => setActiveView("Dashboard")}>
            Get Started for Free
          </button>
        </section>
      </>
    );
  }

  function renderDashboard() {
    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Dashboard</p>
            <h2>Welcome back, {user?.name}</h2>
          </div>
          <button className="button button-primary" onClick={() => setActiveView("Practice")}>
            Continue practice
          </button>
        </div>

        <div className="summary-grid">
          {summaryCards.map((card) => (
            <article className="card summary-card" key={card.label}>
              <div className={`mini-dot ${card.accent}`} />
              <span>{card.label}</span>
              <strong>{card.value}</strong>
            </article>
          ))}
        </div>

        <div className="dashboard-priority-grid">
          <article className="card panel continue-card">
            <div className="panel-heading-split">
              <div><p className="eyebrow">Continue learning</p><h3>Pathology · Previous year questions</h3><p className="panel-copy">Pick up where you left off. Your local progress is saved automatically.</p></div>
              <span className="rank-pill source-official">12 min left</span>
            </div>
            <div className="continue-progress"><span style={{ width: "68%" }} /></div>
            <div className="continue-footer"><span>34 of 50 questions</span><button className="button button-primary" onClick={() => setActiveView("Practice")}>Resume session</button></div>
          </article>

          <article className="card panel exam-countdown-card">
            <p className="eyebrow">Upcoming exam</p><h3>NEET PG</h3><strong className="countdown-number">42</strong><span>days remaining</span>
            <div className="countdown-footer"><span>Weekly target</span><strong>4h 12m / 6h</strong></div>
          </article>
        </div>

        <div className="dashboard-insight-grid">
          <article className="card panel weekly-chart-card">
            <div className="panel-heading-split"><div><h3>Weekly progress</h3><p className="panel-copy">Questions completed per day</p></div><span className="trend-positive">↑ 18% this week</span></div>
            <div className="weekly-bars" aria-label="Weekly questions: Monday 18, Tuesday 26, Wednesday 20, Thursday 34, Friday 42, Saturday 30, Sunday 24">
              {[18, 26, 20, 34, 42, 30, 24].map((value, index) => <div key={index}><span style={{ height: `${Math.max(18, value * 2)}px` }} /><small>{["M", "T", "W", "T", "F", "S", "S"][index]}</small></div>)}
            </div>
          </article>

          <article className="card panel heatmap-card">
            <div className="panel-heading-split"><div><h3>Study consistency</h3><p className="panel-copy">Last 8 weeks</p></div><strong>24 day streak</strong></div>
            <div className="study-heatmap" aria-label="Study activity heatmap for the last eight weeks">
              {Array.from({ length: 56 }, (_, index) => <span key={index} data-level={(index * 7 + index % 5) % 4} title={`Day ${index + 1}`} />)}
            </div>
            <div className="heatmap-legend"><span>Less</span><i data-level="0" /><i data-level="1" /><i data-level="2" /><i data-level="3" /><span>More</span></div>
          </article>
        </div>

        <div className="dashboard-action-grid">
          <article className="card panel recommendation-card">
            <div className="panel-heading-split"><div><h3>Recommended next</h3><p className="panel-copy">Based on recent accuracy</p></div><button className="text-button" onClick={() => setActiveView("Analytics")}>View analytics</button></div>
            <div className="recommendation-list">
              {[{title:"Glomerular disorders",subject:"Pathology",score:"54% mastery"},{title:"Autonomic pharmacology",subject:"Pharmacology",score:"61% mastery"},{title:"Cardiac murmurs",subject:"Medicine",score:"66% mastery"}].map((topic, index) => <button key={topic.title} type="button" onClick={() => setActiveView("Practice")}><span className="recommendation-index">0{index + 1}</span><span><strong>{topic.title}</strong><small>{topic.subject}</small></span><em>{topic.score}</em></button>)}
            </div>
          </article>
          <article className="card panel recent-battles-card">
            <div className="panel-heading-split"><div><h3>Recent battles</h3><p className="panel-copy">Your latest 1v1 sessions</p></div><button className="text-button" onClick={() => setActiveView("Compete")}>Battle now</button></div>
            <div className="battle-list"><div><span className="battle-result win">W</span><span><strong>Ava Patel</strong><small>8–6 · 2h ago</small></span><em>+18 XP</em></div><div><span className="battle-result loss">L</span><span><strong>Noah Chen</strong><small>7–8 · Yesterday</small></span><em>−9 XP</em></div></div>
          </article>
        </div>

        <div className="content-grid">
          <article className="card panel user-profile-panel">
            <div className="profile-overview">
              <div className="profile-avatar-large">{renderAvatar()}</div>
              <div>
                <h3>{user?.name}</h3>
                <p className="panel-copy">{user?.medicalCollege}</p>
                <div className="profile-meta-list">
                  <span>{user?.email}</span>
                  <span>{user?.contactNumber}</span>
                  <span>National rank #{currentUserLeaderboardEntry?.rank ?? "-"}</span>
                  <span>
                    {currentUserLeaderboardEntry?.state ?? "State"} rank #{currentUserStateRank ?? "-"}
                  </span>
                </div>
              </div>
            </div>
            <button className="button button-secondary" onClick={() => setActiveView("Profile")}>
              Edit profile
            </button>
          </article>

          <article className="card panel">
            <h3>Today's snapshot</h3>
            <div className="stack-list">
              <div className="stack-row">
                <span>Questions answered</span>
                <strong>{quickStats.questionsToday}</strong>
              </div>
              <div className="stack-row">
                <span>Study time</span>
                <strong>{quickStats.timeSpent}</strong>
              </div>
              <div className="stack-row">
                <span>Needs review</span>
                <strong>{quickStats.weakArea}</strong>
              </div>
            </div>
          </article>

          <article className="card panel practice-status-panel">
            <div className="panel-heading-split">
              <div>
                <h3>Practice storage</h3>
                <p className="panel-copy">Backend question bank with official and supplemental sources separated.</p>
              </div>
              <span className="rank-pill source-ai">AI ready</span>
            </div>
            <div className="stack-list">
              <div className="stack-row">
                <span>Core source</span>
                <strong>NEET PG PYQs</strong>
              </div>
              <div className="stack-row">
                <span>Extra practice</span>
                <strong>Gemini JSON validated</strong>
              </div>
              <div className="stack-row">
                <span>Local storage</span>
                <strong>Session + theme only</strong>
              </div>
            </div>
            <button className="button button-secondary" onClick={() => setActiveView("Practice")}>
              Review subjects
            </button>
          </article>

          <article className="card panel">
            <h3>Recent activity</h3>
            <div className="feed-list">
              {activityFeed.map((item) => (
                <div className="feed-item" key={item.title}>
                  <div>
                    <strong>{item.title}</strong>
                    <p>{item.detail}</p>
                  </div>
                  <span>{item.time}</span>
                </div>
              ))}
            </div>
          </article>

          <article className="card panel">
            <h3>Account privacy</h3>
            <p className="panel-copy">
              Your login and profile details are now loaded from the local MediComm database before the
              app opens.
            </p>
            <button className="button button-secondary" onClick={handleLogout}>
              Logout
            </button>
          </article>
        </div>
      </section>
    );
  }

  function renderPractice() {
    if (practiceLibraryStatus === "idle" || practiceLibraryStatus === "loading") {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>NEET PG PYQs by year and subject</h2>
            </div>
          </div>

          <article className="card panel practice-skeleton" aria-label="Loading practice library" aria-busy="true">
            <div className="skeleton-line skeleton-title" />
            <div className="skeleton-line" />
            <div className="skeleton-card-grid">{Array.from({ length: 6 }, (_, index) => <div className="skeleton-block" key={index} />)}</div>
          </article>
        </section>
      );
    }

    if (practiceLibraryStatus === "error") {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>NEET PG PYQs by year and subject</h2>
            </div>
          </div>

          <article className="card panel">
            <h3>Practice library unavailable</h3>
            <p className="panel-copy">{practiceLibraryMessage || "We could not load the PYQ database."}</p>
            <button className="button button-secondary" onClick={fetchPracticeLibrary}>
              Retry
            </button>
          </article>
        </section>
      );
    }

    if (!practiceSubjects.length) {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>NEET PG PYQs by year and subject</h2>
            </div>
          </div>

          <article className="card panel">
            <h3>No practice questions yet</h3>
            <p className="panel-copy">The local practice database is empty right now.</p>
          </article>
        </section>
      );
    }

    if (practiceStage === "chapters" || practiceStage === "topics") {
      const topicQuestions = currentPracticeSubject?.questions ?? [];
      const chapters = Object.values(topicQuestions.reduce((groups, question) => {
        const chapterTitle = question.chapterTitle || "General Pathology";
        const chapterOrder = getPracticeChapterOrder({ ...question, chapterTitle }, currentPracticeSubject?.id);
        groups[chapterTitle] ??= { title: chapterTitle, order: chapterOrder, questions: [], topics: {} };
        groups[chapterTitle].order = Math.min(groups[chapterTitle].order, chapterOrder);
        groups[chapterTitle].questions.push(question);
        groups[chapterTitle].topics[question.topic] ??= { topic: question.topic, order: directoryOrder(question.topicOrder), questions: [] };
        groups[chapterTitle].topics[question.topic].order = Math.min(groups[chapterTitle].topics[question.topic].order, directoryOrder(question.topicOrder));
        groups[chapterTitle].topics[question.topic].questions.push(question);
        return groups;
      }, {})).sort(comparePracticeDirectoryEntries);

      if (practiceStage === "chapters") {
        return (
          <section className="app-view topic-wise-directory">
            <div className="view-header"><div><p className="eyebrow">Pathology · Topic Wise</p><h2>Choose a chapter</h2><p className="view-subtitle">Build mastery chapter by chapter. Your progress is saved automatically.</p></div><button className="button button-secondary" onClick={handleBackToPracticeDirectory}>Back to subjects</button></div>
            <div className="topic-directory-list">
              {chapters.map((chapter, index) => {
                const answered = chapter.questions.filter((question) => practiceProgress[question.id]).length;
                const percent = chapter.questions.length ? Math.round((answered / chapter.questions.length) * 100) : 0;
                return <button type="button" className="topic-directory-row chapter-directory-row" key={chapter.title} onClick={() => openPracticeChapter(chapter.title)}><span className="directory-index">{String(index + 1).padStart(2, "0")}</span><span className="directory-main"><span className="directory-kicker">Chapter {index + 1}</span><strong>{chapter.title}</strong><span className="directory-meta">{Object.keys(chapter.topics).length} topics · {chapter.questions.length} questions</span><span className="practice-progress-track"><span style={{ width: `${percent}%` }} /></span><span className="directory-progress-copy">{answered} of {chapter.questions.length} answered · {percent}% complete</span></span><span className="directory-arrow" aria-hidden="true">→</span></button>;
              })}
            </div>
          </section>
        );
      }

      const chapter = chapters.find((entry) => entry.title === selectedPracticeChapter);
      return (
        <section className="app-view topic-wise-directory">
          <div className="view-header"><div><p className="eyebrow">Chapter topics</p><h2>{chapter?.title ?? "Choose a topic"}</h2><p className="view-subtitle">Each topic contains a focused five-question competitive exam set.</p></div><button className="button button-secondary" onClick={() => setPracticeStage("chapters")}>Back to chapters</button></div>
          <div className="topic-directory-list">
            {Object.values(chapter?.topics ?? {}).sort(comparePracticeDirectoryEntries).map(({ topic, questions }, index) => {
              const answered = questions.filter((question) => practiceProgress[question.id]).length;
              const percent = questions.length ? Math.round((answered / questions.length) * 100) : 0;
              return <button type="button" className="topic-directory-row" key={topic} onClick={() => startTopicPractice(topic)}><span className="directory-index">{String(index + 1).padStart(2, "0")}</span><span className="directory-main"><span className="directory-kicker">Topic {index + 1}</span><strong>{topic}</strong><span className="directory-meta">{questions.length} questions · {answered} answered</span><span className="practice-progress-track"><span style={{ width: `${percent}%` }} /></span></span><span className="directory-arrow" aria-hidden="true">→</span></button>;
            })}
          </div>
        </section>
      );
    }
    if (practiceStage === "subject" && (!currentPracticeSubject || !currentPracticeQuestion)) {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>{selectedPracticeMode === "ai" ? "Topic-wise questions are not ready yet" : "No questions found"}</h2>
            </div>
            <button className="button button-secondary" onClick={() => selectedPracticeMode === "ai" ? setPracticeStage("topics") : handleBackToPracticeDirectory()}>
              {selectedPracticeMode === "ai" ? "Back to topics" : "Back to subjects"}
            </button>
          </div>

          <article className="card panel">
            <h3>{selectedPracticeMode === "ai" ? "Generate a 20-question set first" : "No practice questions yet"}</h3>
            <p className="panel-copy">
              {selectedPracticeMode === "ai"
                ? "Open the subject again and choose Topic Wise Questions."
                : "The PYQ database does not have questions for this subject yet."}
            </p>
          </article>
        </section>
      );
    }

    const totalQuestions = currentPracticeQuestions.length;
    const explanationText = formatExplanationText(
      currentPracticeQuestion.explanation || "Answer saved in the NEET PG question bank.",
    );

    if (practiceStage === "subject") {
      return (
        <section className="app-view practice-detail-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>
                {currentPracticeSubject.title}{" "}
                {selectedPracticeMode === "ai" ? "Topic Wise Questions" : currentPracticeQuestionSet?.title ?? "PYQ session"}
              </h2>
            </div>
            <button className="button button-secondary" onClick={() => selectedPracticeMode === "ai" ? setPracticeStage("topics") : handleBackToPracticeDirectory()}>
              {selectedPracticeMode === "ai" ? "Back to topics" : "Back to subjects"}
            </button>
          </div>

          <article className="card quiz-card practice-focus-card">
            <div className="practice-focus-topbar">
              <span className="practice-year-tag">
                {selectedPracticeMode === "ai"
                  ? activePracticeYear?.title ?? "Practice"
                  : currentPracticeQuestionSet?.title ?? "PYQ session"}
              </span>
              <span className={`rank-pill ${selectedPracticeMode === "ai" ? "source-ai" : "source-official"}`}>
                {selectedPracticeMode === "ai" ? "Topic Wise Questions" : "Official PYQ"}
              </span>
            </div>
            <div className="practice-question-status-strip" aria-label="Question progress">
              {currentPracticeQuestions.map((question, index) => {
                const questionProgress = practiceProgress[question.id];
                const isCurrent = index === practiceQuestionIndex;
                const isAnswered = Boolean(questionProgress);
                const wasCorrectLastTime = questionProgress?.correct === true;
                return (
                  <button
                    key={question.id}
                    type="button"
                    className={
                      "practice-question-status" +
                      (isCurrent ? " practice-question-status-current" : "") +
                      (isAnswered
                        ? wasCorrectLastTime
                          ? " practice-question-status-correct"
                          : " practice-question-status-wrong"
                        : "")
                    }
                    onClick={() => {
                      setPracticeQuestionIndex(index);
                      setSelectedOption("");
                      setSubmitted(false);
                      setPracticeQuestionStartedAt(Date.now());
                    }}
                    aria-label={
                      isAnswered
                        ? `Question ${index + 1}, last attempt ${wasCorrectLastTime ? "correct" : "wrong"}`
                        : `Question ${index + 1}, not attempted`
                    }
                    title={
                      isAnswered
                        ? `Question ${index + 1}: last attempt ${wasCorrectLastTime ? "correct" : "wrong"}`
                        : `Question ${index + 1}`
                    }
                  >
                    {isAnswered ? "✓" : index + 1}
                  </button>
                );
              })}
            </div>
            <div className="quiz-meta">
              <span>
                {selectedPracticeMode === "ai"
                  ? "Supplemental topic-wise practice"
                  : currentPracticeQuestion.examTitle ?? currentPracticeQuestionSet?.title ?? `${currentPracticeQuestion.year} PYQ`}
              </span>
              <span>{currentPracticeQuestion.topic}</span>
            </div>
            <h3>{currentPracticeQuestion.prompt}</h3>

            {currentPracticeQuestion.subtopic ? <p className="panel-copy">{currentPracticeQuestion.subtopic}</p> : null}

            {currentPracticeQuestion.imageUrls?.length ? (
              <div className="practice-question-images">
                {currentPracticeQuestion.imageUrls.map((imageUrl, index) => (
                  <img
                    key={`${currentPracticeQuestion.questionNumber}-${imageUrl}`}
                    className="practice-question-image"
                    src={getPracticeImageUrl(imageUrl)}
                    alt={`Question ${currentPracticeQuestion.questionNumber} visual ${index + 1}`}
                    loading="lazy"
                    decoding="async"
                  />
                ))}
              </div>
            ) : null}

            <div className="options-grid">
              {currentPracticeQuestion.options.map((option) => {
                const isActive = selectedOption === option;
                const isAnswer = submitted && option === currentPracticeQuestion.answer;
                const isWrong = submitted && isActive && option !== currentPracticeQuestion.answer;
                return (
                  <button
                    key={option}
                    className={
                      "option-card" +
                      (isActive ? " option-active" : "") +
                      (isAnswer ? " option-correct" : "") +
                      (isWrong ? " option-wrong" : "")
                    }
                    onClick={() => {
                      setSelectedOption(option);
                      setSubmitted(false);
                    }}
                    aria-pressed={isActive}
                  >
                    {option}
                  </button>
                );
              })}
            </div>

            <div className="practice-decision-row">
              <div className="confidence-selector" aria-label="Answer confidence">
                <span>Confidence</span>
                {["Low", "Medium", "High"].map((level) => (
                  <button key={level} type="button" className={answerConfidence === level ? "active" : ""} onClick={() => setAnswerConfidence(level)}>{level}</button>
                ))}
              </div>
              <button className={`flag-button${flaggedQuestions[currentPracticeQuestion.id] ? " active" : ""}`} type="button" onClick={() => setFlaggedQuestions((current) => ({ ...current, [currentPracticeQuestion.id]: !current[currentPracticeQuestion.id] }))}>
                {flaggedQuestions[currentPracticeQuestion.id] ? "Flagged for review" : "Flag for review"} <kbd>F</kbd>
              </button>
            </div>

            <div className="quiz-actions practice-sticky-actions">
              <button className="button button-primary" onClick={handleSubmitAnswer} disabled={!selectedOption}>
                Check answer <kbd>Enter</kbd>
              </button>
              <button
                className="button button-secondary"
                onClick={handleNextPracticeQuestion}
                disabled={practiceQuestionIndex === totalQuestions - 1}
              >
                {practiceQuestionIndex === totalQuestions - 1 ? "Last question" : "Next question"}
              </button>
            </div>

            {submitted ? (
              <div className={"feedback-box " + (isCorrect ? "feedback-good" : "feedback-bad")}>
                <strong>
                  {isCorrect ? "Correct." : "Not quite. Correct answer: " + currentPracticeQuestion.answer + "."}
                </strong>
                <details open><summary>Explanation</summary><p>{explanationText}</p></details>
              </div>
            ) : null}
          </article>
        </section>
      );
    }

    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Practice</p>
            <h2>{practiceLibrary.exam.title} by year and subject</h2>
          </div>
          <button className="button button-secondary" onClick={() => setActiveView("Dashboard")}>
            Back to dashboard
          </button>
        </div>

        {aiPracticeMessage ? <p className="form-message practice-ai-message">{aiPracticeMessage}</p> : null}

        {practiceChoiceSubject ? (
          <div className="practice-choice-backdrop" role="dialog" aria-modal="true" aria-labelledby="practice-choice-title">
            <article className="practice-choice-modal">
              <button className="practice-choice-close" type="button" onClick={closePracticeChoice} aria-label="Close practice chooser">
                x
              </button>
              <div className="practice-choice-heading">
                <div className="icon-badge green">MCQ</div>
                <div>
                  <h3 id="practice-choice-title">Practice {practiceChoiceSubject.title}</h3>
                  <p>Choose PYQs by exam year or practise topic-wise questions.</p>
                </div>
              </div>
              <div className="practice-year-picker">
                <div className="practice-choice-section-heading">
                  <strong>Previous Year Questions</strong>
                  <span>{practiceChoiceSubject.questions.length} official questions</span>
                </div>
                <div className="practice-year-choice-grid">
                  {practiceChoiceYearSets.map((yearSet) => (
                    <button
                      className="practice-year-choice-card"
                      type="button"
                      key={yearSet.id}
                      onClick={() => startPracticeSession(practiceChoiceSubject.id, "pyq", yearSet.id)}
                    >
                      <span className="practice-year-choice-topline">
                        <strong>{yearSet.title}</strong>
                        <small>{yearSet.total} Qs</small>
                      </span>
                      <span className="practice-year-choice-exams">
                        {yearSet.examTitles.slice(0, 2).join(" + ") || "Official PYQs"}
                      </span>
                      <span className="practice-progress-track" aria-hidden="true">
                        <span style={{ width: `${yearSet.progressPercent}%` }} />
                      </span>
                      <span className="practice-progress-copy">
                        {yearSet.answered} / {yearSet.total} answered
                      </span>
                    </button>
                  ))}
                </div>
              </div>
              <div className="practice-choice-grid practice-choice-grid-single">
                <button
                  className="practice-choice-card practice-choice-card-ai"
                  type="button"
                  disabled={aiPracticeBusy}
                  onClick={() => handleStartAiPractice(practiceChoiceSubject.id)}
                >
                  <span className="practice-choice-icon">TQ</span>
                  <strong>Topic Wise Questions</strong>
                  <p>Supplemental topic-wise questions</p>
                  <small>{practiceChoiceAiQuestionCount} questions</small>
                </button>
              </div>
            </article>
          </div>
        ) : null}

        <div className="practice-year-stack">
          {groupedPracticeYears.map((year) => (
            <section className="card panel practice-year-section" key={year.id}>
              <div className="panel-heading-split">
                <div>
                  <h3>{year.title}</h3>
                  <p className="panel-copy">{year.subtitle}</p>
                </div>
                <span className="rank-pill">{year.subjects.length} subjects</span>
              </div>

              <div className="practice-subject-grid">
                {year.subjects.map((subject) => {
                  const aiQuestionCount = aiPracticeQuestionCountsBySubject[subject.id] ?? 0;
                  return (
                    <button
                      key={subject.id}
                      className="practice-subject-card"
                      onClick={() => handleSelectPracticeSubject(subject.id)}
                    >
                      <span className="practice-subject-label">{subject.title}</span>
                      <p className="practice-subject-copy">Choose PYQs or practise topic-wise questions.</p>
                      <span className="practice-subject-counts">
                        <strong>{subject.questions.length} PYQs</strong>
                        <strong>{aiQuestionCount} Topic Wise</strong>
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ))}
          {supplementalAiPracticeSubjects.length ? (
            <section className="card panel practice-year-section">
              <div className="panel-heading-split">
                <div>
                  <h3>Topic-wise question banks</h3>
                  <p className="panel-copy">Supplemental subject-wise practice sets.</p>
                </div>
                <span className="rank-pill">{supplementalAiPracticeSubjects.length} subjects</span>
              </div>

              <div className="practice-subject-grid">
                {supplementalAiPracticeSubjects.map((subject) => {
                  const aiQuestionCount = subject.questions?.length ?? 0;
                  return (
                    <button
                      key={subject.id}
                      className="practice-subject-card"
                      onClick={() => handleSelectPracticeSubject(subject.id)}
                    >
                      <span className="practice-subject-label">{subject.title}</span>
                      <p className="practice-subject-copy">Practise topic-wise questions.</p>
                      <span className="practice-subject-counts">
                        <strong>{aiQuestionCount} Topic Wise</strong>
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ) : null}
        </div>
      </section>
    );
  }

  function renderLeaderboard() {
    const selectedStatePlayers = selectedStateEntry?.players ?? [];

    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Leaderboard</p>
            <h2>Weekly rankings</h2>
            <p className="panel-copy">National ranks and state ranks, sorted by score.</p>
          </div>
          <button className="button button-secondary" onClick={() => setActiveView("Compete")}>
            Join a challenge
          </button>
        </div>

        {liveLeaderboard.length >= 3 ? (
          <div className="leaderboard-podium" aria-label="Top three learners">
            {[liveLeaderboard[1], liveLeaderboard[0], liveLeaderboard[2]].map((player, index) => {
              const place = [2, 1, 3][index];
              return (
                <article className={`podium-card podium-${place}`} key={player.id || player.name}>
                  <span className="podium-medal" aria-label={`Rank ${place}`}>{place}</span>
                  <div className="podium-avatar">{getInitials(player.name)}</div>
                  <strong title={player.name}>{player.isCurrentUser ? "You" : player.name}</strong>
                  <small title={`${player.state}, ${player.college}`}>{player.state}</small>
                  <em>{player.score} pts</em>
                  <div className="podium-level">Level {Math.max(1, Math.floor(player.score / 250))}</div>
                </article>
              );
            })}
          </div>
        ) : null}

        <div className="leaderboard-shell">
          <article className="card panel leaderboard-panel leaderboard-national-panel">
            <div className="leaderboard-panel-head">
              <div>
                <h3>National</h3>
                <p className="panel-copy">{liveLeaderboard.length} ranked learners</p>
              </div>
              <span className="rank-pill">This week</span>
            </div>
            <div className="leaderboard-table" role="table" aria-label="National leaderboard">
              {liveLeaderboard.length ? (
                liveLeaderboard.slice(liveLeaderboard.length >= 3 ? 3 : 0).map((player) => (
                  <div
                    className={`leaderboard-table-row${player.isCurrentUser ? " leaderboard-self" : ""}`}
                    key={`${player.rank}-${player.name}`}
                    role="row"
                  >
                    <span className="leaderboard-rank" role="cell">#{player.rank}</span>
                    <div className="leaderboard-person" role="cell">
                      <div className="leaderboard-avatar">{getInitials(player.name)}</div>
                      <div>
                        <strong>{player.isCurrentUser ? "You" : player.name}</strong>
                        <p title={`${player.state}, ${player.college}`}>{player.state} | {player.college}</p>
                      </div>
                    </div>
                    <span className="leaderboard-streak" role="cell">{player.streak}d</span>
                    <strong className="leaderboard-score" role="cell">{player.score}</strong>
                  </div>
                ))
              ) : (
                <div className="empty-community-state empty-community-state-compact">
                  <h3>No ranked learners yet</h3>
                  <p className="panel-copy">The leaderboard will fill from real signed-up users.</p>
                </div>
              )}
              {liveLeaderboard.length > 0 && liveLeaderboard.length <= 3 ? (
                <p className="leaderboard-all-on-podium">All ranked learners are on the podium.</p>
              ) : null}
            </div>
          </article>

          <article className="card panel leaderboard-panel leaderboard-state-panel">
            <div className="leaderboard-panel-head">
              <div>
                <h3>State</h3>
                <p className="panel-copy">Click a state to rank its users.</p>
              </div>
              <span className="rank-pill">{selectedStatePlayers.length} players</span>
            </div>

            <div className="state-search-block">
              <input
                className="state-search-input"
                type="text"
                placeholder="Search state, for example Rajasthan or Karnataka"
                value={stateSearchTerm}
                onChange={(event) => setStateSearchTerm(event.target.value)}
              />
            </div>

            {filteredStateLeaderboard.length ? (
              <div className="state-chip-list" aria-label="States">
                {filteredStateLeaderboard.map((entry) => (
                  <button
                    type="button"
                    key={entry.state}
                    className={`state-rank-chip${selectedStateEntry?.state === entry.state ? " state-rank-chip-active" : ""}`}
                    onClick={() => setSelectedLeaderboardState(entry.state)}
                  >
                    <strong>{entry.state}</strong>
                    <span>{entry.players.length} players | top {entry.players[0]?.score ?? 0}</span>
                  </button>
                ))}
              </div>
            ) : (
              <div className="empty-community-state empty-community-state-compact">
                <h3>No state found</h3>
                <p className="panel-copy">Try a different state name.</p>
              </div>
            )}

            {selectedStateEntry ? (
              <div className="state-ranking-block">
                <h4>{selectedStateEntry.state}</h4>
                <div className="leaderboard-table leaderboard-table-compact" role="table" aria-label={`${selectedStateEntry.state} leaderboard`}>
                  {selectedStatePlayers.map((player, index) => (
                    <div
                      className={`leaderboard-table-row${player.isCurrentUser ? " leaderboard-self" : ""}`}
                      key={`${selectedStateEntry.state}-${player.name}`}
                      role="row"
                    >
                      <span className="leaderboard-rank" role="cell">#{index + 1}</span>
                      <div className="leaderboard-person" role="cell">
                        <div className="leaderboard-avatar">{getInitials(player.name)}</div>
                        <div>
                          <strong>{player.isCurrentUser ? "You" : player.name}</strong>
                          <p>{player.college}</p>
                        </div>
                      </div>
                      <span className="leaderboard-streak" role="cell">{player.streak}d</span>
                      <strong className="leaderboard-score" role="cell">{player.score}</strong>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </article>
        </div>
      </section>
    );
  }

  function renderCommunities() {
    if (communityStage === "direct" && selectedDirectConversation) {
      return (
        <section className="app-view community-detail-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Messages</p>
              <h2>{selectedDirectConversation.otherParticipant?.name ?? "Direct chat"}</h2>
              <p className="panel-copy">Personal study chats, quick check-ins, and direct 1v1 challenges.</p>
            </div>
            <button className="button button-secondary" onClick={handleBackToCommunityHub}>
              Back to community hub
            </button>
          </div>

          {directMessagesMessage ? <p className="form-message community-message-banner">{directMessagesMessage}</p> : null}

          <article className="card panel community-chat-shell">
            <div className="community-chat-header">
              <div>
                <p className="eyebrow">Message</p>
                <h3>{selectedDirectConversation.otherParticipant?.name ?? "Conversation"}</h3>
                <p className="panel-copy">{selectedDirectConversation.otherParticipant?.medicalCollege}</p>
              </div>
              <div className="community-header-actions">
                <span className="rank-pill">{selectedDirectConversation.otherParticipant?.rating ?? userRating} rating</span>
                <button className="button button-primary" onClick={handleDirectChallenge}>
                  Challenge to 1v1
                </button>
              </div>
            </div>

            <div className="community-chat-meta">
              <span>State: {selectedDirectConversation.otherParticipant?.state ?? "Registered users"}</span>
              <span>Streak: {selectedDirectConversation.otherParticipant?.streak ?? 1} days</span>
            </div>

            <div className="community-chat-body community-chat-shell-body">
              <div className="community-messages-panel">
                <div className="community-messages">
                  {selectedDirectConversation.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`community-message${message.isOwnMessage ? " community-message-own" : ""}`}
                    >
                      <div className={`community-message-bubble${message.type === "challenge" ? " community-message-challenge" : ""}`}>
                        {message.userId ? (
                          <button
                            type="button"
                            className="community-message-profile-button"
                            onClick={() => openPublicProfile(message.userId, "Communities")}
                          >
                            {message.userName}
                          </button>
                        ) : (
                          <strong>{message.userName}</strong>
                        )}
                        <p>{message.text}</p>
                        <span>{formatCommunityTimestamp(message.createdAt)}</span>
                      </div>
                    </div>
                  ))}
                </div>

                <form className="community-chat-form" onSubmit={handleSendDirectMessage}>
                  <input
                    type="text"
                    value={directMessageDraft}
                    onChange={(event) => setDirectMessageDraft(event.target.value)}
                    placeholder="Write a message..."
                  />
                  <button className="button button-primary" type="submit">
                    Send
                  </button>
                </form>
              </div>

              <aside className="community-members-panel community-sidecard">
                <div className="panel-heading-split">
                  <div>
                    <h4>Profile snapshot</h4>
                    <p className="panel-copy">Jump to profile details or launch a duel directly from here.</p>
                  </div>
                </div>
                <div className="community-member-list">
                  <div className="community-member-row">
                    <button
                      type="button"
                      className="community-member-trigger"
                      onClick={() => openPublicProfile(selectedDirectConversation.otherParticipant?.id, "Communities")}
                    >
                      <div className="community-member-main">
                        <div className="avatar community-member-avatar">
                          {selectedDirectConversation.otherParticipant?.profileImageUrl ? (
                            <img
                              className="avatar-image"
                              src={selectedDirectConversation.otherParticipant.profileImageUrl}
                              alt={`${selectedDirectConversation.otherParticipant.name} profile`}
                            />
                          ) : (
                            <span>{getInitials(selectedDirectConversation.otherParticipant?.name)}</span>
                          )}
                        </div>
                        <div>
                          <strong>{selectedDirectConversation.otherParticipant?.name}</strong>
                          <p>{selectedDirectConversation.otherParticipant?.medicalCollege}</p>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>
              </aside>
            </div>
          </article>
        </section>
      );
    }

    if (communityStage === "detail" && selectedCommunity) {
      const communityMessageIds = new Set(selectedCommunity.messages.map((message) => message.id));
      const communityThreadPosts = selectedCommunity.messages.filter(
        (message) => !message.parentMessageId || !communityMessageIds.has(message.parentMessageId),
      );
      const repliesByParent = selectedCommunity.messages.reduce((threads, message) => {
        if (!message.parentMessageId) return threads;
        threads[message.parentMessageId] = [...(threads[message.parentMessageId] ?? []), message];
        return threads;
      }, {});
      const communityThreadWordCount = countWords(communityMessageDraft);

      return (
        <section className="app-view community-detail-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Communities</p>
              <h2>{selectedCommunity.name}</h2>
              <p className="panel-copy">A focused feed of questions, clinical takes, and threaded replies.</p>
            </div>
            <button className="button button-secondary" onClick={handleBackToCommunityHub}>
              Back to community hub
            </button>
          </div>

          {communitiesMessage ? <p className="form-message community-message-banner">{communitiesMessage}</p> : null}

          <article className="card panel community-chat-shell">
            <div className="community-chat-header">
              <div>
                <p className="eyebrow">Community threads</p>
                <h3>{selectedCommunity.name}</h3>
                <p className="panel-copy">{selectedCommunity.description}</p>
              </div>
              <div className="community-header-actions">
                <span className="rank-pill">{selectedCommunity.memberCount} members</span>
                {selectedCommunity.isAdmin ? (
                  <button
                    className="button button-secondary"
                    type="button"
                    onClick={() => handleCopyCommunityInvite(selectedCommunity.id)}
                  >
                    Copy invite link
                  </button>
                ) : null}
                {!selectedCommunity.isMember ? (
                  <button className="button button-primary" onClick={() => handleJoinCommunity(selectedCommunity.id)}>
                    Join community
                  </button>
                ) : null}
              </div>
            </div>

            <div className="community-chat-meta">
              <span>Topic: {selectedCommunity.topic}</span>
              <span>Admin: {selectedCommunity.adminName}</span>
              <span>{communityThreadPosts.length} threads</span>
            </div>

            <div className="community-chat-body community-chat-shell-body">
              <div className="community-messages-panel community-thread-panel">
                {selectedCommunity.isMember ? (
                  <form className="community-thread-composer" onSubmit={(event) => handleSendCommunityMessage(event)}>
                    <div className="avatar community-thread-avatar">
                      {user?.profileImageUrl ? <img className="avatar-image" src={user.profileImageUrl} alt="" /> : <span>{getInitials(user?.name)}</span>}
                    </div>
                    <div className="community-thread-composer-main">
                      <textarea
                        rows="3"
                        value={communityMessageDraft}
                        onChange={(event) => setCommunityMessageDraft(event.target.value)}
                        placeholder="Share a question, clinical pearl, or study update..."
                      />
                      {communityThreadImage ? (
                        <div className="community-thread-image-preview">
                          <img src={communityThreadImage.dataUrl} alt="Thread attachment preview" />
                          <button type="button" onClick={() => setCommunityThreadImage(null)} aria-label="Remove attached image">×</button>
                          <span>{communityThreadImage.name}</span>
                        </div>
                      ) : null}
                      <div>
                        <div className="community-thread-composer-tools">
                          <label className="community-thread-image-button">
                            <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={handleCommunityThreadImageChange} />
                            <span aria-hidden="true">▧</span> Add image
                          </label>
                          <span className={communityThreadWordCount > COMMUNITY_THREAD_WORD_LIMIT ? "community-word-count-over" : ""}>
                            {communityThreadWordCount}/{COMMUNITY_THREAD_WORD_LIMIT} words
                          </span>
                        </div>
                        <button
                          className="button button-primary"
                          type="submit"
                          disabled={(!communityMessageDraft.trim() && !communityThreadImage) || communityThreadWordCount > COMMUNITY_THREAD_WORD_LIMIT}
                        >
                          Post thread
                        </button>
                      </div>
                    </div>
                  </form>
                ) : (
                  <div className="feedback-box feedback-bad">
                    <strong>Join this group to publish and reply.</strong>
                    <p>You can still preview its threads, members, and discussion style before joining.</p>
                  </div>
                )}

                <div className="community-thread-feed-heading">
                  <div><h4>Latest threads</h4><span>Newest conversations first</span></div>
                  <span>{communityThreadPosts.length}</span>
                </div>

                <div className="community-thread-feed">
                  {[...communityThreadPosts].reverse().map((message) => {
                    const replies = repliesByParent[message.id] ?? [];
                    const isExpanded = Boolean(expandedCommunityThreads[message.id]);
                    return (
                      <article className="community-thread-card" key={message.id}>
                        <div className="avatar community-thread-avatar"><span>{getInitials(message.userName)}</span></div>
                        <div className="community-thread-content">
                          <div className="community-thread-author">
                            {message.userId ? (
                              <button type="button" onClick={() => openPublicProfile(message.userId, "Communities")}>{message.userName}</button>
                            ) : <strong>{message.userName}</strong>}
                            {message.isOwnMessage ? <span>You</span> : null}
                            <time>{formatCommunityTimestamp(message.createdAt)}</time>
                          </div>
                          {message.text ? <p>{message.text}</p> : null}
                          {message.imageUrl ? (
                            <a className="community-thread-image" href={message.imageUrl} target="_blank" rel="noreferrer">
                              <img src={message.imageUrl} alt={"Attached to " + message.userName + "'s thread"} />
                            </a>
                          ) : null}
                          <div className="community-thread-actions">
                            <button
                              type="button"
                              onClick={() => toggleCommunityThread(message.id, true)}
                              disabled={!selectedCommunity.isMember}
                              title={selectedCommunity.isMember ? "Reply to this thread" : "Join the community to reply"}
                            >
                              <span aria-hidden="true">↩</span> Reply
                            </button>
                            <button type="button" onClick={() => toggleCommunityThread(message.id)} disabled={!replies.length}>
                              <span aria-hidden="true">◯</span> {replies.length} {replies.length === 1 ? "reply" : "replies"}
                            </button>
                          </div>

                          {isExpanded ? (
                            <div className="community-thread-replies">
                              {replies.map((reply) => (
                                <div className="community-thread-reply" key={reply.id}>
                                  <div className="avatar community-thread-reply-avatar"><span>{getInitials(reply.userName)}</span></div>
                                  <div>
                                    <div className="community-thread-author">
                                      {reply.userId ? <button type="button" onClick={() => openPublicProfile(reply.userId, "Communities")}>{reply.userName}</button> : <strong>{reply.userName}</strong>}
                                      {reply.isOwnMessage ? <span>You</span> : null}
                                      <time>{formatCommunityTimestamp(reply.createdAt)}</time>
                                    </div>
                                    <p>{reply.text}</p>
                                  </div>
                                </div>
                              ))}
                              {selectedCommunity.isMember ? (
                                <form className="community-thread-reply-form" onSubmit={(event) => handleSendCommunityMessage(event, message.id)}>
                                  <div className="avatar community-thread-reply-avatar"><span>{getInitials(user?.name)}</span></div>
                                  <input
                                    type="text"
                                    value={communityReplyDrafts[message.id] ?? ""}
                                    onChange={(event) => setCommunityReplyDrafts((current) => ({ ...current, [message.id]: event.target.value }))}
                                    placeholder={`Reply to ${message.userName}...`}
                                  />
                                  <button className="button button-primary" type="submit" disabled={!(communityReplyDrafts[message.id] ?? "").trim()}>Reply</button>
                                </form>
                              ) : null}
                            </div>
                          ) : null}
                        </div>
                      </article>
                    );
                  })}
                  {!communityThreadPosts.length ? (
                    <div className="empty-community-state empty-community-state-compact">
                      <h3>No threads yet</h3>
                      <p className="panel-copy">Start the first conversation in this room.</p>
                    </div>
                  ) : null}
                </div>
              </div>

              <aside className="community-members-panel community-sidecard">
                <div className="panel-heading-split">
                  <div>
                    <h4>Members</h4>
                    <p className="panel-copy">See who is studying inside this room right now.</p>
                  </div>
                  <span className="rank-pill">{selectedCommunity.memberCount}</span>
                </div>
                <div className="community-member-list">
                  {selectedCommunity.members.map((member) => (
                    <div className="community-member-row" key={member.id}>
                      <button
                        type="button"
                        className="community-member-trigger"
                        onClick={() => openPublicProfile(member.id, "Communities")}
                      >
                        <div className="community-member-main">
                          <div className="avatar community-member-avatar">
                            {member.profileImageUrl ? (
                              <img className="avatar-image" src={member.profileImageUrl} alt={`${member.name} profile`} />
                            ) : (
                              <span>{getInitials(member.name)}</span>
                            )}
                          </div>
                          <div>
                            <strong>
                              {member.id === selectedCommunity.adminUserId ? `${member.name} (Admin)` : member.name}
                            </strong>
                            <p>{member.medicalCollege}</p>
                          </div>
                        </div>
                      </button>
                      {selectedCommunity.isAdmin && member.id !== selectedCommunity.adminUserId ? (
                        <div className="community-member-actions">
                          <button
                            className="button button-secondary community-remove-button"
                            onClick={() => handleOpenDirectChat(member.id)}
                          >
                            Message
                          </button>
                          <button
                            className="button button-secondary community-remove-button"
                            onClick={() => handleRemoveCommunityMember(selectedCommunity.id, member.id)}
                          >
                            Remove
                          </button>
                        </div>
                      ) : member.id !== user?.id ? (
                        <button className="button button-secondary community-remove-button" onClick={() => handleOpenDirectChat(member.id)}>
                          Message
                        </button>
                      ) : null}
                    </div>
                  ))}
                </div>
              </aside>
            </div>
          </article>
        </section>
      );
    }

    const joinedCommunities = communities.filter((community) => community.isMember);
    const totalCommunityMembers = communities.reduce((total, community) => total + (community.memberCount ?? 0), 0);
    const totalCommunityMessages = communities.reduce((total, community) => total + (community.messages?.length ?? 0), 0);

    return (
      <section className="app-view community-hub-view">
        <header className="community-landing-hero">
          <div className="community-hero-orb community-hero-orb-large" aria-hidden="true" />
          <div className="community-hero-orb community-hero-orb-small" aria-hidden="true" />
          <div className="community-hero-content">
            <p className="community-hero-kicker"><span /> MediComm community</p>
            <h2>Study together.<br />Get better, faster.</h2>
            <p>Find focused rooms, trade clinical insights, and keep your closest study partners one message away.</p>
            <div className="community-hero-actions">
              <button
                className="button community-hero-primary"
                onClick={() => document.getElementById("community-groups")?.scrollIntoView({ behavior: "smooth" })}
              >
                Explore study rooms
              </button>
              <button
                className="button community-hero-secondary"
                onClick={() => document.getElementById("community-create")?.scrollIntoView({ behavior: "smooth" })}
              >
                Start a community
              </button>
            </div>
          </div>
          <div className="community-hero-note" aria-label="Community status">
            <span className="community-live-dot" />
            <div><strong>Peer learning is live</strong><small>{joinedCommunities.length} of your rooms are ready</small></div>
          </div>
        </header>

        {communitiesMessage ? <p className="form-message community-message-banner">{communitiesMessage}</p> : null}
        {directMessagesMessage ? <p className="form-message community-message-banner">{directMessagesMessage}</p> : null}

        <div className="community-stat-grid" aria-label="Community overview">
          <div><span>Members across rooms</span><strong>{formatStatValue(totalCommunityMembers)}</strong><small>learning together</small></div>
          <div><span>Study rooms</span><strong>{communities.length}</strong><small>{joinedCommunities.length} joined by you</small></div>
          <div><span>Discussion posts</span><strong>{formatStatValue(totalCommunityMessages)}</strong><small>shared insights</small></div>
          <div><span>Personal chats</span><strong>{directConversations.length}</strong><small>private and focused</small></div>
        </div>

        <div className="community-landing-grid">
          <article className="community-directory-panel community-groups-panel" id="community-groups">
            <div className="panel-heading-split">
              <div>
                <p className="community-section-kicker">Discover</p>
                <h3>Study rooms worth joining</h3>
                <p className="panel-copy">Subject-led groups for questions, cases, resources, and the occasional pre-exam rescue mission.</p>
              </div>
              <button className="community-text-button" type="button" onClick={() => fetchCommunities()}>Refresh rooms <span aria-hidden="true">↻</span></button>
            </div>
            {communitiesBusy ? <p className="panel-copy">Loading communities...</p> : null}

            {communities.length ? (
              <div className="community-directory-grid">
              {communities.map((community) => (
                <article
                  key={community.id}
                  className={`community-directory-card${selectedCommunity?.id === community.id ? " community-directory-card-active" : ""}`}
                >
                  <div className="community-top">
                    <div className="community-room-avatar">{getInitials(community.name)}</div>
                    <div className="community-room-presence"><span /> {community.memberCount} members</div>
                  </div>
                  <div className="community-room-tags">
                    <span>{community.topic}</span>
                    {community.isMember ? <span className="community-room-tag-joined">Joined</span> : null}
                  </div>
                  <strong>{community.name}</strong>
                  <p>{community.description}</p>
                  <div className="community-list-meta">
                    <span>Hosted by <b>{community.adminName}</b></span>
                    <span>{community.messages?.length ?? 0} posts</span>
                  </div>
                  <div className="community-directory-actions">
                    <span className={`community-status-pill${community.isMember ? " community-status-pill-joined" : ""}`}>
                      {community.isAdmin ? "Admin" : community.isMember ? "Joined" : "Open"}
                    </span>
                    {community.isAdmin ? (
                      <button
                        className="button button-secondary"
                        type="button"
                        onClick={() => handleCopyCommunityInvite(community.id)}
                      >
                        Copy invite
                      </button>
                    ) : null}
                    <button className="button community-room-button" onClick={() => openCommunityChat(community.id)}>
                      View room <span aria-hidden="true">→</span>
                    </button>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-community-state">
              <h3>No communities yet</h3>
              <p className="panel-copy">Create the first community to start group discussion and member-led study chats.</p>
            </div>
          )}
          </article>

          <aside className="community-landing-sidebar">
            <article className="community-inbox-panel" id="personal-inbox">
              <div className="community-inbox-heading">
                <div>
                  <p className="community-section-kicker">Personal</p>
                  <h3>Your inbox</h3>
                  <p>Study partners, without the group-chat noise.</p>
                </div>
                <span>{directConversations.length}</span>
              </div>

              <label className="community-user-search">
                <span className="sr-only">Search users</span>
                <span aria-hidden="true">⌕</span>
                <input
                  type="text"
                  value={directSearchTerm}
                  onChange={(event) => setDirectSearchTerm(event.target.value)}
                  placeholder="Find a learner to message"
                />
              </label>
              {directSearchBusy ? <p className="community-search-hint">Searching learners...</p> : null}
              {directSearchTerm.trim().length > 0 && directSearchTerm.trim().length < 2 ? (
                <p className="community-search-hint">Type at least 2 characters to search.</p>
              ) : null}

              {directSearchResults.length ? (
                <div className="community-search-results">
                  <p>People</p>
                  {directSearchResults.map((result) => (
                    <button type="button" key={result.id} onClick={() => handleOpenDirectChat(result.id)}>
                      <div className="avatar community-member-avatar">
                        {result.profileImageUrl ? <img className="avatar-image" src={result.profileImageUrl} alt="" /> : <span>{getInitials(result.name)}</span>}
                      </div>
                      <span><strong>{result.name}</strong><small>{result.medicalCollege}</small></span>
                      <b>Message</b>
                    </button>
                  ))}
                </div>
              ) : null}

              <div className="community-inbox-list">
                {directMessagesBusy ? <p className="community-search-hint">Loading messages...</p> : null}
                {directConversations.length ? directConversations.map((conversation) => {
                  const participant = conversation.otherParticipant;
                  const latestMessage = conversation.messages.at(-1);
                  return (
                    <button type="button" key={conversation.id} onClick={() => openDirectConversation(conversation.id)}>
                      <div className="avatar community-inbox-avatar">
                        {participant?.profileImageUrl ? <img className="avatar-image" src={participant.profileImageUrl} alt="" /> : <span>{getInitials(participant?.name)}</span>}
                        <i aria-hidden="true" />
                      </div>
                      <span className="community-inbox-copy">
                        <span><strong>{participant?.name ?? "Private chat"}</strong><time>{formatCommunityTimestamp(latestMessage?.createdAt)}</time></span>
                        <small>{latestMessage?.text ?? "Start the conversation"}</small>
                      </span>
                      <span className="community-inbox-arrow" aria-hidden="true">›</span>
                    </button>
                  );
                }) : (
                  <div className="empty-community-state empty-community-state-compact">
                    <h3>Your inbox is ready</h3>
                    <p className="panel-copy">Search for a learner above and start a focused study chat.</p>
                  </div>
                )}
              </div>
            </article>

            <article className="community-create-panel" id="community-create">
              <div className="community-create-heading">
                <div className="community-create-icon">+</div>
                <div><p className="community-section-kicker">Lead a room</p><h3>Create a community</h3></div>
              </div>
              <p className="panel-copy">Build the study space you wish already existed. You’ll be its admin.</p>
              <form className="profile-form community-create-form" onSubmit={handleCreateCommunity}>
                <label className="field">
                  <span>Community name</span>
                  <input type="text" value={createCommunityForm.name} onChange={(event) => updateCreateCommunityField("name", event.target.value)} placeholder="Ex: Final Year Surgery Prep" />
                </label>
                <label className="field">
                  <span>Topic</span>
                  <input type="text" value={createCommunityForm.topic} onChange={(event) => updateCreateCommunityField("topic", event.target.value)} placeholder="Ex: Case discussions" />
                </label>
                <label className="field">
                  <span>Description</span>
                  <input type="text" value={createCommunityForm.description} onChange={(event) => updateCreateCommunityField("description", event.target.value)} placeholder="What should members expect?" />
                </label>
                <button className="button button-primary" type="submit">Create my community <span aria-hidden="true">→</span></button>
              </form>
            </article>
          </aside>
        </div>
      </section>
    );
  }

  function renderCompete() {
    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Compete</p>
            <h2>Live challenges and rated duels</h2>
          </div>
          <button className="button button-primary" onClick={() => setActiveView("Practice")}>
            Warm up first
          </button>
        </div>

        {duelStatus === "idle" ? renderDuelLobby() : null}
        {duelStatus === "matchmaking" ? renderMatchmaking() : null}
        {duelStatus === "live" ? renderLiveDuel() : null}
        {duelStatus === "finished" ? renderDuelResult() : null}
        {duelMessage ? <p className="form-message duel-message">{duelMessage}</p> : null}

        {duelStatus === "idle" ? (
          <div className="community-grid extra-top-gap">
            <article className="card community-card">
              <div className="community-top">
                <div className="icon-badge purple">VS</div>
                <span>{formatStatValue(platformSummary.users)} registered learners</span>
              </div>
              <h3>Real-user rated duels</h3>
              <p>Your rating, rank, attempts, and accuracy update from completed practice and duel activity.</p>
              <button className="button button-primary" onClick={() => setActiveView("Leaderboard")}>
                View live ranks
              </button>
            </article>
            <article className="card community-card">
              <div className="community-top">
                <div className="icon-badge cyan">MCQ</div>
                <span>{formatStatValue(platformSummary.attemptedQuestions)} attempts</span>
              </div>
              <h3>Practice activity</h3>
              <p>The challenge surface now reflects real attempts saved from user activity.</p>
              <button className="button button-secondary" onClick={() => setActiveView("Practice")}>
                Practice questions
              </button>
            </article>
          </div>
        ) : null}
      </section>
    );
  }

  function renderDuelLobby() {
    return (
      <article className="card panel duel-matchmaking">
        <div className="panel-heading-split">
          <div>
            <h3>Rated 1v1 duel</h3>
            <p className="panel-copy">Face a live opponent, answer fast, and push your MediComm rating higher.</p>
          </div>
          <span className="rank-pill">Current rating {userRating}</span>
        </div>

        <div className="duel-stats">
          <div className="duel-stat">
            <span>Format</span>
            <strong>{duelQuestions.length} timed MCQs</strong>
          </div>
          <div className="duel-stat">
            <span>Duration</span>
            <strong>{Math.floor(DUEL_DURATION_SECONDS / 60)} min duel</strong>
          </div>
          <div className="duel-stat">
            <span>Scoring</span>
            <strong>Server Elo update</strong>
          </div>
        </div>

        <div className="quiz-actions">
          <button className="button button-primary" onClick={() => startDuel()}>
            Start rated duel
          </button>
          <button className="button button-secondary" onClick={startBotDuel}>
            Compete with bot
          </button>
          <button className="button button-secondary" onClick={() => setActiveView("Practice")}>
            Practice first
          </button>
        </div>
      </article>
    );
  }

  function renderMatchmaking() {
    return (
      <article className="card panel duel-matchmaking duel-waiting-room">
        <div className="duel-radar" aria-hidden="true">
          <span />
          <span />
          <div className="duel-radar-core">VS</div>
        </div>
        <p className="eyebrow">Rated queue</p>
        <h3>Waiting for another challenger</h3>
        <p className="panel-copy">
          You are locked into the live waiting list. The duel will start automatically as soon as one more learner presses
          Start rated duel.
        </p>
        <div className="duel-waiting-grid">
          <div>
            <span>Queue status</span>
            <strong>{duelQueueInfo?.ticketId ? "Ready" : "Joining..."}</strong>
          </div>
          <div>
            <span>Waiting now</span>
            <strong>{duelQueueInfo?.waitingCount ?? 1}</strong>
          </div>
          <div>
            <span>Your rating</span>
            <strong>{userRating}</strong>
          </div>
        </div>
        <div className="duel-waiting-pulse">
          <span />
          <span />
          <span />
        </div>
        <div className="quiz-actions centered-actions">
          <button className="button button-secondary" onClick={leaveDuelQueue}>
            Leave queue
          </button>
        </div>
      </article>
    );
  }

  function renderLiveDuel() {
    const currentDuelImageUrls = getQuestionImageUrls(currentDuelQuestion);

    return (
      <section className="duel-live">
        <div className="duel-scoreboard">
          <div className="duel-player">
            <p>You</p>
            <strong>{user?.name ?? "Player"}</strong>
            <span className="panel-copy">{userDuelAnswered} locked</span>
          </div>
          <div className="duel-timer">
            <p>Time left</p>
            <strong>{formatDuration(duelTimeLeft)}</strong>
          </div>
          <div className="duel-player">
            <p>Opponent</p>
            <strong>{duelOpponent?.name ?? "Matching..."}</strong>
            <span className="panel-copy">
              {duelOpponent?.ratingless ? "Ratingless" : `${duelOpponentProgress.correct} correct`}
            </span>
          </div>
        </div>

        <article className="card panel duel-quiz">
          <div className="panel-heading-split">
            <div>
              <h3>{currentDuelQuestion.prompt}</h3>
              <p className="panel-copy">
                Question {duelIndex + 1} of {duelQuestions.length}
              </p>
            </div>
            <span className="rank-pill">{duelMode === "bot" ? "Bot practice" : "Rated"}</span>
          </div>

          {currentDuelImageUrls.length ? (
            <div className="practice-question-images duel-question-images">
              {currentDuelImageUrls.map((imageUrl, index) => (
                <img
                  key={`${currentDuelQuestion.id}-${imageUrl}`}
                  className="practice-question-image duel-question-image"
                  src={getPracticeImageUrl(imageUrl)}
                  alt={`Compete question ${duelIndex + 1} visual ${index + 1}`}
                />
              ))}
            </div>
          ) : null}

          <div className="options-grid">
            {currentDuelQuestion.options.map((option) => {
              const isActive = currentDuelSelection === option;
              return (
                <button
                  key={option}
                  className={
                    "option-card" +
                    (isActive ? " option-active" : "")
                  }
                  onClick={() => {
                    if (currentDuelSubmitted) return;
                    setDuelSelections((current) => ({ ...current, [duelIndex]: option }));
                  }}
                >
                  {option}
                </button>
              );
            })}
          </div>

          <div className="quiz-actions">
            <button className="button button-primary" onClick={submitDuelAnswer} disabled={!currentDuelSelection || currentDuelSubmitted}>
              {currentDuelSubmitted ? "Locked" : "Lock answer"}
            </button>
            <button className="button button-secondary" onClick={nextDuelQuestion} disabled={!currentDuelSubmitted}>
              {duelIndex === duelQuestions.length - 1 ? "Finish duel" : "Next question"}
            </button>
            <button className="button button-secondary" onClick={forfeitDuel}>
              End match
            </button>
          </div>

          {currentDuelSubmitted ? (
            <div className="feedback-box feedback-good">
              <strong>Answer locked in.</strong>
              <p>Final score is verified by the server after the duel.</p>
            </div>
          ) : null}
        </article>
      </section>
    );
  }

  function renderDuelResult() {
    return (
      <article className="card panel duel-result">
        <div className="panel-heading-split">
          <div>
            <p className="eyebrow">Result</p>
            <h3>
              {duelResult?.forfeited
                ? "You forfeited the duel"
                : duelResult?.verdict === "win"
                ? "You won the duel"
                : duelResult?.verdict === "loss"
                  ? "You lost the duel"
                  : "The duel ended in a draw"}
            </h3>
          </div>
          <span className="rank-pill">
            {duelResult?.ratingAffected === false
              ? "Ratingless"
              : duelResult
                ? `${duelResult.delta > 0 ? "+" : ""}${duelResult.delta} rating`
                : "Rated"}
          </span>
        </div>

        <div className="duel-result-grid">
          <div>
            <span>Your score</span>
            <strong>{duelResult?.userScore ?? userDuelScore}</strong>
          </div>
          <div>
            <span>Opponent score</span>
            <strong>{duelResult?.opponentScore ?? duelOpponentProgress.correct}</strong>
          </div>
          <div>
            <span>New rating</span>
            <strong>{duelResult?.nextRating ?? userRating}</strong>
          </div>
        </div>

        <div className="quiz-actions">
          <button className="button button-primary" onClick={resetDuel}>
            Duel again
          </button>
          <button className="button button-secondary" onClick={() => setActiveView("Leaderboard")}>
            View leaderboard
          </button>
        </div>
      </article>
    );
  }

  function renderPublicProfile() {
    const previewImage = publicProfile?.profileImageUrl;

    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Profile</p>
            <h2>{publicProfile?.isCurrentUser ? "Your account information" : "User profile"}</h2>
          </div>
          <button className="button button-secondary" onClick={closePublicProfile}>
            Back
          </button>
        </div>

        {publicProfileMessage ? <p className="form-message">{publicProfileMessage}</p> : null}

        {publicProfileBusy ? (
          <article className="card panel public-profile-loading">
            <div className="duel-loader" />
            <p className="panel-copy">Loading profile...</p>
          </article>
        ) : publicProfile ? (
          <div className="content-grid profile-layout">
            <article className="card panel profile-photo-card">
              <h3>Profile picture</h3>
              <div className="profile-avatar-xl">
                {previewImage ? (
                  <img className="avatar-image" src={previewImage} alt={`${publicProfile.name} profile`} />
                ) : (
                  <span>{getInitials(publicProfile.name)}</span>
                )}
              </div>
              <p className="panel-copy">{publicProfile.name}</p>
            </article>

            <article className="card panel">
              <h3>Academic snapshot</h3>
              <div className="stack-list">
                <div className="stack-row">
                  <span>Medical college</span>
                  <strong>{publicProfile.medicalCollege}</strong>
                </div>
                <div className="stack-row">
                  <span>State</span>
                  <strong>{publicProfile.state}</strong>
                </div>
                <div className="stack-row">
                  <span>Rating</span>
                  <strong>{publicProfile.rating}</strong>
                </div>
                <div className="stack-row">
                  <span>Streak</span>
                  <strong>{publicProfile.streak} days</strong>
                </div>
                <div className="stack-row">
                  <span>Member since</span>
                  <strong>{new Date(publicProfile.createdAt).toLocaleDateString()}</strong>
                </div>
              </div>
            </article>
          </div>
        ) : null}
      </section>
    );
  }

  function renderProfile() {
    const previewImage = profileState.profileImageDataUrl || user?.profileImageUrl;

    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Profile</p>
            <h2>Your account information</h2>
          </div>
          <button className="button button-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>

        <div className="content-grid profile-layout">
          <article className="card panel profile-photo-card">
            <h3>Profile picture</h3>
            <div className="profile-avatar-xl">
              {previewImage ? (
                <img className="avatar-image" src={previewImage} alt={`${user?.name} profile`} />
              ) : (
                <span>{getInitials(user?.name)}</span>
              )}
            </div>
            <label className="button button-secondary upload-button">
              Change photo
              <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={handleProfilePhotoChange} />
            </label>
            <p className="panel-copy">Upload an image, then save profile to update the account avatar everywhere.</p>
          </article>

          <article className="card panel">
            <h3>Your standing</h3>
            <div className="stack-list">
              <div className="stack-row">
                <span>National rank</span>
                <strong>#{currentUserLeaderboardEntry?.rank ?? "-"}</strong>
              </div>
              <div className="stack-row">
                <span>{currentUserLeaderboardEntry?.state ?? "State"} rank</span>
                <strong>#{currentUserStateRank ?? "-"}</strong>
              </div>
              <div className="stack-row">
                <span>Rating</span>
                <strong>{userRating}</strong>
              </div>
              <div className="stack-row">
                <span>Streak</span>
                <strong>{user?.streak ?? 1} days</strong>
              </div>
            </div>
          </article>

          <article className="card panel">
            <h3>Personal details</h3>
            <form className="profile-form" onSubmit={handleProfileSave}>
              <label className="field">
                <span>Name</span>
                <input
                  type="text"
                  value={profileState.name}
                  onChange={(event) => updateProfileField("name", event.target.value)}
                />
              </label>
              <label className="field">
                <span>Email</span>
                <input type="email" value={user?.email ?? ""} disabled />
              </label>
              <label className="field">
                <span>Medical college</span>
                <input
                  type="text"
                  value={profileState.medicalCollege}
                  onChange={(event) => updateProfileField("medicalCollege", event.target.value)}
                />
              </label>
              <label className="field">
                <span>Contact number</span>
                <input
                  type="tel"
                  value={profileState.contactNumber}
                  onChange={(event) => updateProfileField("contactNumber", event.target.value)}
                />
              </label>

              {profileMessage ? <p className="form-message">{profileMessage}</p> : null}

              <button className="button button-primary" type="submit" disabled={profileBusy}>
                {profileBusy ? "Saving..." : "Save profile"}
              </button>
            </form>
          </article>
        </div>
      </section>
    );
  }

  function renderAnalyticsFunctional() {
    const cutoff = Date.now() - analyticsPeriod * 86400000;
    const events = analyticsEvents.filter((item) => new Date(item.answeredAt).getTime() >= cutoff);
    const correct = events.filter((item) => item.correct).length;
    const periodAccuracy = calculateAccuracy(correct, events.length);
    const seconds = events.reduce((sum, item) => sum + (Number(item.durationSeconds) || 0), 0);
    const subjects = [...events.reduce((map, item) => {
      const id = item.subjectId || "unknown";
      const value = map.get(id) || { id, name: item.subject || practiceSubjects.find((subject) => subject.id === id)?.title || "Other", attempts: 0, correct: 0, topics: {} };
      value.attempts += 1;
      value.correct += item.correct ? 1 : 0;
      if (!item.correct) value.topics[item.topic || "General review"] = (value.topics[item.topic || "General review"] || 0) + 1;
      map.set(id, value);
      return map;
    }, new Map()).values()].map((item) => ({ ...item, accuracy: calculateAccuracy(item.correct, item.attempts) })).sort((a, b) => b.attempts - a.attempts);
    const attention = subjects.flatMap((subject) => Object.entries(subject.topics).map(([topic, count]) => ({ ...subject, topic, count }))).sort((a, b) => b.count - a.count).slice(0, 3);
    const activity = events.reduce((sum, item) => ({ ...sum, [item.activity || "pyq"]: (sum[item.activity || "pyq"] || 0) + (Number(item.durationSeconds) || 0) }), { pyq: 0, revision: 0, battle: 0 });
    const share = (value) => seconds ? Math.round(value / seconds * 100) : 0;
    const pyqShare = share(activity.pyq);
    const revisionShare = share(activity.revision);
    const battleShare = Math.max(0, 100 - pyqShare - revisionShare);
    const days = events.sort((a, b) => new Date(a.answeredAt) - new Date(b.answeredAt)).reduce((list, item) => {
      const key = item.answeredAt.slice(0, 10);
      const current = list[list.length - 1];
      if (current?.key === key) { current.attempts += 1; current.correct += item.correct ? 1 : 0; }
      else list.push({ key, attempts: 1, correct: item.correct ? 1 : 0 });
      return list;
    }, []).slice(-8);
    const chartData = days.map((day, index) => ({
      ...day,
      accuracy: calculateAccuracy(day.correct, day.attempts),
      x: days.length === 1 ? 315 : 50 + index * 530 / (days.length - 1),
      y: 165 - calculateAccuracy(day.correct, day.attempts) * 1.35,
    }));
    const points = chartData.map((day) => `${day.x},${day.y}`).join(" ");
    const areaPoints = chartData.length ? `50,165 ${points} 580,165` : "";
    const timeLabel = seconds >= 3600 ? `${(seconds / 3600).toFixed(1)}h` : `${Math.round(seconds / 60)}m`;
    const pace = events.length ? Math.round(seconds / events.length) : 0;
    const review = (id) => { setActiveView("Practice"); setPracticeChoiceSubjectId(id); };
    return <section className="app-view">
      <div className="view-header"><div><p className="eyebrow">Learning intelligence</p><h2>Performance analytics</h2><p className="view-subtitle">Live insights from your completed practice.</p></div><button className="button button-primary" onClick={() => attention[0] ? review(attention[0].id) : setActiveView("Practice")}>Practice weak topics</button></div>
      <div className="analytics-kpi-grid"><article className="card panel"><span>Accuracy</span><strong>{periodAccuracy}%</strong><small>{correct} correct in this period</small></article><article className="card panel"><span>Questions solved</span><strong>{events.length}</strong><small>In the selected period</small></article><article className="card panel"><span>Average pace</span><strong>{pace < 60 ? `${pace}s` : `${Math.floor(pace / 60)}m ${pace % 60}s`}</strong><small>Per question</small></article><article className="card panel"><span>Study time</span><strong>{timeLabel}</strong><small>Measured active time</small></article></div>
      <div className="analytics-main-grid"><article className="card panel accuracy-trend-card"><div className="panel-heading-split"><div><h3>Accuracy trend</h3><p className="panel-copy">Daily accuracy across your recent study days</p></div><select aria-label="Analytics period" value={analyticsPeriod} onChange={(event) => setAnalyticsPeriod(Number(event.target.value))}><option value="30">Last 30 days</option><option value="90">Last 90 days</option><option value="365">Last year</option></select></div>{days.length ? <div className="line-chart"><div className="chart-summary"><span><strong>{periodAccuracy}%</strong> average accuracy</span><span>{events.length} questions</span></div><svg viewBox="0 0 600 205" role="img" aria-label="Accuracy trend"><defs><linearGradient id="analyticsArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2563eb" stopOpacity=".22"/><stop offset="100%" stopColor="#2563eb" stopOpacity=".01"/></linearGradient></defs>{[25, 50, 75, 100].map((value) => { const y = 165 - value * 1.35; return <g key={value}><line className="chart-gridline" x1="50" x2="580" y1={y} y2={y}/><text className="chart-y-label" x="42" y={y + 4} textAnchor="end">{value}%</text></g>; })}<polygon className="chart-area" points={areaPoints}/><polyline className="chart-line" points={points}/>{chartData.map((day) => <g className="chart-marker" key={day.key}><circle className="chart-point-halo" cx={day.x} cy={day.y} r="9"/><circle className="chart-point" cx={day.x} cy={day.y} r="5"/><text className="chart-value" x={day.x} y={day.y - 14} textAnchor="middle">{day.accuracy}%</text><title>{day.accuracy}% · {day.attempts} questions · {day.key}</title></g>)}</svg><div className="chart-axis">{chartData.map((day) => <span key={day.key}>{new Date(`${day.key}T00:00:00`).toLocaleDateString([], { month: "short", day: "numeric" })}</span>)}</div></div> : <div className="analytics-empty"><span className="analytics-empty-icon">↗</span><strong>Your progress graph starts here</strong><small>Complete a practice question to plot your first result.</small><button className="text-button" onClick={() => setActiveView("Practice")}>Start practice</button></div>}</article>
      <article className="card panel mastery-card"><div className="panel-heading-split"><div><h3>Subject mastery</h3><p className="panel-copy">Accuracy in this period</p></div><button className="text-button" onClick={() => setActiveView("Practice")}>View all</button></div>{subjects.length ? <div className="mastery-list">{subjects.map((subject) => <div key={subject.id}><span><strong>{subject.name}</strong><small>{subject.accuracy}% · {subject.attempts} attempted</small></span><div><i style={{ width: `${subject.accuracy}%` }}/></div></div>)}</div> : <p className="analytics-empty">No subject activity in this period.</p>}</article></div>
      <div className="analytics-bottom-grid"><article className="card panel"><h3>Time by activity</h3><div className="donut-layout"><div className="donut-chart" style={{ background: `conic-gradient(var(--ui-brand) 0 ${pyqShare}%,#10b981 ${pyqShare}% ${pyqShare + revisionShare}%,#8b5cf6 ${pyqShare + revisionShare}% 100%)` }}><span>{timeLabel}<small>total</small></span></div><div className="donut-legend"><span><i className="dot-blue"/>PYQs <strong>{pyqShare}%</strong></span><span><i className="dot-emerald"/>AI revision <strong>{revisionShare}%</strong></span><span><i className="dot-violet"/>Battles <strong>{battleShare}%</strong></span></div></div></article><article className="card panel"><h3>Needs attention</h3>{attention.length ? <div className="attention-list">{attention.map((item) => <button key={`${item.id}-${item.topic}`} onClick={() => review(item.id)}><span>{item.topic}<small>{item.count} incorrect · {item.name}</small></span><strong>Review →</strong></button>)}</div> : <p className="analytics-empty">Incorrect answers will appear here for targeted review.</p>}</article></div>
    </section>;
  }

  function renderAnalytics() {
    const subjectMastery = [
      ["Anatomy", 82], ["Physiology", 74], ["Pathology", 61], ["Pharmacology", 68], ["Microbiology", 77],
    ];
    return (
      <section className="app-view">
        <div className="view-header"><div><p className="eyebrow">Learning intelligence</p><h2>Performance analytics</h2><p className="view-subtitle">Understand what is improving, what needs revision, and where your study time pays off.</p></div><button className="button button-primary" onClick={() => setActiveView("Practice")}>Practice weak topics</button></div>
        <div className="analytics-kpi-grid">
          <article className="card panel"><span>Accuracy</span><strong>{accuracyRate}%</strong><small className="trend-positive">↑ 4.2% vs last week</small></article>
          <article className="card panel"><span>Questions solved</span><strong>{formatStatValue(attemptedQuestions)}</strong><small>Across all subjects</small></article>
          <article className="card panel"><span>Average pace</span><strong>48s</strong><small>Per question</small></article>
          <article className="card panel"><span>Study time</span><strong>8.4h</strong><small className="trend-positive">↑ 1.3h this week</small></article>
        </div>
        <div className="analytics-main-grid">
          <article className="card panel accuracy-trend-card"><div className="panel-heading-split"><div><h3>Accuracy trend</h3><p className="panel-copy">Last 8 study sessions</p></div><select aria-label="Analytics period"><option>Last 30 days</option><option>Last 90 days</option></select></div><div className="line-chart" aria-label="Accuracy improved from 58 to 78 percent"><svg viewBox="0 0 600 190" role="img"><defs><linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2563eb" stopOpacity=".25"/><stop offset="100%" stopColor="#2563eb" stopOpacity="0"/></linearGradient></defs><path className="chart-area" d="M10 155 C80 142,90 130,160 134 S240 112,300 118 S380 88,440 92 S520 54,590 64 L590 185 L10 185 Z"/><path className="chart-line" d="M10 155 C80 142,90 130,160 134 S240 112,300 118 S380 88,440 92 S520 54,590 64"/></svg><div className="chart-axis"><span>May 1</span><span>May 8</span><span>May 15</span><span>May 22</span><span>Today</span></div></div></article>
          <article className="card panel mastery-card"><div className="panel-heading-split"><div><h3>Subject mastery</h3><p className="panel-copy">Accuracy weighted by recency</p></div><button className="text-button" onClick={() => setActiveView("Practice")}>View all</button></div><div className="mastery-list">{subjectMastery.map(([subject, value]) => <div key={subject}><span><strong>{subject}</strong><small>{value}%</small></span><div><i style={{ width: `${value}%` }} /></div></div>)}</div></article>
        </div>
        <div className="analytics-bottom-grid"><article className="card panel"><h3>Time by activity</h3><div className="donut-layout"><div className="donut-chart"><span>8.4h<small>total</small></span></div><div className="donut-legend"><span><i className="dot-blue"/>PYQs <strong>52%</strong></span><span><i className="dot-emerald"/>Revision <strong>28%</strong></span><span><i className="dot-violet"/>Battles <strong>20%</strong></span></div></div></article><article className="card panel"><h3>Needs attention</h3><div className="attention-list"><button onClick={() => setActiveView("Practice")}><span>Renal pathology<small>7 incorrect answers</small></span><strong>Review →</strong></button><button onClick={() => setActiveView("Practice")}><span>Antimicrobials<small>Accuracy below 60%</small></span><strong>Review →</strong></button><button onClick={() => setActiveView("Practice")}><span>Cardiac physiology<small>Not revised in 18 days</small></span><strong>Review →</strong></button></div></article></div>
      </section>
    );
  }

  function renderPricing() {
    const plans = [
      { name: "Lite", price: "₹299", cadence: "/ year", copy: "Perfect for students who want daily practice without spending much.", features: ["5 Battle Points every day", "Performance Analytics", "Daily Practice Access", "Community Access", "Perfect for casual learners"], action: "Get Lite" },
      { name: "Ultra", price: "₹999", cadence: "/ year", copy: "For MBBS students preparing consistently throughout the year.", features: ["Unlimited Battle Points", "Create Communities", "Custom Battles", "Detailed Analytics", "Explanation Access", "Unlock Any 3 Subjects"], action: "Choose Ultra", featured: true },
      { name: "Premium", price: "₹1499", cadence: "/ month", copy: "Built for serious NEET PG aspirants.", features: ["All Subjects Unlocked", "Custom Modules", "Custom Practice", "NEET PG Exam Mode", "Clinical Cases", "Everything in Ultra"], action: "Go Premium" },
    ];
    const assurances = [
      ["◇", "Secure & Trusted", "Your data is safe with us."],
      ["↻", "Cancel Anytime", "No questions asked."],
      ["☏", "24/7 Support", "We're here to help."],
      ["✪", "Loved by Medicos", "Join thousands of students."],
    ];
    return (
      <section className="app-view pricing-page">
        <div className="pricing-hero"><p className="eyebrow">Simple, affordable pricing</p><h2>Master Medicine,<br/>One Question at a Time<span>.</span></h2><p>Practice consistently, compete with friends, analyze your weaknesses, and prepare confidently for university exams and NEET PG.</p><div className="billing-toggle"><button>Monthly</button><button className="active">Annual</button><span>Save up to 30%</span></div></div>
        <div className="pricing-grid">{plans.map((plan) => <article className={`pricing-card${plan.featured ? " pricing-card-featured" : ""}`} key={plan.name}>{plan.featured ? <span className="popular-pill">★ Most popular</span> : null}<h3>{plan.name}</h3><p>{plan.copy}</p><div className="plan-price"><strong>{plan.price}</strong><span>{plan.cadence}</span></div><button className={`button ${plan.featured ? "button-primary" : "button-secondary"}`} onClick={() => document.getElementById("payment-gateway")?.scrollIntoView({ behavior: "smooth" })}>{plan.action}</button><ul>{plan.features.map((feature) => <li key={feature}><span>✓</span>{feature}</li>)}</ul></article>)}</div>
        <div className="pricing-assurance-strip">{assurances.map(([icon, title, copy]) => <div key={title}><span>{icon}</span><strong>{title}</strong><small>{copy}</small></div>)}</div>
        <article className="card panel payment-gateway-section" id="payment-gateway">
          <div className="payment-copy"><p className="eyebrow">Payment gateway · future ready</p><h3>Secure checkout boundary</h3><p className="panel-copy">The interface is prepared for a PCI-compliant provider such as Razorpay or Stripe. MediComm will create orders and store payment status only. Raw card or UPI credentials will never touch the application server.</p><div className="payment-provider-row"><span>UPI</span><span>Cards</span><span>Net banking</span><span>Wallets</span></div></div>
          <div className="payment-summary"><div><span>Selected plan</span><strong>MediComm Ultra</strong></div><div><span>Billing</span><strong>Annual</strong></div><div><span>Amount</span><strong>₹999</strong></div><button className="button button-primary" disabled>Checkout coming soon</button><small>No payment will be collected yet.</small></div>
        </article>
        <div className="pricing-faq"><h3>Common questions</h3><details><summary>Can I keep using MediComm for free?</summary><p>Yes. Core daily practice and community features remain available on the free plan.</p></details><details><summary>Will my progress carry over when I upgrade?</summary><p>Yes. Plans change access, never your saved learning history.</p></details><details><summary>How will payments be secured?</summary><p>Sensitive payment collection will be hosted by a compliant payment provider; MediComm will retain only order and entitlement status.</p></details></div>
      </section>
    );
  }

  function renderSettings() {
    return (
      <section className="app-view settings-page">
        <div className="view-header"><div><p className="eyebrow">Preferences</p><h2>Settings</h2><p className="view-subtitle">Tune your study environment, notifications, privacy, and accessibility.</p></div></div>
        <div className="settings-layout"><aside className="settings-index"><button className="active">Study preferences</button><button>Notifications</button><button>Appearance</button><button>Privacy & security</button><button>Billing</button></aside><div className="settings-content">
          <article className="card panel"><div className="settings-heading"><h3>Study preferences</h3><p>Personalize recommendations and exam planning.</p></div><label className="setting-field"><span>Target exam<small>Used for relevant PYQs and countdowns.</small></span><select defaultValue="neet"><option value="neet">NEET PG</option><option value="ini">INI-CET</option><option value="fmge">FMGE</option></select></label><label className="setting-field"><span>Daily question goal<small>A gentle target, never a punishment.</small></span><select defaultValue="40"><option>20</option><option>40</option><option>60</option><option>100</option></select></label></article>
          <article className="card panel"><div className="settings-heading"><h3>Notifications</h3><p>Choose the nudges that are genuinely useful.</p></div><label className="setting-toggle"><span>Daily study reminder<small>One reminder at your preferred time.</small></span><input type="checkbox" defaultChecked /></label><label className="setting-toggle"><span>Battle invitations<small>Know when a peer challenges you.</small></span><input type="checkbox" defaultChecked /></label><label className="setting-toggle"><span>Community replies<small>Mentions and replies to your discussions.</small></span><input type="checkbox" /></label></article>
          <article className="card panel"><div className="settings-heading"><h3>Appearance & accessibility</h3><p>Comfortable in every study environment.</p></div><div className="theme-choice"><button className={!isDarkMode ? "active" : ""} onClick={() => isDarkMode && setTheme("light")}>Light</button><button className={isDarkMode ? "active" : ""} onClick={() => !isDarkMode && setTheme("dark")}>Dark</button><button onClick={() => setTheme(window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")}>System</button></div><label className="setting-toggle"><span>Reduce motion<small>Minimize nonessential interface animation.</small></span><input type="checkbox" /></label></article>
          <article className="card panel danger-zone"><div><h3>Sign out of this device</h3><p className="panel-copy">Your synced progress remains safe in your account.</p></div><button className="button button-secondary" onClick={handleLogout}>Sign out</button></article>
        </div></div>
      </section>
    );
  }

  function renderView() {
    switch (activeView) {
      case "Dashboard":
        return renderDashboard();
      case "Practice":
        return renderPractice();
      case "Analytics":
        return renderAnalytics();
      case "Leaderboard":
        return renderLeaderboard();
      case "Communities":
        return renderCommunities();
      case "Compete":
        return renderCompete();
      case "Pricing":
        return renderPricing();
      case "Profile":
        return renderProfile();
      case "Settings":
        return renderSettings();
      case "PublicProfile":
        return renderPublicProfile();
      default:
        return renderHome();
    }
  }

  if (authStatus === "loading") {
    return (
      <div className="auth-shell auth-shell-loading">
        <div className="card auth-card auth-loading-card">
          <div className="duel-loader" />
          <h2>Loading your session</h2>
          <p className="panel-copy">Checking the local MediComm database and restoring your account.</p>
        </div>
      </div>
    );
  }

  if (authStatus !== "authenticated" && authStatus !== "guest") {
    return renderAuthPage();
  }

  return (
    <AppShell
      activeView={activeView}
      isDarkMode={isDarkMode}
      navItems={navItems}
      onNavigate={setActiveView}
      onToggleTheme={() => setTheme((currentTheme) => (currentTheme === "dark" ? "light" : "dark"))}
      renderAvatar={renderAvatar}
      user={user}
      userRating={userRating}
      directConversations={directConversations}
    >
      {renderView()}
    </AppShell>
  );
}

export default App;
