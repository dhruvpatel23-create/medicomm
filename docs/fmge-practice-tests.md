# FMGE practice tests

Three full-length tests live under Practice → FMGE Tests → Practice Tests. NEETPG and Grand Tests are unchanged placeholders.

## Blueprint and content

The blueprint is the user's `FMGE_Subject_Wise_Guide.pdf`, not an assertion about the latest official examination bulletin. Each test has 300 questions, two independently timed parts of 150 questions/150 minutes, +1 for correct answers, zero negative marking, and a 150/300 qualifying threshold. The supplied guide does not specify a break duration: practice attempts allow an untimed break, with Part 2 starting explicitly. Subject quotas apply to the entire test; they are not split into preclinical and clinical parts.

`data/fmge-practice-tests.json` is a private, versioned server-side snapshot. Do not copy it into public/ or dist/. `scripts/build_fmge_tests.py` reproduces it from the FMGE and official exam-recall practice banks. It does not generate new questions. The source banks remain untouched. Every selected question retains its source ID, examination, PDF and page provenance.

Screening excludes malformed choices, contradictory keys, editorial flags, filler/placeholder patterns, duplicate stems, incomplete visual questions and short/inadequate explanations. Full-length clinical stems are prioritized. The radiation-pneumonitis recall supplies its image finding explicitly in words, so its source illustration is not necessary. The Bragg peak recall is a deliberate exception to the generic minimum stem length: a short authentic exam item is not filler.

There are **898 distinct questions across 900 slots**. Two radiotherapy items recur in TEST3 because only 13 suitable radiotherapy records passed screening. No test repeats a question internally. This preserves the subject quota without inserting unrelated filler. `docs/fmge-practice-test-selection.json` records counts, exclusions and reuse. Screening is structural/source-based and includes known conflicting recall exclusions; it is not an independent clinical validation of every source answer.

## Server behavior

All endpoints use existing session cookies, origin protection and paid Practice access:

- `GET /api/practice/fmge-tests`: blueprint, tests and the current user's attempt summaries.
- `POST /api/practice/fmge-tests/:testId/start`: start or resume; `startKey` makes retries idempotent.
- `GET /api/practice/fmge-tests/attempts/:id`: refresh/resume; settles expired parts.
- `PATCH /api/practice/fmge-tests/attempts/:id`: save answer, clear answer, review flag or current position, with the current attempt revision.
- `POST .../attempts/:id/finish-part`: submit the specified part. A stale Part 1 retry cannot submit Part 2.
- `POST .../attempts/:id/next-part`: start Part 2 after the break; retries never reset the clock.

Attempts are persisted in `fmgeTestAttempts` using the existing local/Supabase state store and conflict retry rules. Each attempt snapshots the questions so later bank changes cannot alter an ongoing test or its review. Ownership is checked on every request. Unfinished responses never include answer keys, explanations or future-part questions. Only the server grades; submitted client scores are ignored. Flags do not prevent scoring. The UI waits for confirmed saves and offers explicit recovery when a save fails.

Browser refresh, exiting the view, and restarting the server preserve answers and the absolute deadline. Part 1 expiry locks the part and enters the break; Part 2 expiry completes grading on the next request. No separate timer worker is necessary. The application normalizer preserves the new state field on restart. No new external database table is required for the existing JSON app-state persistence model.

## Validation and deployment

Run `node --test server/fmge-tests.test.mjs` for quotas, ownership/access, persistence, duplicate requests, stale edits, expiry, two-part transitions, grade calculation and answer-key isolation.

Build the frontend to `.tmp/fmge-tests-build` with Vite (`copyPublicDir: false` is sufficient for this text-only check), then run `node scripts/check_fmge_tests_ui.cjs` with `PLAYWRIGHT_MODULE` pointing to an installed Playwright package if needed. It uses an isolated temporary paid account/database, a local preview and the actual API. It verifies save failure recovery, server restart/resume, part submission, results and mobile overflow. Screenshots go to `output/fmge-tests-ui/`.

Deploy the server module, private test snapshot, normalizer change and frontend together, then restart the server. Preserve existing runtime data. This work does not itself publish a deployment or change the production database.
