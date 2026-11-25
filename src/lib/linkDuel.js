const INVITE_PREFIX = "#duel-invite=";

export function readDuelInvite() {
  return window.location.hash.startsWith(INVITE_PREFIX) ? window.location.hash.slice(INVITE_PREFIX.length) : "";
}

export function duelInviteUrl(invite) {
  const url = new URL(window.location.pathname, window.location.origin);
  url.hash = INVITE_PREFIX + invite;
  return url.href;
}

export function guestKeyForInvite(invite) {
  const storageKey = `medicomm-duel-guest:${invite}`;
  const saved = sessionStorage.getItem(storageKey);
  if (saved) return saved;
  const key = Array.from(crypto.getRandomValues(new Uint8Array(32)), byte => byte.toString(16).padStart(2, "0")).join("");
  sessionStorage.setItem(storageKey, key);
  return key;
}

export function duelGuestHeaders(guestKey) {
  return guestKey ? { "X-Duel-Guest": guestKey } : {};
}
