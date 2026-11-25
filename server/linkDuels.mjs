import { randomBytes } from 'node:crypto';
import { createMatch } from './duels.mjs';
import { duelSubjectCatalog, validateFriendDuelSettings } from './friendDuelSettings.mjs';
import { HttpError, sessionHash } from './security.mjs';
import { chargeTokens, requireTokens } from './tokens.mjs';

const ROOM_DURATION = 10 * 60_000;
const BATTLE_COST = 5;
const isToken = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);

export const challengeExpiry = room => room.expiresAt ?? (room.createdAtMs || Date.parse(room.createdAt)) + ROOM_DURATION;
export const linkDuelGuest = id => ({ id, name: 'Guest', guest: true });

export function getLinkDuelGuest(duel, key) {
  if (duel?.type !== 'link' || !isToken(key) || duel.guestKeyHash !== sessionHash(key)) return null;
  return linkDuelGuest(duel.guestId);
}

export function createLinkDuelHandlers({ readDatabase, transact, requireSessionUser, getSessionUser,
  parseRequestBody, sendJson, getQuestionPool, pickQuestions, expireDuels }) {
  async function create(request, response) {
    const host = requireSessionUser(request, response, readDatabase());
    if (!host) return;
    const payload = await parseRequestBody(request);
    const pool = getQuestionPool();
    let settings;
    try { settings = validateFriendDuelSettings(payload, pool); }
    catch (error) { throw new HttpError(400, error.message); }
    const subjectTitles = settings.subjectIds === null ? ['All subjects']
      : duelSubjectCatalog(pool).filter(subject => settings.subjectIds.includes(subject.id)).map(subject => subject.title);
    const invite = randomBytes(32).toString('hex');
    const result = await transact(database => {
      const now = Date.now();
      requireTokens(database, host.id, BATTLE_COST, now);
      database.challengeRooms = (database.challengeRooms ?? []).filter(room => challengeExpiry(room) > now);
      for (const room of database.challengeRooms) {
        if (room.kind === 'link' && room.challengerId === host.id && room.status === 'waiting') room.status = 'cancelled';
      }
      const room = {
        id: 'link-' + randomBytes(16).toString('hex'),
        kind: 'link',
        challengerId: host.id,
        inviteHash: sessionHash(invite),
        ...settings,
        subjectTitles,
        status: 'waiting',
        createdAt: new Date(now).toISOString(),
        createdAtMs: now,
        expiresAt: now + ROOM_DURATION,
      };
      database.challengeRooms.push(room);
      return { id: room.id, questionCount: room.questionCount, subjectTitles, expiresAt: room.expiresAt };
    });
    return sendJson(response, 201, { ...result, invite });
  }

  async function join(request, response) {
    const { invite, guestKey } = await parseRequestBody(request);
    if (!isToken(invite) || !isToken(guestKey) || invite === guestKey) {
      throw new HttpError(400, 'This challenge link is invalid.');
    }
    const inviteHash = sessionHash(invite);
    const guestKeyHash = sessionHash(guestKey);
    function findRoom(database) {
      const room = database.challengeRooms?.find(item => item.kind === 'link' && item.inviteHash === inviteHash);
      if (!room || challengeExpiry(room) <= Date.now()) throw new HttpError(410, 'This challenge link has expired. Ask your friend for a new link.');
      if (room.status === 'cancelled') throw new HttpError(410, 'The host cancelled this challenge.');
      if (getSessionUser(request, database)?.id === room.challengerId) {
        throw new HttpError(409, 'Share this link with your friend. Your host match is in the arena.');
      }
      if (room.status === 'matched') {
        const match = database.duels.find(duel => duel.id === room.duelId);
        if (match?.guestKeyHash !== guestKeyHash) throw new HttpError(409, 'A guest has already joined this challenge.');
      }
      return room;
    }
    const existing = findRoom(readDatabase());
    if (existing.status === 'matched') return sendJson(response, 200, { sessionId: existing.duelId });

    const sessionId = await transact(database => {
      const room = findRoom(database);
      if (room.status === 'matched') return room.duelId;
      const host = database.users.find(user => user.id === room.challengerId);
      if (!host) throw new HttpError(410, 'The host is no longer available.');
      expireDuels(database);
      if (database.duels.some(duel => duel.status === 'matched' && duel.playerIds.includes(host.id))) {
        throw new HttpError(409, 'The host is already playing a duel. Try again after it ends.');
      }
      const now = Date.now();
      const guestId = 'duel-guest-' + randomBytes(16).toString('hex');
      const match = createMatch('friend-' + randomBytes(16).toString('hex'), [host.id, guestId],
        pickQuestions(room.questionCount, room.subjectIds), { [host.id]: host.rating }, now, 'link');
      try { chargeTokens(database, host.id, BATTLE_COST, `battle:${match.id}`, now); }
      catch (error) {
        if (error.status === 402) throw new HttpError(402, 'The host needs 5 tokens to start the challenge.');
        throw error;
      }
      match.guestId = guestId;
      match.guestKeyHash = guestKeyHash;
      database.duels.push(match);
      database.duelQueue = database.duelQueue.filter(entry => entry.userId !== host.id);
      room.status = 'matched';
      room.duelId = match.id;
      room.expiresAt = match.expiresAt + ROOM_DURATION;
      return match.id;
    });
    return sendJson(response, 200, { sessionId });
  }

  async function cancel(request, response) {
    const host = requireSessionUser(request, response, readDatabase());
    if (!host) return;
    const { challengeId } = await parseRequestBody(request);
    await transact(database => {
      const room = database.challengeRooms?.find(item => item.kind === 'link' && item.id === challengeId && item.challengerId === host.id);
      if (!room) throw new HttpError(404, 'Challenge room not found.');
      if (room.status === 'matched') throw new HttpError(409, 'Your friend already joined. The match is starting.');
      room.status = 'cancelled';
    });
    return sendJson(response, 200, { success: true });
  }

  return { create, join, cancel };
}
