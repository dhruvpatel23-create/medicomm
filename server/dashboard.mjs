const dayKey = value => new Date(new Date(value).getTime() + 330 * 60000).toISOString().slice(0, 10);
const dayBefore = (day, offset) => new Date(Date.parse(`${day}T00:00:00Z`) - offset * 86400000).toISOString().slice(0, 10);

export function dashboardData(database, user, region, now = Date.now()) {
  const today = dayKey(now);
  const attempts = (database.practiceResults ?? []).filter(item => item.userId === user.id && item.answeredAt).sort((a, b) => b.answeredAt.localeCompare(a.answeredAt));
  const battles = (database.duels ?? []).flatMap(match => match.results?.[user.id] ? [match.results[user.id]] : []).sort((a, b) => String(b.completedAt).localeCompare(String(a.completedAt)));
  const events = [...attempts, ...battles.flatMap(battle => (battle.review ?? []).filter(item => item.selectedIndex !== null).map(item => ({ answeredAt: battle.completedAt, correct: item.status === 'correct', durationSeconds: 0 })))].filter(item => Number.isFinite(Date.parse(item.answeredAt)));
  const counts = new Map();
  for (const event of events) {
    const day = dayKey(event.answeredAt);
    const entry = counts.get(day) ?? { attempts: 0, correct: 0, seconds: 0 };
    entry.attempts++; entry.correct += event.correct ? 1 : 0; entry.seconds += Number(event.durationSeconds) || 0;
    counts.set(day, entry);
  }
  let streak = 0;
  const start = counts.has(today) ? 0 : 1;
  while (counts.has(dayBefore(today, start + streak))) streak++;
  const activity = Array.from({ length: 56 }, (_, index) => {
    const date = dayBefore(today, 55 - index);
    return { date, ...(counts.get(date) ?? { attempts: 0, correct: 0, seconds: 0 }) };
  });
  const ranked = [...database.users].sort((a, b) => (b.rating ?? 1480) - (a.rating ?? 1480) || (b.streak ?? 0) - (a.streak ?? 0) || a.name.localeCompare(b.name));
  const state = region(user.medicalCollege);
  const topics = new Map();
  for (const attempt of attempts) {
    const key = `${attempt.mode}:${attempt.subjectId}:${attempt.topic}`;
    const topic = topics.get(key) ?? { subjectId: attempt.subjectId, subject: attempt.subject, mode: attempt.mode, questionId: attempt.questionId, year: attempt.year, topic: attempt.topic, attempts: 0, correct: 0 };
    topic.attempts++; topic.correct += attempt.correct ? 1 : 0; topics.set(key, topic);
  }
  const attempted = Math.max(0, user.attemptedQuestions ?? 0), correct = Math.max(0, Math.min(attempted, user.correctAnswers ?? 0));
  const recent = attempts[0];
  return {
    stats: { attempted, correct, accuracy: attempted ? Math.round(correct * 100 / attempted) : null, streak, rating: user.rating ?? 1480,
      nationalRank: ranked.findIndex(item => item.id === user.id) + 1, stateRank: ranked.filter(item => region(item.medicalCollege) === state).findIndex(item => item.id === user.id) + 1, state },
    today: counts.get(today) ?? { attempts: 0, correct: 0, seconds: 0 }, activity,
    weekly: activity.slice(-7),
    recommendations: [...topics.values()].filter(item => item.correct < item.attempts).map(item => ({ ...item, accuracy: Math.round(item.correct * 100 / item.attempts) })).sort((a, b) => a.accuracy - b.accuracy || b.attempts - a.attempts).slice(0, 3),
    recent: attempts.slice(0, 5).map(({ userId, selectedAnswer, ...item }) => item),
    resume: recent ? { subjectId: recent.subjectId, subject: recent.subject, mode: recent.mode, questionId: recent.questionId, year: recent.year, answeredAt: recent.answeredAt } : null,
    battles: battles.slice(0, 3).map(item => ({ id: item.duelId, mode: item.mode, verdict: item.verdict, userScore: item.userScore, opponentScore: item.opponentScore, ratingChange: item.delta, completedAt: item.completedAt })),
    goal: user.studyGoal ?? null, todayDate: today,
  };
}

export function validateStudyGoal(payload) {
  const exam = String(payload.exam ?? '').trim(), date = String(payload.date ?? '');
  const weeklyTarget = Number(payload.weeklyTarget);
  if (!exam || exam.length > 80 || !/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(Date.parse(date)) || new Date(date).toISOString().slice(0, 10) !== date
    || !Number.isInteger(weeklyTarget) || weeklyTarget < 1 || weeklyTarget > 5000) throw new Error('Enter an exam name, a valid exam date, and a weekly target from 1 to 5,000 questions.');
  return { exam, date, weeklyTarget };
}

export function recordPracticeAttempt(database, userId, payload, subject, question, now = Date.now()) {
  if (typeof payload.id !== 'string' || !/^[a-zA-Z0-9_-]{10,100}$/.test(payload.id)) throw new Error('Invalid attempt identifier.');
  const user = database.users.find(item => item.id === userId);
  const existing = (database.practiceResults ?? []).find(item => item.userId === userId && item.id === payload.id);
  if (existing) return { user, attempt: existing };
  if (!question || !subject || !question.options.includes(payload.selectedAnswer)) throw new Error('Choose an answer to a valid practice question.');
  const attempt = { id: payload.id, userId, questionId: question.id, subjectId: subject.id, subject: subject.title, mode: payload.mode,
    topic: question.chapterTitle || question.topic || 'General review', year: question.year, correct: payload.selectedAnswer === question.answer,
    selectedAnswer: payload.selectedAnswer, answeredAt: new Date(now).toISOString(), durationSeconds: Math.max(0, Math.min(1800, Math.round(Number(payload.durationSeconds) || 0))) };
  database.practiceResults = [...(database.practiceResults ?? []), attempt];
  user.attemptedQuestions = (user.attemptedQuestions ?? 0) + 1;
  user.correctAnswers = (user.correctAnswers ?? 0) + (attempt.correct ? 1 : 0);
  const today = dayKey(now);
  user.streak = user.lastPracticeDate === today ? (user.streak || 1) : user.lastPracticeDate === dayBefore(today, 1) ? (user.streak || 0) + 1 : 1;
  user.lastPracticeDate = today;
  return { user, attempt };
}
