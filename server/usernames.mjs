import { HttpError } from './security.mjs';

export function cleanUsername(value) {
  return typeof value === 'string' ? value.normalize('NFKC').trim().replace(/\s+/gu, ' ') : '';
}

export function usernameKey(value) { return cleanUsername(value).toLowerCase(); }

export function validateUsername(value) {
  const name = cleanUsername(value);
  if (!name || name.length > 254 || /[\p{Cc}\p{Cf}]/u.test(name)) {
    return 'Enter a username of 1 to 254 characters without hidden control characters.';
  }
  return null;
}

export function requireAvailableUsername(users, value, ownId) {
  const invalid = validateUsername(value);
  if (invalid) throw new HttpError(400, invalid);
  const key = usernameKey(value);
  if (users.some(user => user.id !== ownId && usernameKey(user.username ?? user.name) === key)) {
    throw new HttpError(409, 'This username is already taken. Please choose another username.');
  }
}

// Reserve all existing names first so generated suffixes never take another
// member's original name. Array order breaks ties and makes reruns stable.
export function reconcileUsernames(database) {
  const users = database.users ?? [];
  const reserved = new Set(users.map(user => usernameKey(user.username ?? user.name)));
  const used = new Set();
  let changed = false;
  for (const user of users) {
    const original = user.username ?? user.name;
    const base = cleanUsername(original).replace(/[\p{Cc}\p{Cf}]/gu, '').slice(0, 254) || 'learner';
    let username = base;
    for (let suffix = 2; used.has(usernameKey(username)) || (username !== base && reserved.has(usernameKey(username))); suffix++) {
      const ending = `_${suffix}`;
      username = base.slice(0, 254 - ending.length) + ending;
    }
    used.add(usernameKey(username));
    reserved.add(usernameKey(username));
    if (user.username !== username || user.name !== username) {
      if (user.name !== username && !Object.hasOwn(user, 'previousName')) user.previousName = user.name;
      user.username = username;
      user.name = username;
      changed = true;
    }
  }
  return changed;
}

export function assertUniqueUsernames(database) {
  const used = new Set();
  for (const user of database.users ?? []) {
    const key = usernameKey(user.username ?? user.name);
    if (!key || used.has(key)) throw new HttpError(409, 'This username is already taken. Please choose another username.');
    used.add(key);
  }
}
