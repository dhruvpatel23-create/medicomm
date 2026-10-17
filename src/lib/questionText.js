// Remove imported item labels, never ages, ranges, decimal values or numbered
// statement lists that are part of the question itself.
export function cleanQuestionPrompt(value) {
  const text = String(value ?? '');
  const match = text.match(/^\s*(?:Q(?:uestion)?\.?\s*)?(\d{1,3})[.)]\s+(?=[A-Za-z])/i);
  if (!match) return text;
  const remainder = text.slice(match[0].length);
  if (new RegExp(`(?:^|\\s)${Number(match[1]) + 1}[.)]\\s+[A-Za-z]`).test(remainder)) return text;
  return remainder;
}
