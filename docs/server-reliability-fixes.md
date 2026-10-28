# Server reliability fix tally — 28 October 2026

Implemented in the workspace; these changes have not been deployed to production.

| # | Issue | Change | Status |
|---|---|---|---|
| 1 | A shared proxy/campus IP exhausted 20 authentication requests in 15 minutes | Separate broad IP allowance (600/15 minutes) and normalized, hashed account allowances (30 login/signup attempts; 10 recovery attempts per 15 minutes). Existing recovery-specific safeguards remain. | Implemented |
| 2 | Other authenticated API traffic shared an IP budget | Separate per-account general and exam budgets; unauthenticated traffic retains an IP budget. Forwarded headers remain untrusted by default. | Implemented |
| 3 | Concurrent logins saved stale shared snapshots | Account/token updates read fresh state inside the commit queue. Legacy password verification occurs outside that queue; credentials are rechecked before session issuance. | Implemented |
| 4 | Question navigation wrote to the database | Navigation stays in the tab backup and is piggybacked on the next answer batch. Navigation alone sends no requests. | Implemented |
| 5 | Rapid answer/review changes created excessive writes | Coalesce changes over 300 ms and save batches of at most 150 changes, validated atomically with one revision increment. | Implemented |
| 6 | A timed-out save could freeze submission or be retried ambiguously | Stable mutation IDs make the latest batch idempotent. Read server state after an uncertain save before retrying; preserve genuine other-tab conflicts. A timed-out submission is checked against server state. | Implemented |
| 7 | Reloading discarded pending answers | Store pending changes, save ID, revision, part and navigation in sessionStorage per attempt. Restore/reconcile on reload. Keep retries blocked on real cross-tab conflicts rather than overwriting newer work. | Implemented |
| 8 | Large snapshots and compression delayed unrelated requests | Small account snapshots for session/access checks and user summaries; skip live-stream snapshot creation when nobody is connected; asynchronous Firebase gzip/gunzip. | Implemented |
| 9 | PM2 cluster workers held independent application snapshots | Nimbus defaults to one fork worker until shared storage supports multiple writers. Participant storage remains independent. | Implemented |
| 10 | Insufficient incident evidence | Request logs include path without query string, status, duration and request ID; aborted requests logged separately; production logs CPU, memory and event-loop delay every 30 seconds. | Implemented |
| 11 | Burst password verification exceeded the generic browser deadline | Login/signup/Google requests allow 30 seconds; exam requests retain their explicit 20-second deadline and recovery logic. Password hashing strength is unchanged. | Implemented |
| 12 | Windows delete-pending lock files caused intermittent concurrent-test failures | Bounded wait for Windows lock-open EPERM/EACCES/EBUSY; never steal live locks. | Implemented |

## Verification

- Backend suite: `node --test --test-concurrency=2 server` — 232 passed, zero failures.
- Tests cover batch validation/idempotency, uncertain commit recovery, reload restoration, cross-tab conflicts, navigation without writes, 100 shared-IP accounts and 100 concurrent queued session updates.
- Updated the HTTP rate-limit regression to the new policy. Corrected two existing VM test extraction boundaries so they no longer accidentally execute notepad startup code.
- Frontend production build verified in a separate output directory; existing large-chunk warning remains.
- Local HTTP load check: `node scripts/load-grand-test.mjs`. Starts its own loopback server and synthetic temporary database; never connects to production. Tests 20, 50 and 100 simultaneous candidates through password login, start, six 50-answer batches, both submissions and the Part 2 transition. All 1,870 requests passed and all candidates saved 300 answers and completed.
- Raw results: `output/server-reliability-load.json`. Backend results: `output/server-reliability-tests.tap`.

| Simultaneous candidates | Login p95 | Part 1 submit p95 | Final submit p95 | Request failures |
|---|---:|---:|---:|---:|
| 20 | 4,943 ms | 135 ms | 951 ms | 0 |
| 50 | 8,458 ms | 247 ms | 2,604 ms | 0 |
| 100 | 18,258 ms | 465 ms | 5,554 ms | 0 |

These are development-machine results with local filesystem storage, not a capacity guarantee for the 4-core server, Firebase or Supabase. Other development checks were running during part of the load check. They establish correctness under local HTTP concurrency and record latency for this run. This environment uses Node 20.17.0; production is configured for Node 22 and must be verified there.

## Rollout and remaining work

Deploy the updated backend and frontend together. Back up the existing application state and grand-test participant storage; no reset, reseed or schema migration is required for this patch. Old clients can continue sending individual answer changes. New clients require the updated backend to recognize answer batches.

Keep one application worker/replica. Existing PM2 deployments must be explicitly reloaded/reconfigured; changing nimbus.yaml alone does not stop existing cluster workers. Preserve the current persistent runtime directory. Do not enable TRUST_PROXY unless direct access is restricted and the actual proxy header chain has been verified.

Before the next live sitting, verify the deployed revision, proxy configuration, database region/latency and provider quotas, then exercise the same workload against staging on Node 22 with production-like historical data. Watch request paths, 429/409/5xx rates, aborted requests, process_metrics and database timings. The local harness deliberately does not generate production traffic.

The wider application still stores accounts/sessions and several features in a shared snapshot. This patch removes avoidable reads and stale concurrent account mutations; it does not migrate the whole application into independent records. That migration and durable workers for long AI jobs remain separate staging-backed work before enabling multiple application instances or claiming higher production capacity.

Tab backup survives reloads, not closing the tab or clearing browser storage. If browser storage is unavailable, the UI warns to keep the tab open until saves are confirmed. Server deadlines remain authoritative; pending answers arriving after expiry cannot be accepted.
