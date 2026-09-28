# Duel backend

`duels.mjs` owns deterministic option-index grading and match transitions. No model evaluates answers. Each match saves the exact questions, options, keys, explanations, starting ratings, deadline, locked answers and results. Raw conflicting keys and duplicate question IDs are excluded before selection. This validates key consistency, not the medical accuracy of the source bank.

Rated participants share a match and deadline. `/api/duels/answer` accepts only a participant's question ID and integer option index. Identical retries succeed; changing a locked answer fails. `/api/duels/complete` ignores client-supplied scores, answers, ratings and question lists. Both players settle together when both finish, either forfeits, or the deadline expires. Expiration is reconciled on status requests and queue activity. Equal scores draw. Bot progress is generated and stored by the server and cannot affect ratings.

Live payloads omit answer keys, explanations and opponent selections. Completed participant-only status returns the saved review. The browser remembers the last session per account and restores it on refresh, including locked answers and completed reviews. Finished matches are retained for seven days; waiting queue entries expire after five minutes. Existing matches from the previous implementation cannot be resumed.

Question selection caches a validated bank until its file changes and samples only the required questions. Unchanged status polling does not write storage. The UI polls serially every two seconds and retries connection errors without inventing a result. Mutating handlers parse request bodies before reading state, then perform all local mutations without yielding; answer locking, settlement and both users' statistics are committed in one write.

## Deployment boundary

The existing application repository stores the whole database in a JSON file, optionally mirrored as one Supabase document. It remains a **single-writer deployment**. This change does not make that storage safe for multiple Node processes or replicas; unrelated legacy handlers also use this shared persistence. There is no distributed transaction or load-test claim.

Before horizontal scaling, move matches, unique `(match_id, user_id, question_id)` answers, unique `(match_id, user_id)` results, queue membership and rating updates into database tables. Lock each match during settlement and commit both users' results and rating increments in one transaction. Use an indexed queue and an expiration worker. The isolated engine and its transition tests can remain unchanged behind that repository implementation.

## Verification

Run `npm run test:duels`. The engine and actual API-handler tests cover exact grading, review statuses, immutable submissions, deadlines, forfeits, duplicate completion, two-player ratings, bot isolation, authentication boundaries, forged completion data, simultaneous queue joins, slow request-body races and read-only polling. API tests use isolated in-memory persistence; they do not start the production server or touch user data. Build the frontend with Vite to verify JSX integration.
