# Practice first attempts

The earliest committed `practiceResults` entry for a user and question ID controls the first-attempt marker across practice modes. Retries never replace it. Existing saved history participates in this lookup; browser-only history is not authoritative. Historical attempts are not awarded retrospective rating points.

For a new question, the server grades the submitted option against the question bank. A correct first submission adds exactly 1 to the current rating. Wrong submissions and later submissions add 0. The attempt, its `ratingDelta`, and the user rating are committed in the same state-store write. Attempt IDs make delivery retries idempotent. Concurrent state changes return a conflict instead of overwriting a committed result; the client retries its pending queue with the same IDs.

`GET /api/practice/progress` requires authentication and returns only the signed-in user's first results. The client displays checkmarks only for confirmed first-attempt successes and refreshes on login, focus, reconnect, and periodically. Pending attempts are retained in browser storage until acknowledged. Across devices, first means first committed by the server, not a client-supplied timestamp.

Keep `practiceResults` when migrating or restoring the database: it is the durable source of first-attempt history. The existing Supabase revision check and local atomic replacement protect the combined state write. Run `node --test server/dashboard.test.mjs server/practice-trial.test.mjs server/security.test.mjs` to verify grading, historical wrong answers, restarts, duplicate deliveries, concurrent writes, and lost commit responses.


`GET /api/practice/live` is an authenticated SSE stream. Each successful database commit publishes the latest account rating and first-attempt progress to connected sessions. Failed writes publish nothing. Connections receive an initial snapshot, recheck session validity on updates and heartbeats, and close on logout/revocation or backpressure. EventSource reconnects automatically; the ordinary progress fetch remains a fallback and also refreshes the rating. The question navigator and question header show an explicit ?1st attempt? label; a newly awarded answer shows ?+1 Elo earned?.

Live fan-out uses the existing single-server deployment. Horizontal scaling requires a shared commit notification channel and refreshed database snapshots in each instance. Test live delivery and isolation with `node --test server/practiceLive.test.mjs`; `scripts/check_first_attempt_ui.cjs` uses an isolated backend and two browser tabs to exercise the full flow.
