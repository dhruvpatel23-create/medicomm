# Scheduled FMGE grand test

The event in `data/fmge-practice-tests.json` opens its waiting room at
**27 October 2026, 13:00 Asia/Kolkata**, and releases questions at **14:00**.
These checks use server time on every waiting-room, start and attempt request.
There is no scheduled background job or browser-clock dependency.

`eventId` identifies this official sitting. It allows one attempt per account,
including after completion; start retries and multiple tabs return the same ID.
The existing format remains two independently timed 150-minute parts, with an
untimed break. Individual scores and answer reviews are available immediately on
completion. Ranks and the leaderboard are hidden by the API until **27 October
2026, 20:00 Asia/Kolkata**, and appear automatically on the result screen and the
grand-test listing. Grand Test 1 is free for every signed-in account, including
free, lower-plan and expired-plan members. The FMGE Tests directory is open to
these members; its Practice Tests tab and all practice-attempt API routes still
require an active Premium plan. The free grand test retains its opening times,
one-attempt rule, account ownership checks and rank publication time.

Ranking uses completed attempts only, highest score first. Equal scores share
competition ranks (1, 1, 3). No shared finishing time or entry cutoff has been set,
so the leaderboard continues updating with late completions after publication.
The backend shares ranking reads for up to 30 seconds per process; browsers refresh
automatically. Responses include the snapshot time. Scores and participant names
are never returned by the leaderboard endpoint before publication, including via
direct requests or a modified browser clock. Email addresses and internal account
IDs are not included in public ranking rows.

## Persistence

Grand-test participants are stored separately from the shared application state.
On Firebase, they use `medullaApps/{namespace}/massTestParticipants`, with a
transaction per participant. Immutable question snapshots are stored once through
`massTestQuestionSets` and the existing content-addressed blob store. The existing
Firestore rules deny direct browser access; all reads and writes go through Node.
Back up these collections and blobs with the application data.

Locally, participant records, lock files and immutable question snapshots live in
`RUNTIME_DATA_DIR/mass-tests/` (default `runtime-data/mass-tests/`). Writes use
participant-scoped locks and atomic renames. Preserve this directory across local
restarts and back it up with `users.json`. Local file storage requires a persistent
filesystem shared by any local workers; use Firebase for multiple deployment hosts.

The catalogue and waiting room never return questions or answer keys. Waiting-room
status requests do not write to the database, and browsers stagger their polling.
Test API rate limits apply per authenticated account so candidates sharing a public
IP do not consume one common test-request allowance. Authentication checks use
small session/account snapshots rather than cloning the question bank each time.

## Validation and deployment

Run `node server/fmge-tests.test.mjs`, `node server/stateStore.test.mjs`, and
`node server/firebase-email-auth.test.mjs`. Tests cover the exact opening boundaries,
direct endpoint bypasses, ownership, 100 simultaneous participant starts, duplicate
starts, stale revisions, completion, and recovery using a new local store instance.
This is a concurrency correctness check, not a production capacity benchmark.
The Firebase adapter uses Firestore transactions; local concurrency tests do not
measure deployed Firebase latency, quotas or host capacity.

Deploy the updated backend and frontend together before the waiting room opens.
The server clock must be synchronized. Copying frontend files alone does not apply
the API guards. Previous preview attempts for this test must be removed from the
deployment's own `fmgeTestAttempts` array; keep other tests' attempts and take a
backup first. Local cleanup does not delete anything in the live database.
