export function cleanUsername(value) {
  return typeof value === 'string' ? value.normalize('NFKC').trim().replace(/\s+/gu, ' ') : '';
}

export function validateUsername(value) {
  const name = cleanUsername(value);
  if (typeof value !== 'string' || /[\p{Cc}\p{Cf}]/u.test(value)
      || [...name].length < 2 || [...name].length > 40) {
    return 'Enter a username of 2 to 40 characters without hidden control characters.';
  }
  if (!/^[\p{L}\p{M}\p{N} ._'’\-]+$/u.test(name)
      || (name.match(/\p{L}/gu) ?? []).length < 2) {
    return 'Use at least two letters. You can also use numbers, spaces, dots, underscores, apostrophes, and hyphens.';
  }
  const compact = name.toLowerCase().replace(/[ ._'’\-]/gu, '');
  const tokens = name.toLowerCase().match(/[a-z]+/g) ?? [];
  const keyboardRows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'abcdefghijklmnopqrstuvwxyz'];
  const keyboardMash = tokens.some(token => token.length >= 4 && keyboardRows.some(row =>
    row.includes(token) || [...row].reverse().join('').includes(token)));
  if (/(.)\1{3}/u.test(compact) || /^(.{2,3})\1{2,}$/u.test(compact)
      || keyboardMash || tokens.some(token => token.length >= 6 && !/[aeiouy]/.test(token))) {
    return 'Choose a readable name or handle instead of random letters, keyboard sequences, or repeated characters.';
  }
  return null;
}
