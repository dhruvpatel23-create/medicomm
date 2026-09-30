# Backend rollout: Render and Supabase

This change hardens the existing backend. It is **not yet a public-launch certification**. The remaining architecture work is listed below. Do not deploy this binary over the old one without the database and upload preparation.

## Implemented

- Production refuses missing database, origin and private upload-bucket configuration. Supabase errors never start a local fallback, and missing remote state is never auto-seeded.
- Writes use a revision condition in Postgres and publish the in-memory snapshot only after persistence succeeds. Overlapping stale mutations return 409 instead of silently losing data. An uncertain remote write triggers a reload; failed reload leaves the process unready. Restart after resolving an outage that leaves it unready.
- Password hashing runs asynchronously using PBKDF2-SHA512 with 220,000 iterations. Successful login upgrades older hashes. New passwords require 12–128 characters. Existing passwords remain valid.
- Sessions expire after seven days, are stored as hashes, are limited to five per account, and are revoked on logout. HttpOnly, SameSite cookies are Secure in production. Old indefinite sessions are intentionally invalidated; learners must sign in again. Browser storage holds only a UI marker.
- Explicit origin allowlist, cookie mutation origin checks, request limits (256 KB normally, 8 MB on image routes), HTTP timeouts, bounded in-process rate limits, per-user and process-wide AI limits.
- New uploads use a private Supabase bucket, with a 5 MB limit, MIME/signature checks and random filenames. The API checks authentication and community membership before serving attachments. Existing upload names also require authorization.
- Minimal liveness/readiness endpoints, request IDs and structured request logs, generic uncaught-error responses, and bounded shutdown. Clinical generation acknowledges only after the pending job is persisted.
- The seed command only inserts; it cannot replace an existing state row.

## Staging setup

1. Create a separate Supabase staging project. Take a verified production backup before migration work. Copy only appropriately sanitized data into staging.
2. Run `scripts/supabase-schema.sql` in the staging SQL editor. This adds `app_state.revision` and a private `medicomm-uploads` bucket without replacing existing state. If the bucket already exists, verify it is private and has the stated file/MIME limits.
3. For a new empty project only, explicitly initialize `app_state` using the insert-only seed script and a reviewed source file. Existing projects must retain their current row.
4. Inventory old uploaded files on the host where they exist using `node scripts/migrate-user-uploads.mjs`. With the correct target environment variables set, run again with `--apply` to upload referenced files. Resolve missing files before switching hosts. This does not alter names, delete local files or overwrite remote objects.
5. Set Render environment variables: `NODE_ENV=production`, `SUPABASE_URL`, `SUPABASE_SECRET_KEY`, and the server-side AI key. On Render, an unset `APP_ORIGINS` defaults to the platform-provided `RENDER_EXTERNAL_URL`, and an unset `SUPABASE_UPLOAD_BUCKET` defaults to `medicomm-uploads`. For custom domains, explicitly set `APP_ORIGINS` to the exact HTTPS origins (comma-separated, no trailing slash). Override `SUPABASE_UPLOAD_BUCKET` if using another private bucket. These defaults do not create the database revision column or upload bucket: complete steps 2–4 first. Never put secrets in Vite variables. Production ignores local `.env` files.
6. Use the paid Render service described by `render.yaml`, with `/health/ready` as its health check. Keep frontend and API on the same origin for this cookie deployment. Set `APP_ORIGINS` to the exact browser origin, without a trailing slash. Local Vite uses port 4173; include it in local overrides.
7. Keep **one API instance**. Do not connect development servers to the production database. Verify Render's actual forwarding behavior and restrict direct access before enabling `TRUST_PROXY=true`; until then, limits are conservative and shared by clients behind the same proxy address.
8. Run `npm run test:backend` and build the frontend. In staging, test signup, existing-account login, reload, logout, profile images, community membership/attachments, messages, practice, duels and all AI flows. Test database outage, restart, upload-store outage and simultaneous mutations. A 409 requires the user to refresh/retry; do not blindly retry costly operations.
9. Stop all old writers before deploying revision-aware code to production. Old binaries and direct SQL edits bypass application revision checks. Never roll back to a binary that ignores revisions while writes are active.

## Recovery and launch gates still outstanding

- **Relational migration:** app state remains one JSONB row. The revision guard prevents lost writes but does not remove the snapshot/memory bottleneck or make multiple instances supported. Move accounts, sessions, messages, matches, learning activity and jobs into indexed tables with constraints and transactional mutations. Test migration against a staging copy before cutover.
- **Account lifecycle:** custom auth remains. Email verification, password reset, account deletion and recovery are not implemented. Plan a Supabase Auth migration or complete these flows before public registration.
- **Background jobs and abuse controls:** clinical generation is still in-process; a restart can interrupt it. Add durable workers/idempotency, shared limits and enforce provider-side AI spending budgets. Current rate limits reset on restart. Add upload quotas, orphan cleanup, full image decoding/re-encoding and metadata stripping; signature validation is not a malware scan.
- **Operational proof:** configure uptime/error alerts, define recovery-time and recovery-point targets, verify Supabase backup retention for the actual plan, and separately back up Storage objects. Restore into an isolated project, verify counts and sampled records, then exercise account/message/upload flows. Record the restore duration and outcome before launch.
- **Data handling:** define retention and deletion behavior, document AI transfers, and obtain review appropriate to the learner data being collected.
- **Staging/load evidence:** local tests use isolated storage and mocks; they do not certify live Render, Supabase permissions, email delivery, provider behavior or capacity. Load-test realistic traffic and measure latency, memory and conflict rates.

Keep migration backups outside the app host with restricted access. Never commit user data exports or secrets. Recovery should restore both the database and its referenced files, with the API stopped until consistency has been checked.

References: [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [Supabase private buckets](https://supabase.com/docs/guides/storage/buckets/fundamentals), [Storage access control](https://supabase.com/docs/guides/storage/security/access-control).
