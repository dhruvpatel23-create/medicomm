export const CUSTOM_TEST_SIZES = [10, 20, 30];

export function buildCustomModuleCatalog(subjects) {
  return subjects.map(subject => {
    const chapters = new Map();
    for (const question of subject.questions ?? []) {
      if (!question.id || !question.prompt || !Array.isArray(question.options) || question.options.length < 2) continue;
      const answerIndex = Number.isInteger(question.answerIndex) ? question.answerIndex : question.options.indexOf(question.answer);
      if (answerIndex < 0 || answerIndex >= question.options.length) continue;
      const title = question.chapterTitle?.trim() || 'General concepts';
      const chapter = chapters.get(title) ?? { key: JSON.stringify([subject.id, title]), title, order: Number.MAX_SAFE_INTEGER, questions: [] };
      if (Number.isFinite(question.chapterOrder)) chapter.order = Math.min(chapter.order, question.chapterOrder);
      chapter.questions.push({ ...question, answerIndex, subjectId: subject.id, subjectTitle: subject.title });
      chapters.set(title, chapter);
    }
    return { id: subject.id, title: subject.title, chapters: [...chapters.values()].sort((a, b) => a.order - b.order || a.title.localeCompare(b.title)) };
  });
}

export function customModulePool(catalog, selectedChapters) {
  const selected = new Set(selectedChapters);
  const questions = new Map();
  for (const subject of catalog) for (const chapter of subject.chapters) {
    if (selected.has(chapter.key)) for (const question of chapter.questions) questions.set(question.id, question);
  }
  return [...questions.values()];
}

export function sampleCustomModule(pool, count, random = Math.random) {
  const unique = [...new Map(pool.map(question => [question.id, question])).values()];
  if (!CUSTOM_TEST_SIZES.includes(count) || unique.length < count) throw new Error('Select more chapters to create this test.');
  for (let i = unique.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [unique[i], unique[j]] = [unique[j], unique[i]];
  }
  return unique.slice(0, count);
}

export function customModuleResult(session) {
  let correct = 0, incorrect = 0, skipped = 0;
  for (const question of session.questions) {
    const answer = session.answers[question.id];
    if (!Number.isInteger(answer)) skipped++;
    else if (answer === question.answerIndex) correct++;
    else incorrect++;
  }
  return { correct, incorrect, skipped, total: session.questions.length };
}

export function readCustomModuleSession(key) {
  try {
    const session = JSON.parse(sessionStorage.getItem(key) || 'null');
    if (!session || session.version !== 1 || !['active', 'complete'].includes(session.status)
      || !CUSTOM_TEST_SIZES.includes(session.questions?.length) || !Number.isFinite(session.startedAt)
      || !session.answers || !Array.isArray(session.flags) || !Number.isInteger(session.index)
      || session.index < 0 || session.index >= session.questions.length
      || (session.status === 'complete' && !Number.isFinite(session.finishedAt))) return null;
    if (session.questions.some(q => !q.id || !Array.isArray(q.options) || !Number.isInteger(q.answerIndex) || q.answerIndex < 0 || q.answerIndex >= q.options.length)) return null;
    return session;
  } catch { return null; }
}
