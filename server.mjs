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
const DEFAULT_USER_RATING = 1480;
const DEFAULT_USER_STREAK = 1;
const DEFAULT_CORRECT_ANSWERS = 0;
const DEFAULT_ATTEMPTED_QUESTIONS = 0;
const PASSWORD_HASH_ITERATIONS = 60000;
const LEGACY_PASSWORD_HASH_ITERATIONS = 120000;

ensureStorage();

const seedCommunities = [
  {
    id: "community-usmle-step-1",
    name: "USMLE Step 1",
    description: "High-yield foundational review, daily recall prompts, and exam strategy discussions.",
    topic: "Foundational review",
    adminUserId: null,
    memberIds: [],
    messages: [
      {
        id: "message-usmle-1",
        userId: null,
        userName: "MediComm Bot",
        text: "Welcome to the USMLE Step 1 group. Share mnemonics, doubts, and daily progress here.",
        createdAt: new Date().toISOString(),
      },
    ],
    createdAt: new Date().toISOString(),
  },
  {
    id: "community-emergency-medicine",
    name: "Emergency Medicine",
    description: "Rapid-fire acute care cases, trauma pearls, and emergency room learning threads.",
    topic: "Acute care",
    adminUserId: null,
    memberIds: [],
    messages: [
      {
        id: "message-emergency-1",
        userId: null,
        userName: "MediComm Bot",
        text: "Use this room like a focused WhatsApp study group for emergency medicine cases.",
        createdAt: new Date().toISOString(),
      },
    ],
    createdAt: new Date().toISOString(),
  },
  {
    id: "community-radiology-rounds",
    name: "Radiology Rounds",
    description: "Image-based practice, interpretation tips, and fast differential diagnosis discussions.",
    topic: "Image-based practice",
    adminUserId: null,
    memberIds: [],
    messages: [
      {
        id: "message-radiology-1",
        userId: null,
        userName: "MediComm Bot",
        text: "Drop image interpretation tips, pattern-recognition shortcuts, and tricky radiology cases here.",
        createdAt: new Date().toISOString(),
      },
    ],
    createdAt: new Date().toISOString(),
  },
];

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

function readDatabase() {
  const raw = readFileSync(databasePath, "utf8");
  const parsed = JSON.parse(raw);
  const communities = Array.isArray(parsed.communities) && parsed.communities.length ? parsed.communities : seedCommunities;
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
  };
}

function writeDatabase(data) {
  writeFileSync(databasePath, JSON.stringify(data, null, 2));
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

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
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
  if (database.users.some((user) => user.email.toLowerCase() === email)) {
    return sendJson(response, 409, { message: "An account with this email already exists." });
  }

  const { hash, salt, iterations } = hashPassword(String(payload.password));
  const user = {
    id: randomBytes(12).toString("hex"),
    name: String(payload.name).trim(),
    email,
    medicalCollege: String(payload.medicalCollege).trim(),
    contactNumber: String(payload.contactNumber).trim(),
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
  writeDatabase(database);

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
  writeDatabase(database);

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

function handleLogout(request, response) {
  const database = readDatabase();
  const token = getTokenFromRequest(request);

  if (token && database.sessions[token]) {
    delete database.sessions[token];
    writeDatabase(database);
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

  if (!name || !medicalCollege || !contactNumber) {
    return sendJson(response, 400, { message: "Name, medical college, and contact number are required." });
  }

  const userIndex = database.users.findIndex((user) => user.id === sessionUser.id);
  const updatedUser = {
    ...database.users[userIndex],
    name,
    medicalCollege,
    contactNumber,
  };

  if (payload.profileImageDataUrl) {
    updatedUser.profileImagePath = await saveProfileImage(
      updatedUser.id,
      payload.profileImageDataUrl,
      updatedUser.profileImagePath,
    );
  }

  database.users[userIndex] = updatedUser;
  writeDatabase(database);

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

  const nextRating = Number.isFinite(payload.rating)
    ? Math.max(0, Math.round(payload.rating))
    : database.users[userIndex].rating;
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
  writeDatabase(database);

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
    writeDatabase(database);
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
  writeDatabase(database);

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

function handlePracticeQuestionBank(response) {
  return sendJson(response, 200, readPracticeQuestionBank());
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
  writeDatabase(database);

  return sendJson(response, 201, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

function handleJoinCommunity(request, response, communityId) {
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
    writeDatabase(database);
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
  writeDatabase(database);

  return sendJson(response, 200, {
    community: sanitizeCommunity(community, database.users, currentUser.id),
  });
}

function handleRemoveCommunityMember(request, response, communityId, memberId) {
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
  writeDatabase(database);

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
    if (request.method === "GET" && url.pathname === "/api/practice") return handlePracticeQuestionBank(response);
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

createServer(handleRequest).listen(port, host, () => {
  console.log(`MediComm listening on http://${host}:${port}`);
});
