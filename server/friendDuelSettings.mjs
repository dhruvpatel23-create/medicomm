export const FRIEND_DUEL_COUNTS = [5, 10, 15];

export function duelSubjectCatalog(pool) {
  const subjects = new Map();
  for (const question of pool) {
    if (!question.subjectId) continue;
    const subject = subjects.get(question.subjectId) ?? {
      id: question.subjectId, title: question.subjectTitle || question.subjectId, questionCount: 0,
    };
    subject.questionCount++;
    subjects.set(subject.id, subject);
  }
  return [...subjects.values()].sort((a, b) => a.title.localeCompare(b.title));
}

export function validateFriendDuelSettings(payload, pool) {
  const questionCount = payload.questionCount ?? 5;
  if (!FRIEND_DUEL_COUNTS.includes(questionCount)) throw new Error('Choose 5, 10, or 15 questions.');
  const subjectIds = payload.subjectIds ?? null; // null means all eligible subjects.
  if (subjectIds !== null && (!Array.isArray(subjectIds) || !subjectIds.length ||
      subjectIds.some(id => typeof id !== 'string'))) throw new Error('Select at least one subject or All subjects.');
  const catalog = duelSubjectCatalog(pool);
  if (subjectIds?.some(id => !catalog.some(subject => subject.id === id))) throw new Error('Choose valid subjects.');
  const selected = subjectIds === null ? null : [...new Set(subjectIds)];
  if (pool.filter(q => selected === null || selected.includes(q.subjectId)).length < questionCount) {
    throw new Error('Not enough questions in these subjects. Select more subjects or fewer questions.');
  }
  return { questionCount, subjectIds: selected };
}
