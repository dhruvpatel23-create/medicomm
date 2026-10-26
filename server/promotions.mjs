import { HttpError } from './security.mjs';

// Change this campaign for the next promotion. Use a NEW id for each event so
// existing registrations remain attached to the event the learner chose.
export const HOME_PROMOTION = {
  id: 'fmge-grand-test-2026-10-27',
  enabled: true,
  eyebrow: 'THE NEXT STEP IN YOUR FMGE PREP',
  title: 'FMGE Grand Test',
  description: 'Put your preparation into perspective. Register for the upcoming grand test and take your next step with confidence.',
  startsAt: '2026-10-27T14:00:00+05:30',
  timeZone: 'Asia/Kolkata',
};

export function createPromotionsHandler({ readDatabase, writeDatabase, getSessionUser, sendJson, now = Date.now, promotion = HOME_PROMOTION }) {
  const headers = { 'Cache-Control': 'private, no-store' };
  const findRegistration = (database, user) => (database.promotionRegistrations ?? [])
    .find(row => row.promotionId === promotion.id && row.userId === user?.id);
  const status = (registration, clock) => ({
    promotion: promotion.enabled ? promotion : null,
    registered: Boolean(registration),
    registeredAt: registration?.registeredAt ?? null,
    registrationOpen: promotion.enabled && clock < Date.parse(promotion.startsAt),
  });

  return async function handlePromotions(request, response, url) {
    if (request.method === 'GET' && url.pathname === '/api/promotions/current') {
      const database = readDatabase();
      return sendJson(response, 200, status(findRegistration(database, getSessionUser(request, database)), now()), headers);
    }
    if (request.method !== 'POST' || url.pathname !== `/api/promotions/${promotion.id}/register`) {
      throw new HttpError(404, 'Promotion not found.');
    }
    // Optimistic database writes protect against concurrent requests on every
    // storage adapter. Retry conflicts using fresh state, never stale snapshots.
    for (let retry = 0; retry < 4; retry++) {
      const database = readDatabase();
      const user = getSessionUser(request, database);
      if (!user) throw new HttpError(401, 'Please sign in to register.');
      const clock = now();
      const existing = findRegistration(database, user);
      if (existing) return sendJson(response, 200, { ...status(existing, clock), alreadyRegistered: true, message: 'You are already registered for this test.' }, headers);
      if (!promotion.enabled || clock >= Date.parse(promotion.startsAt)) throw new HttpError(409, 'Registration for this event has closed.');
      const registration = {
        promotionId: promotion.id, eventTitle: promotion.title, startsAt: promotion.startsAt,
        userId: user.id, name: user.name, email: user.email,
        contactNumber: user.contactNumber ?? '', medicalCollege: user.medicalCollege ?? '',
        medicalState: user.medicalState ?? '', medicalCountry: user.medicalCountry ?? '',
        mbbsBatch: user.mbbsBatch ?? '', registeredAt: new Date(clock).toISOString(),
      };
      database.promotionRegistrations ??= [];
      database.promotionRegistrations.push(registration);
      try { await writeDatabase(database); }
      catch (error) {
        if (error.status === 409 && retry < 3) continue;
        throw error;
      }
      return sendJson(response, 201, { ...status(registration, clock), message: 'Thank you for registration!' }, headers);
    }
  };
}
