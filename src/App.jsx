import { useEffect, useMemo, useState } from "react";
import { AppShell } from "./components/AppShell";
import { apiRequest } from "./lib/api";
import { SESSION_TOKEN_KEY, THEME_STORAGE_KEY } from "./lib/clientStorage";

const PRACTICE_LIBRARY_URL = "/api/practice";

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

const navItems = ["Home", "Dashboard", "Practice", "Leaderboard", "Communities", "Compete", "Profile"];

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

function formatStatValue(value) {
  return Number.isFinite(value) ? value.toLocaleString("en-IN") : "0";
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
  const [practiceLibrary, setPracticeLibrary] = useState(emptyPracticeLibrary);
  const [practiceLibraryStatus, setPracticeLibraryStatus] = useState("idle");
  const [practiceLibraryMessage, setPracticeLibraryMessage] = useState("");
  const [aiPracticeBusy, setAiPracticeBusy] = useState(false);
  const [aiPracticeMessage, setAiPracticeMessage] = useState("");
  const [selectedPracticeSubjectId, setSelectedPracticeSubjectId] = useState("");
  const [selectedPracticeMode, setSelectedPracticeMode] = useState("pyq");
  const [practiceChoiceSubjectId, setPracticeChoiceSubjectId] = useState("");
  const [practiceQuestionIndex, setPracticeQuestionIndex] = useState(0);
  const [practiceStage, setPracticeStage] = useState("catalog");
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
  const practiceYears = practiceLibrary.years ?? [];
  const activePracticeSubjects = selectedPracticeMode === "ai" ? aiPracticeSubjects : practiceSubjects;
  const currentPracticeSubject =
    activePracticeSubjects.find((subject) => subject.id === selectedPracticeSubjectId) ??
    activePracticeSubjects[0] ??
    null;
  const currentPracticeQuestion = currentPracticeSubject?.questions?.[practiceQuestionIndex] ?? null;
  const practiceChoiceSubject =
    practiceSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ??
    null;
  const currentAiPracticeSubject = aiPracticeSubjects.find((subject) => subject.id === practiceChoiceSubjectId) ?? null;
  const groupedPracticeYears = practiceYears.map((year) => ({
    ...year,
    subjects: year.subjectIds
      .map((subjectId) => practiceSubjects.find((subject) => subject.id === subjectId))
      .filter(Boolean),
  }));
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
        return total + (duelSelections[index] === question.answer ? 1 : 0);
      }, 0),
    [duelSelections, duelSubmitted],
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
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 8000);

    try {
      setPracticeLibraryStatus("loading");
      const response = await fetch(PRACTICE_LIBRARY_URL, {
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error("Could not load practice questions.");
      }

      const data = await response.json();
      const nextLibrary = {
        exam: data.exam ?? emptyPracticeLibrary.exam,
        years: data.years ?? [],
        subjects: data.subjects ?? [],
        aiSubjects: data.aiSubjects ?? [],
      };
      setPracticeLibrary(nextLibrary);
      setSelectedPracticeSubjectId((current) => {
        if (current && nextLibrary.subjects.some((subject) => subject.id === current)) return current;
        return nextLibrary.subjects[0]?.id ?? "";
      });
      setPracticeLibraryMessage("");
      setPracticeLibraryStatus("ready");
    } catch (error) {
      setPracticeLibrary(emptyPracticeLibrary);
      setSelectedPracticeSubjectId("");
      setPracticeLibraryMessage(error instanceof Error ? error.message : "Could not load practice questions.");
      setPracticeLibraryStatus("error");
    } finally {
      window.clearTimeout(timeoutId);
    }
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
    fetchLeaderboard();
    fetchPlatformSummary();
  }, [authStatus]);

  useEffect(() => {
    if (activeView !== "Practice" || practiceLibraryStatus !== "idle") return;
    fetchPracticeLibrary();
  }, [activeView, practiceLibraryStatus]);

  async function fetchCommunities() {
    if (authStatus !== "authenticated") return;

    try {
      setCommunitiesBusy(true);
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
      setCommunitiesBusy(false);
    }
  }

  async function fetchDirectConversations() {
    if (authStatus !== "authenticated") return;

    try {
      setDirectMessagesBusy(true);
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
      setDirectMessagesBusy(false);
    }
  }

  useEffect(() => {
    if (authStatus !== "authenticated") return;
    fetchCommunities();
    fetchDirectConversations();
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

    fetchCommunities();
    fetchDirectConversations();

    const interval = window.setInterval(() => {
      fetchCommunities();
      fetchDirectConversations();
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
          const questions = duelQuestions.length ? duelQuestions : await loadDuelQuestions();
          beginLiveDuel(data.opponent, {
            mode: "rated",
            questions,
            sessionId: data.duel?.id ?? `rated-${Date.now()}`,
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
    const answered = duelOpponentTimeline.filter((step) => step.revealAt <= elapsed).length;
    const correct = duelOpponentTimeline.filter((step) => step.revealAt <= elapsed && step.correct).length;
    setDuelOpponentProgress({ answered, correct });
  }, [duelStatus, duelTimeLeft, duelOpponentTimeline]);

  useEffect(() => {
    if (duelStatus !== "finished" || !duelOpponent || duelResult) return;

    const opponentCorrect = duelOpponentTimeline.filter((step) => step.correct).length;
    const opponentAnswered = duelOpponentTimeline.length;
    const userAnswered = Object.keys(duelSubmitted).length;
    const userCompletedEarlier = userAnswered === duelQuestions.length && duelTimeLeft > 0;
    const opponentCompletedEarlier = duelOpponentTimeline.every((step) => step.revealAt < DUEL_DURATION_SECONDS - duelTimeLeft);

    let actualScore = 0.5;
    let verdict = "draw";

    if (userDuelScore > opponentCorrect) {
      actualScore = 1;
      verdict = "win";
    } else if (userDuelScore < opponentCorrect) {
      actualScore = 0;
      verdict = "loss";
    } else if (userCompletedEarlier && !opponentCompletedEarlier) {
      actualScore = 1;
      verdict = "win";
    } else if (!userCompletedEarlier && opponentCompletedEarlier) {
      actualScore = 0;
      verdict = "loss";
    }

    setDuelOpponentProgress({ answered: opponentAnswered, correct: opponentCorrect });

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
        });
      }
    };

    void completeDuel();
  }, [
    duelMode,
    duelOpponent,
    duelOpponentTimeline,
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

  function startPracticeSession(subjectId, mode) {
    setSelectedPracticeSubjectId(subjectId);
    setSelectedPracticeMode(mode);
    setPracticeQuestionIndex(0);
    setSelectedOption("");
    setSubmitted(false);
    setPracticeStage("subject");
    setPracticeChoiceSubjectId("");
  }

  function handleBackToPracticeDirectory() {
    setPracticeStage("catalog");
    setSelectedPracticeMode("pyq");
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
    setDirectMessageDraft("");
  }

  function handleNextPracticeQuestion() {
    if (!currentPracticeSubject) return;
    if (practiceQuestionIndex >= currentPracticeSubject.questions.length - 1) return;
    setPracticeQuestionIndex((current) => current + 1);
    setSelectedOption("");
    setSubmitted(false);
  }

  async function handleStartAiPractice(subjectId) {
    const subject = practiceSubjects.find((entry) => entry.id === subjectId);
    if (!subject) return;

    try {
      setAiPracticeBusy(true);
      setAiPracticeMessage("");
      await apiRequest("/api/generate-questions", {
        method: "POST",
        timeoutMs: 120000,
        body: JSON.stringify({
          examId: practiceLibrary.exam?.id ?? "neet-pg-pyqs",
          subjectId,
          count: 20,
          topic: subject.questions?.[0]?.topic ?? "High-yield review",
          difficulty: "exam",
        }),
      });
      await fetchPracticeLibrary();
      setSelectedPracticeSubjectId(subjectId);
      setSelectedPracticeMode("ai");
      setPracticeStage("subject");
      setPracticeChoiceSubjectId("");
      setPracticeQuestionIndex(0);
      setSelectedOption("");
      setSubmitted(false);
      setAiPracticeMessage(`${subject.title} AI practice is ready with 20 supplemental questions.`);
    } catch (error) {
      setAiPracticeMessage(error instanceof Error ? error.message : "Could not generate supplemental practice.");
    } finally {
      setAiPracticeBusy(false);
    }
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

  async function handleSendCommunityMessage(event) {
    event.preventDefault();
    if (!selectedCommunity || !communityMessageDraft.trim()) return;

    setCommunitiesMessage("");

    try {
      const data = await apiRequest(`/api/communities/${selectedCommunity.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ text: communityMessageDraft }),
      });
      setCommunities((current) =>
        current.map((community) => (community.id === selectedCommunity.id ? data.community : community)),
      );
      setCommunityMessageDraft("");
    } catch (error) {
      setCommunitiesMessage(error instanceof Error ? error.message : "Could not send message.");
    }
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

  async function loadDuelQuestions() {
    try {
      const data = await apiRequest(`/api/duels/questions?count=${fallbackDuelQuestions.length}`);
      return Array.isArray(data.questions) && data.questions.length ? data.questions : fallbackDuelQuestions;
    } catch {
      return fallbackDuelQuestions;
    }
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
    setDuelStatus("live");
  }

  async function startDuel(preferredOpponent = null) {
    if (preferredOpponent) {
      const questions = await loadDuelQuestions();
      beginLiveDuel(preferredOpponent, {
        mode: "rated",
        questions,
        sessionId: `challenge-${Date.now()}`,
      });
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
      const questions = await loadDuelQuestions();
      const data = await apiRequest("/api/duels/rated/queue", {
        method: "POST",
      });

      if (data.status === "matched" && data.opponent) {
        beginLiveDuel(data.opponent, {
          mode: "rated",
          questions,
          sessionId: data.duel?.id ?? `rated-${Date.now()}`,
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
    const questions = await loadDuelQuestions();
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
        sessionId: `bot-${Date.now()}`,
      },
    );
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
          <p className="eyebrow">Secure access</p>
          <h1>Log in to your MediComm profile</h1>
          <p>
            Create an account with your name, email, medical college, contact number, and password.
            Your information is stored in this project&apos;s local database and shown inside the app
            after login.
          </p>
        </section>

        <section className="card auth-card">
          <div className="auth-tabs">
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

            {authMessage ? <p className="form-message">{authMessage}</p> : null}

            <button className="button button-primary auth-submit" type="submit" disabled={authBusy}>
              {authBusy ? "Please wait..." : isSignup ? "Create account" : "Login"}
            </button>
          </form>
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
              <h2>Official PYQs stay trusted. AI questions stay supplemental.</h2>
              <p className="panel-copy">
                The practice library now loads from the backend, keeps NEET PG PYQs as the core bank, and labels
                Gemini-generated MCQs separately so they never look like official exam material.
              </p>
            </div>
            <div className="practice-upgrade-actions">
              <span className="rank-pill source-official">Official PYQ bank</span>
              <span className="rank-pill source-ai">Supplemental AI</span>
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

          <article className="card panel">
            <p className="panel-copy">Loading the NEET PG question bank...</p>
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

    if (practiceStage === "subject" && (!currentPracticeSubject || !currentPracticeQuestion)) {
      return (
        <section className="app-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>{selectedPracticeMode === "ai" ? "AI practice is not ready yet" : "No questions found"}</h2>
            </div>
            <button className="button button-secondary" onClick={handleBackToPracticeDirectory}>
              Back to subjects
            </button>
          </div>

          <article className="card panel">
            <h3>{selectedPracticeMode === "ai" ? "Generate a 20-question set first" : "No practice questions yet"}</h3>
            <p className="panel-copy">
              {selectedPracticeMode === "ai"
                ? "Open the subject again and choose AI Practice so MediComm can create the separate supplemental set."
                : "The PYQ database does not have questions for this subject yet."}
            </p>
          </article>
        </section>
      );
    }

    const totalQuestions = currentPracticeSubject.questions.length;

    if (practiceStage === "subject") {
      return (
        <section className="app-view practice-detail-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Practice</p>
              <h2>{currentPracticeSubject.title} {selectedPracticeMode === "ai" ? "AI practice" : "PYQ session"}</h2>
            </div>
            <button className="button button-secondary" onClick={handleBackToPracticeDirectory}>
              Back to subjects
            </button>
          </div>

          <article className="card quiz-card practice-focus-card">
            <div className="practice-focus-topbar">
              <span className="practice-year-tag">{activePracticeYear?.title ?? "Practice"}</span>
              <span className={`rank-pill ${selectedPracticeMode === "ai" ? "source-ai" : "source-official"}`}>
                {selectedPracticeMode === "ai" ? "Supplemental AI" : "Official PYQ"}
              </span>
              <span className="rank-pill">
                Question {practiceQuestionIndex + 1} of {totalQuestions}
              </span>
            </div>
            <div className="quiz-meta">
              <span>
                {selectedPracticeMode === "ai"
                  ? "Supplemental topic-wise practice"
                  : currentPracticeQuestion.examTitle ?? `${currentPracticeQuestion.year} PYQ`}
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
                    src={imageUrl}
                    alt={`Question ${currentPracticeQuestion.questionNumber} visual ${index + 1}`}
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
                  >
                    {option}
                  </button>
                );
              })}
            </div>

            <div className="quiz-actions">
              <button className="button button-primary" onClick={handleSubmitAnswer} disabled={!selectedOption}>
                Check answer
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
                <p>{currentPracticeQuestion.explanation || "Answer saved in the NEET PG question bank."}</p>
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
                  <p>Choose how you want to practice this subject.</p>
                </div>
              </div>
              <div className="practice-choice-grid">
                <button className="practice-choice-card" type="button" onClick={() => startPracticeSession(practiceChoiceSubject.id, "pyq")}>
                  <span className="practice-choice-icon">PYQ</span>
                  <strong>PYQs</strong>
                  <p>Previous Year Questions</p>
                  <small>{practiceChoiceSubject.questions.length} official questions</small>
                </button>
                <button
                  className="practice-choice-card practice-choice-card-ai"
                  type="button"
                  disabled={aiPracticeBusy}
                  onClick={() => handleStartAiPractice(practiceChoiceSubject.id)}
                >
                  <span className="practice-choice-icon">AI</span>
                  <strong>AI Practice</strong>
                  <p>Supplemental topic-wise questions</p>
                  <small>
                    {aiPracticeBusy
                      ? "Generating 20..."
                      : `${Math.min(currentAiPracticeSubject?.questions?.length ?? 0, 20)} / 20 ready`}
                  </small>
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
                {year.subjects.map((subject) => (
                  <button
                    key={subject.id}
                    className="practice-subject-card"
                    onClick={() => handleSelectPracticeSubject(subject.id)}
                  >
                    <span className="practice-subject-label">{subject.title}</span>
                    <p className="practice-subject-copy">Choose PYQs or a separate 20-question AI practice set.</p>
                    <strong>{subject.questions.length} PYQs</strong>
                  </button>
                ))}
              </div>
            </section>
          ))}
        </div>
      </section>
    );
  }

  function renderLeaderboard() {
    return (
      <section className="app-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Leaderboard</p>
            <h2>Weekly rankings</h2>
          </div>
          <button className="button button-secondary" onClick={() => setActiveView("Compete")}>
            Join a challenge
          </button>
        </div>

        <div className="content-grid leaderboard-layout">
          <article className="card panel">
            <h3>National rankings</h3>
            <div className="leaderboard-list">
              {liveLeaderboard.length ? (
                liveLeaderboard.map((player) => (
                  <div
                    className={`leaderboard-row${player.isCurrentUser ? " leaderboard-self" : ""}`}
                    key={`${player.rank}-${player.name}`}
                  >
                    <div className="leaderboard-user">
                      <span className="rank-pill">#{player.rank}</span>
                      <div>
                        <strong>{player.isCurrentUser ? "You" : player.name}</strong>
                        <p>
                          {player.state} | {player.streak} day streak
                        </p>
                      </div>
                    </div>
                    <strong>{player.score} pts</strong>
                  </div>
                ))
              ) : (
                <div className="empty-community-state empty-community-state-compact">
                  <h3>No ranked learners yet</h3>
                  <p className="panel-copy">The leaderboard will fill from real signed-up users.</p>
                </div>
              )}
            </div>
          </article>

          <article className="card panel">
            <div className="panel-heading-split">
              <div>
                <h3>State-wise rankings</h3>
                <p className="panel-copy">Click a state to view players and colleges from account profiles.</p>
              </div>
            </div>

            <div className="state-search-block">
              <input
                className="state-search-input"
                type="text"
                placeholder="Search state, for example Rajasthan or Karnataka"
                value={stateSearchTerm}
                onChange={(event) => setStateSearchTerm(event.target.value)}
              />
              <p className="state-search-helper">
                {stateSearchTerm.trim()
                  ? filteredStateLeaderboard.length
                    ? `Showing state match for "${stateSearchTerm}". Refine further if needed.`
                    : "No state matched that search."
                  : "Type a state name to jump directly to its leaderboard."}
              </p>
            </div>

            {filteredStateLeaderboard.length ? (
              <div className="leaderboard-list">
                {filteredStateLeaderboard.map((entry) => (
                  <button
                    type="button"
                    key={entry.state}
                    className={`community-list-item${selectedStateEntry?.state === entry.state ? " community-list-item-active" : ""}`}
                    onClick={() => setSelectedLeaderboardState(entry.state)}
                  >
                    <div className="community-top">
                      <div className="icon-badge blue">ST</div>
                      <span>{entry.players.length} players</span>
                    </div>
                    <strong>{entry.state}</strong>
                    <p>Top score {entry.players[0]?.score ?? 0} pts</p>
                  </button>
                ))}
              </div>
            ) : null}

            {selectedStateEntry ? (
              <div className="state-detail-card">
                <div className="state-detail-header">
                  <div>
                    <strong>{selectedStateEntry.state}</strong>
                    <p>Players ranked by score with college pulled from account information</p>
                  </div>
                  <span className="rank-pill">{selectedStateEntry.players.length} players</span>
                </div>

                <div className="state-player-list">
                  {selectedStateEntry.players.map((player, index) => (
                    <div
                      className={`state-player-row${player.isCurrentUser ? " leaderboard-self" : ""}`}
                      key={`${selectedStateEntry.state}-${player.name}`}
                    >
                      <div className="state-player-main">
                        <span className="rank-pill">#{index + 1}</span>
                        <div>
                          <strong>{player.isCurrentUser ? "You" : player.name}</strong>
                          <p>{player.college}</p>
                        </div>
                      </div>
                      <div className="state-player-meta">
                        <strong>{player.score} pts</strong>
                        <span>{player.streak} day streak</span>
                      </div>
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
      return (
        <section className="app-view community-detail-view">
          <div className="view-header">
            <div>
              <p className="eyebrow">Communities</p>
              <h2>{selectedCommunity.name}</h2>
              <p className="panel-copy">A focused study room with live chat, members, and admin controls.</p>
            </div>
            <button className="button button-secondary" onClick={handleBackToCommunityHub}>
              Back to community hub
            </button>
          </div>

          {communitiesMessage ? <p className="form-message community-message-banner">{communitiesMessage}</p> : null}

          <article className="card panel community-chat-shell">
            <div className="community-chat-header">
              <div>
                <p className="eyebrow">Live study room</p>
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

            {selectedCommunity.isAdmin ? (
              <div className="community-invite-box">
                <span>Invite link</span>
                <code>{getCommunityInviteUrl(selectedCommunity.id)}</code>
              </div>
            ) : null}

            <div className="community-chat-meta">
              <span>Topic: {selectedCommunity.topic}</span>
              <span>Admin: {selectedCommunity.adminName}</span>
            </div>

            <div className="community-chat-body community-chat-shell-body">
              <div className="community-messages-panel">
                <div className="community-messages">
                  {selectedCommunity.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`community-message${message.isOwnMessage ? " community-message-own" : ""}`}
                    >
                      <div className="community-message-bubble">
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

                {selectedCommunity.isMember ? (
                  <form className="community-chat-form" onSubmit={handleSendCommunityMessage}>
                    <input
                      type="text"
                      value={communityMessageDraft}
                      onChange={(event) => setCommunityMessageDraft(event.target.value)}
                      placeholder="Write a message to the group..."
                    />
                    <button className="button button-primary" type="submit">
                      Send
                    </button>
                  </form>
                ) : (
                  <div className="feedback-box feedback-bad">
                    <strong>Join this group to take part in the chat.</strong>
                    <p>You can still preview the community, its members, and the discussion style before joining.</p>
                  </div>
                )}
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

    return (
      <section className="app-view community-hub-view">
        <div className="view-header">
          <div>
            <p className="eyebrow">Communities</p>
            <h2>Discover study groups and open focused chats</h2>
          </div>
          <button className="button button-secondary" onClick={fetchCommunities}>
            Refresh chats
          </button>
        </div>

        {communitiesMessage ? <p className="form-message community-message-banner">{communitiesMessage}</p> : null}
        {directMessagesMessage ? <p className="form-message community-message-banner">{directMessagesMessage}</p> : null}

        <article className="card panel community-overview-panel community-overview-top">
          <div className="panel-heading-split">
            <div>
              <h3>Community flow</h3>
              <p className="panel-copy">Move from study groups to personal chats without leaving the community section.</p>
            </div>
            <span className="community-info-pill">Organized hub</span>
          </div>
          <div className="community-overview-list community-overview-list-wide">
            <div className="community-overview-step">
              <strong>Create or browse</strong>
              <p>Find a focused study room by topic, year, or exam vibe.</p>
            </div>
            <div className="community-overview-step">
              <strong>Open the chat room</strong>
              <p>Enter a dedicated chat view instead of reading messages in a crowded dashboard.</p>
            </div>
            <div className="community-overview-step">
              <strong>Message and challenge</strong>
              <p>Search any learner, open a private thread, and send a direct 1v1 invite.</p>
            </div>
            <div className="community-overview-step">
              <strong>Moderate if you are admin</strong>
              <p>Keep the group useful by removing unwanted members directly from the room.</p>
            </div>
          </div>
        </article>

        <div className="community-hub-main">
          <article className="card panel community-create-panel">
            <div className="panel-heading-split">
              <div>
                <h3>Create a community</h3>
                <p className="panel-copy">
                  Start a clean WhatsApp-style study room. The creator becomes admin and can moderate members.
                </p>
              </div>
              <span className="community-info-pill">Admin controls included</span>
            </div>
            <form className="profile-form community-create-form" onSubmit={handleCreateCommunity}>
              <label className="field">
                <span>Community name</span>
                <input
                  type="text"
                  value={createCommunityForm.name}
                  onChange={(event) => updateCreateCommunityField("name", event.target.value)}
                  placeholder="Ex: Final Year Surgery Prep"
                />
              </label>
              <div className="community-create-row">
                <label className="field">
                  <span>Topic</span>
                  <input
                    type="text"
                    value={createCommunityForm.topic}
                    onChange={(event) => updateCreateCommunityField("topic", event.target.value)}
                    placeholder="Ex: Case discussions"
                  />
                </label>
                <label className="field">
                  <span>Description</span>
                  <input
                    type="text"
                    value={createCommunityForm.description}
                    onChange={(event) => updateCreateCommunityField("description", event.target.value)}
                    placeholder="What should people expect in this community?"
                  />
                </label>
              </div>
              <button className="button button-primary" type="submit">
                Create community
              </button>
            </form>
          </article>

          <article className="card panel community-directory-panel community-dm-panel">
          <div className="panel-heading-split">
            <div>
              <h3>Private messages</h3>
              <p className="panel-copy">Search for any user, open a direct thread, and challenge them to a duel.</p>
            </div>
            <span className="rank-pill">{directConversations.length} chats</span>
          </div>

          <div className="community-chat-body community-chat-shell-body">
            <div className="community-messages-panel">
              <label className="field">
                <span>Search users</span>
                <input
                  type="text"
                  value={directSearchTerm}
                  onChange={(event) => setDirectSearchTerm(event.target.value)}
                  placeholder="Search by name, college, or state"
                />
              </label>
              {directSearchBusy ? <p className="panel-copy">Searching learners...</p> : null}
              {directSearchTerm.trim().length > 0 && directSearchTerm.trim().length < 2 ? (
                <p className="panel-copy">Type at least 2 characters to search.</p>
              ) : null}
              <div className="community-member-list">
                {directSearchResults.map((result) => (
                  <div className="community-member-row" key={result.id}>
                    <button type="button" className="community-member-trigger" onClick={() => handleOpenDirectChat(result.id)}>
                      <div className="community-member-main">
                        <div className="avatar community-member-avatar">
                          {result.profileImageUrl ? (
                            <img className="avatar-image" src={result.profileImageUrl} alt={`${result.name} profile`} />
                          ) : (
                            <span>{getInitials(result.name)}</span>
                          )}
                        </div>
                        <div>
                          <strong>{result.name}</strong>
                          <p>{result.medicalCollege}</p>
                        </div>
                      </div>
                    </button>
                    <button className="button button-secondary community-remove-button" onClick={() => handleOpenDirectChat(result.id)}>
                      Message
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <aside className="community-members-panel community-sidecard">
              <div className="panel-heading-split">
                <div>
                  <h4>Inbox</h4>
                </div>
                <span className="rank-pill">{directConversations.length}</span>
              </div>
              {directMessagesBusy ? <p className="panel-copy">Loading messages...</p> : null}
              <div className="community-member-list">
                {directConversations.length ? (
                  directConversations.map((conversation) => (
                    <button
                      type="button"
                      key={conversation.id}
                      className={`community-list-item community-inbox-item${selectedDirectConversation?.id === conversation.id ? " community-list-item-active" : ""}`}
                      onClick={() => openDirectConversation(conversation.id)}
                    >
                      <div className="community-top">
                        <div className="icon-badge cyan">DM</div>
                        <span>{conversation.messages.length} messages</span>
                      </div>
                      <strong>{conversation.otherParticipant?.name ?? "Private chat"}</strong>
                      <p>{conversation.messages.at(-1)?.text ?? "No messages yet."}</p>
                    </button>
                  ))
                ) : (
                  <div className="empty-community-state empty-community-state-compact">
                    <h3>No private chats yet</h3>
                    <p className="panel-copy">Search for a user to start your first direct conversation.</p>
                  </div>
                )}
              </div>
            </aside>
          </div>
          </article>
        </div>

        <article className="card panel community-directory-panel">
          <div className="panel-heading-split">
            <div>
              <h3>Available groups</h3>
              <p className="panel-copy">Open a community card to see its dedicated chat room and member space.</p>
            </div>
            <span className="rank-pill">{communities.length} groups</span>
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
                    <div className="icon-badge green">HUB</div>
                    <span>{community.memberCount} members</span>
                  </div>
                  <strong>{community.name}</strong>
                  <p>{community.description}</p>
                  <div className="community-list-meta">
                    <span>Admin: {community.adminName}</span>
                    <span>{community.topic}</span>
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
                    <button className="button button-secondary" onClick={() => openCommunityChat(community.id)}>
                      Open room
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
              {duelResult?.verdict === "win"
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

  function renderView() {
    switch (activeView) {
      case "Dashboard":
        return renderDashboard();
      case "Practice":
        return renderPractice();
      case "Leaderboard":
        return renderLeaderboard();
      case "Communities":
        return renderCommunities();
      case "Compete":
        return renderCompete();
      case "Profile":
        return renderProfile();
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

  if (authStatus !== "authenticated") {
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
    >
      {renderView()}
    </AppShell>
  );
}

export default App;
