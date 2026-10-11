export function hasQuestionImage(question) {
  // Include explanation images, but not source references or planned asset targets.
  const images = [
    ...(Array.isArray(question.imageUrls) ? question.imageUrls : []),
    ...(Array.isArray(question.images) ? question.images : []),
    ...(Array.isArray(question.explanationImageUrls) ? question.explanationImageUrls : []),
    question.imageUrl,
    question.image,
  ].filter(value => value != null && String(value).trim());
  return images.length > 0;
}

export function filterPracticeLibraryForUi(library) {
  const hiddenQuestionIds = new Set();
  const finalYearSubjectIds = new Set((library.years ?? []).find(year => year.id === 'final-year')?.subjectIds ?? []);
  const filterSets = (sets, shouldFilter) => (sets ?? []).map(set => {
    if (!shouldFilter(set)) return set;
    const questions = (set.questions ?? []).filter(question => {
      if (!hasQuestionImage(question)) return true;
      hiddenQuestionIds.add(question.id);
      return false;
    });
    return { ...set, questions, questionCount: questions.length };
  });
  const subjects = filterSets(library.subjects, subject => subject.yearId === 'final-year' || finalYearSubjectIds.has(subject.id));
  const fmgeSessions = filterSets(library.fmgeSessions, () => true);
  return {
    ...library,
    subjects,
    fmgeSessions,
    exam: { ...library.exam, questionCount: subjects.reduce((sum, subject) => sum + subject.questions.length, 0) },
    hiddenQuestionIds,
  };
}
