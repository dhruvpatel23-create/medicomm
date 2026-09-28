import { randomBytes } from 'node:crypto';

export function validDuelQuestion(q) {
  return Boolean(q?.id && q.prompt && Array.isArray(q.options) && q.options.length === 4 &&
    q.options.every(x => typeof x === 'string' && x.trim()) && new Set(q.options.map(x => x.trim())).size === 4 &&
    Number.isInteger(q.answerIndex) && q.answerIndex >= 0 && q.answerIndex < 4 &&
    (!q.answer || (typeof q.answer === 'string' && q.answer.trim() === q.options[q.answerIndex].trim())));
}

export function createMatch(id, playerIds, questions, ratings, now = Date.now(), type = 'rated') {
  if (!questions.length || questions.some(q => !validDuelQuestion(q)) || new Set(questions.map(q => q.id)).size !== questions.length) {
    throw new Error('No valid question set is available.');
  }
  return { id, type, status: 'matched', playerIds, ratings, questions: structuredClone(questions),
    createdAt: new Date(now).toISOString(), startedAt: new Date(now).toISOString(), expiresAt: now + 180000,
    answers: {}, finished: {}, forfeits: {}, results: {},
    botTimeline: type === 'bot' ? questions.map((q, i) => ({ at: now + (i + 1) * 24000,
      correct: randomBytes(1)[0] < 166 })) : [] };
}

export function lockAnswer(match, userId, questionId, optionIndex, now = Date.now()) {
  if (!match.playerIds.includes(userId)) throw new Error('You are not a participant in this match.');
  const question = match.questions.find(q => q.id === questionId);
  if (!question || !Number.isInteger(optionIndex) || optionIndex < 0 || optionIndex >= question.options.length) {
    throw new Error('Choose a valid option for a question in this match.');
  }
  const answers = match.answers[userId] ?? {};
  if (Object.hasOwn(answers, questionId)) {
    if (answers[questionId] !== optionIndex) throw new Error('This answer is already locked.');
    return; // An identical retry is safe, including after completion.
  }
  if (match.status !== 'matched' || match.finished[userId] || now >= match.expiresAt) throw new Error('This match no longer accepts answers.');
  answers[questionId] = optionIndex;
  match.answers[userId] = answers;
}

export function reviewMatch(match, userId) {
  return match.questions.map(q => {
    const selectedIndex = match.answers[userId]?.[q.id] ?? null;
    return { ...q, selectedIndex, correctIndex: q.answerIndex,
      status: selectedIndex === null ? 'unanswered' : selectedIndex === q.answerIndex ? 'correct' : 'incorrect' };
  });
}

// Called in the same synchronous mutation as answer/finish/status processing.
// Both players' results and rating changes are committed together, exactly once.
export function settleMatch(match, users, now = Date.now()) {
  if (match.status === 'completed') return false;
  if (now < match.expiresAt && !match.playerIds.every(id => match.finished[id]) &&
      !Object.values(match.forfeits).some(Boolean)) return false;
  const reviews = Object.fromEntries(match.playerIds.map(id => [id, reviewMatch(match, id)]));
  const scores = Object.fromEntries(match.playerIds.map(id => [id, reviews[id].filter(q => q.status === 'correct').length]));
  const botScore = match.botTimeline.filter(step => step.at <= now && step.correct).length;
  for (const id of match.playerIds) {
    const user = users.find(u => u.id === id);
    if (!user) throw new Error('Match participant is missing.');
    const opponentId = match.playerIds.find(other => other !== id);
    const opponentScore = opponentId ? scores[opponentId] : botScore;
    const verdict = match.forfeits[id] ? 'loss' : match.forfeits[opponentId] ? 'win' :
      scores[id] > opponentScore ? 'win' : scores[id] < opponentScore ? 'loss' : 'draw';
    const actual = verdict === 'win' ? 1 : verdict === 'loss' ? 0 : 0.5;
    const expected = 1 / (1 + 10 ** (((match.ratings[opponentId] ?? match.ratings[id]) - match.ratings[id]) / 400));
    const previousRating = user.rating ?? 1480;
    const delta = match.type === 'bot' ? 0 : Math.round(32 * (actual - expected));
    const attempted = reviews[id].filter(q => q.selectedIndex !== null).length;
    const nextRating = Math.max(0, previousRating + delta);
    match.results[id] = { duelId: match.id, mode: match.type, verdict, delta: nextRating - previousRating,
      previousRating, nextRating, userScore: scores[id], opponentScore, attemptedQuestions: attempted,
      correctAnswers: scores[id], ratingAffected: match.type === 'rated', forfeited: Boolean(match.forfeits[id]),
      completedAt: new Date(now).toISOString(), review: reviews[id] };
    user.rating = nextRating;
    user.correctAnswers = (user.correctAnswers ?? 0) + scores[id];
    user.attemptedQuestions = (user.attemptedQuestions ?? 0) + attempted;
  }
  match.status = 'completed';
  return true;
}

export function matchProgress(match, userId, now = Date.now()) {
  const opponentId = match.playerIds.find(id => id !== userId);
  return { status: match.status, expiresAt: match.expiresAt, serverNow: now,
    answers: match.answers[userId] ?? {}, finished: Boolean(match.finished[userId]),
    opponentAnswered: opponentId ? Object.keys(match.answers[opponentId] ?? {}).length : match.botTimeline.filter(s => s.at <= now).length,
    result: match.results[userId] ?? null };
}
