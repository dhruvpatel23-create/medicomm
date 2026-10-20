// Shuffle a display copy; saved answers and the source bank keep their identity.
export function shuffleQuestionOptions(question, random = Math.random) {
  if (!question || !Array.isArray(question.options) || question.options.length < 2) return question;
  const indices = question.options.map((_, index) => index);
  for (let index = indices.length - 1; index > 0; index -= 1) {
    const target = Math.floor(random() * (index + 1));
    [indices[index], indices[target]] = [indices[target], indices[index]];
  }
  return {
    ...question,
    options: indices.map(index => question.options[index]),
    ...(Number.isInteger(question.answerIndex)
      ? { answerIndex: indices.indexOf(question.answerIndex) } : {}),
    ...(Array.isArray(question.optionExplanations)
      ? { optionExplanations: indices.map(index => question.optionExplanations[index]) } : {}),
  };
}
