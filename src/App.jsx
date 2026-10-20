import EmailVerification from "./components/EmailVerification";
import { useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { AppShell } from "./components/AppShellV2";
import WebsiteReviews from "./components/WebsiteReviews";
import CompeteArena from "./components/CompeteArena";
import Leaderboard from "./components/Leaderboard";
import CommunityHub from "./components/CommunityHub";
import CommunityThreads from "./components/CommunityThreads";
import HomeBattleSection from "./components/HomeBattleSection";
import { socialPage, surface as socialSurface, primary as socialPrimary, secondary as socialSecondary, field as socialField, avatar as socialAvatar } from "./components/SocialUI";
import PracticeSelection from "./components/PracticeSelection";
import FeatureAccessDialog from "./components/FeatureAccessDialog";
import { LockKeyhole } from "lucide-react";
import { canAccessFeature, practiceFeature, filterLibraryByPlan } from "./data/planAccess";
import TestSections from "./components/TestSections";
import PracticeSubjectDirectory from "./components/PracticeSubjectDirectory";
import CustomModules from "./components/CustomModules";
import UsmleModules from "./components/UsmleModules";
import FmgeYears from "./components/FmgeYears";
import ShortNotes from "./components/ShortNotes";
import AnswerNotepad from "./components/AnswerNotepad";
import TextbookSources from "./components/TextbookSources";
import { DashboardSummary, ProfileOverview } from "./components/AccountOverview";
import DashboardActivity from "./components/DashboardActivity";
import RazorpayCheckout from "./components/RazorpayCheckout";
import { PAYMENT_PLANS } from "./data/paymentPlans";
import { filterPracticeLibraryForUi } from "./lib/practiceImageVisibility";
import { getDuelImageUrls } from "./lib/duelImages";
import { useAccountOverview, usePracticeRecorder } from "./lib/useAccountOverview";
import { BrandMark } from "./components/BrandMark";
import { ABROAD_STATE, medicalCollegesByState, signupStateOptions } from "./data/medicalColleges";
import CountrySelect from "./components/CountrySelect";
import { VIVA_CHAPTER_FALLBACKS } from "./data/vivaChapters";
import { apiRequest } from "./lib/api";
import { SESSION_TOKEN_KEY, THEME_STORAGE_KEY } from "./lib/clientStorage";

const PRACTICE_LIBRARY_URL = "/api/practice";
const PRACTICE_LIBRARY_CACHE_KEY = "medicomm-practice-library-cache-v20261016-surgery-img1-b5";
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

const GENERAL_SURGERY_CHAPTER_ORDER = new Map([
  "BASIC PRINCIPLES OF SURGERY",
  "GENERAL SURGERY",
  "GASTROINTESTINAL SURGERY",
  "UROLOGY",
  "SPECIALITIES",
].map((title, index) => [title, index + 1]));

const OBGYN_CHAPTER_ORDER = new Map([
  "BASIC SCIENCES, ANATOMY, EMBRYOLOGY & DIAGNOSTICS",
  "REPRODUCTIVE ENDOCRINOLOGY, INFERTILITY & CONTRACEPTION",
  "GYNAECOLOGICAL INFECTIONS, PELVIC PAIN & UROGYNAECOLOGY",
  "BENIGN GYNAECOLOGICAL DISORDERS & EARLY PREGNANCY",
  "GYNAECOLOGIC ONCOLOGY & THERAPEUTICS",
].map((title, index) => [title, index + 1]));

const PEDIATRICS_CHAPTER_ORDER = new Map([
  "INTRODUCTION, GROWTH, DEVELOPMENT & ADOLESCENCE",
  "FLUIDS, ELECTROLYTES, NUTRITION & MICRONUTRIENTS",
  "NEWBORN INFANTS (NEONATOLOGY) - CARE & INFECTIONS",
  "NEWBORN INFANTS - SYSTEMIC DISORDERS",
  "IMMUNIZATION & IMMUNODEFICIENCY",
].map((title, index) => [title, index + 1]));

function getPracticeChapterOrder(question, subjectId) {
  if (subjectId === "pathology") {
    return PATHOLOGY_CHAPTER_ORDER.get(question.chapterTitle) ?? directoryOrder(question.chapterOrder);
  }
  if (subjectId === "general-surgery") {
    return GENERAL_SURGERY_CHAPTER_ORDER.get(question.chapterTitle) ?? directoryOrder(question.chapterOrder);
  }
  if (subjectId === "obgyn") {
    return OBGYN_CHAPTER_ORDER.get(question.chapterTitle) ?? directoryOrder(question.chapterOrder);
  }
  if (subjectId === "pediatrics") {
    return PEDIATRICS_CHAPTER_ORDER.get(question.chapterTitle) ?? directoryOrder(question.chapterOrder);
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

function readCachedPracticeLibrary(membership) {
  if (typeof window === "undefined") return null;
  try {
    const cached = JSON.parse(localStorage.getItem(`${PRACTICE_LIBRARY_CACHE_KEY}:${membership?.id}:${membership?.plan}`) || "null");
    if (!cached || !Array.isArray(cached.subjects)) return null;
    return filterLibraryByPlan(normalizePracticeLibrary(cached), membership);
  } catch {
    return null;
  }
}

function writeCachedPracticeLibrary(library, membership) {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(`${PRACTICE_LIBRARY_CACHE_KEY}:${membership?.id}:${membership?.plan}`, JSON.stringify(library));
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
  return getDuelImageUrls(question);
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
  const [lockedFeature, setLockedFeature] = useState(null);
  function requestFeature(feature) {
    if (canAccessFeature(user, feature)) return true;
    setLockedFeature(feature);
    return false;
  }

  function scrollPageToTop() {
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    const mainEl = document.getElementById("main-content");
    if (mainEl) mainEl.scrollTop = 0;
    const workspaceEl = document.querySelector(".shell-workspace");
    if (workspaceEl) workspaceEl.scrollTop = 0;
  }

  function setActiveView(view) {
    if (view === "Practice") {
      handleBackToPracticeDirectory();
      setPracticeChoiceSubjectId("");
      setPracticeStage("selection");
    }
    updateActiveView(view);
    scrollPageToTop();
    window.requestAnimationFrame(() => {
      scrollPageToTop();
    });
  }

  useEffect(() => {
    scrollPageToTop();
  }, [activeView]);
  const [selectedOption, setSelectedOption] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const practiceAnswerLockedRef = useRef(false);
  const practiceLockedAnswersRef = useRef(new Map());
  const [answerConfidence, setAnswerConfidence] = useState("");
  const [flaggedQuestions, setFlaggedQuestions] = useState({});
  const [practiceLibrary, setPracticeLibrary] = useState(emptyPracticeLibrary);
  const [practiceLibraryStatus, setPracticeLibraryStatus] = useState("idle");
  const practiceLibraryRequestRef = useRef(0);
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
  const [analyticsShowAll, setAnalyticsShowAll] = useState(false);
  const [practiceQuestionStartedAt, setPracticeQuestionStartedAt] = useState(Date.now());
  const [userRating, setUserRating] = useState(1480);
  const [profilePhotoPreparing, setProfilePhotoPreparing] = useState(false);
  const [paymentPlanId, setPaymentPlanId] = useState("ultra");
  const duelDeadlineRef = useRef(0);
  const loadedDuelRef = useRef(null);
  const duelAnswerPendingRef = useRef(null);
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
  const [activeChallenge, setActiveChallenge] = useState(null); // { id, opponent, role: 'host' | 'guest' }
  const [selectedLeaderboardState, setSelectedLeaderboardState] = useState("");
  const [selectedLeaderboardCollege, setSelectedLeaderboardCollege] = useState("");
  const [authStatus, setAuthStatus] = useState("loading");
  const [authMode, setAuthMode] = useState("login");
  const [authBusy, setAuthBusy] = useState(false);
  const [emailChallenge, setEmailChallenge] = useState(null);
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
  const [incomingFriendRequests, setIncomingFriendRequests] = useState([]);
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
    medicalCountry: "",
    medicalCollege: "",
    contactNumber: "",
    password: "",
  });

  const visiblePracticeLibrary = useMemo(() => filterPracticeLibraryForUi(practiceLibrary), [practiceLibrary]);
  const practiceSubjects = visiblePracticeLibrary.subjects;
  const aiPracticeSubjects = practiceLibrary.aiSubjects ?? [];
  const usmlePracticeSubjects = practiceLibrary.usmleSubjects ?? [];
  const usmleModules = practiceLibrary.usmleModules ?? [];
  const fmgeSessions = visiblePracticeLibrary.fmgeSessions;
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
      ? (currentPracticeSubject?.questions ?? []).filter((question) => question.topic === selectedPracticeTopic
          && (selectedPracticeMode !== "ai" || !selectedPracticeChapter || (question.chapterTitle || "General Pathology") === selectedPracticeChapter))
      : currentPracticeQuestionSet?.questions ?? currentPracticeSubject?.questions ?? [];
  const currentPracticeQuestions =
    selectedPracticeMode === "usmle" && usmlePracticeQuestionIds.length
      ? usmlePracticeQuestionIds
          .map((questionId) => basePracticeQuestions.find((question) => question.id === questionId))
          .filter(Boolean)
      : basePracticeQuestions;
  const currentPracticeQuestion = currentPracticeQuestions[practiceQuestionIndex] ?? null;
  const questionBookmarks = (Array.isArray(user?.questionBookmarks) ? user.questionBookmarks : []).filter(bookmark =>
    !["pyq", "fmge"].includes(bookmark.mode) || !visiblePracticeLibrary.hiddenQuestionIds.has(bookmark.questionId),
  );
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
      .sort((left, right) => (right.players[0]?.score ?? 0) - (left.players[0]?.score ?? 0));
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
  const requestId = ++practiceLibraryRequestRef.current;
  const cachedLibrary = readCachedPracticeLibrary(user);
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

      const nextLibrary = filterLibraryByPlan(normalizePracticeLibrary(await response.json()), user);
      if (requestId !== practiceLibraryRequestRef.current) return;
      setPracticeLibrary(nextLibrary);
      writeCachedPracticeLibrary(nextLibrary, user);
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

  if (requestId !== practiceLibraryRequestRef.current) return;
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
    const previousFocus = document.activeElement;
    const modal = document.querySelector('.practice-choice-modal');
    modal?.querySelector('button')?.focus({ preventScroll: true });
    const handleKey = event => {
      if (event.key === 'Escape') { event.preventDefault(); closePracticeChoice(); }
      if (event.key !== 'Tab') return;
      const controls = [...(modal?.querySelectorAll('button:not(:disabled), a[href], input:not(:disabled), select:not(:disabled), [tabindex="0"]') || [])].filter(element => element.getClientRects().length);
      const first = controls[0], last = controls.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener('keydown', handleKey);
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
      document.removeEventListener('keydown', handleKey);
      if (previousFocus?.isConnected) previousFocus.focus({ preventScroll: true });
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
    practiceLibraryRequestRef.current += 1;
    setPracticeLibrary(emptyPracticeLibrary);
    setPracticeLibraryStatus("idle");
    setLockedFeature(null);
  }, [user?.id, user?.plan, user?.hasPracticeAccess]);

  useEffect(() => {
    const needsPracticeLibrary = activeView === "Practice" || (activeView === "Bookmarks" && questionBookmarks.length > 0);
    if (!user?.hasPracticeAccess || !needsPracticeLibrary || practiceLibraryStatus !== "idle") return;
    fetchPracticeLibrary();
  }, [activeView, practiceLibraryStatus, questionBookmarks.length, user?.hasPracticeAccess, user?.plan]);

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
        event.preventDefault();
        if (!event.repeat) handleSubmitAnswer(currentPracticeQuestion.options[optionIndex]);
      }
      if (event.key.toLowerCase() === "f" && currentPracticeQuestion) {
        setFlaggedQuestions((current) => ({ ...current, [currentPracticeQuestion.id]: !current[currentPracticeQuestion.id] }));
      }
      if (event.key === "Enter") {
        event.preventDefault();
        if (submitted) handleNextPracticeQuestion();
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

  async function fetchFriendRequests() {
    if (authStatus !== "authenticated") return;
    try {
      const data = await apiRequest("/api/friends");
      setIncomingFriendRequests(data.incomingRequests ?? []);
    } catch {}
  }

  useEffect(() => {
    if (authStatus !== "authenticated") return undefined;
    fetchCommunities();
    fetchDirectConversations();
    fetchFriendRequests();
    const messageInterval = window.setInterval(() => {
      fetchDirectConversations({ silent: true });
      fetchFriendRequests();
    }, 8000);
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
    if (duelStatus !== "challenge_waiting" || !activeChallenge?.id) return undefined;

    let cancelled = false;
    const pollChallenge = async () => {
      try {
        const data = await apiRequest(`/api/duels/challenge/status?id=${encodeURIComponent(activeChallenge.id)}`);
        if (cancelled) return;

        if (data.status === "matched" && data.duelId) {
          const questions = await loadDuelQuestions(data.duelId);
          beginLiveDuel(data.opponent ?? activeChallenge.opponent, {
            mode: "challenge",
            questions,
            sessionId: data.duelId,
          });
          return;
        }

        if (data.status === "declined") {
          setDuelStatus("idle");
          setActiveChallenge(null);
          setDuelMessage(`${activeChallenge.opponent?.name || "The opponent"} declined your 1v1 challenge.`);
          return;
        }

        if (data.status === "cancelled") {
          setDuelStatus("idle");
          setActiveChallenge(null);
          setDuelMessage("This 1v1 challenge was cancelled.");
          return;
        }
      } catch (error) {
        if (!cancelled) {
          setDuelMessage(error instanceof Error ? error.message : "Could not check challenge status.");
        }
      }
    };

    const intervalId = window.setInterval(pollChallenge, 1500);
    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, [activeChallenge, duelStatus]);

  useEffect(() => {
    if (!duelSessionId || !["live", "finished"].includes(duelStatus) || duelResult) return;
    let cancelled = false;
    let timer;
    const syncMatch = async () => {
      try {
        if (duelStatus === "finished") {
          await duelAnswerPendingRef.current?.tail;
          if (cancelled) return;
        }
        const data = duelStatus === "finished"
          ? await apiRequest("/api/duels/complete", { method: "POST", body: JSON.stringify({ sessionId: duelSessionId, forfeit: duelForfeited }) })
          : await apiRequest(`/api/duels/status?session=${encodeURIComponent(duelSessionId)}`);
        if (cancelled) return;
        duelDeadlineRef.current = Date.now() + Math.max(0, data.expiresAt - data.serverNow);
        setDuelOpponentProgress({ answered: data.opponentAnswered, correct: 0 });
        const locked = {};
        const selections = {};
        duelQuestions.forEach((q, index) => {
          if (Object.hasOwn(data.answers, q.id)) {
            locked[index] = true;
            selections[index] = q.options[data.answers[q.id]];
            const queue = duelAnswerPendingRef.current;
            if (queue?.sessionId === duelSessionId) {
              queue.confirmed.add(q.id);
              queue.locked.add(q.id);
              queue.failed.delete(index);
            }
          }
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
        if (!duelAnswerPendingRef.current?.failed.size) {
          setDuelMessage(duelStatus === "finished" ? "Answers saved. Waiting for your opponent or the match timer to finish." : "");
        }
      } catch (error) {
        if (!cancelled) setDuelMessage(`${error.message} Retrying connection...`);
      }
      if (!cancelled) timer = window.setTimeout(syncMatch, 2000);
    };
    void syncMatch();
    return () => { cancelled = true; window.clearTimeout(timer); };
  }, [duelSessionId, duelStatus, duelForfeited, duelResult]);

  function handleSubmitAnswer(option) {
    if (submitted || practiceAnswerLockedRef.current || !currentPracticeQuestion || !user || !currentPracticeQuestion.options.includes(option)) return;
    practiceAnswerLockedRef.current = true;
    practiceLockedAnswersRef.current.set(currentPracticeQuestion.id, option);
    setSelectedOption(option);

    const wasCorrect = option === currentPracticeQuestion.answer;
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
        mode: selectedPracticeMode,
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
      mode: selectedPracticeMode, selectedAnswer: option,
      durationSeconds: Math.max(1, Math.min(1800, Math.round((Date.now() - practiceQuestionStartedAt) / 1000))),
    });
  }

  function handleSelectPracticeSubject(subjectId) {
    if (practicePathTitle === "TOPIC WISE questions") {
      if (aiPracticeQuestionCountsBySubject[subjectId] > 0) handleStartAiPractice(subjectId);
      return;
    }
    setPracticeChoicePanel(practicePathTitle === "NEET PG / INICET" ? "pyq" : "formats");
    setPracticeChoiceSubjectId(subjectId);
  }

  function handleCustomModuleComplete(session) {
    const answeredAt = new Date(session.finishedAt).toISOString();
    const answered = session.questions.filter(question => Number.isInteger(session.answers[question.id]));
    const durationSeconds = Math.max(1, Math.min(1800, Math.round((session.finishedAt - session.startedAt) / 1000 / Math.max(1, answered.length))));
    const events = answered.map((question, index) => ({
      id: `${session.id}-${index}`, questionId: question.id, subjectId: question.subjectId,
      subject: question.subjectTitle, topic: question.topic, mode: "ai", activity: "revision", answeredAt,
      correct: session.answers[question.id] === question.answerIndex, durationSeconds,
    }));
    setAnalyticsEvents(current => {
      const next = [...current, ...events];
      writeAnalyticsEvents(user, next);
      return next;
    });
    setPracticeProgress(current => {
      const next = { ...current };
      for (const event of events) next[event.questionId] = { answeredAt, correct: event.correct, subjectId: event.subjectId };
      writePracticeProgress(user, next);
      return next;
    });
    for (const [index, question] of answered.entries()) practiceSync.record({
      id: `${session.id}-${index}`, questionId: question.id, subjectId: question.subjectId,
      mode: "ai", selectedAnswer: question.options[session.answers[question.id]], durationSeconds,
    });
  }

  function closePracticeChoice() {
    setPracticeChoiceSubjectId("");
    setPracticeChoicePanel("formats");
  }

  function handleOpenMindMaps(subjectId) {
    if (!requestFeature("theory")) return;
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
    if (!requestFeature(mode === "usmle" ? "usmle" : "practice")) return;
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode(mode);
    setSelectedPracticeExamYear(mode === "pyq" ? examYear : "");
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
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
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
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
    if (!requestFeature("community")) return;
    setSelectedCommunityId(communityId);
    setCommunityStage("detail");
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    document.getElementById("main-content")?.scrollTo?.({ top: 0, left: 0, behavior: "instant" });
  }

  function openDirectConversation(conversationId) {
    if (!requestFeature("inbox")) return;
    setSelectedDirectConversationId(conversationId);
    setCommunityStage("direct");
    setDirectMessageDraft("");
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    document.getElementById("main-content")?.scrollTo?.({ top: 0, left: 0, behavior: "instant" });
  }

  function handleBackToCommunityHub() {
    setCommunityStage("hub");
    setCommunityMessageDraft("");
    setCommunityThreadImage(null);
    setDirectMessageDraft("");
    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    document.getElementById("main-content")?.scrollTo?.({ top: 0, left: 0, behavior: "instant" });
  }

  function restorePracticeAnswer(question) {
    const locked = practiceLockedAnswersRef.current.has(question.id);
    practiceAnswerLockedRef.current = locked;
    setSelectedOption(practiceLockedAnswersRef.current.get(question.id) ?? "");
    setSubmitted(locked);
  }

  function handleNextPracticeQuestion() {
    if (!currentPracticeSubject) return;
    if (practiceQuestionIndex >= currentPracticeQuestions.length - 1) return;
    setPracticeQuestionIndex((current) => current + 1);
    restorePracticeAnswer(currentPracticeQuestions[practiceQuestionIndex + 1]);
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
    if (!requestFeature((entry?.bookmark?.mode || entry?.resolved?.mode) === "usmle" ? "usmle" : "practice")) return;
    if (!entry?.resolved) {
      setBookmarkMessage("That question is no longer available in the current practice library.");
      return;
    }

    const { mode, subject, question } = entry.resolved;
    setPracticePathTitle(mode === "fmge" ? "FMGE" : mode === "usmle" ? "USMLE–STEP 1" : mode === "ai" ? "TOPIC WISE questions" : "NEET PG / INICET");
    setSelectedPracticeSubjectId(subject.id);
    setSelectedPracticeMode(mode);
    setSelectedPracticeTopic("");
    setSelectedPracticeChapter("");
    setSelectedOption("");
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
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
    if (!requestFeature("practice")) return;
    const subject = aiPracticeSubjects.find((entry) => entry.id === subjectId);
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
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
    setSubmitted(false);
    setUsmlePracticeQuestionIds([]);
    scrollPracticeViewToTop();
  }

  function handleStartUsmlePractice(subjectId) {
    if (!requestFeature("usmle")) return;
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
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
    setSubmitted(false);
    setPracticeQuestionStartedAt(Date.now());
    scrollPracticeViewToTop();
  }

  function handleStartVivaSetup(subjectId) {
    if (!requestFeature("theory")) return;
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
    if (!requestFeature("theory")) return;
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
      setClinicalSessionMessage("AI is preparing the cases. This page will open them automatically when they are ready.");

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
        throw new Error(readySession.generationError || "AI could not prepare these clinical cases.");
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
    practiceAnswerLockedRef.current = false;
    practiceLockedAnswersRef.current.clear();
    setSubmitted(false);
    setPracticeStage("subject");
    setPracticeQuestionStartedAt(Date.now());
    scrollPracticeViewToTop();
  }
  async function handleCreateCommunity(event) {
    event.preventDefault();
    if (!requestFeature("community")) return;
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
    if (!requestFeature("community")) return;
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
    if (!requestFeature("inbox")) return;
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

    try {
      const data = await apiRequest("/api/duels/challenge/create", {
        method: "POST",
        body: JSON.stringify({ opponentId: opponentProfile.id }),
      });

      if (data.conversation) {
        setDirectConversations((current) => {
          const filtered = current.filter((c) => c.id !== data.conversation.id);
          return [data.conversation, ...filtered];
        });
      }

      setActiveView("Compete");
      setActiveChallenge({
        id: data.challenge.id,
        opponent: data.challenge.opponent,
        role: "host",
      });
      setDuelOpponent(data.challenge.opponent);
      setDuelStatus("challenge_waiting");
      setDuelMessage("");
    } catch (error) {
      setDirectMessagesMessage(error instanceof Error ? error.message : "Could not create 1v1 challenge room.");
    }
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
    duelAnswerPendingRef.current = { sessionId: options.sessionId ?? "", tail: Promise.resolve(), locked: new Set(), confirmed: new Set(), failed: new Set(), pending: 0 };
    setDuelAnswerBusy(false);
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

  function submitDuelAnswer(selection) {
    const queue = duelAnswerPendingRef.current;
    if (currentDuelSubmitted || !currentDuelQuestion || !user || !queue || queue.sessionId !== duelSessionId || queue.locked.has(currentDuelQuestion.id) || !currentDuelQuestion.options.includes(selection)) return;
    const index = duelIndex;
    const questionId = currentDuelQuestion.id;
    const optionIndex = currentDuelQuestion.options.indexOf(selection);
    queue.locked.add(questionId);
    queue.failed.delete(index);
    queue.pending++;
    setDuelSelections(current => ({ ...current, [index]: selection }));
    setDuelSubmitted(current => ({ ...current, [index]: true }));
    setDuelAnswerBusy(true);
    setDuelMessage("");
    queue.tail = queue.tail.then(async () => {
      await apiRequest("/api/duels/answer", { method: "POST", body: JSON.stringify({
        sessionId: queue.sessionId, questionId, optionIndex,
      }) });
      queue.confirmed.add(questionId);
    }).catch(error => {
      if (queue.confirmed.has(questionId)) return;
      queue.locked.delete(questionId);
      queue.failed.add(index);
      if (duelAnswerPendingRef.current !== queue) return;
      setDuelSubmitted(current => ({ ...current, [index]: false }));
      setDuelIndex(index);
      setDuelMessage(`Question ${index + 1} could not be saved. Select your answer again to retry. ${error.message}`);
    }).finally(() => {
      queue.pending--;
      if (duelAnswerPendingRef.current === queue) setDuelAnswerBusy(queue.pending > 0);
    });
  }

  async function nextDuelQuestion() {
    if (!currentDuelSubmitted) return;
    if (duelIndex === duelQuestions.length - 1) {
      const queue = duelAnswerPendingRef.current;
      await queue?.tail;
      if (duelAnswerPendingRef.current !== queue || queue?.failed.size) return;
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

  async function cancelDuelChallenge() {
    if (activeChallenge?.id) {
      try {
        await apiRequest("/api/duels/challenge/cancel", {
          method: "POST",
          body: JSON.stringify({ challengeId: activeChallenge.id }),
        });
      } catch {}
    }
    setActiveChallenge(null);
    setDuelStatus("idle");
    setDuelMessage("");
  }

  async function handleAcceptNotification(notification) {
    if (notification.type === "challenge") {
      try {
        const challengeId = notification.challengeId;
        if (!challengeId) {
          setActiveView("Compete");
          return;
        }
        const data = await apiRequest("/api/duels/challenge/accept", {
          method: "POST",
          body: JSON.stringify({ challengeId }),
        });

        if (data.status === "matched" && data.duel) {
          const questions = await loadDuelQuestions(data.duel.id);
          beginLiveDuel(data.opponent ?? notification.otherParticipant, {
            mode: "challenge",
            questions,
            sessionId: data.duel.id,
          });
        }
      } catch (error) {
        setDuelMessage(error instanceof Error ? error.message : "Could not join 1v1 challenge room.");
        setActiveView("Compete");
      }
      return;
    }

    if (notification.type === "friend_request" && notification.requestId) {
      try {
        await apiRequest("/api/friends/accept", {
          method: "POST",
          body: JSON.stringify({ requestId: notification.requestId, userId: notification.requestUser?.id }),
        });
        fetchFriendRequests();
      } catch {}
      return;
    }

    setActiveView(notification.destination || "Dashboard");
  }

  async function handleDeclineNotification(notification) {
    if (notification.type === "challenge") {
      try {
        if (notification.challengeId) {
          await apiRequest("/api/duels/challenge/decline", {
            method: "POST",
            body: JSON.stringify({ challengeId: notification.challengeId }),
          });
        }
      } catch {}
      return;
    }

    if (notification.type === "friend_request" && notification.requestId) {
      try {
        await apiRequest("/api/friends/decline", {
          method: "POST",
          body: JSON.stringify({ requestId: notification.requestId, userId: notification.requestUser?.id }),
        });
        fetchFriendRequests();
      } catch {}
      return;
    }
  }

  function resetDuel(syncServer = true) {
    duelAnswerPendingRef.current = null;
    setDuelAnswerBusy(false);
    localStorage.removeItem(`medicomm-duel:${user?.id}`);
    loadedDuelRef.current = null;
    if (syncServer && activeChallenge?.id && duelStatus === "challenge_waiting") {
      void apiRequest("/api/duels/challenge/cancel", {
        method: "POST",
        body: JSON.stringify({ challengeId: activeChallenge.id }),
      }).catch(() => undefined);
    }
    if (syncServer && (duelStatus === "matchmaking" || duelStatus === "live" || duelStatus === "finished")) {
      void apiRequest("/api/duels/rated/queue", {
        method: "DELETE",
      }).catch(() => undefined);
    }
    setActiveChallenge(null);
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
      medicalCountry: "",
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

  async function finishAuthentication(data) {
    setEmailChallenge(null);
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
      medicalCountry: "",
      medicalCollege: "",
      contactNumber: "",
      password: "",
    });
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
            username: authForm.name,
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

      if (data.verificationRequired) {
        setEmailChallenge(data);
        setAuthForm(current => ({ ...current, password: "" }));
        return;
      }
      await finishAuthentication(data);
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
            <h2>{emailChallenge ? "Verify your email" : isSignup ? "Create your study account" : "Continue your learning"}</h2>
            <p>{isSignup ? "Set up your profile in under a minute." : "Sign in to sync progress across devices."}</p>
          </div>
          {!emailChallenge && <div className="auth-tabs" role="tablist" aria-label="Authentication mode">
            <button
              className={`auth-tab${authMode === "login" ? " auth-tab-active" : ""}`}
              type="button"
              onClick={() => {
                setAuthMode("login");
                setAuthForm((current) => ({ ...current, email: "", password: "" }));
                setPasswordVisible(false);
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
                setAuthForm((current) => ({ ...current, email: "", password: "" }));
                setPasswordVisible(false);
                setAuthMessage("");
              }}
            >
              Sign up
            </button>
          </div>}

          {emailChallenge ? <EmailVerification key={emailChallenge.challengeId} challenge={emailChallenge} onVerified={finishAuthentication}
            onCancel={() => { setEmailChallenge(null); setAuthMessage(""); }} /> : <form key={authMode} className="auth-form" onSubmit={handleAuthSubmit} autoComplete="off">
            {isSignup ? (
              <>
                <label className="field">
                  <span>Username</span>
                  <input
                    type="text"
                    autoComplete="off"
                    value={authForm.name}
                    maxLength={254}
                    required
                    onChange={(event) => updateAuthField("name", event.target.value)}
                    placeholder="Choose a unique username"
                  />
                  <small>Your username must be unique. Capitalisation does not make it different.</small>
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
                    <CountrySelect value={authForm.medicalCountry} onChange={(value) => updateAuthField("medicalCountry", value)} />
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
                name={isSignup ? "signup-email" : "login-email"}
                autoComplete="off"
                value={authForm.email}
                onChange={(event) => updateAuthField("email", event.target.value)}
                placeholder="Enter your email"
              />
            </label>

            <label className="field">
              <span>Password</span>
              <div className="password-input-wrap">
                <input
                  type={passwordVisible ? "text" : "password"}
                  name={isSignup ? "signup-password" : "login-password"}
                  autoComplete={isSignup ? "new-password" : "current-password"}
                  value={authForm.password}
                  onChange={(event) => updateAuthField("password", event.target.value)}
                  placeholder={isSignup ? "Create a password" : "Enter your password"}
                  required
                  minLength={isSignup ? 8 : undefined}
                  maxLength={128}
                  pattern={isSignup ? "(?=.*[0-9])(?=.*[^\\p{L}\\p{N}\\s]).{8,128}" : undefined}
                  title={isSignup ? "Use 8 to 128 characters, including at least one number and one special character." : undefined}
                  aria-describedby={isSignup ? "signup-password-requirements" : undefined}
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
              {isSignup ? <small id="signup-password-requirements">8 to 128 characters, including at least one number and one special character.</small> : null}
            </label>

            {authMessage ? <p className="form-message" role="alert">{authMessage}</p> : null}

            <button className="button button-primary auth-submit" type="submit" disabled={authBusy}>
              {authBusy ? "Please wait..." : isSignup ? "Create account" : "Login"}
            </button>
          </form>}
          {!emailChallenge && <><div className="auth-divider"><span>or</span></div>
          <button className="button button-secondary guest-button" type="button" onClick={handleGuestLogin}>
            Explore as guest
          </button>
          <p className="auth-fine-print">Guest progress stays on this device. Create an account anytime to sync it.</p></>}
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

        <HomeBattleSection
          onCompete={() => setActiveView("Compete")}
          onLeaderboard={() => setActiveView("Leaderboard")}
          userRating={userRating}
        />

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

        <WebsiteReviews key={user?.id || "guest"} compact canReview={authStatus === "authenticated"} onSignIn={handleLogout} onViewAll={() => setActiveView("Reviews")} />

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

  function renderPractice() {
    const isTheory = practicePathTitle === "THEORY";
    const isPyqOnly = practicePathTitle === "NEET PG / INICET";
    const isTopicWise = practicePathTitle === "TOPIC WISE questions";
    const catalogTitle = isTheory ? "Cases and short notes by subject" : isTopicWise ? "Topic-wise questions by subject" : `${practiceLibrary.exam.title} by year and subject`;
    const feature = ["neetpg-tests", "fmge-tests"].includes(practiceStage) ? "tests"
      : isTheory || /^(viva-|clinical-|mind-map-)/.test(practiceStage) ? "theory"
      : practicePathTitle.startsWith("USMLE") || (practiceStage !== "catalog" && selectedPracticeMode === "usmle") ? "usmle" : "practice";
    if (practiceStage === "selection" || !canAccessFeature(user, feature)) {
      return <PracticeSelection isLocked={id => !canAccessFeature(user, practiceFeature(id))} onSelect={(title, id) => {
        if (!requestFeature(practiceFeature(id))) return;
        setPracticePathTitle(title);
        setPracticeStage(["neetpg-tests", "fmge-tests"].includes(id) ? id : id === "usmle" ? "usmle-modules" : id === "fmge" ? "fmge-years" : id === "custom-modules" ? "custom-modules" : "catalog");
        scrollPracticeViewToTop();
      }} />;
    }

    if (["neetpg-tests", "fmge-tests"].includes(practiceStage)) {
      return <TestSections key={practiceStage}
        exam={practiceStage === "fmge-tests" ? "fmge" : "neetpg"}
        title={practiceStage === "neetpg-tests" ? "NEETPG Tests" : "FMGE Tests"}
        onBack={() => { setPracticeStage("selection"); scrollPracticeViewToTop(); }} />;
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

    if (practiceStage === "custom-modules") {
      return <CustomModules key={user.id} subjects={aiPracticeSubjects} userId={user.id}
        onBack={() => { setPracticeStage("selection"); scrollPracticeViewToTop(); }}
        onComplete={handleCustomModuleComplete} syncMessage={practiceSync.message} />;
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
              <p className="view-subtitle">AI reviewed all three theory responses against case-specific marking points.</p>
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
                    <p className="eyebrow">AI theory review</p>
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
                  {currentClinicalEvaluation.hasImage ? <p className="viva-submitted-image-note">A photographed written answer was included in AI&apos;s review.</p> : null}
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
                      <span>AI can review clear handwriting from a photographed answer sheet.</span>
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
                  <p>AI will grade diagnosis, reasoning, morphology, and investigations against private case-specific marking points.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={(!clinicalAnswerImage && clinicalAnswerDraft.trim().length < 3) || clinicalAnswerBusy || clinicalAnswerImageBusy}
                    onClick={handleSubmitClinicalCaseAnswer}
                    aria-busy={clinicalAnswerBusy}
                  >
                    {clinicalAnswerBusy ? "AI is reviewing..." : "Submit case for AI review"}
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
              <p className="view-subtitle">AI will create three applied theory cases in the selected chapters.</p>
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
                {clinicalSessionBusy ? "Preparing clinical cases..." : "Generate 3 cases (30 tokens)"}
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
              <p className="view-subtitle">AI reviewed all five responses against the question-specific marking points.</p>
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
                    <p className="eyebrow">AI review</p>
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
                  {currentVivaEvaluation.hasImage ? <p className="viva-submitted-image-note">A photographed written answer was included in AI&apos;s review.</p> : null}
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
                      <span>Skip lengthy typing—AI can read clear handwriting from a photo.</span>
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
                  <p>AI will review your typed response, uploaded answer, or both against the private marking points and prepare a score and model answer.</p>
                  <button
                    className="button button-primary"
                    type="button"
                    disabled={(!vivaAnswerImage && vivaAnswerDraft.trim().length < 3) || vivaAnswerBusy || vivaAnswerImageBusy}
                    onClick={handleSubmitVivaAnswer}
                    aria-busy={vivaAnswerBusy}
                  >
                    {vivaAnswerBusy ? "AI is reviewing..." : "Submit for AI review"}
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
                <small>Your selected chapters, typed responses, and any uploaded answer images will be sent to the configured AI provider. Answer images are not saved in your Viva history. With the free tier, the AI service may process submitted content according to standard AI terms. Do not include names, contact details, or patient-identifiable information.</small>
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
                      restorePracticeAnswer(currentPracticeQuestions[index]);
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
                        loading="eager"
                        fetchPriority={index === 0 ? "high" : "auto"}
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
                    onClick={() => handleSubmitAnswer(option)}
                    disabled={submitted}
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
              <span role="status">{submitted ? "Answer locked" : "Select an option to lock your answer"}</span>
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
        {practicePathTitle !== "NEET PG / INICET" ? (
        <div className="view-header">
          <div>
            <p className="eyebrow">{isTheory ? "Theory" : "Practice"}</p>
            <h2>{catalogTitle}</h2>
            {isTopicWise && <p className="view-subtitle">Choose a subject, then a chapter and topic to practise prepared questions.</p>}
          </div>
          <button className="button button-secondary" onClick={() => setActiveView("Practice")}>
            Back
          </button>
        </div>
        ) : null}

        {aiPracticeMessage ? <p className="form-message practice-ai-message">{aiPracticeMessage}</p> : null}

        {practiceChoiceSubject ? createPortal(
          <div className="practice-choice-backdrop" onClick={event => { if (event.target === event.currentTarget) closePracticeChoice(); }}>
            <article className="practice-choice-modal" role="dialog" aria-modal="true" aria-labelledby="practice-choice-title">
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
              ) : isPyqOnly || practiceChoicePanel === "pyq" ? (
                <div className="practice-year-picker">
                  <div className="practice-choice-section-heading">
                    <button className="practice-choice-back-link" type="button" onClick={isPyqOnly ? closePracticeChoice : () => setPracticeChoicePanel("formats")}>
                      {isPyqOnly ? "← All subjects" : "← All practice modes"}
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
                    <small>Type or photograph answers · AI theory review</small>
                  </button>
                </div>
              )}
            </article>
          </div>, document.body
        ) : null}

        {practicePathTitle === "NEET PG / INICET" ? <PracticeSubjectDirectory
          years={groupedPracticeYears}
          onSelect={handleSelectPracticeSubject}
          onBack={() => setActiveView("Practice")}
        /> : (
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
                      disabled={isTopicWise && aiQuestionCount === 0}
                      onClick={() => handleSelectPracticeSubject(subject.id)}
                    >
                      <span className="practice-subject-label">{subject.title}</span>
                      <p className="practice-subject-copy">{isTheory ? "Study this subject through cases and short notes." : isTopicWise ? aiQuestionCount ? "Browse chapters, choose a topic, and practise its questions." : "Topic-wise questions are being prepared." : "Choose PYQs, topic-wise questions, USMLE practice, Mind Maps, an AI viva, or Clinical Cases."}</p>
                      <span className="practice-subject-counts">
                        {isTheory ? <><strong>Cases</strong><strong>Short Notes</strong></> : isTopicWise ? <strong>{aiQuestionCount ? `${aiQuestionCount} questions` : "Coming soon"}</strong> : <><strong>{subject.questions.length} PYQs</strong><strong>{aiQuestionCount} Topic Wise</strong></>}
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
                      disabled={isTopicWise && aiQuestionCount === 0}
                      onClick={() => handleSelectPracticeSubject(subject.id)}
                    >
                      <span className="practice-subject-label">{subject.title}</span>
                      <p className="practice-subject-copy">Practise topic-wise questions.</p>
                      <span className="practice-subject-counts">
                        <strong>{isTopicWise && !aiQuestionCount ? "Coming soon" : `${aiQuestionCount} Topic Wise`}</strong>
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ) : null}
        </div>
        )}
      </section>
    );
  }

  function renderBookmarks() {
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
            {user?.hasPracticeAccess && (practiceLibraryStatus === "loading" || practiceLibraryStatus === "idle") ? (
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
                const locked = !canAccessFeature(user, bookmark.mode === "usmle" ? "usmle" : "practice");
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
                      <button className="button button-primary" type="button" disabled={!locked && !resolved} onClick={() => openBookmarkedQuestion(entry)}>
                        {locked ? <><LockKeyhole size={16} aria-hidden="true" /> Unlock Question</> : resolved
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
    const communityAccess = canAccessFeature(user, "community");
    if (communityAccess && communityStage === "direct" && selectedDirectConversation) {
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
              <div className="direct-chat-wallpaper min-w-0 p-5">
                <div className="flex max-h-[60vh] min-h-64 flex-col gap-4 overflow-y-auto pb-5">
                  {selectedDirectConversation.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.isOwnMessage ? "justify-end" : "justify-start"}`}
                    >
                      <div className={`max-w-[90%] space-y-2 rounded-2xl p-4 text-sm [&_p]:whitespace-pre-wrap [&_p]:break-words [&>span]:block [&>span]:text-[10px] ${message.isOwnMessage ? "bg-slate-900 text-white dark:bg-neutral-800 dark:text-white [&>span]:text-slate-300 dark:[&>span]:text-neutral-400" : "bg-slate-100 text-slate-900 dark:bg-neutral-900 dark:text-neutral-100 border border-slate-200/60 dark:border-neutral-800 [&>span]:text-slate-500 dark:[&>span]:text-neutral-400"} ${message.type === "challenge" ? "border-2 border-amber-500" : ""}`}>
                        {message.userId ? (
                          <button
                            type="button"
                            className={`text-xs font-semibold hover:underline ${message.isOwnMessage ? "text-teal-200" : "text-teal-600 dark:text-teal-400"}`}
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

    if (communityAccess && communityStage === "detail" && selectedCommunity) {
      return <CommunityThreads key={selectedCommunity.id} room={selectedCommunity} user={user}
        message={communitiesMessage} timestamp={formatCommunityTimestamp} limit={COMMUNITY_THREAD_WORD_LIMIT}
        draft={communityMessageDraft} onDraft={setCommunityMessageDraft}
        image={communityThreadImage} onImage={handleCommunityThreadImageChange} onRemoveImage={() => setCommunityThreadImage(null)}
        replyDrafts={communityReplyDrafts} onReplyDraft={(id, value) => setCommunityReplyDrafts(current => ({ ...current, [id]: value }))}
        expanded={expandedCommunityThreads} onToggle={toggleCommunityThread} onSend={handleSendCommunityMessage}
        onBack={handleBackToCommunityHub} onJoin={handleJoinCommunity} onInvite={handleCopyCommunityInvite}
        onProfile={id => openPublicProfile(id, "Communities")} onDirect={handleOpenDirectChat}
        onRemoveMember={handleRemoveCommunityMember}
        conversations={directConversations} directBusy={directMessagesBusy}
        directSearch={directSearchTerm} onDirectSearch={setDirectSearchTerm}
        directSearchBusy={directSearchBusy} directResults={directSearchResults}
        onConversation={openDirectConversation}
        communities={communities} onOpenRoom={openCommunityChat} />;
    }

    return <CommunityHub communities={communities} busy={communitiesBusy}
      locked={!communityAccess} onUnlock={requestFeature}
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
      challengeOpponent={activeChallenge?.opponent ?? duelOpponent}
      onCancelChallenge={cancelDuelChallenge}
      onStart={() => startDuel()} onBot={startBotDuel} onLeave={leaveDuelQueue}
      onPractice={() => setActiveView("Practice")}
      onLeaderboard={() => setActiveView("Leaderboard")}
      onNext={nextDuelQuestion} onForfeit={forfeitDuel}
      onAgain={() => resetDuel()} onToggleReview={() => setShowDuelReview(value => !value)}
      onSelect={submitDuelAnswer}
      renderDetails={question => <>
        <QuestionLaboratoryTable findings={question.laboratoryFindings} compact />
        {getQuestionImageUrls(question).length > 0 && <div className={getQuestionImageUrls(question).length === 1 ? "mx-auto mt-5 grid w-full max-w-lg gap-3" : "mt-5 grid gap-3 sm:grid-cols-2"}>
          {getQuestionImageUrls(question).map((imageUrl, index) => <span key={imageUrl} className="relative flex min-w-0 items-center justify-center overflow-hidden rounded-xl bg-black">
            <img className="block h-auto w-full object-contain object-center" src={getPracticeImageUrl(imageUrl)} alt={`Question visual ${index + 1}`} />
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
        {authStatus !== "guest" && (user?.hasPracticeAccess || user?.subscriptionExpiresAt) && <article className="card panel">
          <h3>Your subscription</h3>
          <div className="stack-list">
            {user.subscriptionPurchasedAt && <div className="stack-row"><span>Purchased on</span><strong>{new Date(user.subscriptionPurchasedAt).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', day: 'numeric', month: 'long', year: 'numeric' })}</strong></div>}
            <div className="stack-row"><span>{user.subscriptionStatus === 'expired' ? 'Expired on' : 'Expires on'}</span><strong>{user.subscriptionExpiresAt ? new Date(user.subscriptionExpiresAt).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', day: 'numeric', month: 'long', year: 'numeric' }) : 'Purchase date awaiting verification'}</strong></div>
          </div>
          <p className="panel-copy">{user.subscriptionExpiresAt ? 'Your annual membership dates are saved to your account.' : 'Your existing access is preserved while the purchase date is confirmed.'}</p>
        </article>}
        <div className="content-grid profile-layout">
          <article className="card panel">
            <h3>Personal details</h3>
            <form className="profile-form" onSubmit={handleProfileSave}>
              <label className="field">
                <span>Username</span>
                <input
                  type="text"
                  value={profileState.name}
                  maxLength={254}
                  required
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
    const activity = events.reduce((sum, item) => ({ ...sum, [item.activity || "pyq"]: (sum[item.activity || "pyq"] || 0) + (Number(item.durationSeconds) || 0) }), { pyq: 0, revision: 0, battle: 0, usmle: 0 });
    const share = (value) => seconds ? Math.round(value / seconds * 100) : 0;
    const pyqShare = share(activity.pyq);
    const revisionShare = share(activity.revision);
    const battleShare = share(activity.battle);
    const usmleShare = share(activity.usmle);
    const days = events.sort((a, b) => new Date(a.answeredAt) - new Date(b.answeredAt)).reduce((list, item) => {
      const key = new Date(new Date(item.answeredAt).getTime() + 330 * 60000).toISOString().slice(0, 10);
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
    const review = (item) => {
      const missed = [...events].reverse().find(event => !event.correct && event.subjectId === item.id && (event.topic || "General review") === item.topic && event.activity !== "battle");
      if (missed) {
        continueDashboardPractice({ ...missed, topic: missed.topic || "General review", mode: missed.mode || (missed.activity === "revision" ? "ai" : missed.activity === "usmle" ? "usmle" : "pyq") });
      } else {
        setActiveView("Practice");
        if (practiceSubjects.some(subject => subject.id === item.id)) setPracticeChoiceSubjectId(item.id);
      }
    };
    return <section className="app-view">
      <div className="view-header"><div><p className="eyebrow">Learning intelligence</p><h2>Performance analytics</h2><p className="view-subtitle">Live insights from your completed practice.</p></div><button className="button button-primary" onClick={() => attention[0] ? review(attention[0]) : setActiveView("Practice")}>Practice weak topics</button></div>
      <div className="analytics-kpi-grid"><article className="card panel"><span>Accuracy</span><strong>{periodAccuracy}%</strong><small>{correct} correct in this period</small></article><article className="card panel"><span>Questions solved</span><strong>{events.length}</strong><small>In the selected period</small></article><article className="card panel"><span>Average pace</span><strong>{pace < 60 ? `${pace}s` : `${Math.floor(pace / 60)}m ${pace % 60}s`}</strong><small>Per question</small></article><article className="card panel"><span>Study time</span><strong>{timeLabel}</strong><small>Measured active time</small></article></div>
      <div className="analytics-main-grid"><article className="card panel accuracy-trend-card"><div className="panel-heading-split"><div><h3>Accuracy trend</h3></div><select aria-label="Analytics period" value={analyticsPeriod} onChange={(event) => setAnalyticsPeriod(Number(event.target.value))}><option value="30">Last 30 days</option><option value="90">Last 90 days</option><option value="365">Last year</option></select></div>{days.length ? <div className="line-chart"><div className="chart-summary"><span><strong>{periodAccuracy}%</strong> average accuracy</span><span>{events.length} questions</span></div><svg viewBox="0 0 600 205" role="img" aria-label="Accuracy trend"><defs><linearGradient id="analyticsArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#2563eb" stopOpacity=".22"/><stop offset="100%" stopColor="#2563eb" stopOpacity=".01"/></linearGradient></defs>{[25, 50, 75, 100].map((value) => { const y = 165 - value * 1.35; return <g key={value}><line className="chart-gridline" x1="50" x2="580" y1={y} y2={y}/><text className="chart-y-label" x="42" y={y + 4} textAnchor="end">{value}%</text></g>; })}<polygon className="chart-area" points={areaPoints}/><polyline className="chart-line" points={points}/>{chartData.map((day) => <g className="chart-marker" key={day.key}><circle className="chart-point-halo" cx={day.x} cy={day.y} r="9"/><circle className="chart-point" cx={day.x} cy={day.y} r="5"/><text className="chart-value" x={day.x} y={day.y - 14} textAnchor="middle">{day.accuracy}%</text><title>{day.accuracy}% · {day.attempts} questions · {day.key}</title></g>)}</svg><div className="chart-axis">{chartData.map((day) => <span key={day.key}>{new Date(`${day.key}T00:00:00`).toLocaleDateString([], { month: "short", day: "numeric" })}</span>)}</div></div> : <div className="analytics-empty"><span className="analytics-empty-icon">↗</span><strong>Your progress graph starts here</strong><small>Complete a practice question to plot your first result.</small><button className="text-button" onClick={() => setActiveView("Practice")}>Start practice</button></div>}</article>
      <article className="card panel mastery-card"><div className="panel-heading-split"><div><h3>Subject mastery</h3><p className="panel-copy">Accuracy in this period</p></div><button className="text-button" aria-expanded={analyticsShowAll} onClick={() => setAnalyticsShowAll(value => !value)}>{analyticsShowAll ? "Show less" : "View all"}</button></div>{subjects.length ? <div className="mastery-list">{(analyticsShowAll ? subjects : subjects.slice(0, 5)).map((subject) => <div key={subject.id}><span><strong>{subject.name}</strong><small>{subject.accuracy}% · {subject.attempts} attempted</small></span><div><i style={{ width: `${subject.accuracy}%` }}/></div></div>)}</div> : <p className="analytics-empty">No subject activity in this period.</p>}</article></div>
      <div className="analytics-bottom-grid"><article className="card panel"><h3>Time by activity</h3><div className="donut-layout"><div className="donut-chart" style={{ background: seconds ? `conic-gradient(var(--ui-brand) 0 ${pyqShare}%,#10b981 ${pyqShare}% ${pyqShare + revisionShare}%,#8b5cf6 ${pyqShare + revisionShare}% ${pyqShare + revisionShare + battleShare}%,#f59e0b ${pyqShare + revisionShare + battleShare}% 100%)` : "var(--ui-border, #334155)" }}><span>{timeLabel}<small>total</small></span></div><div className="donut-legend"><span><i className="dot-blue"/>PYQs <strong>{pyqShare}%</strong></span><span><i className="dot-emerald"/>AI revision <strong>{revisionShare}%</strong></span><span><i className="dot-violet"/>Battles <strong>{battleShare}%</strong></span><span><i style={{ background: "#f59e0b" }}/>USMLE <strong>{usmleShare}%</strong></span></div></div><p className="panel-copy">{seconds ? "Recorded question time only. Battle duration is not tracked." : "No study time recorded in this period yet."}</p></article><article className="card panel"><h3>Needs attention</h3>{attention.length ? <div className="attention-list">{attention.map((item) => <button key={`${item.id}-${item.topic}`} onClick={() => review(item)}><span>{item.topic}<small>{item.count} incorrect · {item.name}</small></span><strong>Review →</strong></button>)}</div> : <p className="analytics-empty">Incorrect answers will appear here for targeted review.</p>}</article></div>
    </section>;
  }

  function renderPricing() {
    const planFeatures = (tokens, theory, usmle) => [
      { label: `${tokens} tokens per day`, included: true },
      { label: "Community Access", included: true },
      { label: "Personal Inbox Access", included: true },
      { label: "NEET PG Questions", included: true },
      { label: "FMGE Questions", included: true },
      { label: "Topic-Wise Questions", included: true },
      { label: "Theory Practice", included: theory },
      { label: "USMLE Practice Questions", included: usmle },
      { label: "MEDULLA Practice Test", included: usmle },
    ];
    const plans = [
      { name: "Lite", price: "₹799", cadence: "/ year", copy: "Perfect for students who want daily practice without spending much.", features: planFeatures(100, false, false), action: "Get Lite" },
      { name: "Ultra", price: "₹1199", cadence: "/ year", copy: "For MBBS students preparing consistently throughout the year.", features: planFeatures(200, true, false), action: "Choose Ultra", featured: true },
      { name: "Premium", price: "₹1599", cadence: "/ year", copy: "Built for serious NEET PG aspirants.", features: planFeatures(300, true, true), action: "Go Premium" },
    ];
    return (
      <section className="app-view pricing-page">
        <div className="pricing-hero"><p className="eyebrow">Simple, affordable pricing</p><h2>Master Medicine,<br/>One Question at a Time<span>.</span></h2><p>Practice consistently, compete with friends, analyze your weaknesses, and prepare confidently for university exams and NEET PG.</p><div className="billing-toggle"><span>Annual plans · one-time payment</span></div></div>
        <div className="pricing-grid">{plans.map((plan) => <article className={`pricing-card${plan.featured ? " pricing-card-featured" : ""}`} key={plan.name}>{plan.featured ? <span className="popular-pill">★ Most popular</span> : null}<h3>{plan.name}</h3><p>{plan.copy}</p><div className="plan-price"><strong>{plan.price}</strong><span>{plan.cadence}</span></div><button className={`button ${plan.featured ? "button-primary" : "button-secondary"}`} onClick={() => { setPaymentPlanId(plan.name.toLowerCase()); document.getElementById("payment-gateway")?.scrollIntoView({ behavior: "smooth" }); }}>{plan.action}</button><ul>{plan.features.map((feature) => <li key={feature.label} className={feature.included ? "plan-feature-included" : "plan-feature-excluded"}><span role="img" aria-label={feature.included ? "Included" : "Not included"}>{feature.included ? "\u2713" : "\u2715"}</span>{feature.label}</li>)}</ul></article>)}</div>
        <article className="card panel payment-gateway-section" id="payment-gateway">
          <div className="payment-copy"><p className="eyebrow">Razorpay Checkout</p><h3>Complete your payment securely</h3><p className="panel-copy">Choose a plan above, then pay using Razorpay. Your payment is confirmed by our server and saved to your account.</p><div className="payment-provider-row"><span>UPI</span><span>Cards</span><span>Net banking</span><span>Wallets</span></div></div>
          <RazorpayCheckout key={user?.id || "guest"} plan={PAYMENT_PLANS.find(plan => plan.id === paymentPlanId)} user={user} guest={authStatus !== "authenticated"} onVerified={payment => { if (payment.hasPracticeAccess) { setUser(current => current?.id === user?.id ? { ...current, hasPracticeAccess: true, subscriptionPurchasedAt: payment.subscriptionPurchasedAt, subscriptionExpiresAt: payment.subscriptionExpiresAt, subscriptionStatus: payment.subscriptionStatus, plan: payment.plan } : current); setPracticeLibraryStatus("idle"); } }} />
        </article>
        <div className="pricing-faq"><h3>Common questions</h3><details><summary>Can I keep using Medulla for free?</summary><p>Yes. Explore the feature pages, browse the community directory, and compete using your free tokens. A paid plan unlocks practice questions, community participation, and your personal inbox.</p></details><details><summary>Will my progress carry over when I upgrade?</summary><p>Yes. Plans change access, never your saved learning history.</p></details><details><summary>How will payments be secured?</summary><p>Razorpay collects payment details securely. Medulla stores the order and verified payment status.</p></details></div>
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
        return <div className="app-view"><WebsiteReviews key={user?.id || "guest"} canReview={authStatus === "authenticated"} onSignIn={handleLogout} /></div>;
      case "Practice":
        return <>
          {!["selection", "usmle-modules", "fmge-years", "custom-modules", "neetpg-tests", "fmge-tests"].includes(practiceStage) && !(practiceStage === "catalog" && practicePathTitle === "NEET PG / INICET") && <div className="practice-path-breadcrumb">
            <button type="button" className="text-button" onClick={() => setActiveView("Practice")}>← All practice options</button>
            {practicePathTitle && <span>{practicePathTitle} practice</span>}
          </div>}
          {renderPractice()}
        </>;
      case "Bookmarks":
        return renderBookmarks();
      case "Analytics":
        return renderAnalyticsFunctional();
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
      incomingFriendRequests={incomingFriendRequests}
      onAcceptNotification={handleAcceptNotification}
      onDeclineNotification={handleDeclineNotification}
    >
      {renderView()}
      <FeatureAccessDialog feature={lockedFeature} onClose={() => setLockedFeature(null)} onPlans={() => { setLockedFeature(null); setActiveView("Pricing"); }} />
    </AppShell>
  );
}

export default App;
