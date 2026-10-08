import { useEffect, useMemo, useRef, useState } from "react";
import { AppShell } from "./components/AppShellV2";
import WebsiteReviews from "./components/WebsiteReviews";
import CompeteArena from "./components/CompeteArena";
import Leaderboard from "./components/Leaderboard";
import CommunityHub from "./components/CommunityHub";
import { socialPage, surface as socialSurface, primary as socialPrimary, secondary as socialSecondary, field as socialField, avatar as socialAvatar } from "./components/SocialUI";
import PracticeSelection from "./components/PracticeSelection";
import UsmleModules from "./components/UsmleModules";
import FmgeYears from "./components/FmgeYears";
import ShortNotes from "./components/ShortNotes";
import AnswerNotepad from "./components/AnswerNotepad";
import TextbookSources from "./components/TextbookSources";
import { DashboardSummary, ProfileOverview } from "./components/AccountOverview";
import DashboardActivity from "./components/DashboardActivity";
import RazorpayCheckout from "./components/RazorpayCheckout";
import { PAYMENT_PLANS } from "./data/paymentPlans";
import { useAccountOverview, usePracticeRecorder } from "./lib/useAccountOverview";
import { BrandMark } from "./components/BrandMark";
import { ABROAD_STATE, medicalCollegesByState, signupStateOptions } from "./data/medicalColleges";
import { VIVA_CHAPTER_FALLBACKS } from "./data/vivaChapters";
import { apiRequest } from "./lib/api";
import { SESSION_TOKEN_KEY, THEME_STORAGE_KEY } from "./lib/clientStorage";

const PRACTICE_LIBRARY_URL = "/api/practice";
const PRACTICE_LIBRARY_CACHE_KEY = "medicomm-practice-library-cache-v20260930-all-image-sync";
const PRACTICE_PROGRESS_STORAGE_KEY = "medicomm-practice-progress";
const ANALYTICS_EVENTS_STORAGE_KEY = "medicomm-analytics-events";
const QUESTION_BOOKMARKS_STORAGE_KEY = "medicomm-question-bookmarks";
const COMMUNITY_THREAD_WORD_LIMIT = 300;
const COMMUNITY_THREAD_IMAGE_LIMIT_BYTES = 5 * 1024 * 1024;
const VIVA_ANSWER_IMAGE_INPUT_LIMIT_BYTES = 12 * 1024 * 1024;
const VIVA_ANSWER_IMAGE_OUTPUT_LIMIT_BYTES = 5 * 1024 * 1024;
const VIVA_ANSWER_IMAGE_MAX_DIMENSION = 2048;
const CLINICAL_CASE_GENERATION_POLL_MS = 2000;
const CLINICAL_CASE_GENERATION_WAIT_MS = 4 * 60 * 1000;
// Atlas artwork was replaced in place, so use a versioned URL to ensure clients
// don't keep showing a previously cached source image.
const ATLAS_IMAGE_VERSION = "20260930-no-watermarks";
const MIND_MAP_ASSET_VERSION = "20260830-teacher-notes";

const MIND_MAP_ASSETS = {
  pharmacology: {
    "General Principles of Antimicrobial Therapy": `/uploads/pharmacology-ch07-t01-general-principles-mind-map.png?v=${MIND_MAP_ASSET_VERSION}`,
    "DNA Disruptors: Sulfonamides, Quinolones, and Nitroimidazoles": `/uploads/pharmacology-ch07-t02-dna-disruptors-mind-map.png?v=${MIND_MAP_ASSET_VERSION}`,
    "Cell Envelope Disruptors: β-Lactam, Glycopeptide, and Lipopeptide Antibacterials": `/uploads/pharmacology-ch07-t03-cell-envelope-disruptors-mind-map.png?v=${MIND_MAP_ASSET_VERSION}`,
    "Miscellaneous Antibacterials: Aminoglycosides, Polymyxins, Urinary Antiseptics, Bacteriophages": `/uploads/pharmacology-ch07-t04-misc-antibacterials-mind-map.png?v=${MIND_MAP_ASSET_VERSION}`,
    "Protein Synthesis Inhibitors": `/uploads/pharmacology-ch07-t05-protein-synthesis-inhibitors-mind-map.png?v=${MIND_MAP_ASSET_VERSION}`,
  },
};

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

function getVivaChapterOptions(subjectId, aiSubjects = [], usmleSubjects = []) {
  const chapterCounts = new Map();
  const sourceSubjects = [
    aiSubjects.find((subject) => subject.id === subjectId),
    usmleSubjects.find((subject) => subject.id === subjectId),
  ].filter(Boolean);

  for (const subject of sourceSubjects) {
    for (const question of subject.questions ?? []) {
      const title = String(question.chapterTitle ?? "").trim();
      if (!title) continue;
      const current = chapterCounts.get(title) ?? { title, count: 0, order: Number.MAX_SAFE_INTEGER };
      current.count += 1;
      current.order = Math.min(current.order, getPracticeChapterOrder(question, subjectId));
      chapterCounts.set(title, current);
    }
  }

  if (chapterCounts.size) return [...chapterCounts.values()].sort(comparePracticeDirectoryEntries);

  return (VIVA_CHAPTER_FALLBACKS[subjectId] ?? []).map((title, index) => ({ title, count: 0, order: index + 1 }));
}

function shuffleQuestionIds(questions = []) {
  const ids = questions.map((question) => question.id);

  for (let index = ids.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [ids[index], ids[randomIndex]] = [ids[randomIndex], ids[index]];
  }

  return ids;
}

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

const navItems = ["Home", "Dashboard", "Practice", "Bookmarks", "Analytics", "Leaderboard", "Communities", "Reviews", "Compete", "Pricing", "Profile", "Settings"];

const emptyPracticeLibrary = {
  exam: {
    id: "neet-pg-pyqs",
    title: "NEET PG PYQs",
    questionCount: 0,
  },
  years: [],
  subjects: [],
  aiSubjects: [],
  usmleSubjects: [],
  usmleModules: [],
  fmgeSessions: [],
};

