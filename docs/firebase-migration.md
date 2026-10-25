# Supabase → Firebase migration

The website keeps its existing Node.js authentication, password hashes, sessions,
Razorpay verification and feature permissions. This is a database migration, not a
switch to Firebase Authentication. No frontend Firebase private credentials exist.
Supabase remains selected until `DATABASE_PROVIDER=firebase` is explicitly set.

## Before the final migration

1. Back up the current server environment and Supabase database using your existing
   backup procedure. Do not publish environment files, service-account JSON, or the
   migration backup. The backup includes password hashes and session records.
2. Deploy this code with Supabase still selected. Run `npm ci` on the server.
3. Copy your Firebase credential JSON to a private path on the server, such as
   `/etc/medulla/firebase-admin.json`, readable only by the app's operating-system
   user (`chmod 600`). A Windows D: path will not work on the Linux server.
4. Add these to the server's private environment, retaining its existing Supabase,
   Razorpay, Gemini, email and origin settings:

   ```dotenv
   GOOGLE_APPLICATION_CREDENTIALS=/etc/medulla/firebase-admin.json
   FIREBASE_PROJECT_ID=medullaprep
   FIREBASE_NAMESPACE=medicomm
   DATABASE_PROVIDER=supabase
   UPLOAD_STORAGE=local
   RUNTIME_DATA_DIR=/var/lib/medulla
   ```

   `/var/lib/medulla` must be persistent, private, writable by the app user, and
   outside the public website directory. Migration copies private uploads there.
   Public question images and the bundled question banks remain in the deployment.
5. Run `npm run check:firebase`. It must report `firestoreReachable: true` and
   project `medullaprep`. `migrated: false` is expected before the import.
   The CLI reads `.env.local`, `.env`, and its process environment. If your server
   uses a different private env file, use Node's `--env-file` option, e.g.:

   ```sh
   node --env-file=/etc/medulla/server.env scripts/firebase-migration.mjs check
   ```

   PM2's stored environment does not automatically become your SSH shell's environment.
6. Keep Firestore rules server-only. `firestore.rules` denies browser clients;
   Admin SDK access uses Google IAM. `firestore.indexes.json` disables indexing
   large binary payloads. To publish these files using the Firebase CLI:

   ```sh
   npx firebase-tools deploy --only firestore --project medullaprep
   ```

   This publishes the repository's Firestore rules/index configuration. Use it on
   the dedicated Medulla project, not a project shared with unrelated client apps.

## Final copy and verification (maintenance window)

Stop **every** app process using the Supabase database, including any older `medulla`
PM2 cluster processes, the current `medullaprep` process, payment/email workers, and
any local dev server connected to production. Keep the source stopped until cutover
finishes. `--source-paused` is your acknowledgement that these writers are stopped;
the script cannot remotely prove that. Check `pm2 list`; don't assume restarting
only one process stops every writer. Do not stop unrelated services.

From the project directory, with source Supabase and destination Firebase credentials
available in the CLI environment:

```sh
node scripts/firebase-migration.mjs export --source-paused --dir tmp/firebase-final
node scripts/firebase-migration.mjs import --dir tmp/firebase-final
node scripts/firebase-migration.mjs verify --dir tmp/firebase-final
```

Run each command only after the previous succeeds. Add `node --env-file=...`
before the script path if required as above. Never use the repository's `data/users.json`
or a dev `runtime-data/users.json` as a replacement for the live source.

The export includes app state (accounts, subscriptions, progress, tests, messages,
sessions, etc.), the independent paid-membership ledger, notepad drafts/reviews,
legacy saved reviews, and every object in the configured private Supabase bucket.
Missing tables, inaccessible files, a changing source revision, or a corrupt backup
stop migration; no source records are deleted or updated. If a source table is
missing, check the existing Supabase migrations and configuration before proceeding.

The backup directory contains a SHA-256 manifest. Import is resumable from the
same verified directory; it never overwrites different destination records. Blob
uploads and notepad rows are staged first. The final app-state pointer is created
only after those imports verify. `verify` compares the complete app state, ledger,
each notepad row and each uploaded file; counts alone are not sufficient.

The final backup must be copied outside the deployment and retained securely.
It is needed to recover if the app host is lost while migration is in progress.

## Switch the server

Only after `verify` reports `verified: true`:

1. Change the server environment to `DATABASE_PROVIDER=firebase`.
2. Preserve the other Firebase/storage settings above and all application secrets.
3. Start **one** app server with the updated environment. For the existing PM2
   process use `pm2 restart medullaprep --update-env` after updating its environment
   correctly. Do not restart old Supabase writers.
4. Check `/health/ready`, then sign in with an existing account. Check its paid
   plan/expiry, practice history, a saved test, notepad and private images.
5. Test one new saved answer and refresh to confirm persistence.

Existing accounts retain their passwords. Existing sessions are copied, subject
to their normal expiry. The app's independent membership ledger survives accidental
loss of transient profile flags/payment copies.

## Storage and operating limits

Firebase data lives under `medullaApps/{namespace}`. Top-level application fields
are independently encoded as gzip-compressed, immutable 512 KiB binary chunks.
A transactional, revision-checked manifest makes all changed fields visible at
once, preserving this application's existing whole-state consistency contract.
Unchanged fields reuse their chunks. Large drawings and test snapshots therefore
do not hit Firestore's 1 MiB document limit. This compatibility adapter does not
turn the application into a per-record Firestore query engine; its existing single
logical writer/revision contention remains. Do not scale to competing app writers.

Chunks from old snapshots and interrupted imports are retained for recovery; no
automatic deletion/garbage collection runs. They consume storage and need a later
retention policy once rollback requirements are settled. Firebase reads, writes and
storage count against the project's quotas/billing. This migration does not enable
Blaze or change the billing plan.

Default private uploads stay on the VPS to avoid requiring Firebase Storage. Back
up `/var/lib/medulla/uploads` independently. For Firebase Storage instead, explicitly
set `UPLOAD_STORAGE=firebase` and `FIREBASE_STORAGE_BUCKET` before importing. A private
bucket and Firebase's applicable billing plan are required; do not switch upload
backends after import without transferring the files again.

## Rollback

Before any Firebase-only writes, the unchanged Supabase source is available for
rollback by restoring the previous provider/environment and starting the old
deployment. After users have written to Firebase, simply switching back would lose
those new changes: stop traffic, back up Firebase and reconcile them first. This
tool does not implement reverse migration. Do not delete Supabase or its backups
until the migration has been accepted.

Sources:
- https://firebase.google.com/docs/admin/setup
- https://firebase.google.com/docs/firestore/quotas
- https://firebase.google.com/docs/firestore/manage-data/transactions
- https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024
