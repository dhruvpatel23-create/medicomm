export const DEFAULT_DAILY_QUESTION_GOAL = 40;

export function dailyQuestionGoal(user) {
  const saved = user?.dailyQuestionGoal ?? user?.studyGoal?.dailyTarget;
  if (Number.isInteger(saved) && saved >= 1 && saved <= 5000) return saved;
  const weekly = user?.studyGoal?.weeklyTarget;
  if (Number.isInteger(weekly) && weekly >= 1 && weekly <= 5000) return Math.ceil(weekly / 7);
  return DEFAULT_DAILY_QUESTION_GOAL;
}