function normalizePracticeLibrary(data) {
  return {
    exam: data?.exam ?? emptyPracticeLibrary.exam,
    years: data?.years ?? [],
    subjects: data?.subjects ?? [],
    aiSubjects: data?.aiSubjects ?? [],
    usmleSubjects: data?.usmleSubjects ?? [],
    usmleModules: data?.usmleModules ?? [],
    fmgeSessions: data?.fmgeSessions ?? [],
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

function QuestionLaboratoryTable({ findings = [], compact = false }) {
  if (!Array.isArray(findings) || !findings.length) return null;

  return (
    <div className={`question-laboratory-panel${compact ? " question-laboratory-panel-compact" : ""}`}>
      <table className="question-laboratory-table">
        <caption>Laboratory studies</caption>
        <thead>
          <tr><th>Test</th><th>Patient</th><th>Reference range</th></tr>
        </thead>
        <tbody>
          {findings.map((finding) => (
            <tr key={`${finding.test}-${finding.value}`}>
              <th scope="row">{finding.test}</th>
              <td>{finding.value}</td>
              <td>{finding.reference || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
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

function getPracticeImageUrl(imageUrl) {
  if (!imageUrl?.includes("/medicomm-")) return imageUrl;
  const separator = imageUrl.includes("?") ? "&" : "?";
  return `${imageUrl}${separator}v=${ATLAS_IMAGE_VERSION}`;
}

function isUsmleImage(imageUrl) {
  return String(imageUrl ?? "").includes("/usmle-");
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

function formatDuration(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
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

function getQuestionBookmarksStorageKey(user) {
  const userKey = user?.id ?? user?.email ?? "guest";
  return `${QUESTION_BOOKMARKS_STORAGE_KEY}:${userKey}`;
}

function readQuestionBookmarks(user) {
  if (typeof window === "undefined") return [];
  try {
    const parsed = JSON.parse(localStorage.getItem(getQuestionBookmarksStorageKey(user)) || "[]");
    return Array.isArray(parsed) ? parsed.slice(0, 500) : [];
  } catch {
    return [];
  }
}

function writeQuestionBookmarks(user, bookmarks) {
  if (typeof window === "undefined") return;
  localStorage.setItem(getQuestionBookmarksStorageKey(user), JSON.stringify(bookmarks.slice(0, 500)));
}

function getQuestionBookmarkKey(bookmark) {
  return `${bookmark?.mode ?? ""}:${bookmark?.subjectId ?? ""}:${bookmark?.questionId ?? ""}`;
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
  const [activeView, updateActiveView] = useState("Home");
  const [practicePathTitle, setPracticePathTitle] = useState("");

  function setActiveView(view) {
    if (view === "Practice") {
      handleBackToPracticeDirectory();
      setPracticeChoiceSubjectId("");
      setPracticeStage("selection");
    }
    updateActiveView(view);
  }
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
  const [practiceChoicePanel, setPracticeChoicePanel] = useState("formats");
  const [practiceQuestionIndex, setPracticeQuestionIndex] = useState(0);
  const [usmlePracticeQuestionIds, setUsmlePracticeQuestionIds] = useState([]);
  const [vivaSelectedChapters, setVivaSelectedChapters] = useState([]);
  const [vivaPrivacyAccepted, setVivaPrivacyAccepted] = useState(false);
  const [vivaSessionBusy, setVivaSessionBusy] = useState(false);
  const [vivaSessionMessage, setVivaSessionMessage] = useState("");
  const [vivaSession, setVivaSession] = useState(null);
  const [vivaAnswerDraft, setVivaAnswerDraft] = useState("");
  const [vivaAnswerImage, setVivaAnswerImage] = useState(null);
  const [vivaAnswerImageBusy, setVivaAnswerImageBusy] = useState(false);
  const [vivaAnswerBusy, setVivaAnswerBusy] = useState(false);
  const [vivaAnswerMessage, setVivaAnswerMessage] = useState("");
  const [clinicalSelectedChapters, setClinicalSelectedChapters] = useState([]);
  const [clinicalPrivacyAccepted, setClinicalPrivacyAccepted] = useState(false);
  const [clinicalSessionBusy, setClinicalSessionBusy] = useState(false);
  const [clinicalSessionMessage, setClinicalSessionMessage] = useState("");
  const [clinicalSession, setClinicalSession] = useState(null);
  const [clinicalAnswerDraft, setClinicalAnswerDraft] = useState("");
  const [clinicalAnswerImage, setClinicalAnswerImage] = useState(null);
  const [clinicalAnswerImageBusy, setClinicalAnswerImageBusy] = useState(false);
  const [clinicalAnswerBusy, setClinicalAnswerBusy] = useState(false);
  const [clinicalAnswerMessage, setClinicalAnswerMessage] = useState("");
  const [practiceStage, setPracticeStage] = useState("selection");
  const [practiceProgress, setPracticeProgress] = useState({});
  const [dashboardPracticeTarget, setDashboardPracticeTarget] = useState(null);
  const [bookmarkMessage, setBookmarkMessage] = useState("");
  const [bookmarkBusyKeys, setBookmarkBusyKeys] = useState([]);
  const bookmarkPendingKeysRef = useRef(new Set());
  const bookmarkMutationQueueRef = useRef(Promise.resolve());
  const [analyticsEvents, setAnalyticsEvents] = useState([]);
  const [analyticsPeriod, setAnalyticsPeriod] = useState(30);
  const [practiceQuestionStartedAt, setPracticeQuestionStartedAt] = useState(Date.now());
  const [userRating, setUserRating] = useState(1480);
  const [profilePhotoPreparing, setProfilePhotoPreparing] = useState(false);
  const [paymentPlanId, setPaymentPlanId] = useState("ultra");
  const duelDeadlineRef = useRef(0);
  const loadedDuelRef = useRef(null);
  const duelAnswerPendingRef = useRef(false);
  const [duelAnswerBusy, setDuelAnswerBusy] = useState(false);
  const [showDuelReview, setShowDuelReview] = useState(false);
  const [duelStatus, setDuelStatus] = useState("idle");
  const [duelQuestions, setDuelQuestions] = useState(fallbackDuelQuestions);
  const [duelMode, setDuelMode] = useState("rated");
  const [duelSessionId, setDuelSessionId] = useState("");
  const [duelOpponent, setDuelOpponent] = useState(null);
  const [duelTimeLeft, setDuelTimeLeft] = useState(DUEL_DURATION_SECONDS);
  const [duelIndex, setDuelIndex] = useState(0);
  const [duelSelections, setDuelSelections] = useState({});
  const [duelSubmitted, setDuelSubmitted] = useState({});
  const [duelOpponentProgress, setDuelOpponentProgress] = useState({ answered: 0, correct: 0 });
  const [duelResult, setDuelResult] = useState(null);
  const [duelQueueInfo, setDuelQueueInfo] = useState(null);
  const [duelMessage, setDuelMessage] = useState("");
  const [duelForfeited, setDuelForfeited] = useState(false);
  const [selectedLeaderboardState, setSelectedLeaderboardState] = useState("");
  const [selectedLeaderboardCollege, setSelectedLeaderboardCollege] = useState("");
  const [authStatus, setAuthStatus] = useState("loading");
  const [authMode, setAuthMode] = useState("login");
  const [authBusy, setAuthBusy] = useState(false);
  const [authMessage, setAuthMessage] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [user, setUser] = useState(null);
  const accountOverview = useAccountOverview(user?.id, activeView, `${user?.attemptedQuestions}:${user?.rating}:${user?.medicalCollege}`);
  const practiceSync = usePracticeRecorder(authStatus === "authenticated" ? user?.id : null, savedUser => {
    setUser(current => current?.id === savedUser.id ? { ...current, ...savedUser } : current);
    setUserRating(savedUser.rating);
    accountOverview.reload();
  });
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
    medicalState: "",
    medicalCollege: "",
    contactNumber: "",
    password: "",
  });

  const practiceSubjects = practiceLibrary.subjects ?? [];
  const aiPracticeSubjects = practiceLibrary.aiSubjects ?? [];
  const usmlePracticeSubjects = practiceLibrary.usmleSubjects ?? [];
  const usmleModules = practiceLibrary.usmleModules ?? [];
  const fmgeSessions = practiceLibrary.fmgeSessions ?? [];
  const allUsmlePracticeSets = useMemo(() => [...usmlePracticeSubjects, ...usmleModules], [usmlePracticeSubjects, usmleModules]);
  const aiPracticeQuestionCountsBySubject = useMemo(
    () =>
      Object.fromEntries(
        aiPracticeSubjects.map((subject) => [subject.id, subject.questions?.length ?? 0]),
      ),
    [aiPracticeSubjects],
  );
  const practiceYears = practiceLibrary.years ?? [];
  const activePracticeSubjects =
    selectedPracticeMode === "ai"
      ? aiPracticeSubjects
      : selectedPracticeMode === "usmle"
        ? allUsmlePracticeSets
        : selectedPracticeMode === "fmge"
          ? fmgeSessions
        : practiceSubjects;
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
  const basePracticeQuestions =
    selectedPracticeMode !== "pyq" && selectedPracticeTopic
      ? (currentPracticeSubject?.questions ?? []).filter((question) => question.topic === selectedPracticeTopic)
      : currentPracticeQuestionSet?.questions ?? currentPracticeSubject?.questions ?? [];
  const currentPracticeQuestions =
    selectedPracticeMode === "usmle" && usmlePracticeQuestionIds.length
      ? usmlePracticeQuestionIds
          .map((questionId) => basePracticeQuestions.find((question) => question.id === questionId))
          .filter(Boolean)
      : basePracticeQuestions;
  const currentPracticeQuestion = currentPracticeQuestions[practiceQuestionIndex] ?? null;
  const questionBookmarks = Array.isArray(user?.questionBookmarks) ? user.questionBookmarks : [];
  const bookmarkQuestionIndex = useMemo(() => {
    const index = new Map();
    const sources = [
      ["pyq", practiceSubjects],
      ["ai", aiPracticeSubjects],
      ["usmle", allUsmlePracticeSets],
      ["fmge", fmgeSessions],
    ];
    for (const [mode, subjects] of sources) {
      for (const subject of subjects) {
        for (const question of subject.questions ?? []) {
          index.set(getQuestionBookmarkKey({ mode, subjectId: subject.id, questionId: question.id }), {
            mode,
            subject,
            question,
          });
        }
      }
    }
    return index;
  }, [practiceSubjects, aiPracticeSubjects, allUsmlePracticeSets, fmgeSessions]);
  const bookmarkedQuestionEntries = questionBookmarks.map((bookmark) => ({
    bookmark,
    resolved: bookmarkQuestionIndex.get(getQuestionBookmarkKey(bookmark)) ?? null,
  }));
  const isCurrentPracticeQuestionBookmarked = currentPracticeQuestion
    ? questionBookmarks.some((bookmark) => getQuestionBookmarkKey(bookmark) === getQuestionBookmarkKey({
        mode: selectedPracticeMode,
        subjectId: currentPracticeSubject?.id,
        questionId: currentPracticeQuestion.id,
      }))
    : false;
  const practiceChoiceSubject =
    practiceSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    usmlePracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    null;
  const practiceChoiceYearSets = useMemo(
    () => buildSubjectYearSets(practiceChoiceSubject, practiceProgress),
    [practiceChoiceSubject, practiceProgress],
  );
  const currentAiPracticeSubject = aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ?? null;
  const practiceChoiceAiQuestionCount = currentAiPracticeSubject?.questions?.length ?? 0;
  const currentUsmlePracticeSubject = usmlePracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ?? null;
  const practiceChoiceUsmleQuestionCount = currentUsmlePracticeSubject?.questions?.length ?? 0;
  const vivaChapterOptions = useMemo(
    () => getVivaChapterOptions(selectedPracticeSubjectId, aiPracticeSubjects, usmlePracticeSubjects),
    [selectedPracticeSubjectId, aiPracticeSubjects, usmlePracticeSubjects],
  );
  const currentVivaQuestion = vivaSession?.questions?.[vivaSession.currentQuestionIndex ?? 0] ?? null;
  const currentVivaEvaluation = currentVivaQuestion
    ? vivaSession?.answers?.find((answer) => answer.questionId === currentVivaQuestion.id) ?? null
    : null;
  const currentClinicalCase = clinicalSession?.cases?.[clinicalSession.currentCaseIndex ?? 0] ?? null;
  const currentClinicalEvaluation = currentClinicalCase
    ? clinicalSession?.answers?.find((answer) => answer.caseId === currentClinicalCase.id) ?? null
    : null;
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

  const userDuelAnswered = Object.keys(duelSubmitted).length;
  const signupCollegeOptions = authForm.medicalState && authForm.medicalState !== ABROAD_STATE
    ? medicalCollegesByState[authForm.medicalState] ?? []
    : [];

  const attemptedQuestions = user?.attemptedQuestions ?? 0;
  const correctAnswers = user?.correctAnswers ?? 0;
  const accuracyRate = calculateAccuracy(correctAnswers, attemptedQuestions);

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

  const stateLeaderboardByName = useMemo(
    () => new Map(stateLeaderboard.map((entry) => [entry.state, entry])),
    [stateLeaderboard],
  );

  const leaderboardStateOptions = useMemo(() => {
    const rankedStates = new Set(stateLeaderboard.map((entry) => entry.state));
    return signupStateOptions
      .filter((state) => state !== ABROAD_STATE || rankedStates.has(state))
      .map((state) => ({
        state,
        players: stateLeaderboardByName.get(state)?.players ?? [],
      }))
      .sort((left, right) => {
        const playerDifference = right.players.length - left.players.length;
        if (playerDifference !== 0) return playerDifference;
        return left.state.localeCompare(right.state);
      });
  }, [stateLeaderboard, stateLeaderboardByName]);

  const selectedStateEntry =
    leaderboardStateOptions.find((entry) => entry.state === selectedLeaderboardState) ?? leaderboardStateOptions[0];

  const selectedLeaderboardCollegeOptions = selectedStateEntry?.state && selectedStateEntry.state !== ABROAD_STATE
    ? medicalCollegesByState[selectedStateEntry.state] ?? []
    : [];

  const selectedStatePlayers = useMemo(() => {
    const players = selectedStateEntry?.players ?? [];
    if (!selectedLeaderboardCollege) return players;
    return players.filter((player) => player.college === selectedLeaderboardCollege);
  }, [selectedLeaderboardCollege, selectedStateEntry]);

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
      const hasCurrentSubject = [...cachedLibrary.subjects, ...(cachedLibrary.aiSubjects ?? []), ...(cachedLibrary.usmleSubjects ?? []), ...(cachedLibrary.usmleModules ?? []), ...(cachedLibrary.fmgeSessions ?? [])].some((subject) => subject.id === current);
      return hasCurrentSubject ? current : cachedLibrary.subjects[0]?.id ?? cachedLibrary.aiSubjects?.[0]?.id ?? cachedLibrary.usmleSubjects?.[0]?.id ?? "";
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
        cache: "no-store",
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error("Could not load practice questions.");
      }

      const nextLibrary = normalizePracticeLibrary(await response.json());
      setPracticeLibrary(nextLibrary);
      writeCachedPracticeLibrary(nextLibrary);
      setSelectedPracticeSubjectId((current) => {
        const hasCurrentSubject = [...nextLibrary.subjects, ...(nextLibrary.aiSubjects ?? []), ...(nextLibrary.usmleSubjects ?? []), ...(nextLibrary.usmleModules ?? []), ...(nextLibrary.fmgeSessions ?? [])].some((subject) => subject.id === current);
        if (hasCurrentSubject) return current;
        return nextLibrary.subjects[0]?.id ?? nextLibrary.aiSubjects?.[0]?.id ?? nextLibrary.usmleSubjects?.[0]?.id ?? "";
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
    let isActive = true;

    apiRequest("/api/auth/session", { timeoutMs: 3000 })
      .then((data) => {
        if (!isActive) return;
        localStorage.setItem(SESSION_TOKEN_KEY, "true");
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

    const scrollY = window.scrollY;
    const previousBodyStyles = {
      overflow: document.body.style.overflow,
      position: document.body.style.position,
      top: document.body.style.top,
      width: document.body.style.width,
    };
    const previousHtmlOverflow = document.documentElement.style.overflow;

    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    document.body.style.position = "fixed";
    document.body.style.top = `-${scrollY}px`;
    document.body.style.width = "100%";

    return () => {
      document.documentElement.style.overflow = previousHtmlOverflow;
      Object.assign(document.body.style, previousBodyStyles);
      window.scrollTo(0, scrollY);
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
    const needsPracticeLibrary = activeView === "Practice" || (activeView === "Bookmarks" && questionBookmarks.length > 0);
    if (!user?.hasPracticeAccess || !needsPracticeLibrary || practiceLibraryStatus !== "idle") return;
    fetchPracticeLibrary();
  }, [activeView, practiceLibraryStatus, questionBookmarks.length, user?.hasPracticeAccess]);

  useEffect(() => {
    if (!dashboardPracticeTarget) return;
    if (activeView !== "Practice") { setDashboardPracticeTarget(null); return; }
    if (practiceLibraryStatus === "ready") {
      setDashboardPracticeTarget(null);
      continueDashboardPractice(dashboardPracticeTarget);
    }
  }, [dashboardPracticeTarget, practiceLibraryStatus, activeView]);

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
    if (!selectedStateEntry && leaderboardStateOptions.length) {
      setSelectedLeaderboardState(leaderboardStateOptions[0].state);
      setSelectedLeaderboardCollege("");
      return;
    }

    if (!selectedLeaderboardState && currentUserLeaderboardEntry?.state) {
      setSelectedLeaderboardState(currentUserLeaderboardEntry.state);
    }
  }, [currentUserLeaderboardEntry, leaderboardStateOptions, selectedLeaderboardState, selectedStateEntry]);

  useEffect(() => {
    if (!selectedLeaderboardCollege) return;
    if (!selectedLeaderboardCollegeOptions.includes(selectedLeaderboardCollege)) {
      setSelectedLeaderboardCollege("");
    }
  }, [selectedLeaderboardCollege, selectedLeaderboardCollegeOptions]);

  useEffect(() => {
    if (!user?.id) return;
    let cancelled = false;
    const saved = localStorage.getItem(`medicomm-duel:${user.id}`);
    if (saved) void loadDuelQuestions(saved).then(questions => {
      if (cancelled) return;
      const data = loadedDuelRef.current;
      beginLiveDuel(data.opponent, { sessionId: saved, questions, mode: data.mode });
    }).catch(error => { if (!cancelled) setDuelMessage(`Could not restore the previous match: ${error.message}`); });
    return () => { cancelled = true; };
  }, [user?.id]);

  useEffect(() => {
    if (duelStatus !== "live") return undefined;

    const timer = window.setInterval(() => {
      const remaining = Math.max(0, Math.ceil((duelDeadlineRef.current - Date.now()) / 1000));
      setDuelTimeLeft(remaining);
      if (!remaining) setDuelStatus("finished");
    }, 250);

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
    if (!duelSessionId || !["live", "finished"].includes(duelStatus) || duelResult) return;
    let cancelled = false;
    let timer;
    const syncMatch = async () => {
      try {
        const data = duelStatus === "finished"
          ? await apiRequest("/api/duels/complete", { method: "POST", body: JSON.stringify({ sessionId: duelSessionId, forfeit: duelForfeited }) })
          : await apiRequest(`/api/duels/status?session=${encodeURIComponent(duelSessionId)}`);
        if (cancelled) return;
        duelDeadlineRef.current = Date.now() + Math.max(0, data.expiresAt - data.serverNow);
        setDuelOpponentProgress({ answered: data.opponentAnswered, correct: 0 });
        const locked = {};
        const selections = {};
        duelQuestions.forEach((q, index) => {
          if (Object.hasOwn(data.answers, q.id)) { locked[index] = true; selections[index] = q.options[data.answers[q.id]]; }
        });
        setDuelSubmitted(current => ({ ...current, ...locked }));
        setDuelSelections(current => ({ ...current, ...selections }));
        if (data.finished) setDuelStatus("finished");
        if (data.result) {
          setDuelResult(data.result);
          setDuelStatus("finished");
          setDuelMessage("");
          const mergedUser = mergeUserPerformance(data.user);
          setUser(mergedUser);
          setUserRating(data.user.rating);
          setAnalyticsEvents(current => {
            const existing = new Set(current.map(event => event.id));
            const events = data.result.review.filter(q => q.selectedIndex !== null).map(q => ({
              id: `${duelSessionId}-${q.id}`, questionId: q.id, correct: q.status === "correct",
              subjectId: q.subjectId || "mixed-duel", subject: q.subjectTitle || "Mixed battle",
              activity: "battle", answeredAt: data.result.completedAt, seconds: 0,
            })).filter(event => !existing.has(event.id));
            const next = [...current, ...events];
            writeAnalyticsEvents(user, next);
            return next;
          });
          void fetchLeaderboard();
          void fetchPlatformSummary();
          return;
        }
        setDuelMessage(duelStatus === "finished" ? "Answers saved. Waiting for your opponent or the match timer to finish." : "");
      } catch (error) {
        if (!cancelled) setDuelMessage(`${error.message} Retrying connection...`);
      }
      if (!cancelled) timer = window.setTimeout(syncMatch, 2000);
    };
    void syncMatch();
    return () => { cancelled = true; window.clearTimeout(timer); };
  }, [duelSessionId, duelStatus, duelForfeited, duelResult]);

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
        activity: selectedPracticeMode === "usmle" ? "usmle" : selectedPracticeMode === "ai" ? "revision" : "pyq",
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
    practiceSync.record({
      id: crypto.randomUUID(), questionId: currentPracticeQuestion.id, subjectId: currentPracticeSubject.id,
      mode: selectedPracticeMode, selectedAnswer: selectedOption,
      durationSeconds: Math.max(1, Math.min(1800, Math.round((Date.now() - practiceQuestionStartedAt) / 1000))),
    });
  }

  function handleSelectPracticeSubject(subjectId) {
    setPracticeChoicePanel("formats");
    setPracticeChoiceSubjectId(subjectId);
  }

  function closePracticeChoice() {
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
  }

  function handleOpenMindMaps(subjectId) {
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode("ai");
    setSelectedPracticeExamYear("");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setPracticeStage("mind-map-chapters");
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
    scrollPracticeViewToTop();
  }

  function startPracticeSession(subjectId, mode, examYear = "") {
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode(mode);
    setSelectedPracticeExamYear(mode === "pyq" ? examYear : "");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setUsmlePracticeQuestionIds([]);
    setPracticeStage("subject");
    setPracticeQuestionStartedAt(Date.now());
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
  }

  function handleBackToPracticeDirectory() {
    setPracticeStage("catalog");
    setSelectedPracticeMode("pyq");
    setSelectedPracticeExamYear("");
    setSelectedOption("");
    setSubmitted(false);
    setUsmlePracticeQuestionIds([]);
    setVivaSelectedChapters([]);
    setVivaPrivacyAccepted(false);
    setVivaSessionMessage("");
    setVivaSession(null);
    setVivaAnswerDraft("");
    setVivaAnswerImage(null);
    setVivaAnswerBusy(false);
    setVivaAnswerMessage("");
    setClinicalSelectedChapters([]);
    setClinicalPrivacyAccepted(false);
    setClinicalSessionMessage("");
    setClinicalSession(null);
    setClinicalAnswerDraft("");
    setClinicalAnswerImage(null);
    setClinicalAnswerBusy(false);
    setClinicalAnswerMessage("");
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
    setBookmarkMessage("");
    setPracticeQuestionStartedAt(Date.now());
  }

  async function updateQuestionBookmark(bookmarkInput, shouldSave) {
    const bookmarkKey = getQuestionBookmarkKey(bookmarkInput);
    if (!bookmarkInput.questionId || !bookmarkInput.subjectId || bookmarkPendingKeysRef.current.has(bookmarkKey)) return;

    const previousBookmarks = Array.isArray(user?.questionBookmarks) ? user.questionBookmarks : [];
    const optimisticBookmark = {
      questionId: bookmarkInput.questionId,
      subjectId: bookmarkInput.subjectId,
      mode: bookmarkInput.mode,
      subjectTitle: bookmarkInput.subjectTitle ?? "Practice",
      topic: bookmarkInput.topic ?? "General review",
      year: Number.isFinite(bookmarkInput.year) ? bookmarkInput.year : null,
      preview: String(bookmarkInput.preview ?? "Saved practice question").slice(0, 500),
      savedAt: bookmarkInput.savedAt ?? new Date().toISOString(),
    };
    const nextBookmarks = shouldSave
      ? [optimisticBookmark, ...previousBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey)].slice(0, 500)
      : previousBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey);

    bookmarkPendingKeysRef.current.add(bookmarkKey);
    setBookmarkBusyKeys((current) => [...current, bookmarkKey]);
    setBookmarkMessage(shouldSave ? "Question saved to Bookmarks." : "Question removed from Bookmarks.");
    setUser((current) => {
      if (!current) return current;
      const currentBookmarks = Array.isArray(current.questionBookmarks) ? current.questionBookmarks : [];
      const optimisticBookmarks = shouldSave
        ? [optimisticBookmark, ...currentBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey)].slice(0, 500)
        : currentBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey);
      return { ...current, questionBookmarks: optimisticBookmarks };
    });

    if (authStatus === "guest") {
      writeQuestionBookmarks(user, nextBookmarks);
      bookmarkPendingKeysRef.current.delete(bookmarkKey);
      setBookmarkBusyKeys((current) => current.filter((key) => key !== bookmarkKey));
      return;
    }

    const mutation = bookmarkMutationQueueRef.current
      .catch(() => undefined)
      .then(async () => {
        const data = await apiRequest("/api/profile/question-bookmarks", {
          method: "PATCH",
          body: JSON.stringify({
            questionId: bookmarkInput.questionId,
            subjectId: bookmarkInput.subjectId,
            mode: bookmarkInput.mode,
            saved: shouldSave,
          }),
          timeoutMs: 30000,
        });
        const savedBookmark = (data.bookmarks ?? []).find((bookmark) => getQuestionBookmarkKey(bookmark) === bookmarkKey);
        setUser((current) => {
          if (!current) return current;
          const currentBookmarks = Array.isArray(current.questionBookmarks) ? current.questionBookmarks : [];
          const withoutCurrent = currentBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey);
          return {
            ...current,
            questionBookmarks: shouldSave && savedBookmark
              ? [savedBookmark, ...withoutCurrent].slice(0, 500)
              : withoutCurrent,
          };
        });
      })
      .catch((error) => {
        setUser((current) => {
          if (!current) return current;
          const currentBookmarks = Array.isArray(current.questionBookmarks) ? current.questionBookmarks : [];
          const withoutCurrent = currentBookmarks.filter((bookmark) => getQuestionBookmarkKey(bookmark) !== bookmarkKey);
          return {
            ...current,
            questionBookmarks: shouldSave ? withoutCurrent : [optimisticBookmark, ...withoutCurrent].slice(0, 500),
          };
        });
        setBookmarkMessage(error instanceof Error ? error.message : "Could not update this bookmark.");
      })
      .finally(() => {
        bookmarkPendingKeysRef.current.delete(bookmarkKey);
        setBookmarkBusyKeys((current) => current.filter((key) => key !== bookmarkKey));
      });

    bookmarkMutationQueueRef.current = mutation;
    await mutation;
  }

  function toggleCurrentQuestionBookmark() {
    if (!currentPracticeQuestion || !currentPracticeSubject) return;
    void updateQuestionBookmark({
      questionId: currentPracticeQuestion.id,
      subjectId: currentPracticeSubject.id,
      mode: selectedPracticeMode,
      subjectTitle: currentPracticeSubject.title,
      topic: currentPracticeQuestion.chapterTitle || currentPracticeQuestion.topic,
      year: currentPracticeQuestion.year,
      preview: currentPracticeQuestion.leadIn || currentPracticeQuestion.prompt,
    }, !isCurrentPracticeQuestionBookmarked);
  }

  function openBookmarkedQuestion(entry) {
    if (!user?.hasPracticeAccess) { setActiveView("Practice"); return; }
    if (!entry?.resolved) {
      setBookmarkMessage("That question is no longer available in the current practice library.");
      return;
    }

    const { mode, subject, question } = entry.resolved;
    if (mode === "fmge") setPracticePathTitle("FMGE");
    if (subject.moduleNumber) setPracticePathTitle("USMLE–STEP 1");
    setSelectedPracticeSubjectId(subject.id);
    setSelectedPracticeMode(mode);
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setSelectedOption("");
    setSubmitted(false);
    setAnswerConfidence("");
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");

    if (mode === "pyq") {
      const yearKey = getQuestionYearKey(question);
      const yearQuestions = (subject.questions ?? []).filter((entryQuestion) => getQuestionYearKey(entryQuestion) === yearKey);
      setSelectedPracticeExamYear(yearKey);
      setUsmlePracticeQuestionIds([]);
      setPracticeQuestionIndex(Math.max(0, yearQuestions.findIndex((entryQuestion) => entryQuestion.id === question.id)));
    } else if (mode === "usmle") {
      setSelectedPracticeExamYear("");
      setUsmlePracticeQuestionIds([question.id]);
      setPracticeQuestionIndex(0);
    } else {
      setSelectedPracticeExamYear("");
      setUsmlePracticeQuestionIds([]);
      setPracticeQuestionIndex(Math.max(0, (subject.questions ?? []).findIndex((entryQuestion) => entryQuestion.id === question.id)));
    }

    setPracticeStage("subject");
    setPracticeQuestionStartedAt(Date.now());
    setBookmarkMessage("");
    updateActiveView("Practice");
    scrollPracticeViewToTop();
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
    setPracticeChoicePanel("formats");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setUsmlePracticeQuestionIds([]);
    scrollPracticeViewToTop();
  }

  function handleStartUsmlePractice(subjectId) {
    const catalogSubject = practiceSubjects.find((entry) => entry.id === subjectId);
    if (!catalogSubject) return;
    const subject = usmlePracticeSubjects.find((entry) => entry.id === subjectId);

    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode("usmle");
    setSelectedPracticeExamYear("");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setUsmlePracticeQuestionIds(shuffleQuestionIds(subject?.questions ?? []));
    setPracticeStage("subject");
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setPracticeQuestionStartedAt(Date.now());
    scrollPracticeViewToTop();
  }

  function handleStartVivaSetup(subjectId) {
    const subject = practiceSubjects.find((entry) => entry.id === subjectId);
    if (!subject) return;

    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode("viva");
    setSelectedPracticeExamYear("");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setVivaSelectedChapters([]);
    setVivaPrivacyAccepted(false);
    setVivaSessionMessage("");
    setVivaSession(null);
    setVivaAnswerDraft("");
    setVivaAnswerImage(null);
    setVivaAnswerBusy(false);
    setVivaAnswerMessage("");
    setPracticeStage("viva-setup");
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
    scrollPracticeViewToTop();
  }

  function toggleVivaChapter(chapterTitle) {
    setVivaSelectedChapters((current) =>
      current.includes(chapterTitle)
        ? current.filter((title) => title !== chapterTitle)
        : [...current, chapterTitle],
    );
  }

  async function handleCreateVivaSession() {
    if (!selectedPracticeSubjectId || !vivaSelectedChapters.length || !vivaPrivacyAccepted || vivaSessionBusy) return;

    setVivaSessionBusy(true);
    setVivaSessionMessage("");
    try {
      const data = await apiRequest("/api/viva/sessions", {
        method: "POST",
        body: JSON.stringify({
          subjectId: selectedPracticeSubjectId,
          chapters: vivaSelectedChapters,
          privacyAccepted: true,
        }),
        timeoutMs: 150000,
      });
      setVivaSession(data.session);
      setVivaAnswerDraft("");
      setVivaAnswerImage(null);
      setVivaAnswerMessage("");
      setPracticeStage("viva-session");
      scrollPracticeViewToTop();
    } catch (error) {
      setVivaSessionMessage(error.message);
    } finally {
      setVivaSessionBusy(false);
    }
  }

  async function handleSubmitVivaAnswer() {
    const answer = vivaAnswerDraft.trim();
    if (!vivaSession || !currentVivaQuestion || (!vivaAnswerImage && answer.length < 3) || vivaAnswerBusy || vivaAnswerImageBusy || currentVivaEvaluation) return;

    setVivaAnswerBusy(true);
    setVivaAnswerMessage("");
    try {
      const data = await apiRequest(`/api/viva/sessions/${vivaSession.id}/answers`, {
        method: "POST",
        body: JSON.stringify({
          questionId: currentVivaQuestion.id,
          answer,
          answerImageDataUrl: vivaAnswerImage?.dataUrl ?? null,
        }),
        timeoutMs: 150000,
      });
      setVivaSession(data.session);
      setVivaAnswerImage(null);
      scrollPracticeViewToTop();
    } catch (error) {
      setVivaAnswerMessage(error.message);
    } finally {
      setVivaAnswerBusy(false);
    }
  }

  async function handleAdvanceVivaSession() {
    if (!vivaSession || !currentVivaEvaluation || vivaAnswerBusy) return;

    setVivaAnswerBusy(true);
    setVivaAnswerMessage("");
    try {
      const data = await apiRequest(`/api/viva/sessions/${vivaSession.id}/advance`, {
        method: "POST",
        body: JSON.stringify({}),
        timeoutMs: 30000,
      });
      setVivaSession(data.session);
      setVivaAnswerDraft("");
      setVivaAnswerImage(null);
      if (data.session.status === "completed") setPracticeStage("viva-complete");
      scrollPracticeViewToTop();
    } catch (error) {
      setVivaAnswerMessage(error.message);
    } finally {
      setVivaAnswerBusy(false);
    }
  }

  function handleStartClinicalCasesSetup(subjectId) {
    const subject = practiceSubjects.find((entry) => entry.id === subjectId);
    if (!subject) return;

    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode("clinical-cases");
    setSelectedPracticeExamYear("");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setClinicalSelectedChapters([]);
    setClinicalPrivacyAccepted(false);
    setClinicalSessionMessage("");
    setClinicalSession(null);
    setClinicalAnswerDraft("");
    setClinicalAnswerImage(null);
    setClinicalAnswerBusy(false);
    setClinicalAnswerMessage("");
    setPracticeStage("clinical-setup");
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
    scrollPracticeViewToTop();
  }

  function toggleClinicalChapter(chapterTitle) {
    setClinicalSelectedChapters((current) =>
      current.includes(chapterTitle)
        ? current.filter((title) => title !== chapterTitle)
        : [...current, chapterTitle],
    );
  }

  async function handleCreateClinicalCaseSession() {
    if (!selectedPracticeSubjectId || !clinicalSelectedChapters.length || !clinicalPrivacyAccepted || clinicalSessionBusy) return;

    setClinicalSessionBusy(true);
    setClinicalSessionMessage("");
    try {
      const data = await apiRequest("/api/clinical-cases/sessions", {
        method: "POST",
        body: JSON.stringify({
          subjectId: selectedPracticeSubjectId,
          chapters: clinicalSelectedChapters,
          privacyAccepted: true,
        }),
        timeoutMs: 45000,
      });
      let readySession = data.session;
      const generationDeadline = Date.now() + CLINICAL_CASE_GENERATION_WAIT_MS;
      setClinicalSessionMessage("Gemini is preparing the cases. This page will open them automatically when they are ready.");

      while (readySession?.status === "generating" && Date.now() < generationDeadline) {
        await new Promise((resolve) => window.setTimeout(resolve, CLINICAL_CASE_GENERATION_POLL_MS));
        try {
          const statusData = await apiRequest(`/api/clinical-cases/sessions/${readySession.id}`, { timeoutMs: 15000 });
          readySession = statusData.session;
        } catch {
          // A brief Render/network interruption should not discard a generation job
          // that is still running safely on the server.
        }
      }

      if (readySession?.status === "generation_failed") {
        throw new Error(readySession.generationError || "Gemini could not prepare these clinical cases.");
      }
      if (readySession?.status !== "active") {
        throw new Error("Clinical Case generation is still running. Press Start clinical cases again to reconnect to it.");
      }

      setClinicalSession(readySession);
      setClinicalAnswerDraft("");
      setClinicalAnswerImage(null);
      setClinicalAnswerMessage("");
      setClinicalSessionMessage("");
      setPracticeStage("clinical-session");
      scrollPracticeViewToTop();
    } catch (error) {
      setClinicalSessionMessage(error instanceof Error ? error.message : "Could not create these clinical cases.");
    } finally {
      setClinicalSessionBusy(false);
    }
  }

  async function handleSubmitClinicalCaseAnswer() {
    const answer = clinicalAnswerDraft.trim();
    if (!clinicalSession || !currentClinicalCase || (!clinicalAnswerImage && answer.length < 3) || clinicalAnswerBusy || clinicalAnswerImageBusy || currentClinicalEvaluation) return;

    setClinicalAnswerBusy(true);
    setClinicalAnswerMessage("");
    try {
      const data = await apiRequest(`/api/clinical-cases/sessions/${clinicalSession.id}/answers`, {
        method: "POST",
        body: JSON.stringify({
          caseId: currentClinicalCase.id,
          answer,
          answerImageDataUrl: clinicalAnswerImage?.dataUrl ?? null,
        }),
        timeoutMs: 150000,
      });
      setClinicalSession(data.session);
      setClinicalAnswerImage(null);
      scrollPracticeViewToTop();
    } catch (error) {
      setClinicalAnswerMessage(error instanceof Error ? error.message : "Could not review this clinical case.");
    } finally {
      setClinicalAnswerBusy(false);
    }
  }

  async function handleAdvanceClinicalCaseSession() {
    if (!clinicalSession || !currentClinicalEvaluation || clinicalAnswerBusy) return;

    setClinicalAnswerBusy(true);
    setClinicalAnswerMessage("");
    try {
      const data = await apiRequest(`/api/clinical-cases/sessions/${clinicalSession.id}/advance`, {
        method: "POST",
        body: JSON.stringify({}),
        timeoutMs: 30000,
      });
      setClinicalSession(data.session);
      setClinicalAnswerDraft("");
      setClinicalAnswerImage(null);
      if (data.session.status === "completed") setPracticeStage("clinical-complete");
      scrollPracticeViewToTop();
    } catch (error) {
      setClinicalAnswerMessage(error instanceof Error ? error.message : "Could not continue this Clinical Cases session.");
    } finally {
      setClinicalAnswerBusy(false);
    }
  }

  function openPracticeChapter(chapterTitle) {
    setSelectedPracticeChapter(chapterTitle);
    setPracticeStage("topics");
    scrollPracticeViewToTop();
  }

  function openMindMapChapter(chapterTitle) {
    setSelectedPracticeChapter(chapterTitle);
    setSelectedPracticeTopic("");
    setPracticeStage("mind-map-topics");
    scrollPracticeViewToTop();
  }

  function openMindMapTopic(topic) {
    setSelectedPracticeTopic(topic);
    setPracticeStage("mind-map-detail");
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
    const data = await apiRequest(`/api/duels/questions?session=${encodeURIComponent(sessionId)}`, { cache: "no-store" });
    if (!Array.isArray(data.questions) || !data.questions.length) throw new Error("Could not load match questions.");
    duelDeadlineRef.current = Date.now() + Math.max(0, data.expiresAt - data.serverNow);
    loadedDuelRef.current = data;
    return data.questions;
  }

  function beginLiveDuel(opponent, options = {}) {
    const questions = Array.isArray(options.questions) && options.questions.length ? options.questions : fallbackDuelQuestions;
    setActiveView("Compete");
    setDuelQuestions(questions);
    setDuelMode(options.mode ?? "rated");
    setDuelSessionId(options.sessionId ?? "");
    setDuelOpponent(opponent);
    setShowDuelReview(false);
    setDuelTimeLeft(Math.max(0, Math.ceil((duelDeadlineRef.current - Date.now()) / 1000)));
    setDuelIndex(0);
    setDuelSelections({});
    setDuelSubmitted({});
    setDuelOpponentProgress({ answered: 0, correct: 0 });
    setDuelResult(null);
    setDuelQueueInfo(null);
    setDuelMessage("");
    setDuelForfeited(false);
    const saved = loadedDuelRef.current;
    if (saved) {
      const selections = {};
      const locked = {};
      questions.forEach((q, index) => {
        if (Object.hasOwn(saved.answers, q.id)) { selections[index] = q.options[saved.answers[q.id]]; locked[index] = true; }
      });
      setDuelSelections(selections);
      setDuelSubmitted(locked);
      const nextIndex = questions.findIndex((q, index) => !locked[index]);
      setDuelIndex(nextIndex < 0 ? questions.length - 1 : nextIndex);
    }
    localStorage.setItem(`medicomm-duel:${user.id}`, options.sessionId);
    setDuelStatus(saved?.finished || saved?.result ? "finished" : "live");
  }

  async function startDuel(preferredOpponent = null) {
    if (!user) {
      setAuthMode("login");
      setActiveView("Profile");
      return;
    }

    setActiveView("Compete");
    setDuelOpponent(null);
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

  async function submitDuelAnswer() {
    if (!currentDuelSelection || currentDuelSubmitted || !currentDuelQuestion || !user || duelAnswerPendingRef.current) return;
    const index = duelIndex;
    const selection = currentDuelSelection;
    duelAnswerPendingRef.current = true;
    setDuelAnswerBusy(true);
    try {
      await apiRequest("/api/duels/answer", { method: "POST", body: JSON.stringify({
        sessionId: duelSessionId, questionId: currentDuelQuestion.id,
        optionIndex: currentDuelQuestion.options.indexOf(selection),
      }) });
      setDuelSelections(current => ({ ...current, [index]: selection }));
      setDuelSubmitted(current => ({ ...current, [index]: true }));
      setDuelMessage("");
    } catch (error) { setDuelMessage(error.message); }
    finally { duelAnswerPendingRef.current = false; setDuelAnswerBusy(false); }
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
    localStorage.removeItem(`medicomm-duel:${user?.id}`);
    loadedDuelRef.current = null;
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
    setDuelOpponentProgress({ answered: 0, correct: 0 });
    setDuelResult(null);
    setDuelQueueInfo(null);
    setDuelMessage("");
    setDuelForfeited(false);
  }

  function updateAuthField(field, value) {
    setAuthForm((current) => ({ ...current, [field]: value }));
  }

  function updateSignupState(value) {
    setAuthForm((current) => ({
      ...current,
      medicalState: value,
      medicalCollege: value === ABROAD_STATE ? ABROAD_STATE : "",
    }));
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

  async function prepareVivaAnswerImage(file) {
    if (!file.type.startsWith("image/")) {
      throw new Error("Choose a photo or image of your written answer.");
    }
    if (file.size > VIVA_ANSWER_IMAGE_INPUT_LIMIT_BYTES) {
      throw new Error("Choose an image smaller than 12 MB.");
    }

    const sourceDataUrl = await convertFileToDataUrl(file);
    const image = await new Promise((resolve, reject) => {
      const previewImage = new Image();
      previewImage.onload = () => resolve(previewImage);
      previewImage.onerror = () => reject(new Error("This image format could not be opened. Try JPG, PNG, or WEBP."));
      previewImage.src = sourceDataUrl;
    });
    const scale = Math.min(1, VIVA_ANSWER_IMAGE_MAX_DIMENSION / Math.max(image.naturalWidth, image.naturalHeight));
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
    const context = canvas.getContext("2d");
    if (!context) throw new Error("This device could not prepare the image.");

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.drawImage(image, 0, 0, canvas.width, canvas.height);

    let quality = 0.9;
    let dataUrl = canvas.toDataURL("image/jpeg", quality);
    const getDataSize = (value) => Math.ceil(((value.split(",")[1] ?? "").length * 3) / 4);
    while (getDataSize(dataUrl) > VIVA_ANSWER_IMAGE_OUTPUT_LIMIT_BYTES && quality > 0.5) {
      quality -= 0.1;
      dataUrl = canvas.toDataURL("image/jpeg", quality);
    }
    if (getDataSize(dataUrl) > VIVA_ANSWER_IMAGE_OUTPUT_LIMIT_BYTES) {
      throw new Error("The prepared image is still too large. Crop it closer to your answer and try again.");
    }

    return {
      dataUrl,
      name: file.name || "Camera answer.jpg",
      width: canvas.width,
      height: canvas.height,
    };
  }

  async function handleVivaAnswerImageChange(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || vivaAnswerBusy || vivaAnswerImageBusy) return;

    setVivaAnswerImageBusy(true);
    setVivaAnswerMessage("Preparing your answer image...");
    try {
      const preparedImage = await prepareVivaAnswerImage(file);
      setVivaAnswerImage(preparedImage);
      setVivaAnswerMessage("");
    } catch (error) {
      setVivaAnswerMessage(error instanceof Error ? error.message : "Could not prepare that image.");
    } finally {
      setVivaAnswerImageBusy(false);
    }
  }

  async function handleClinicalAnswerImageChange(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || clinicalAnswerBusy || clinicalAnswerImageBusy) return;

    setClinicalAnswerImageBusy(true);
    setClinicalAnswerMessage("Preparing your answer image...");
    try {
      const preparedImage = await prepareVivaAnswerImage(file);
      setClinicalAnswerImage(preparedImage);
      setClinicalAnswerMessage("");
    } catch (error) {
      setClinicalAnswerMessage(error instanceof Error ? error.message : "Could not prepare that image.");
    } finally {
      setClinicalAnswerImageBusy(false);
    }
  }

  async function handleProfilePhotoChange(event) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || profileBusy || profilePhotoPreparing) return;
    if (!["image/png", "image/jpeg", "image/webp", "image/gif"].includes(file.type) || file.size > 5 * 1024 * 1024) {
      setProfileMessage("Choose a PNG, JPG, WebP or GIF image up to 5 MB."); return;
    }
    setProfilePhotoPreparing(true);
    try {
      const dataUrl = await convertFileToDataUrl(file);
      await new Promise((resolve, reject) => { const image = new Image(); image.onload = resolve; image.onerror = () => reject(new Error("This image could not be opened. Please choose another photo.")); image.src = dataUrl; });
      updateProfileField("profileImageDataUrl", dataUrl);
      setProfileMessage("Preview ready. Save photo to update your account.");
    } catch (error) {
      setProfileMessage(error instanceof Error ? error.message : "Could not load that image.");
    } finally { setProfilePhotoPreparing(false); }
  }

  async function handleAuthSubmit(event) {
    event.preventDefault();
    setAuthBusy(true);
    setAuthMessage("");

    const endpoint = authMode === "signup" ? "/api/auth/signup" : "/api/auth/login";
    const payload =
      authMode === "signup"
        ? {
            ...authForm,
            medicalCollege: authForm.medicalState === ABROAD_STATE ? ABROAD_STATE : authForm.medicalCollege,
          }
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

      localStorage.setItem(SESSION_TOKEN_KEY, "true");
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
        medicalState: "",
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
      questionBookmarks: [],
    };
    guestUser.questionBookmarks = readQuestionBookmarks(guestUser);
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

  async function handleProfileSave(event, photoOnly = false) {
    event?.preventDefault();
    if (profileBusy || profilePhotoPreparing) return;
    if (authStatus === "guest") {
      setProfileMessage("Create a free account to save profile changes across devices.");
      return;
    }
    setProfileBusy(true);
    setProfileMessage("");

    try {
      const data = await apiRequest("/api/profile", {
        method: "PATCH",
        body: JSON.stringify(photoOnly ? { ...createProfileState(user), profileImageDataUrl: profileState.profileImageDataUrl } : profileState),
        timeoutMs: 30000,
      });

      const mergedUser = mergeUserPerformance(data.user);
      setUser(mergedUser);
      setUserRating(mergedUser.rating ?? userRating);
      setProfileState(current => photoOnly ? { ...current, profileImageDataUrl: "" } : createProfileState(mergedUser));
      await fetchLeaderboard();
      setProfileMessage(photoOnly ? "Profile photo saved." : "Profile updated successfully.");
      accountOverview.reload();
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
          <div className="auth-brand"><span className="brand-mark" aria-hidden="true"><BrandMark title="" /></span><strong><span className="brand-medi">Med</span><span className="brand-comm">ulla</span></strong></div>
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
            <p className="eyebrow">Welcome to Medulla</p>
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
                <div className="auth-location-fields">
                  <label className="field">
                    <span>State</span>
                    <select
                      value={authForm.medicalState}
                      onChange={(event) => updateSignupState(event.target.value)}
                    >
                      <option value="">Select your state</option>
                      {signupStateOptions.map((state) => (
                        <option key={state} value={state}>{state}</option>
                      ))}
                    </select>
                  </label>
                  {authForm.medicalState && authForm.medicalState !== ABROAD_STATE ? (
                    <label className="field">
                      <span>Medical college</span>
                      <select
                        value={authForm.medicalCollege}
                        onChange={(event) => updateAuthField("medicalCollege", event.target.value)}
                      >
                        <option value="">Select from {signupCollegeOptions.length} colleges</option>
                        {signupCollegeOptions.map((college) => (
                          <option key={college} value={college}>{college}</option>
                        ))}
                      </select>
                    </label>
                  ) : null}
                  {authForm.medicalState === ABROAD_STATE ? (
                    <p className="auth-location-note">Foreign students can continue without selecting an Indian college.</p>
                  ) : null}
                </div>
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
                  placeholder="12 to 128 characters"
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
            <h2>Why Choose Medulla?</h2>
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

        <WebsiteReviews compact canReview={authStatus === "authenticated"} onSignIn={handleLogout} onViewAll={() => setActiveView("Reviews")} />

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

  function continueDashboardPractice(entry) {
    if (!entry) { setActiveView("Practice"); return; }
    if (practiceLibraryStatus !== "ready") {
      setDashboardPracticeTarget(entry);
      setActiveView("Practice");
      return;
    }
    const resolved = bookmarkQuestionIndex.get(getQuestionBookmarkKey(entry));
    if (!resolved) { setActiveView("Practice"); return; }
    const questions = resolved.subject.questions ?? [];
    const index = questions.findIndex(question => question.id === resolved.question.id);
    const next = !entry.topic ? questions[index + 1] : null;
    setPracticePathTitle(entry.mode === "fmge" ? "FMGE" : entry.mode === "usmle" ? "USMLE–STEP 1" : "NEET PG / INICET");
    openBookmarkedQuestion({ resolved: next ? { ...resolved, question: next } : resolved });
  }

  function renderDashboard() {
    return <section className="app-view">
      <DashboardSummary user={user} overview={accountOverview} guest={authStatus === "guest"} onContinue={() => continueDashboardPractice(accountOverview.data?.resume)} />
      <DashboardActivity overview={accountOverview} guest={authStatus === "guest"} sync={practiceSync} onPractice={continueDashboardPractice} onCompete={() => setActiveView("Compete")} onProfile={() => setActiveView("Profile")} />
    </section>;
  }

  function renderPracticeLock() {
    return <section className="app-view"><div className="practice-access-lock"><span className="lock-symbol" aria-hidden="true">🔒</span><p className="eyebrow">Your next chapter starts here</p><h2>Unlock your practice journey</h2><p>Get access to questions, theory and saved practice after your payment is verified. Use <strong>PRELAUNCH</strong> at checkout to start for just <strong>₹9</strong>.</p><button className="button button-primary" onClick={() => setActiveView("Pricing")}>View plans &amp; unlock Practice</button></div></section>;
  }

  function renderPractice() {
    if (!user?.hasPracticeAccess) return renderPracticeLock();
    const isTheory = practicePathTitle === "THEORY";
    const catalogTitle = isTheory ? "Cases and short notes by subject" : `${practiceLibrary.exam.title} by year and subject`;
    if (practiceStage === "selection") {
      return <PracticeSelection onSelect={(title, id) => {
        setPracticePathTitle(title);
        setPracticeStage(id === "usmle" ? "usmle-modules" : id === "fmge" ? "fmge-years" : "catalog");
        scrollPracticeViewToTop();
      }} />;
    }

    if (practiceStage === "fmge-years") {
      return <FmgeYears sessions={fmgeSessions} progress={practiceProgress} status={practiceLibraryStatus} onRetry={fetchPracticeLibrary} onStart={(sessionId) => {
        startPracticeSession(sessionId, "fmge");
        scrollPracticeViewToTop();
      }} onBack={() => {
        setPracticeStage("selection");
        scrollPracticeViewToTop();
      }} />;
    }

    if (practiceStage === "usmle-modules") {
      return <UsmleModules modules={usmleModules} progress={practiceProgress} status={practiceLibraryStatus} onRetry={fetchPracticeLibrary} onStart={(moduleId) => {
        startPracticeSession(moduleId, "usmle");
        scrollPracticeViewToTop();
      }} onBack={() => {
        setActiveView("Practice");
        scrollPracticeViewToTop();
      }} />;
    }

    if (practiceLibraryStatus === "idle" || practiceLibraryStatus === "loading") {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
              <h2>{catalogTitle}</h2>
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
              <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
              <h2>{catalogTitle}</h2>
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

    if (!practiceSubjects.length && !currentPracticeSubject?.moduleNumber && selectedPracticeMode !== "fmge") {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
              <h2>{catalogTitle}</h2>
            </div>
          </div>

          <article className="card panel">
            <h3>No practice questions yet</h3>
            <p className="panel-copy">The local practice database is empty right now.</p>
          </article>
        </section>
      );
    }

    if (isTheory && practiceStage === "short-notes") {
      return <ShortNotes
        key={`${user?.id || "guest"}-${selectedPracticeSubjectId}`}
        subjectId={selectedPracticeSubjectId}
        subjectTitle={currentPracticeSubject?.title}
        userId={user?.id}
        onBack={handleBackToPracticeDirectory}
        prepareImage={prepareVivaAnswerImage}
        onNavigate={scrollPracticeViewToTop}
      />;
    }

    const isUsmlePractice = selectedPracticeMode === "usmle";
    const isFmgePractice = selectedPracticeMode === "fmge";
    const isModulePractice = isUsmlePractice && Boolean(currentPracticeSubject?.moduleNumber);
    const isSupplementalPractice = selectedPracticeMode === "ai" || isUsmlePractice;
    const isDirectoryPractice = selectedPracticeMode === "ai";
    const directoryModeTitle = isModulePractice ? "USMLE Step 1 · Integrated practice" : isUsmlePractice ? "USMLE Step-1 Format Questions" : "Topic Wise Questions";

    if (["mind-map-chapters", "mind-map-topics", "mind-map-detail"].includes(practiceStage)) {
      const mindMapSubject = aiPracticeSubjects.find((subject) => subject.id === selectedPracticeSubjectId) ?? null;
      const chapters = Object.values((mindMapSubject?.questions ?? []).reduce((groups, question) => {
        const chapterTitle = question.chapterTitle || "General Concepts";
        const chapterOrder = getPracticeChapterOrder({ ...question, chapterTitle }, mindMapSubject?.id);
        const topic = question.topic || "General Review";
        groups[chapterTitle] ??= { title: chapterTitle, order: chapterOrder, topics: {} };
        groups[chapterTitle].order = Math.min(groups[chapterTitle].order, chapterOrder);
        groups[chapterTitle].topics[topic] ??= { topic, order: directoryOrder(question.topicOrder), questions: [] };
        groups[chapterTitle].topics[topic].order = Math.min(groups[chapterTitle].topics[topic].order, directoryOrder(question.topicOrder));
        groups[chapterTitle].topics[topic].questions.push(question);
        return groups;
      }, {})).sort(comparePracticeDirectoryEntries);

      if (!chapters.length) {
        return (
          <section className="app-view mind-maps-view topic-wise-directory">
            <div className="view-header">
              <div>
                <p className="eyebrow">{mindMapSubject?.title ?? "Subject"} · Mind Maps</p>
                <h2>Mind map directory is not ready yet</h2>
                <p className="view-subtitle">Chapters and topics will appear here when topic-wise content is added for this subject.</p>
              </div>
              <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
            </div>
          </section>
        );
      }

      if (practiceStage === "mind-map-chapters") {
        return (
          <section className="app-view mind-maps-view topic-wise-directory">
            <div className="view-header">
              <div>
                <p className="eyebrow">{mindMapSubject?.title} · Mind Maps</p>
                <h2>Choose a chapter</h2>
                <p className="view-subtitle">Browse the same chapter structure as Topic Wise Questions.</p>
              </div>
              <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
            </div>
            <div className="topic-directory-list">
              {chapters.map((chapter, index) => (
                <button type="button" className="topic-directory-row chapter-directory-row" key={chapter.title} onClick={() => openMindMapChapter(chapter.title)}>
                  <span className="directory-index">{String(index + 1).padStart(2, "0")}</span>
                  <span className="directory-main">
                    <span className="directory-kicker">Chapter {index + 1}</span>
                    <strong>{chapter.title}</strong>
                    <span className="directory-meta">{Object.keys(chapter.topics).length} topics</span>
                  </span>
                  <span className="directory-arrow" aria-hidden="true">→</span>
                </button>
              ))}
            </div>
          </section>
        );
      }

      const chapter = chapters.find((entry) => entry.title === selectedPracticeChapter);
      const selectedMindMapAsset = MIND_MAP_ASSETS[selectedPracticeSubjectId]?.[selectedPracticeTopic] ?? "";

      if (practiceStage === "mind-map-topics") {
        return (
          <section className="app-view mind-maps-view topic-wise-directory">
            <div className="view-header">
              <div>
                <p className="eyebrow">Mind Maps · Chapter topics</p>
                <h2>{chapter?.title ?? "Choose a topic"}</h2>
                <p className="view-subtitle">Choose a topic to open its visual revision map.</p>
              </div>
              <button className="button button-secondary" type="button" onClick={() => setPracticeStage("mind-map-chapters")}>Back to chapters</button>
            </div>
            <div className="topic-directory-list">
              {Object.values(chapter?.topics ?? {}).sort(comparePracticeDirectoryEntries).map(({ topic }, index) => {
                const hasMindMap = Boolean(MIND_MAP_ASSETS[selectedPracticeSubjectId]?.[topic]);
                return (
                  <button type="button" className="topic-directory-row" key={topic} onClick={() => openMindMapTopic(topic)}>
                    <span className="directory-index">{String(index + 1).padStart(2, "0")}</span>
                    <span className="directory-main">
                      <span className="directory-kicker">Topic {index + 1}</span>
                      <strong>{topic}</strong>
                      <span className={`directory-meta${hasMindMap ? " mind-map-available" : ""}`}>{hasMindMap ? "Mind map available" : "Coming soon"}</span>
                    </span>
                    <span className="directory-arrow" aria-hidden="true">→</span>
                  </button>
                );
              })}
            </div>
          </section>
        );
      }

      return (
        <section className="app-view mind-maps-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{mindMapSubject?.title} · {chapter?.title}</p>
              <h2>{selectedPracticeTopic}</h2>
              <p className="view-subtitle">Mind Map</p>
            </div>
            <button className="button button-secondary" type="button" onClick={() => setPracticeStage("mind-map-topics")}>Back to topics</button>
          </div>
          {selectedMindMapAsset ? (
            <article className="card panel mind-map-reader">
              <img src={selectedMindMapAsset} alt={`${selectedPracticeTopic} pharmacology mind map`} />
              <div className="mind-map-reader-actions">
                <a className="button button-secondary" href={selectedMindMapAsset} target="_blank" rel="noreferrer">Open full size</a>
                <a className="button button-primary" href={selectedMindMapAsset} download>Download 4K notes</a>
              </div>
            </article>
          ) : (
            <article className="card panel mind-maps-empty-state">
              <span className="mind-maps-empty-icon" aria-hidden="true">MAP</span>
              <div>
                <h3>This mind map is coming soon</h3>
                <p className="panel-copy">The chapter and topic directory is ready for visual summaries to be added.</p>
              </div>
            </article>
          )}
        </section>
      );
    }

    if (practiceStage === "clinical-complete" && clinicalSession) {
      return (
        <section className="app-view viva-session-view clinical-session-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{clinicalSession.subjectTitle} · Clinical Cases complete</p>
              <h2>Your final score is {clinicalSession.averageScore} / 10</h2>
              <p className="view-subtitle">Gemini reviewed all three theory responses against case-specific marking points.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
          </div>

          <article className="card panel viva-complete-panel clinical-complete-panel">
            <div className="viva-final-score" aria-label={`Final Clinical Cases score ${clinicalSession.averageScore} out of 10`}>
              <strong>{clinicalSession.averageScore}</strong>
              <span>out of 10</span>
              <small>{clinicalSession.totalScore} points across {clinicalSession.caseCount} cases</small>
            </div>
            <div className="viva-score-list">
              {(clinicalSession.answers ?? []).map((evaluation, index) => {
                const clinicalCase = clinicalSession.cases?.[evaluation.caseIndex];
                return (
                  <article key={evaluation.caseId}>
                    <span>C{index + 1}</span>
                    <div>
                      <strong>{clinicalCase?.stem ?? `Clinical case ${index + 1}`}</strong>
                      <small>{evaluation.feedback}</small>
                    </div>
                    <em>{evaluation.score}/10</em>
                  </article>
                );
              })}
            </div>
            <button
              className="button button-primary"
              type="button"
              onClick={() => {
                setClinicalSession(null);
                setClinicalAnswerDraft("");
                setClinicalAnswerImage(null);
                setClinicalAnswerMessage("");
                setPracticeStage("clinical-setup");
                scrollPracticeViewToTop();
              }}
            >
              Start another case set
            </button>
          </article>
        </section>
      );
    }

    if (practiceStage === "clinical-session" && clinicalSession && currentClinicalCase) {
      const caseNumber = (clinicalSession.currentCaseIndex ?? 0) + 1;
      const progressPercent = Math.round((caseNumber / clinicalSession.caseCount) * 100);

      return (
        <section className="app-view viva-session-view clinical-session-view">
          <div className="view-header viva-session-header">
            <div>
              <p className="eyebrow">{clinicalSession.subjectTitle} · Clinical Cases</p>
              <h2>Case {caseNumber} of {clinicalSession.caseCount}</h2>
              <p className="view-subtitle">Write a structured theory answer covering every labeled question.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={() => setPracticeStage("clinical-setup")}>Change chapters</button>
          </div>

          <article className="card panel viva-question-panel clinical-case-panel">
            <div className="viva-session-progress-copy">
              <span>{progressPercent}% through this case set</span>
              <span>Final score after {clinicalSession.caseCount} cases</span>
            </div>
            <span className="practice-progress-track viva-session-progress" aria-hidden="true"><span style={{ width: `${progressPercent}%` }} /></span>

            <div className="viva-question-meta">
              <span className="rank-pill source-clinical">{currentClinicalCase.chapterTitle}</span>
              <span>{currentClinicalCase.difficulty}</span>
            </div>
            <section className="clinical-case-stem" aria-labelledby="clinical-case-title">
              <p className="eyebrow">Case stem</p>
              <h3 id="clinical-case-title">{currentClinicalCase.stem}</h3>
            </section>
            <ol className="clinical-subquestions">
              {currentClinicalCase.subquestions.map((subquestion) => (
                <li key={`${subquestion.label}-${subquestion.prompt}`}>
                  <span>{subquestion.label}</span>
                  <p>{subquestion.prompt}</p>
                  <em>{subquestion.marks} {subquestion.marks === 1 ? "mark" : "marks"}</em>
                </li>
              ))}
            </ol>

            {currentClinicalEvaluation ? (
              <div className="viva-evaluation" aria-live="polite">
                <div className="viva-evaluation-heading">
                  <div className="viva-score-badge">
                    <strong>{currentClinicalEvaluation.score}</strong>
                    <span>/ 10</span>
                  </div>
                  <div>
                    <p className="eyebrow">Gemini theory review</p>
                    <h4>{currentClinicalEvaluation.feedback}</h4>
                  </div>
                </div>

                <div className="viva-evaluation-grid">
                  <section>
                    <h5>What you did well</h5>
                    {currentClinicalEvaluation.strengths?.length ? (
                      <ul>{currentClinicalEvaluation.strengths.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}</ul>
                    ) : (
                      <p>Build a more complete response using the improvements below.</p>
                    )}
                  </section>
                  <section>
                    <h5>How to improve</h5>
                    <ul>{currentClinicalEvaluation.improvements.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}</ul>
                  </section>
                </div>

                <section className="viva-model-answer">
                  <h5>Exam-ready model answer</h5>
                  {currentClinicalEvaluation.modelAnswerSections?.length ? (
                    <div className="clinical-model-answer-sections">
                      {currentClinicalEvaluation.modelAnswerSections.map((section) => (
                        <article key={section.label} className="clinical-model-answer-section">
                          <header>
                            <span>{section.label}</span>
                            <h6>{section.heading}</h6>
                          </header>
                          <ul>
                            {section.points.map((point, index) => <li key={`${section.label}-${index}-${point}`}>{point}</li>)}
                          </ul>
                          {section.flowchart ? (
                            <div className="clinical-model-flowchart">
                              <strong>Flowchart</strong>
                              <p>{section.flowchart}</p>
                            </div>
                          ) : null}
                        </article>
                      ))}
                    </div>
                  ) : (
                    <p>{currentClinicalEvaluation.modelAnswer}</p>
                  )}
                </section>

                <TextbookSources sources={currentClinicalEvaluation.textbookSources} />
                <AnswerNotepad key={currentClinicalCase.id} draftId={`clinical:${user?.id || "guest"}:${clinicalSession.id}:${currentClinicalCase.id}`} prompt={currentClinicalCase.stem} />
                <details className="viva-submitted-answer">
                  <summary>Your submitted response</summary>
                  {currentClinicalEvaluation.answer ? <p>{currentClinicalEvaluation.answer}</p> : null}
                  {currentClinicalEvaluation.hasImage ? <p className="viva-submitted-image-note">A photographed written answer was included in Gemini&apos;s review.</p> : null}
                </details>

                {clinicalAnswerMessage ? <p className="form-message" role="alert">{clinicalAnswerMessage}</p> : null}
                <div className="viva-answer-actions">
                  <p>Your score and review have been saved to this Clinical Cases session.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={clinicalAnswerBusy}
                    onClick={handleAdvanceClinicalCaseSession}
                    aria-busy={clinicalAnswerBusy}
                  >
                    {clinicalAnswerBusy
                      ? "Loading..."
                      : caseNumber === clinicalSession.caseCount
                        ? "Finish case set"
                        : "Next case"}
                  </button>
                </div>
              </div>
            ) : (
              <>
                <label className="viva-answer-field">
                  <span>Your complete theory response</span>
                  <textarea
                    value={clinicalAnswerDraft}
                    onChange={(event) => setClinicalAnswerDraft(event.target.value.slice(0, 8000))}
                    rows={13}
                    placeholder="A. Diagnosis…\nB. Pathogenesis…\nC. Morphology / investigations…"
                    disabled={clinicalAnswerBusy}
                    autoFocus
                  />
                  <small>{clinicalAnswerDraft.length} / 8000 characters</small>
                </label>

                <section className="viva-image-answer" aria-labelledby="clinical-image-answer-title">
                  <div className="viva-image-answer-heading">
                    <div>
                      <strong id="clinical-image-answer-title">Upload your written theory answer</strong>
                      <span>Gemini can review clear handwriting from a photographed answer sheet.</span>
                    </div>
                    <span className="viva-image-optional">Optional</span>
                  </div>

                  {clinicalAnswerImage ? (
                    <div className="viva-image-preview">
                      <img src={clinicalAnswerImage.dataUrl} alt="Preview of your written clinical case answer" />
                      <div>
                        <strong>{clinicalAnswerImage.name}</strong>
                        <span>{clinicalAnswerImage.width} × {clinicalAnswerImage.height}px · ready for review</span>
                      </div>
                      <button type="button" onClick={() => setClinicalAnswerImage(null)} disabled={clinicalAnswerBusy} aria-label="Remove written answer image">×</button>
                    </div>
                  ) : (
                    <div className="viva-image-picker-actions">
                      <label className="button button-secondary viva-image-picker-button">
                        <input type="file" accept="image/*" capture="environment" onChange={handleClinicalAnswerImageChange} disabled={clinicalAnswerBusy || clinicalAnswerImageBusy} />
                        <span aria-hidden="true">◉</span> Take photo
                      </label>
                      <label className="button button-secondary viva-image-picker-button">
                        <input type="file" accept="image/jpeg,image/png,image/webp,image/heic,image/heif" onChange={handleClinicalAnswerImageChange} disabled={clinicalAnswerBusy || clinicalAnswerImageBusy} />
                        <span aria-hidden="true">▧</span> Choose from gallery
                      </label>
                    </div>
                  )}
                  <small>Use good lighting, keep the full page in frame, and do not include patient-identifiable information.</small>
                  <AnswerNotepad key={currentClinicalCase.id} draftId={`clinical:${user?.id || "guest"}:${clinicalSession.id}:${currentClinicalCase.id}`} prompt={currentClinicalCase.stem} disabled={clinicalAnswerBusy || clinicalAnswerImageBusy} hasImage={Boolean(clinicalAnswerImage)} onSave={image => { setClinicalAnswerImage(image); setClinicalAnswerMessage(""); }} />
                </section>

                {clinicalAnswerMessage ? <p className="form-message" role="alert">{clinicalAnswerMessage}</p> : null}
                <div className="viva-answer-actions">
                  <p>Gemini will grade diagnosis, reasoning, morphology, and investigations against private case-specific marking points.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={(!clinicalAnswerImage && clinicalAnswerDraft.trim().length < 3) || clinicalAnswerBusy || clinicalAnswerImageBusy}
                    onClick={handleSubmitClinicalCaseAnswer}
                    aria-busy={clinicalAnswerBusy}
                  >
                    {clinicalAnswerBusy ? "Gemini is reviewing..." : "Submit case for AI review"}
                  </button>
                </div>
              </>
            )}
          </article>
        </section>
      );
    }

    if (practiceStage === "clinical-setup") {
      const clinicalSubject = practiceSubjects.find((subject) => subject.id === selectedPracticeSubjectId) ?? null;
      const allChaptersSelected = vivaChapterOptions.length > 0 && clinicalSelectedChapters.length === vivaChapterOptions.length;

      return (
        <section className="app-view viva-setup-view clinical-setup-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{clinicalSubject?.title ?? "Practice"} · Clinical Cases</p>
              <h2>Choose one or more chapters</h2>
              <p className="view-subtitle">Gemini will create three applied theory cases in the selected chapters.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
          </div>

          <article className="card panel viva-setup-panel clinical-setup-panel">
            <div className="viva-setup-toolbar">
              <div>
                <strong>{clinicalSelectedChapters.length} selected</strong>
                <span>Choose a focused chapter or mix several for a broader case paper.</span>
              </div>
              <button
                className="button button-secondary"
                type="button"
                onClick={() => setClinicalSelectedChapters(allChaptersSelected ? [] : vivaChapterOptions.map((chapter) => chapter.title))}
              >
                {allChaptersSelected ? "Clear all" : "Select all"}
              </button>
            </div>

            {vivaChapterOptions.length ? (
              <div className="viva-chapter-grid">
                {vivaChapterOptions.map((chapter, index) => {
                  const selected = clinicalSelectedChapters.includes(chapter.title);
                  return (
                    <button
                      className={`viva-chapter-card clinical-chapter-card${selected ? " is-selected" : ""}`}
                      type="button"
                      key={chapter.title}
                      aria-pressed={selected}
                      onClick={() => toggleClinicalChapter(chapter.title)}
                    >
                      <span className="viva-chapter-check" aria-hidden="true">{selected ? "✓" : String(index + 1).padStart(2, "0")}</span>
                      <span>
                        <strong>{chapter.title}</strong>
                        <small>{chapter.count ? `${chapter.count} source questions available` : "Curriculum chapter"}</small>
                      </span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <p className="form-message">A chapter directory has not been added for this subject yet.</p>
            )}

            <label className="viva-privacy-notice clinical-privacy-notice">
              <input type="checkbox" checked={clinicalPrivacyAccepted} onChange={(event) => setClinicalPrivacyAccepted(event.target.checked)} />
              <span>
                <strong>AI privacy notice</strong>
                <small>Your selected chapters, typed answers, and uploaded answer images will be sent to the configured AI provider. Images are not saved in your Clinical Cases history. Do not include names, contact details, or patient-identifiable information.</small>
              </span>
            </label>

            {clinicalSessionMessage ? <p className="form-message viva-session-message" role="alert">{clinicalSessionMessage}</p> : null}

            <div className="viva-setup-footer">
              <p><strong>3 applied cases</strong><span>Diagnosis + theory prompts · typed or photographed answers · score out of 10</span></p>
              <button
                className="button button-primary"
                type="button"
                disabled={!clinicalSelectedChapters.length || !clinicalPrivacyAccepted || clinicalSessionBusy}
                onClick={handleCreateClinicalCaseSession}
                aria-busy={clinicalSessionBusy}
              >
                {clinicalSessionBusy ? "Preparing clinical cases..." : "Start clinical cases"}
              </button>
            </div>
            <p className="viva-build-note">Preparing three applied cases usually takes a few seconds.</p>
          </article>
        </section>
      );
    }

    if (practiceStage === "viva-complete" && vivaSession) {
      return (
        <section className="app-view viva-session-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{vivaSession.subjectTitle} · AI Viva complete</p>
              <h2>Your final score is {vivaSession.averageScore} / 10</h2>
              <p className="view-subtitle">Gemini reviewed all five responses against the question-specific marking points.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
          </div>

          <article className="card panel viva-complete-panel">
            <div className="viva-final-score" aria-label={`Final Viva score ${vivaSession.averageScore} out of 10`}>
              <strong>{vivaSession.averageScore}</strong>
              <span>out of 10</span>
              <small>{vivaSession.totalScore} points across {vivaSession.questionCount} questions</small>
            </div>
            <div className="viva-score-list">
              {(vivaSession.answers ?? []).map((evaluation, index) => {
                const question = vivaSession.questions?.[evaluation.questionIndex];
                return (
                  <article key={evaluation.questionId}>
                    <span>Q{index + 1}</span>
                    <div>
                      <strong>{question?.prompt ?? `Question ${index + 1}`}</strong>
                      <small>{evaluation.feedback}</small>
                    </div>
                    <em>{evaluation.score}/10</em>
                  </article>
                );
              })}
            </div>
            <button
              className="button button-primary"
              type="button"
              onClick={() => {
                setVivaSession(null);
                setVivaAnswerDraft("");
                setVivaAnswerImage(null);
                setVivaAnswerMessage("");
                setPracticeStage("viva-setup");
                scrollPracticeViewToTop();
              }}
            >
              Start another viva
            </button>
          </article>
        </section>
      );
    }

    if (practiceStage === "viva-session" && vivaSession && currentVivaQuestion) {
      const questionNumber = (vivaSession.currentQuestionIndex ?? 0) + 1;
      const progressPercent = Math.round((questionNumber / vivaSession.questionCount) * 100);

      return (
        <section className="app-view viva-session-view">
          <div className="view-header viva-session-header">
            <div>
              <p className="eyebrow">{vivaSession.subjectTitle} · AI Viva</p>
              <h2>Question {questionNumber} of {vivaSession.questionCount}</h2>
              <p className="view-subtitle">Answer naturally, as you would when speaking to an examiner.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={() => setPracticeStage("viva-setup")}>Change chapters</button>
          </div>

          <article className="card panel viva-question-panel">
            <div className="viva-session-progress-copy">
              <span>{progressPercent}% through this viva</span>
              <span>Final score after 5 questions</span>
            </div>
            <span className="practice-progress-track viva-session-progress" aria-hidden="true"><span style={{ width: `${progressPercent}%` }} /></span>

            <div className="viva-question-meta">
              <span className="rank-pill source-viva">{currentVivaQuestion.chapterTitle}</span>
              <span>{currentVivaQuestion.difficulty}</span>
            </div>
            <h3>{currentVivaQuestion.prompt}</h3>

            {currentVivaEvaluation ? (
              <div className="viva-evaluation" aria-live="polite">
                <div className="viva-evaluation-heading">
                  <div className="viva-score-badge">
                    <strong>{currentVivaEvaluation.score}</strong>
                    <span>/ 10</span>
                  </div>
                  <div>
                    <p className="eyebrow">Gemini review</p>
                    <h4>{currentVivaEvaluation.feedback}</h4>
                  </div>
                </div>

                <div className="viva-evaluation-grid">
                  <section>
                    <h5>What you did well</h5>
                    {currentVivaEvaluation.strengths?.length ? (
                      <ul>{currentVivaEvaluation.strengths.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}</ul>
                    ) : (
                      <p>Build a more complete response using the improvements below.</p>
                    )}
                  </section>
                  <section>
                    <h5>How to improve</h5>
                    <ul>{currentVivaEvaluation.improvements.map((item, index) => <li key={`${index}-${item}`}>{item}</li>)}</ul>
                  </section>
                </div>

                <section className="viva-model-answer">
                  <h5>Exam-ready model answer</h5>
                  <p>{currentVivaEvaluation.modelAnswer}</p>
                </section>

                <details className="viva-submitted-answer">
                  <summary>Your submitted response</summary>
                  {currentVivaEvaluation.answer ? <p>{currentVivaEvaluation.answer}</p> : null}
                  {currentVivaEvaluation.hasImage ? <p className="viva-submitted-image-note">A photographed written answer was included in Gemini&apos;s review.</p> : null}
                </details>

                {vivaAnswerMessage ? <p className="form-message" role="alert">{vivaAnswerMessage}</p> : null}
                <div className="viva-answer-actions">
                  <p>Your score and review have been saved to this Viva session.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={vivaAnswerBusy}
                    onClick={handleAdvanceVivaSession}
                    aria-busy={vivaAnswerBusy}
                  >
                    {vivaAnswerBusy
                      ? "Loading..."
                      : questionNumber === vivaSession.questionCount
                        ? "Finish viva"
                        : "Next question"}
                  </button>
                </div>
              </div>
            ) : (
              <>
                <label className="viva-answer-field">
                  <span>Your response</span>
                  <textarea
                    value={vivaAnswerDraft}
                    onChange={(event) => setVivaAnswerDraft(event.target.value.slice(0, 4000))}
                    rows={9}
                    placeholder="Explain your answer in a clear, structured way..."
                    disabled={vivaAnswerBusy}
                    autoFocus
                  />
                  <small>{vivaAnswerDraft.length} / 4000 characters</small>
                </label>

                <section className="viva-image-answer" aria-labelledby="viva-image-answer-title">
                  <div className="viva-image-answer-heading">
                    <div>
                      <strong id="viva-image-answer-title">Upload your written answer</strong>
                      <span>Skip lengthy typing—Gemini can read clear handwriting from a photo.</span>
                    </div>
                    <span className="viva-image-optional">Optional</span>
                  </div>

                  {vivaAnswerImage ? (
                    <div className="viva-image-preview">
                      <img src={vivaAnswerImage.dataUrl} alt="Preview of your written Viva answer" />
                      <div>
                        <strong>{vivaAnswerImage.name}</strong>
                        <span>{vivaAnswerImage.width} × {vivaAnswerImage.height}px · ready for review</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => setVivaAnswerImage(null)}
                        disabled={vivaAnswerBusy}
                        aria-label="Remove written answer image"
                      >
                        ×
                      </button>
                    </div>
                  ) : (
                    <div className="viva-image-picker-actions">
                      <label className="button button-secondary viva-image-picker-button">
                        <input
                          type="file"
                          accept="image/*"
                          capture="environment"
                          onChange={handleVivaAnswerImageChange}
                          disabled={vivaAnswerBusy || vivaAnswerImageBusy}
                        />
                        <span aria-hidden="true">◉</span> Take photo
                      </label>
                      <label className="button button-secondary viva-image-picker-button">
                        <input
                          type="file"
                          accept="image/jpeg,image/png,image/webp,image/heic,image/heif"
                          onChange={handleVivaAnswerImageChange}
                          disabled={vivaAnswerBusy || vivaAnswerImageBusy}
                        />
                        <span aria-hidden="true">▧</span> Choose from gallery
                      </label>
                    </div>
                  )}
                  <small>For best results, use good lighting, keep the full page in frame, and avoid patient-identifiable information.</small>
                  <AnswerNotepad key={currentVivaQuestion.id} draftId={`viva:${user?.id || "guest"}:${vivaSession.id}:${currentVivaQuestion.id}`} prompt={currentVivaQuestion.prompt} disabled={vivaAnswerBusy || vivaAnswerImageBusy} hasImage={Boolean(vivaAnswerImage)} onSave={image => { setVivaAnswerImage(image); setVivaAnswerMessage(""); }} />
                </section>

                {vivaAnswerMessage ? <p className="form-message" role="alert">{vivaAnswerMessage}</p> : null}
                <div className="viva-answer-actions">
                  <p>Gemini will review your typed response, uploaded answer, or both against the private marking points and prepare a score and model answer.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={(!vivaAnswerImage && vivaAnswerDraft.trim().length < 3) || vivaAnswerBusy || vivaAnswerImageBusy}
                    onClick={handleSubmitVivaAnswer}
                    aria-busy={vivaAnswerBusy}
                  >
                    {vivaAnswerBusy ? "Gemini is reviewing..." : "Submit for AI review"}
                  </button>
                </div>
              </>
            )}
          </article>
        </section>
      );
    }

    if (practiceStage === "viva-setup") {
      const vivaSubject = practiceSubjects.find((subject) => subject.id === selectedPracticeSubjectId) ?? null;
      const allChaptersSelected = vivaChapterOptions.length > 0 && vivaSelectedChapters.length === vivaChapterOptions.length;

      return (
        <section className="app-view viva-setup-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">{vivaSubject?.title ?? "Practice"} · AI Viva</p>
              <h2>Choose one or more chapters</h2>
              <p className="view-subtitle">Your examiner will ask five explanatory questions drawn only from the chapters you select.</p>
            </div>
            <button className="button button-secondary" type="button" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
          </div>

          <article className="card panel viva-setup-panel">
            <div className="viva-setup-toolbar">
              <div>
                <strong>{vivaSelectedChapters.length} selected</strong>
                <span>Select a focused chapter or mix several for a broader viva.</span>
              </div>
              <button
                className="button button-secondary"
                type="button"
                onClick={() => setVivaSelectedChapters(allChaptersSelected ? [] : vivaChapterOptions.map((chapter) => chapter.title))}
              >
                {allChaptersSelected ? "Clear all" : "Select all"}
              </button>
            </div>

            {vivaChapterOptions.length ? (
              <div className="viva-chapter-grid">
                {vivaChapterOptions.map((chapter, index) => {
                  const selected = vivaSelectedChapters.includes(chapter.title);
                  return (
                    <button
                      className={`viva-chapter-card${selected ? " is-selected" : ""}`}
                      type="button"
                      key={chapter.title}
                      aria-pressed={selected}
                      onClick={() => toggleVivaChapter(chapter.title)}
                    >
                      <span className="viva-chapter-check" aria-hidden="true">{selected ? "✓" : String(index + 1).padStart(2, "0")}</span>
                      <span>
                        <strong>{chapter.title}</strong>
                        <small>{chapter.count ? `${chapter.count} source questions available` : "Curriculum chapter"}</small>
                      </span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <p className="form-message">A chapter directory has not been added for this subject yet.</p>
            )}

            <label className="viva-privacy-notice">
              <input
                type="checkbox"
                checked={vivaPrivacyAccepted}
                onChange={(event) => setVivaPrivacyAccepted(event.target.checked)}
              />
              <span>
                <strong>AI privacy notice</strong>
                <small>Your selected chapters, typed responses, and any uploaded answer images will be sent to the configured AI provider. Answer images are not saved in your Viva history. With Gemini&apos;s free tier, Google may use submitted content to improve its products. Do not include names, contact details, or patient-identifiable information.</small>
              </span>
            </label>

            {vivaSessionMessage ? <p className="form-message viva-session-message" role="alert">{vivaSessionMessage}</p> : null}

            <div className="viva-setup-footer">
              <p><strong>5 questions</strong><span>Type or photograph answers · feedback after each · final score out of 10</span></p>
              <button
                className="button button-primary"
                type="button"
                disabled={!vivaSelectedChapters.length || !vivaPrivacyAccepted || vivaSessionBusy}
                onClick={handleCreateVivaSession}
                aria-busy={vivaSessionBusy}
              >
                {vivaSessionBusy ? "Preparing your viva..." : "Continue to viva"}
              </button>
            </div>
            <p className="viva-build-note">Preparing five balanced questions usually takes a few seconds.</p>
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

      if (!chapters.length) {
        return (
          <section className="app-view topic-wise-directory">
            <div className="view-header">
              <div>
                <p className="eyebrow">{currentPracticeSubject?.title ?? "Practice"} · {isUsmlePractice ? "USMLE Step 1" : "Topic Wise"}</p>
                <h2>{isUsmlePractice ? "USMLE Step-1 format questions are not ready yet" : "Topic-wise questions are not ready yet"}</h2>
                <p className="view-subtitle">
                  {isUsmlePractice
                    ? "USMLE-style questions will appear here after they are added to this subject."
                    : "Topic-wise questions will appear here after they are added to this subject."}
                </p>
              </div>
              <button className="button button-secondary" onClick={handleBackToPracticeDirectory}>Back to subjects</button>
            </div>
            <article className="card panel">
              <h3>No {directoryModeTitle.toLowerCase()} yet</h3>
              <p className="panel-copy">This category is kept separate so its questions do not mix with PYQs or other supplemental practice.</p>
            </article>
          </section>
        );
      }

      if (practiceStage === "chapters") {
        return (
          <section className="app-view topic-wise-directory">
            <div className="view-header"><div><p className="eyebrow">{currentPracticeSubject?.title} · {isUsmlePractice ? "USMLE Step 1" : "Topic Wise"}</p><h2>Choose a chapter</h2><p className="view-subtitle">{isUsmlePractice ? "Practise clinically framed, one-best-answer questions chapter by chapter." : "Build mastery chapter by chapter. Your progress is saved automatically."}</p></div><button className="button button-secondary" onClick={handleBackToPracticeDirectory}>Back to subjects</button></div>
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
          <div className="view-header"><div><p className="eyebrow">{isUsmlePractice ? "USMLE Step 1 · Chapter topics" : "Chapter topics"}</p><h2>{chapter?.title ?? "Choose a topic"}</h2><p className="view-subtitle">{isUsmlePractice ? "Each topic contains clinically framed Step 1-style questions." : "Each topic contains a focused five-question competitive exam set."}</p></div><button className="button button-secondary" onClick={() => setPracticeStage("chapters")}>Back to chapters</button></div>
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
              <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
              <h2>{isSupplementalPractice ? `${directoryModeTitle} are not ready yet` : "No questions found"}</h2>
            </div>
            <button className="button button-secondary" onClick={() => isDirectoryPractice ? setPracticeStage("topics") : handleBackToPracticeDirectory()}>
              {isDirectoryPractice ? "Back to topics" : "Back to subjects"}
            </button>
          </div>

          <article className="card panel">
            <h3>{isUsmlePractice ? "No USMLE Step-1 format questions in this subject" : selectedPracticeMode === "ai" ? "Generate a 20-question set first" : "No practice questions yet"}</h3>
            <p className="panel-copy">
              {isUsmlePractice
                ? "Choose another subject or add USMLE Step-1 format questions to this subject."
                : selectedPracticeMode === "ai"
                ? "Open the subject again and choose Topic Wise Questions."
                : "The PYQ database does not have questions for this subject yet."}
            </p>
          </article>
        </section>
      );
    }

    const totalQuestions = currentPracticeQuestions.length;
    const explanationText = formatExplanationText(
      currentPracticeQuestion?.explanation || "Answer saved in the NEET PG question bank.",
    );

    if (practiceStage === "subject") {
      return (
        <section className={`app-view practice-detail-view${isModulePractice ? " usmle-module-session practice-path-red" : isFmgePractice ? " fmge-session usmle-module-session practice-path-teal" : ""}`}>
          <div className="view-header">
            <div>
              <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
              <h2>
                {currentPracticeSubject.title}{" "}
                {isFmgePractice ? "practice" : isSupplementalPractice ? directoryModeTitle : currentPracticeQuestionSet?.title ?? "PYQ session"}
              </h2>
            </div>
            <button className="button button-secondary" onClick={() => isFmgePractice ? setPracticeStage("fmge-years") : isModulePractice ? setPracticeStage("usmle-modules") : isDirectoryPractice ? setPracticeStage("topics") : handleBackToPracticeDirectory()}>
              {isFmgePractice ? "Back to years" : isModulePractice ? "Back to modules" : isDirectoryPractice ? "Back to topics" : "Back to subjects"}
            </button>
          </div>

          <article className="card quiz-card practice-focus-card">
            <div className="practice-focus-topbar">
              <span className="practice-year-tag">
                {isFmgePractice ? currentPracticeSubject.title : isUsmlePractice
                  ? `Mixed ${totalQuestions}-question set`
                  : isDirectoryPractice
                    ? activePracticeYear?.title ?? "Practice"
                  : currentPracticeQuestionSet?.title ?? "PYQ session"}
              </span>
              <span className={`rank-pill ${isUsmlePractice ? "source-usmle" : selectedPracticeMode === "ai" ? "source-ai" : "source-official"}`}>
                {isFmgePractice ? "FMGE recall questions" : isSupplementalPractice ? directoryModeTitle : "Official PYQ"}
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
                {isUsmlePractice
                  ? "USMLE Step 1-style practice"
                  : selectedPracticeMode === "ai"
                  ? "Supplemental topic-wise practice"
                  : currentPracticeQuestion.examTitle ?? currentPracticeQuestionSet?.title ?? `${currentPracticeQuestion.year} PYQ`}
              </span>
              <span>{isModulePractice || isFmgePractice ? `${currentPracticeQuestion.part ? `Part ${currentPracticeQuestion.part} · ` : ""}Question ${practiceQuestionIndex + 1} of ${totalQuestions}` : currentPracticeQuestion.topic}</span>
            </div>
            <h3>{currentPracticeQuestion.prompt}</h3>
            {isFmgePractice && currentPracticeQuestion.sourceNote && <p className="fmge-review-note" role="note">{currentPracticeQuestion.sourceNote}</p>}

            {currentPracticeQuestion.subtopic ? <p className="panel-copy">{currentPracticeQuestion.subtopic}</p> : null}

            <QuestionLaboratoryTable findings={currentPracticeQuestion.laboratoryFindings} />

            {currentPracticeQuestion.imageUrls?.length ? (
              <div className="practice-question-images">
                {currentPracticeQuestion.imageUrls.map((imageUrl, index) => {
                  const isUsmle = isUsmleImage(imageUrl);
                  return (
                    <span
                      className={`practice-question-image-frame${isUsmle ? " practice-question-image-frame-usmle" : ""}`}
                      key={`${currentPracticeQuestion.questionNumber}-${imageUrl}`}
                    >
                      <img
                        className="practice-question-image"
                        src={getPracticeImageUrl(imageUrl)}
                        alt={`Question ${currentPracticeQuestion.questionNumber} visual ${index + 1}`}
                        loading="lazy"
                        decoding="async"
                      />
                    </span>
                  );
                })}
              </div>
            ) : null}

            {currentPracticeQuestion.leadIn ? <h3 className="practice-question-lead-in">{currentPracticeQuestion.leadIn}</h3> : null}

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
                    {isModulePractice || isFmgePractice ? `(${String.fromCharCode(65 + currentPracticeQuestion.options.indexOf(option))}) ${option}` : option}
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
              <div className="practice-question-tools">
                <button
                  className={`bookmark-button${isCurrentPracticeQuestionBookmarked ? " active" : ""}`}
                  type="button"
                  disabled={bookmarkBusyKeys.includes(getQuestionBookmarkKey({ mode: selectedPracticeMode, subjectId: currentPracticeSubject.id, questionId: currentPracticeQuestion.id }))}
                  onClick={toggleCurrentQuestionBookmark}
                  aria-pressed={isCurrentPracticeQuestionBookmarked}
                >
                  <span aria-hidden="true">{isCurrentPracticeQuestionBookmarked ? "★" : "☆"}</span>
                  {isCurrentPracticeQuestionBookmarked ? "Saved" : "Save question"}
                </button>
                <button className={`flag-button${flaggedQuestions[currentPracticeQuestion.id] ? " active" : ""}`} type="button" onClick={() => setFlaggedQuestions((current) => ({ ...current, [currentPracticeQuestion.id]: !current[currentPracticeQuestion.id] }))}>
                  {flaggedQuestions[currentPracticeQuestion.id] ? "Flagged for review" : "Flag for review"} <kbd>F</kbd>
                </button>
              </div>
            </div>

            {bookmarkMessage ? <p className="bookmark-inline-message" role="status">{bookmarkMessage}</p> : null}

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
                  {isFmgePractice && currentPracticeQuestion.reviewNote ? "Recall key: " + currentPracticeQuestion.answer + ". See the review note below." : isCorrect ? "Correct." : "Not quite. Correct answer: " + currentPracticeQuestion.answer + "."}
                </strong>
                <details open><summary>Explanation</summary><p>{explanationText}</p></details>
                {isFmgePractice && <div className="usmle-teaching-notes">
                  {currentPracticeQuestion.reviewNote && <p className="fmge-review-note"><strong>Recall review note:</strong> {currentPracticeQuestion.reviewNote}</p>}
                  {currentPracticeQuestion.educationalObjective && <p><strong>Learning objective:</strong> {currentPracticeQuestion.educationalObjective}</p>}
                  {currentPracticeQuestion.reasoningChain && <p><strong>Reasoning:</strong> {currentPracticeQuestion.reasoningChain}</p>}
                  {currentPracticeQuestion.optionExplanations?.length === 4 && <details open><summary>Option-by-option review</summary><ol type="A">{currentPracticeQuestion.optionExplanations.map((note, index) => <li key={index}><strong>{currentPracticeQuestion.options[index]}</strong><p>{note}</p></li>)}</ol></details>}
                  {currentPracticeQuestion.explanationImageUrls?.length > 0 && <div className="practice-question-images">{currentPracticeQuestion.explanationImageUrls.map((url, index) => <img key={url} className="practice-question-image" src={getPracticeImageUrl(url)} alt={`Explanation visual ${index + 1}`} loading="lazy" />)}</div>}
                </div>}
                {isModulePractice && <div className="usmle-teaching-notes">
                  <p><strong>Learning objective:</strong> {currentPracticeQuestion.educationalObjective}</p>
                  <p><strong>Reasoning:</strong> {currentPracticeQuestion.reasoningChain}</p>
                  <p><strong>Integrated disciplines:</strong> {currentPracticeQuestion.disciplines.join(" · ")}</p>
                  <details open><summary>Option-by-option review</summary>
                    <ol type="A">{currentPracticeQuestion.optionExplanations.map((explanation, index) => <li key={index}><strong>{currentPracticeQuestion.options[index]}</strong><p>{explanation}</p></li>)}</ol>
                  </details>
                  {currentPracticeQuestion.references.length > 0 && <details><summary>Textbook references</summary>
                    <ul>{currentPracticeQuestion.references.map((reference, index) => <li key={index}>
                      {reference.book}, {reference.edition}. {reference.chapter}{reference.pages ? `, pp. ${reference.pages}` : ""}{reference.pdfPages ? ` (PDF pages ${reference.pdfPages})` : ""}.
                      {reference.url && <> <a href={reference.url} target="_blank" rel="noreferrer">Read chapter</a></>}
                    </li>)}</ul>
                  </details>}
                </div>}
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
            <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
            <h2>{catalogTitle}</h2>
          </div>
          <button className="button button-secondary" onClick={() => setActiveView("Practice")}>
            Back
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
                <div className="icon-badge green">{isTheory ? "TH" : practiceChoicePanel === "pyq" ? "PYQ" : "MCQ"}</div>
                <div>
                  <h3 id="practice-choice-title">
                    {isTheory ? `${practiceChoiceSubject.title} Theory` : practiceChoicePanel === "pyq" ? `${practiceChoiceSubject.title} PYQs` : `Practice ${practiceChoiceSubject.title}`}
                  </h3>
                  <p>
                    {isTheory ? "Choose cases or short notes to study this subject." : practiceChoicePanel === "pyq"
                      ? "Choose a year to start solving official previous year questions."
                      : "Choose PYQs, topic-wise practice, USMLE Step-1 questions, Mind Maps, an AI viva, or Clinical Cases."}
                  </p>
                </div>
              </div>
              {isTheory ? (
                <div className="practice-choice-grid">
                  <button className="practice-choice-card practice-choice-card-clinical" type="button" onClick={() => handleStartClinicalCasesSetup(practiceChoiceSubject.id)}>
                    <span className="practice-choice-icon">CASE</span><strong>Cases</strong>
                    <p>Apply your knowledge with clinical cases and structured theory answers.</p>
                  </button>
                  <button className="practice-choice-card practice-choice-card-mind-maps" type="button" onClick={() => {
                    setSelectedPracticeSubjectId(practiceChoiceSubject.id);
                    setSelectedPracticeMode("pyq");
                    closePracticeChoice();
                    setPracticeStage("short-notes");
                    scrollPracticeViewToTop();
                  }}>
                    <span className="practice-choice-icon">NOTE</span><strong>Short Notes</strong>
                    <p>Choose a topic, write a theory answer, and get AI feedback.</p>
                  </button>
                </div>
              ) : practiceChoicePanel === "pyq" ? (
                <div className="practice-year-picker">
                  <div className="practice-choice-section-heading">
                    <button className="practice-choice-back-link" type="button" onClick={() => setPracticeChoicePanel("formats")}>
                      ← All practice modes
                    </button>
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
              ) : (
                <div className="practice-choice-grid practice-choice-grid-formats">
                  <button
                    className="practice-choice-card practice-choice-card-pyq"
                    type="button"
                    onClick={() => setPracticeChoicePanel("pyq")}
                  >
                    <span className="practice-choice-icon">PYQ</span>
                    <strong>Previous Year Questions</strong>
                    <p>Official INI-CET and NEET PG questions grouped by year</p>
                    <small>{practiceChoiceSubject.questions.length} questions</small>
                  </button>
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
                  <button
                    className="practice-choice-card practice-choice-card-usmle"
                    type="button"
                    onClick={() => handleStartUsmlePractice(practiceChoiceSubject.id)}
                  >
                    <span className="practice-choice-icon">S1</span>
                    <strong>USMLE Step-1 Format Questions</strong>
                    <p>Mixed, clinically framed one-best-answer questions</p>
                    <small>{practiceChoiceUsmleQuestionCount} questions · shuffled each session</small>
                  </button>
                  <button
                    className="practice-choice-card practice-choice-card-mind-maps"
                    type="button"
                    onClick={() => handleOpenMindMaps(practiceChoiceSubject.id)}
                  >
                    <span className="practice-choice-icon">MAP</span>
                    <strong>Mind Maps</strong>
                    <p>Visual, high-yield connections for rapid revision</p>
                    <small>Chapter-wise visual summaries</small>
                  </button>
                  <button
                    className="practice-choice-card practice-choice-card-viva"
                    type="button"
                    onClick={() => handleStartVivaSetup(practiceChoiceSubject.id)}
                  >
                    <span className="practice-choice-icon">VIVA</span>
                    <strong>AI Viva</strong>
                    <p>Choose chapters and answer five explanatory questions</p>
                    <small>Feedback after every answer · score out of 10</small>
                  </button>
                  <button
                    className="practice-choice-card practice-choice-card-clinical"
                    type="button"
                    onClick={() => handleStartClinicalCasesSetup(practiceChoiceSubject.id)}
                  >
                    <span className="practice-choice-icon">CASE</span>
                    <strong>Clinical Cases</strong>
                    <p>Applied theory cases with diagnosis and structured follow-up questions</p>
                    <small>Type or photograph answers · Gemini theory review</small>
                  </button>
                </div>
              )}
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
                      <p className="practice-subject-copy">{isTheory ? "Study this subject through cases and short notes." : "Choose PYQs, topic-wise questions, USMLE practice, Mind Maps, an AI viva, or Clinical Cases."}</p>
                      <span className="practice-subject-counts">
                        {isTheory ? <><strong>Cases</strong><strong>Short Notes</strong></> : <><strong>{subject.questions.length} PYQs</strong><strong>{aiQuestionCount} Topic Wise</strong></>}
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ))}
          {!isTheory && supplementalAiPracticeSubjects.length ? (
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

  function renderBookmarks() {
    if (!user?.hasPracticeAccess) return renderPracticeLock();
    const modeLabels = {
      pyq: "Previous Year Question",
      ai: "Topic-wise Question",
      usmle: "USMLE Step-1 Question",
      fmge: "FMGE Question",
    };
    const availableCount = bookmarkedQuestionEntries.filter((entry) => entry.resolved).length;

    return (
      <section className="app-view bookmarks-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Saved for revision</p>
            <h2>Bookmarked questions</h2>
            <p className="view-subtitle">Keep valuable questions close and reopen them whenever you want to revise.</p>
          </div>
          <button className="button button-primary" type="button" onClick={() => setActiveView("Practice")}>Browse questions</button>
        </div>

        {bookmarkMessage ? <p className="form-message bookmark-page-message" role="status">{bookmarkMessage}</p> : null}

        {questionBookmarks.length ? (
          <>
            {practiceLibraryStatus === "loading" || practiceLibraryStatus === "idle" ? (
              <p className="form-message bookmark-page-message" role="status">Saved bookmarks are ready. Loading full question details in the background…</p>
            ) : practiceLibraryStatus === "error" ? (
              <div className="form-message bookmark-page-message" role="alert">
                <span>{practiceLibraryMessage || "Question details could not be loaded."}</span>{" "}
                <button className="text-button" type="button" onClick={fetchPracticeLibrary}>Retry</button>
              </div>
            ) : null}
            <div className="bookmark-summary-row" aria-label="Bookmark summary">
              <article className="card"><span>Saved questions</span><strong>{questionBookmarks.length}</strong></article>
              <article className="card"><span>Ready to review</span><strong>{availableCount}</strong></article>
              <article className="card"><span>Answered before</span><strong>{questionBookmarks.filter((bookmark) => practiceProgress[bookmark.questionId]).length}</strong></article>
            </div>
            <div className="bookmark-question-list">
              {bookmarkedQuestionEntries.map((entry) => {
                const { bookmark, resolved } = entry;
                const question = resolved?.question;
                const subjectTitle = resolved?.subject?.title ?? bookmark.subjectTitle ?? "Practice";
                const topic = question?.chapterTitle || question?.topic || bookmark.topic || "General review";
                const preview = question?.leadIn || question?.prompt || bookmark.preview || "Saved practice question";
                const progress = practiceProgress[bookmark.questionId];
                return (
                  <article className={`card panel bookmark-question-card${resolved ? "" : " bookmark-question-unavailable"}`} key={getQuestionBookmarkKey(bookmark)}>
                    <div className="bookmark-question-meta">
                      <span>{modeLabels[bookmark.mode] ?? "Practice Question"}</span>
                      {bookmark.year ? <span>{bookmark.year}</span> : null}
                      <span>{progress ? (progress.correct ? "Previously correct" : "Needs another look") : "Not answered yet"}</span>
                    </div>
                    <h3>{preview}</h3>
                    <p>{subjectTitle} · {topic}</p>
                    <div className="bookmark-question-actions">
                      <button className="button button-primary" type="button" disabled={!resolved} onClick={() => openBookmarkedQuestion(entry)}>
                        {resolved
                          ? "Review question"
                          : practiceLibraryStatus === "loading" || practiceLibraryStatus === "idle"
                            ? "Loading question…"
                            : "Question unavailable"}
                      </button>
                      <button
                        className="button button-secondary bookmark-remove-button"
                        type="button"
                        disabled={bookmarkBusyKeys.includes(getQuestionBookmarkKey(bookmark))}
                        onClick={() => void updateQuestionBookmark(bookmark, false)}
                      >
                        Remove bookmark
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          </>
        ) : (
          <article className="card panel bookmarks-empty-state">
            <span className="bookmarks-empty-icon" aria-hidden="true">☆</span>
            <h3>No bookmarked questions yet</h3>
            <p>Use “Save question” while practising PYQs, topic-wise questions, or USMLE questions. They will appear here for revision.</p>
            <button className="button button-primary" type="button" onClick={() => setActiveView("Practice")}>Find questions to save</button>
          </article>
        )}
      </section>
    );
  }

  function renderLeaderboard() {
    return <Leaderboard players={liveLeaderboard} statePlayers={selectedStatePlayers}
      state={selectedStateEntry} states={leaderboardStateOptions}
      college={selectedLeaderboardCollege} colleges={selectedLeaderboardCollegeOptions}
      onState={(value) => { setSelectedLeaderboardState(value); setSelectedLeaderboardCollege(""); }}
      onCollege={setSelectedLeaderboardCollege} onCompete={() => setActiveView("Compete")}
      onProfile={(id) => openPublicProfile(id, "Leaderboard")} />;
  }

  function renderCommunities() {
    if (communityStage === "direct" && selectedDirectConversation) {
      return (
        <section className={socialPage}>
          <div className="flex flex-wrap items-center justify-between gap-4 [&_h2]:text-3xl [&_h2]:font-bold [&_h2]:tracking-tight">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:text-cyan-300">Messages</p>
              <h2>{selectedDirectConversation.otherParticipant?.name ?? "Direct chat"}</h2>
              <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">Personal study chats, quick check-ins, and direct 1v1 challenges.</p>
            </div>
            <button className={socialSecondary} onClick={handleBackToCommunityHub}>
              Back to community hub
            </button>
          </div>

          {directMessagesMessage ? <p className="rounded-xl border border-cyan-200 bg-cyan-50 p-4 text-sm text-cyan-900 dark:border-cyan-900 dark:bg-cyan-950 dark:text-cyan-100">{directMessagesMessage}</p> : null}

          <article className={`${socialSurface} overflow-hidden`}>
            <div className="flex flex-wrap items-center justify-between gap-5 p-5 sm:p-6 [&_h3]:text-xl [&_h3]:font-semibold">
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:text-cyan-300">Message</p>
                <h3>{selectedDirectConversation.otherParticipant?.name ?? "Conversation"}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">{selectedDirectConversation.otherParticipant?.medicalCollege}</p>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">{selectedDirectConversation.otherParticipant?.rating ?? userRating} rating</span>
                <button className={socialPrimary} onClick={handleDirectChallenge}>
                  Challenge to 1v1
                </button>
              </div>
            </div>

            <div className="flex flex-wrap gap-x-6 gap-y-2 border-y border-slate-100 bg-slate-50 px-5 py-3 text-xs text-slate-500 dark:border-slate-800 dark:bg-slate-950/50 dark:text-slate-400">
              <span>State: {selectedDirectConversation.otherParticipant?.state ?? "Registered users"}</span>
              <span>Streak: {selectedDirectConversation.otherParticipant?.streak ?? 1} days</span>
            </div>

            <div className="grid items-start lg:grid-cols-[minmax(0,1fr)_280px]">
              <div className="min-w-0 p-5">
                <div className="flex max-h-[60vh] min-h-64 flex-col gap-4 overflow-y-auto pb-5">
                  {selectedDirectConversation.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.isOwnMessage ? "justify-end" : "justify-start"}`}
                    >
                      <div className={`max-w-[90%] space-y-2 rounded-2xl p-4 text-sm [&_p]:whitespace-pre-wrap [&_p]:break-words [&>span]:block [&>span]:text-[10px] [&>span]:text-slate-500 dark:[&>span]:text-slate-400 ${message.isOwnMessage ? "bg-cyan-50 dark:bg-cyan-950" : "bg-slate-100 dark:bg-slate-800"} ${message.type === "challenge" ? "border border-cyan-300 dark:border-cyan-800" : ""}`}>
                        {message.userId ? (
                          <button
                            type="button"
                            className="text-xs font-semibold text-cyan-700 hover:underline dark:text-cyan-300"
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

                <form className="flex items-center gap-3 border-t border-slate-100 pt-4 dark:border-slate-800" onSubmit={handleSendDirectMessage}>
                  <input
                    type="text" className={socialField} aria-label="Message"
                    value={directMessageDraft}
                    onChange={(event) => setDirectMessageDraft(event.target.value)}
                    placeholder="Write a message..."
                  />
                  <button className={socialPrimary} type="submit" disabled={!directMessageDraft.trim()}>
                    Send
                  </button>
                </form>
              </div>

              <aside className="min-w-0 border-t border-slate-100 bg-slate-50/60 p-5 lg:border-l lg:border-t-0 dark:border-slate-800 dark:bg-slate-950/30">
                <div className="flex items-center justify-between gap-3 [&_h4]:font-semibold">
                  <div>
                    <h4>Profile snapshot</h4>
                    <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">Jump to profile details or launch a duel directly from here.</p>
                  </div>
                </div>
                <div className="mt-5 max-h-[600px] space-y-4 overflow-y-auto">
                  <div className="space-y-2">
                    <button
                      type="button"
                      className="w-full rounded-xl p-1 text-left transition hover:bg-slate-100 dark:hover:bg-slate-800 motion-reduce:transition-none"
                      onClick={() => openPublicProfile(selectedDirectConversation.otherParticipant?.id, "Communities")}
                    >
                      <div className="flex min-w-0 items-center gap-3 [&>div:last-child]:min-w-0 [&_strong]:block [&_strong]:text-sm [&_p]:mt-1 [&_p]:truncate [&_p]:text-xs [&_p]:text-slate-500 dark:[&_p]:text-slate-400">
                        <div className={socialAvatar}>
                          {selectedDirectConversation.otherParticipant?.profileImageUrl ? (
                            <img
                              className="h-full w-full object-cover"
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
        <section className={socialPage}>
          <div className="flex flex-wrap items-center justify-between gap-4 [&_h2]:text-3xl [&_h2]:font-bold [&_h2]:tracking-tight">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:text-cyan-300">Communities</p>
              <h2>{selectedCommunity.name}</h2>
              <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">A focused feed of questions, clinical takes, and threaded replies.</p>
            </div>
            <button className={socialSecondary} onClick={handleBackToCommunityHub}>
              Back to community hub
            </button>
          </div>

          {communitiesMessage ? <p className="rounded-xl border border-cyan-200 bg-cyan-50 p-4 text-sm text-cyan-900 dark:border-cyan-900 dark:bg-cyan-950 dark:text-cyan-100">{communitiesMessage}</p> : null}

          <article className={`${socialSurface} overflow-hidden`}>
            <div className="flex flex-wrap items-center justify-between gap-5 p-5 sm:p-6 [&_h3]:text-xl [&_h3]:font-semibold">
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:text-cyan-300">Community threads</p>
                <h3>{selectedCommunity.name}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">{selectedCommunity.description}</p>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">{selectedCommunity.memberCount} members</span>
                {selectedCommunity.isAdmin ? (
                  <button
                    className={socialSecondary}
                    type="button"
                    onClick={() => handleCopyCommunityInvite(selectedCommunity.id)}
                  >
                    Copy invite link
                  </button>
                ) : null}
                {!selectedCommunity.isMember ? (
                  <button className={socialPrimary} onClick={() => handleJoinCommunity(selectedCommunity.id)}>
                    Join community
                  </button>
                ) : null}
              </div>
            </div>

            <div className="flex flex-wrap gap-x-6 gap-y-2 border-y border-slate-100 bg-slate-50 px-5 py-3 text-xs text-slate-500 dark:border-slate-800 dark:bg-slate-950/50 dark:text-slate-400">
              <span>Topic: {selectedCommunity.topic}</span>
              <span>Admin: {selectedCommunity.adminName}</span>
              <span>{communityThreadPosts.length} threads</span>
            </div>

            <div className="grid items-start lg:grid-cols-[minmax(0,1fr)_280px]">
              <div className="min-w-0 p-4 sm:p-6">
                {selectedCommunity.isMember ? (
                  <form className="flex items-start gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3 sm:p-4 dark:border-slate-700 dark:bg-slate-950/50" onSubmit={(event) => handleSendCommunityMessage(event)}>
                    <div className={`${socialAvatar} hidden sm:flex`}>
                      {user?.profileImageUrl ? <img className="h-full w-full object-cover" src={user.profileImageUrl} alt="" /> : <span>{getInitials(user?.name)}</span>}
                    </div>
                    <div className="min-w-0 flex-1 space-y-3 [&>div:last-child]:flex [&>div:last-child]:flex-wrap [&>div:last-child]:items-center [&>div:last-child]:justify-between [&>div:last-child]:gap-3">
                      <textarea className={socialField} aria-label="New discussion thread"
                        rows="3"
                        value={communityMessageDraft}
                        onChange={(event) => setCommunityMessageDraft(event.target.value)}
                        placeholder="Share a question, clinical pearl, or study update..."
                      />
                      {communityThreadImage ? (
                        <div className="relative space-y-2 [&_img]:max-h-56 [&_img]:rounded-xl [&_button]:absolute [&_button]:right-2 [&_button]:top-2 [&_button]:rounded-lg [&_button]:bg-slate-900 [&_button]:px-3 [&_button]:py-1 [&_button]:text-white [&_span]:block [&_span]:truncate [&_span]:text-xs">
                          <img src={communityThreadImage.dataUrl} alt="Thread attachment preview" />
                          <button type="button" onClick={() => setCommunityThreadImage(null)} aria-label="Remove attached image">×</button>
                          <span>{communityThreadImage.name}</span>
                        </div>
                      ) : null}
                      <div>
                        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
                          <label className="relative inline-flex min-h-10 cursor-pointer items-center gap-2 rounded-lg border border-slate-200 px-3 text-xs font-semibold hover:bg-white focus-within:ring-2 focus-within:ring-cyan-500 dark:border-slate-700 dark:hover:bg-slate-800 [&_input]:absolute [&_input]:inset-0 [&_input]:w-full [&_input]:cursor-pointer [&_input]:opacity-0">
                            <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={handleCommunityThreadImageChange} />
                            <span aria-hidden="true">▧</span> Add image
                          </label>
                          <span className={communityThreadWordCount > COMMUNITY_THREAD_WORD_LIMIT ? "font-semibold text-red-600 dark:text-red-400" : ""}>
                            {communityThreadWordCount}/{COMMUNITY_THREAD_WORD_LIMIT} words
                          </span>
                        </div>
                        <button
                          className={socialPrimary}
                          type="submit"
                          disabled={(!communityMessageDraft.trim() && !communityThreadImage) || communityThreadWordCount > COMMUNITY_THREAD_WORD_LIMIT}
                        >
                          Post thread
                        </button>
                      </div>
                    </div>
                  </form>
                ) : (
                  <div className="rounded-xl border border-cyan-200 bg-cyan-50 p-4 text-sm text-cyan-900 dark:border-cyan-800 dark:bg-cyan-950 dark:text-cyan-100 [&_p]:mt-2">
                    <strong>Join this group to publish and reply.</strong>
                    <p>You can still preview its threads, members, and discussion style before joining.</p>
                  </div>
                )}

                <div className="mb-2 mt-7 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 [&_h4]:mb-1 [&_h4]:text-base [&_h4]:font-semibold [&_h4]:text-slate-900 dark:[&_h4]:text-slate-100">
                  <div><h4>Latest threads</h4><span>Newest conversations first</span></div>
                  <span>{communityThreadPosts.length}</span>
                </div>

                <div className="divide-y divide-slate-100 dark:divide-slate-800">
                  {[...communityThreadPosts].reverse().map((message) => {
                    const replies = repliesByParent[message.id] ?? [];
                    const isExpanded = Boolean(expandedCommunityThreads[message.id]);
                    return (
                      <article className="flex gap-3 py-6" key={message.id}>
                        <div className={`${socialAvatar} hidden sm:flex`}><span>{getInitials(message.userName)}</span></div>
                        <div className="min-w-0 flex-1 [&>p]:mt-3 [&>p]:whitespace-pre-wrap [&>p]:break-words [&>p]:text-sm [&>p]:leading-7">
                          <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs [&_button]:font-semibold [&_button]:hover:text-cyan-600 [&_strong]:font-semibold [&_span]:text-cyan-600 [&_time]:text-slate-400">
                            {message.userId ? (
                              <button type="button" onClick={() => openPublicProfile(message.userId, "Communities")}>{message.userName}</button>
                            ) : <strong>{message.userName}</strong>}
                            {message.isOwnMessage ? <span>You</span> : null}
                            <time>{formatCommunityTimestamp(message.createdAt)}</time>
                          </div>
                          {message.text ? <p>{message.text}</p> : null}
                          {message.imageUrl ? (
                            <a className="mt-4 block [&_img]:max-h-96 [&_img]:rounded-xl [&_img]:object-contain" href={message.imageUrl} target="_blank" rel="noreferrer">
                              <img src={message.imageUrl} alt={"Attached to " + message.userName + "'s thread"} />
                            </a>
                          ) : null}
                          <div className="mt-4 flex gap-3 [&_button]:min-h-10 [&_button]:rounded-lg [&_button]:px-3 [&_button]:text-xs [&_button]:font-semibold [&_button]:text-cyan-700 [&_button]:hover:bg-cyan-50 dark:[&_button]:text-cyan-300 dark:[&_button]:hover:bg-cyan-950">
                            <button
                              type="button"
                              aria-expanded={isExpanded}
                              onClick={() => toggleCommunityThread(message.id, true)}
                              disabled={!selectedCommunity.isMember}
                              title={selectedCommunity.isMember ? "Reply to this thread" : "Join the community to reply"}
                            >
                              <span aria-hidden="true">↩</span> Reply
                            </button>
                            <button type="button" aria-expanded={isExpanded} onClick={() => toggleCommunityThread(message.id)} disabled={!replies.length}>
                              <span aria-hidden="true">◯</span> {replies.length} {replies.length === 1 ? "reply" : "replies"}
                            </button>
                          </div>

                          {isExpanded ? (
                            <div className="mt-3 space-y-4 border-l-2 border-cyan-100 pl-3 motion-safe:animate-in motion-safe:fade-in motion-safe:slide-in-from-top-1 motion-safe:duration-200 dark:border-cyan-900 sm:pl-4">
                              {replies.map((reply) => (
                                <div className="flex gap-3 [&>div:last-child]:min-w-0 [&_p]:mt-2 [&_p]:whitespace-pre-wrap [&_p]:break-words [&_p]:text-sm [&_p]:leading-relaxed" key={reply.id}>
                                  <div className={`${socialAvatar} hidden sm:flex`}><span>{getInitials(reply.userName)}</span></div>
                                  <div>
                                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs [&_button]:font-semibold [&_button]:hover:text-cyan-600 [&_strong]:font-semibold [&_span]:text-cyan-600 [&_time]:text-slate-400">
                                      {reply.userId ? <button type="button" onClick={() => openPublicProfile(reply.userId, "Communities")}>{reply.userName}</button> : <strong>{reply.userName}</strong>}
                                      {reply.isOwnMessage ? <span>You</span> : null}
                                      <time>{formatCommunityTimestamp(reply.createdAt)}</time>
                                    </div>
                                    <p>{reply.text}</p>
                                  </div>
                                </div>
                              ))}
                              {selectedCommunity.isMember ? (
                                <form className="flex flex-wrap items-center gap-2 pt-2 [&_input]:min-w-0 [&_input]:flex-1" onSubmit={(event) => handleSendCommunityMessage(event, message.id)}>
                                  <div className={`${socialAvatar} hidden sm:flex`}><span>{getInitials(user?.name)}</span></div>
                                  <input
                                    type="text" className={socialField} aria-label="Message"
                                    value={communityReplyDrafts[message.id] ?? ""}
                                    onChange={(event) => setCommunityReplyDrafts((current) => ({ ...current, [message.id]: event.target.value }))}
                                    placeholder={`Reply to ${message.userName}...`}
                                  />
                                  <button className={socialPrimary} type="submit" disabled={!(communityReplyDrafts[message.id] ?? "").trim()}>Reply</button>
                                </form>
                              ) : null}
                            </div>
                          ) : null}
                        </div>
                      </article>
                    );
                  })}
                  {!communityThreadPosts.length ? (
                    <div className="py-12 text-center [&_h3]:font-semibold">
                      <h3>No threads yet</h3>
                      <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">Start the first conversation in this room.</p>
                    </div>
                  ) : null}
                </div>
              </div>

              <aside className="min-w-0 border-t border-slate-100 bg-slate-50/60 p-5 lg:border-l lg:border-t-0 dark:border-slate-800 dark:bg-slate-950/30">
                <div className="flex items-center justify-between gap-3 [&_h4]:font-semibold">
                  <div>
                    <h4>Members</h4>
                    <p className="mt-2 text-sm leading-relaxed text-slate-500 dark:text-slate-400">Get to know the learners in this room.</p>
                  </div>
                  <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">{selectedCommunity.memberCount}</span>
                </div>
                <div className="mt-5 max-h-[600px] space-y-4 overflow-y-auto">
                  {selectedCommunity.members.map((member) => (
                    <div className="space-y-2" key={member.id}>
                      <button
                        type="button"
                        className="w-full rounded-xl p-1 text-left transition hover:bg-slate-100 dark:hover:bg-slate-800 motion-reduce:transition-none"
                        onClick={() => openPublicProfile(member.id, "Communities")}
                      >
                        <div className="flex min-w-0 items-center gap-3 [&>div:last-child]:min-w-0 [&_strong]:block [&_strong]:text-sm [&_p]:mt-1 [&_p]:truncate [&_p]:text-xs [&_p]:text-slate-500 dark:[&_p]:text-slate-400">
                          <div className={socialAvatar}>
                            {member.profileImageUrl ? (
                              <img className="h-full w-full object-cover" src={member.profileImageUrl} alt={`${member.name} profile`} />
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
                        <div className="flex flex-wrap gap-2">
                          <button
                            className={`${socialSecondary} !min-h-9 !px-3 !py-1.5 !text-xs`}
                            onClick={() => handleOpenDirectChat(member.id)}
                          >
                            Message
                          </button>
                          <button
                            className={`${socialSecondary} !min-h-9 !px-3 !py-1.5 !text-xs`}
                            onClick={() => handleRemoveCommunityMember(selectedCommunity.id, member.id)}
                          >
                            Remove
                          </button>
                        </div>
                      ) : member.id !== user?.id ? (
                        <button className={`${socialSecondary} !min-h-9 !px-3 !py-1.5 !text-xs`} onClick={() => handleOpenDirectChat(member.id)}>
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

    return <CommunityHub communities={communities} busy={communitiesBusy}
      message={communitiesMessage} directMessage={directMessagesMessage}
      onRefresh={fetchCommunities} onOpen={openCommunityChat} onInvite={handleCopyCommunityInvite}
      conversations={directConversations} directBusy={directMessagesBusy}
      search={directSearchTerm} onSearch={setDirectSearchTerm} searchBusy={directSearchBusy}
      results={directSearchResults} onDirect={handleOpenDirectChat} onConversation={openDirectConversation}
      timestamp={formatCommunityTimestamp} form={createCommunityForm}
      onField={updateCreateCommunityField} onCreate={handleCreateCommunity} />;
  }

  function renderCompete() {
    return <CompeteArena
      status={duelStatus} name={user?.name ?? "Challenger"} rating={userRating}
      learners={platformSummary.users} attempts={platformSummary.attemptedQuestions}
      questions={duelQuestions} minutes={DUEL_DURATION_SECONDS / 60}
      queue={duelQueueInfo} message={duelMessage} mode={duelMode}
      index={duelIndex} timeLeft={duelTimeLeft} answered={userDuelAnswered}
      opponent={duelOpponent} opponentAnswered={duelOpponentProgress.answered}
      selection={currentDuelSelection} locked={currentDuelSubmitted}
      submitted={duelSubmitted} answerBusy={duelAnswerBusy}
      result={duelResult} showReview={showDuelReview}
      onStart={() => startDuel()} onBot={startBotDuel} onLeave={leaveDuelQueue}
      onPractice={() => setActiveView("Practice")}
      onLeaderboard={() => setActiveView("Leaderboard")}
      onLock={submitDuelAnswer} onNext={nextDuelQuestion} onForfeit={forfeitDuel}
      onAgain={() => resetDuel()} onToggleReview={() => setShowDuelReview(value => !value)}
      onSelect={option => {
        if (currentDuelSubmitted || duelAnswerBusy) return;
        setDuelSelections(current => ({ ...current, [duelIndex]: option }));
      }}
      renderDetails={question => <>
        <QuestionLaboratoryTable findings={question.laboratoryFindings} compact />
        {getQuestionImageUrls(question).length > 0 && <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {getQuestionImageUrls(question).map((imageUrl, index) => <span key={imageUrl} className="relative flex min-w-0 items-center justify-center overflow-hidden rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-700">
            <img className="max-h-80 max-w-full object-contain" src={getPracticeImageUrl(imageUrl)} alt={`Question visual ${index + 1}`} />
          </span>)}
        </div>}
      </>}
    />;
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
        <ProfileOverview user={user} overview={accountOverview} guest={authStatus === "guest"}
          previewImage={previewImage} photoBusy={profileBusy || profilePhotoPreparing} pendingPhoto={Boolean(profileState.profileImageDataUrl)}
          onPhoto={handleProfilePhotoChange} onSavePhoto={() => handleProfileSave(null, true)}
          onCancelPhoto={() => { updateProfileField("profileImageDataUrl", ""); setProfileMessage(""); }}
          onLogout={handleLogout} message={profileMessage} />
        <div className="content-grid profile-layout">
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
      { name: "Lite", price: "₹499", cadence: "/ year", copy: "Perfect for students who want daily practice without spending much.", features: ["5 Battle Points every day", "Performance Analytics", "Daily Practice Access", "Community Access", "Perfect for casual learners"], action: "Get Lite" },
      { name: "Ultra", price: "₹999", cadence: "/ year", copy: "For MBBS students preparing consistently throughout the year.", features: ["Unlimited Battle Points", "Create Communities", "Custom Battles", "Detailed Analytics", "Explanation Access", "Unlock Any 3 Subjects"], action: "Choose Ultra", featured: true },
      { name: "Premium", price: "₹1499", cadence: "/ year", copy: "Built for serious NEET PG aspirants.", features: ["All Subjects Unlocked", "Custom Modules", "Custom Practice", "NEET PG Exam Mode", "Clinical Cases", "Everything in Ultra"], action: "Go Premium" },
    ];
    const assurances = [
      ["◇", "Secure & Trusted", "Your data is safe with us."],
      ["↻", "Cancel Anytime", "No questions asked."],
      ["☏", "24/7 Support", "We're here to help."],
      ["✪", "Loved by Medicos", "Join thousands of students."],
    ];
    return (
      <section className="app-view pricing-page">
        <div className="pricing-hero"><p className="eyebrow">Simple, affordable pricing</p><h2>Master Medicine,<br/>One Question at a Time<span>.</span></h2><p>Practice consistently, compete with friends, analyze your weaknesses, and prepare confidently for university exams and NEET PG.</p><div className="billing-toggle"><span>Annual plans · one-time payment</span></div></div>
        <div className="pricing-grid">{plans.map((plan) => <article className={`pricing-card${plan.featured ? " pricing-card-featured" : ""}`} key={plan.name}>{plan.featured ? <span className="popular-pill">★ Most popular</span> : null}<h3>{plan.name}</h3><p>{plan.copy}</p><div className="plan-price"><strong>{plan.price}</strong><span>{plan.cadence}</span></div><button className={`button ${plan.featured ? "button-primary" : "button-secondary"}`} onClick={() => { setPaymentPlanId(plan.name.toLowerCase()); document.getElementById("payment-gateway")?.scrollIntoView({ behavior: "smooth" }); }}>{plan.action}</button><ul>{plan.features.map((feature) => <li key={feature}><span>✓</span>{feature}</li>)}</ul></article>)}</div>
        <div className="pricing-assurance-strip">{assurances.map(([icon, title, copy]) => <div key={title}><span>{icon}</span><strong>{title}</strong><small>{copy}</small></div>)}</div>
        <article className="card panel payment-gateway-section" id="payment-gateway">
          <div className="payment-copy"><p className="eyebrow">Razorpay Checkout</p><h3>Complete your payment securely</h3><p className="panel-copy">Choose a plan above, then pay using Razorpay. Your payment is confirmed by our server and saved to your account.</p><div className="payment-provider-row"><span>UPI</span><span>Cards</span><span>Net banking</span><span>Wallets</span></div></div>
          <RazorpayCheckout key={user?.id || "guest"} plan={PAYMENT_PLANS.find(plan => plan.id === paymentPlanId)} user={user} guest={authStatus !== "authenticated"} onVerified={payment => { if (payment.hasPracticeAccess) { setUser(current => current?.id === user?.id ? { ...current, hasPracticeAccess: true } : current); setPracticeLibraryStatus("idle"); } }} />
        </article>
        <div className="pricing-faq"><h3>Common questions</h3><details><summary>Can I keep using Medulla for free?</summary><p>Yes. Core daily practice and community features remain available on the free plan.</p></details><details><summary>Will my progress carry over when I upgrade?</summary><p>Yes. Plans change access, never your saved learning history.</p></details><details><summary>How will payments be secured?</summary><p>Razorpay collects payment details securely. Medulla stores the order and verified payment status.</p></details></div>
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
      case "Reviews":
        return <div className="app-view"><WebsiteReviews canReview={authStatus === "authenticated"} onSignIn={handleLogout} /></div>;
      case "Practice":
        return <>
          {!["selection", "usmle-modules", "fmge-years"].includes(practiceStage) && <div className="practice-path-breadcrumb">
            <button type="button" className="text-button" onClick={() => setActiveView("Practice")}>← All practice options</button>
            {practicePathTitle && <span>{practicePathTitle} practice</span>}
          </div>}
          {renderPractice()}
        </>;
      case "Bookmarks":
        return renderBookmarks();
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
          <p className="panel-copy">Checking the local Medulla database and restoring your account.</p>
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
