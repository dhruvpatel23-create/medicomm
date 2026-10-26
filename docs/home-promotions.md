# Home page promotions

Edit `HOME_PROMOTION` in `server/promotions.mjs` to update the home banner's title, description, eyebrow, start time, or visibility. Deploy/restart the server after editing. Set `enabled: false` to hide the banner. Always give a new event a new `id`; previous registrations retain their original event ID and date. Dates include an explicit UTC offset; the current event is 27 October 2026, 2:00 p.m. IST (`Asia/Kolkata`). Registration closes at that start time.

Signed-in learners register using their existing account, without a separate form or a plan requirement. Guests are sent to sign-in. The server derives personal details from the authenticated session and stores one registration per account and event in `promotionRegistrations` in the existing app database state. This persists through the configured Firebase, Supabase, or local database adapter. Database revision checks and conflict retries prevent simultaneous requests from creating duplicates. No schema migration is required.

Each registration contains `promotionId`, `eventTitle`, `startsAt`, `userId`, `name`, `email`, `contactNumber`, `medicalCollege`, `medicalState`, `medicalCountry`, `mbbsBatch`, and `registeredAt`. Inspect this collection in the backend state using the same authorized database access used for existing user records. The public API exposes only the event and the current user's registration status; it never lists personal details. An admin registration listing is not included.

`GET /api/promotions/current` supplies the active banner and session-specific registration status. `POST /api/promotions/:id/register` saves the registration, or acknowledges an existing registration without inserting another record. The dialog confirms only a successful server response.

New login, Google sign-in, verified signup, guest entry, and reopening the app land on Home. The Dashboard remains accessible in navigation.
