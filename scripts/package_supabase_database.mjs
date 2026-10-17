import { existsSync, readFileSync, writeFileSync, mkdirSync, cpSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

// Load env files if they exist
for (const envFile of [".env.local", ".env"]) {
  const envPath = path.join(rootDir, envFile);
  if (existsSync(envPath)) {
    try {
      process.loadEnvFile(envPath);
    } catch {
      // Ignore
    }
  }
}

const supabaseUrl = (process.env.SUPABASE_URL ?? "").replace(/\/$/, "");
const serviceKey =
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  process.env.SUPABASE_SECRET_KEY ||
  process.env.SUPABASE_SERVICE_KEY ||
  "";
const stateKey = process.env.SUPABASE_STATE_KEY ?? "medicomm";
const tableName = process.env.SUPABASE_STATE_TABLE ?? "app_state";

const stagingDir = path.join(rootDir, "temp_database_export_package");
const rawJsonDir = path.join(stagingDir, "raw_json");
const migrationsDir = path.join(stagingDir, "migrations");
const zipOutputFile = path.join(rootDir, "supabase_database_backup.zip");

async function run() {
  console.log("==========================================");
  console.log("  Medulla / Supabase Database Backup Tool ");
  console.log("==========================================");

  if (existsSync(stagingDir)) {
    rmSync(stagingDir, { recursive: true, force: true });
  }
  mkdirSync(stagingDir, { recursive: true });
  mkdirSync(rawJsonDir, { recursive: true });
  mkdirSync(migrationsDir, { recursive: true });

  let stateData = null;
  let stateRevision = 0;
  let dataSource = "local";

  // Check if live Supabase is configured
  if (supabaseUrl && serviceKey) {
    console.log(`Checking remote Supabase at ${supabaseUrl}...`);
    try {
      const headers = {
        apikey: serviceKey,
        Authorization: `Bearer ${serviceKey}`,
      };
      const url = `${supabaseUrl}/rest/v1/${encodeURIComponent(tableName)}?key=eq.${encodeURIComponent(stateKey)}&select=*`;
      const res = await fetch(url, { headers, signal: AbortSignal.timeout(10000) });
      if (res.ok) {
        const rows = await res.json();
        if (Array.isArray(rows) && rows.length > 0 && rows[0].data) {
          stateData = rows[0].data;
          stateRevision = rows[0].revision || 0;
          dataSource = "live Supabase REST API";
          console.log(`Successfully fetched latest live state from Supabase (Revision: ${stateRevision})`);
        }
      } else {
        console.warn(`Supabase returned HTTP ${res.status}. Falling back to local data.`);
      }
    } catch (err) {
      console.warn(`Could not connect to remote Supabase (${err.message}). Falling back to local data.`);
    }
  }

  // Fallback to local files
  const runtimeDbPath = path.join(rootDir, "runtime-data", "users.json");
  const fallbackDbPath = path.join(rootDir, "data", "users.json");

  if (!stateData) {
    if (existsSync(runtimeDbPath)) {
      console.log(`Using active runtime database: ${runtimeDbPath}`);
      stateData = JSON.parse(readFileSync(runtimeDbPath, "utf8"));
      dataSource = "runtime-data/users.json";
    } else if (existsSync(fallbackDbPath)) {
      console.log(`Using base database: ${fallbackDbPath}`);
      stateData = JSON.parse(readFileSync(fallbackDbPath, "utf8"));
      dataSource = "data/users.json";
    } else {
      throw new Error("No database file found in runtime-data/ or data/.");
    }
  }

  // 1. Write the active JSON state
  writeFileSync(path.join(rawJsonDir, "users.json"), JSON.stringify(stateData, null, 2), "utf8");

  // 2. Copy question bank and supplementary data files
  const dataFiles = [
    "practice-question-bank.json",
    "fmge-question-bank.json",
    "usmle-module-bank.json",
    "fmge-editorial-notes.json",
  ];

  for (const file of dataFiles) {
    const src = path.join(rootDir, "data", file);
    if (existsSync(src)) {
      cpSync(src, path.join(rawJsonDir, file));
      console.log(`Included data file: ${file}`);
    }
  }

  // 3. Copy migration files
  const migrationsSrcDir = path.join(rootDir, "supabase", "migrations");
  if (existsSync(migrationsSrcDir)) {
    cpSync(migrationsSrcDir, migrationsDir, { recursive: true });
    console.log("Included all Supabase SQL migrations.");
  }
  const rootSchema = path.join(rootDir, "scripts", "supabase-schema.sql");
  if (existsSync(rootSchema)) {
    cpSync(rootSchema, path.join(migrationsDir, "00_supabase_schema_base.sql"));
  }

  // 4. Generate the monolithic PostgreSQL Dump SQL
  console.log("Generating full PostgreSQL database dump script...");
  const jsonLiteral = JSON.stringify(stateData);

  const sqlDump = `-- =====================================================================
-- Medulla Supabase Full Database Dump & Schema Restore
-- Generated At: ${new Date().toISOString()}
-- Data Source: ${dataSource}
-- Application Key: ${stateKey}
-- Revision: ${stateRevision}
-- =====================================================================

BEGIN;

-- 1. Create table public.app_state
CREATE TABLE IF NOT EXISTS public.app_state (
  key text PRIMARY KEY,
  data jsonb NOT NULL DEFAULT '{}'::jsonb,
  revision bigint NOT NULL DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- Ensure revision column exists
ALTER TABLE public.app_state ADD COLUMN IF NOT EXISTS revision bigint NOT NULL DEFAULT 0;

-- Row Level Security
ALTER TABLE public.app_state ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "service role manages app state" ON public.app_state;
CREATE POLICY "service role manages app state"
  ON public.app_state
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- 2. Insert or Update the complete Application State
INSERT INTO public.app_state (key, data, revision, updated_at)
VALUES (
  '${stateKey}',
  $medulla_payload$${jsonLiteral}$medulla_payload$::jsonb,
  ${stateRevision},
  now()
)
ON CONFLICT (key) DO UPDATE
SET data = EXCLUDED.data,
    revision = EXCLUDED.revision,
    updated_at = EXCLUDED.updated_at;

-- 3. Storage bucket setup
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'storage' AND table_name = 'buckets') THEN
    INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
    VALUES ('medicomm-uploads', 'medicomm-uploads', false, 5242880,
            ARRAY['image/png','image/jpeg','image/webp','image/gif'])
    ON CONFLICT (id) DO NOTHING;
  END IF;
END $$;

-- 4. Paid Memberships Ledger Table
CREATE TABLE IF NOT EXISTS public.medicomm_paid_memberships (
  app_key text NOT NULL,
  order_id text NOT NULL,
  user_id text NOT NULL,
  payment_id text NOT NULL,
  plan_id text,
  amount_paise bigint,
  currency text,
  purchased_at timestamptz NOT NULL,
  expires_at timestamptz GENERATED ALWAYS AS
    (((purchased_at AT TIME ZONE 'Asia/Kolkata') + interval '1 year') AT TIME ZONE 'Asia/Kolkata') STORED,
  purchase_date_source text NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (app_key, order_id)
);

CREATE INDEX IF NOT EXISTS medicomm_paid_memberships_user_idx
  ON public.medicomm_paid_memberships (app_key, user_id, expires_at desc);

ALTER TABLE public.medicomm_paid_memberships ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.medicomm_paid_memberships FROM public, anon, authenticated, service_role;
GRANT SELECT, INSERT ON public.medicomm_paid_memberships TO service_role;

DROP POLICY IF EXISTS "server reads memberships" ON public.medicomm_paid_memberships;
CREATE POLICY "server reads memberships" ON public.medicomm_paid_memberships
  FOR SELECT TO service_role USING (true);

DROP POLICY IF EXISTS "server records memberships" ON public.medicomm_paid_memberships;
CREATE POLICY "server records memberships" ON public.medicomm_paid_memberships
  FOR INSERT TO service_role WITH CHECK (true);

-- 5. Membership preservation trigger function
CREATE OR REPLACE FUNCTION public.medicomm_preserve_memberships()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path = '' AS $$
DECLARE
  payment jsonb;
  learner jsonb;
  members jsonb := '[]'::jsonb;
  orders jsonb := '[]'::jsonb;
  term public.medicomm_paid_memberships%rowtype;
BEGIN
  FOR payment IN SELECT value FROM jsonb_array_elements(coalesce(new.data->'paymentOrders', '[]'::jsonb)) LOOP
    IF payment->>'status' = 'paid'
      AND nullif(payment->>'paymentId', '') IS NOT NULL
      AND nullif(payment->>'verifiedAt', '') IS NOT NULL
      AND nullif(payment->>'userId', '') IS NOT NULL
      AND nullif(payment->>'orderId', '') IS NOT NULL THEN
      INSERT INTO public.medicomm_paid_memberships
        (app_key, order_id, user_id, payment_id, plan_id, amount_paise, currency, purchased_at, purchase_date_source)
      VALUES (new.key, payment->>'orderId', payment->>'userId', payment->>'paymentId',
        payment->>'planId', (payment->>'amount')::bigint, payment->>'currency',
        coalesce(nullif(payment->>'purchasedAt', ''), payment->>'verifiedAt')::timestamptz,
        coalesce(nullif(payment->>'purchaseDateSource', ''), 'saved_verification'))
      ON CONFLICT (app_key, order_id) DO NOTHING;
      SELECT * INTO term FROM public.medicomm_paid_memberships
        WHERE app_key = new.key AND order_id = payment->>'orderId';
      IF found THEN
        payment := payment || jsonb_build_object('purchasedAt', term.purchased_at,
          'expiresAt', term.expires_at, 'purchaseDateSource', term.purchase_date_source);
      END IF;
    END IF;
    orders := orders || jsonb_build_array(payment);
  END LOOP;
  new.data := jsonb_set(new.data, '{paymentOrders}', orders);
  FOR learner IN SELECT value FROM jsonb_array_elements(coalesce(new.data->'users', '[]'::jsonb)) LOOP
    SELECT * INTO term FROM public.medicomm_paid_memberships
      WHERE app_key = new.key AND user_id = learner->>'id'
      ORDER BY expires_at desc, order_id LIMIT 1;
    IF found THEN
      learner := learner || jsonb_build_object(
        'subscriptionPurchasedAt', term.purchased_at,
        'subscriptionExpiresAt', term.expires_at,
        'subscriptionOrderId', term.order_id,
        'plan', term.plan_id);
    END IF;
    members := members || jsonb_build_array(learner);
  END LOOP;
  new.data := jsonb_set(new.data, '{users}', members);
  RETURN new;
END;
$$;

REVOKE ALL ON FUNCTION public.medicomm_preserve_memberships() FROM public, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.medicomm_preserve_memberships() TO service_role;

DROP TRIGGER IF EXISTS medicomm_preserve_memberships ON public.app_state;
CREATE TRIGGER medicomm_preserve_memberships BEFORE INSERT OR UPDATE OF data
  ON public.app_state FOR EACH ROW EXECUTE FUNCTION public.medicomm_preserve_memberships();

-- 6. Views for Reports, Reviews, and Member Directory
CREATE OR REPLACE VIEW public.medicomm_reviews
WITH (security_invoker = true) AS
SELECT
  state.key AS app_key,
  review.item->>'id' AS review_id,
  review.item->>'userId' AS user_id,
  coalesce(nullif(learner.item->>'name', ''), 'Medulla learner') AS name,
  (review.item->>'rating')::integer AS rating,
  review.item->>'comment' AS comment,
  (review.item->>'createdAt')::timestamptz AS created_at,
  (review.item->>'updatedAt')::timestamptz AS updated_at
FROM public.app_state AS state
CROSS JOIN LATERAL jsonb_array_elements(coalesce(state.data->'websiteReviews', '[]'::jsonb)) AS review(item)
LEFT JOIN LATERAL jsonb_array_elements(coalesce(state.data->'users', '[]'::jsonb)) AS learner(item)
  ON learner.item->>'id' = review.item->>'userId';

CREATE OR REPLACE VIEW public.medicomm_overview
WITH (security_invoker = true) AS
SELECT
  state.key AS app_key,
  state.updated_at AS last_saved_at,
  jsonb_array_length(coalesce(state.data->'users', '[]'::jsonb)) AS users,
  jsonb_array_length(coalesce(state.data->'websiteReviews', '[]'::jsonb)) AS reviews,
  jsonb_array_length(coalesce(state.data->'communities', '[]'::jsonb)) AS communities,
  jsonb_array_length(coalesce(state.data->'practiceResults', '[]'::jsonb)) AS practice_results,
  jsonb_array_length(coalesce(state.data->'duelResults', '[]'::jsonb)) AS duel_results,
  jsonb_array_length(coalesce(state.data->'vivaSessions', '[]'::jsonb)) AS viva_sessions,
  jsonb_array_length(coalesce(state.data->'clinicalCaseSessions', '[]'::jsonb)) AS clinical_case_sessions
FROM public.app_state AS state;

CREATE OR REPLACE VIEW public.medicomm_member_sessions WITH (security_invoker = true) AS
SELECT state.key AS app_key, session.value->>'userId' AS user_id,
  nullif(session.value->>'createdAt', '')::timestamptz AS logged_in_at,
  to_timestamp((session.value->>'expiresAt')::double precision / 1000) AS session_expires_at,
  to_timestamp((session.value->>'expiresAt')::double precision / 1000) > now() AS is_valid
FROM public.app_state state
CROSS JOIN LATERAL jsonb_each(coalesce(state.data->'sessions', '{}'::jsonb)) session
WHERE jsonb_typeof(session.value) = 'object' AND jsonb_typeof(session.value->'expiresAt') = 'number';

CREATE OR REPLACE VIEW public.medicomm_member_attempts WITH (security_invoker = true) AS
SELECT state.key AS app_key, item->>'id' AS attempt_id, item->>'userId' AS user_id,
  item->>'questionId' AS question_id, item->>'subjectId' AS subject_id,
  item->>'subject' AS subject, item->>'topic' AS topic, item->>'mode' AS mode,
  (item->>'correct')::boolean AS correct,
  coalesce((item->>'durationSeconds')::integer, 0) AS duration_seconds,
  (item->>'answeredAt')::timestamptz AS answered_at
FROM public.app_state state
CROSS JOIN LATERAL jsonb_array_elements(coalesce(state.data->'practiceResults', '[]'::jsonb)) item;

CREATE OR REPLACE VIEW public.medicomm_member_progress WITH (security_invoker = true) AS
SELECT app_key, user_id, subject_id, subject, topic, mode, count(*) AS attempts,
  count(*) filter (WHERE correct) AS correct_answers,
  round(100.0 * count(*) filter (WHERE correct) / nullif(count(*), 0), 1) AS accuracy_percent,
  sum(duration_seconds) AS study_seconds, max(answered_at) AS last_practised_at
FROM public.medicomm_member_attempts
GROUP BY app_key, user_id, subject_id, subject, topic, mode;

CREATE OR REPLACE VIEW public.medicomm_members WITH (security_invoker = true) AS
SELECT state.key AS app_key, learner->>'id' AS user_id, learner->>'name' AS name,
  learner->>'email' AS email, learner->>'contactNumber' AS contact_number,
  learner->>'medicalCollege' AS medical_college,
  nullif(learner->>'createdAt', '')::timestamptz AS joined_at,
  nullif(learner->>'lastLoginAt', '')::timestamptz AS last_login_at,
  coalesce(sessions.active_sessions, 0) AS active_sessions,
  coalesce(sessions.active_sessions, 0) > 0 AS is_logged_in,
  sessions.latest_session_expiry,
  coalesce(membership.plan_id, learner->>'plan', learner->>'subscription') AS plan,
  membership.purchased_at, membership.expires_at,
  CASE WHEN membership.expires_at > now() THEN 'active'
       WHEN membership.expires_at IS NOT NULL THEN 'expired'
       WHEN learner->>'hasPracticeAccess' = 'true' OR learner->>'isSubscribed' = 'true'
         OR nullif(learner->>'plan', '') IS NOT NULL OR nullif(learner->>'subscription', '') IS NOT NULL
         THEN 'purchase_date_required'
       ELSE 'free' END AS subscription_status,
  membership.purchase_date_source,
  coalesce((learner->>'attemptedQuestions')::bigint, 0) AS total_attempted,
  coalesce((learner->>'correctAnswers')::bigint, 0) AS total_correct,
  coalesce((learner->>'streak')::integer, 0) AS streak_days,
  learner->'studyGoal' AS study_goal,
  activity.last_practised_at
FROM public.app_state state
CROSS JOIN LATERAL jsonb_array_elements(coalesce(state.data->'users', '[]'::jsonb)) learner
LEFT JOIN LATERAL (
  SELECT count(*) filter (WHERE is_valid) AS active_sessions,
    max(session_expires_at) filter (WHERE is_valid) AS latest_session_expiry
  FROM public.medicomm_member_sessions s WHERE s.app_key = state.key AND s.user_id = learner->>'id'
) sessions ON true
LEFT JOIN LATERAL (
  SELECT * FROM public.medicomm_paid_memberships m
  WHERE m.app_key = state.key AND m.user_id = learner->>'id'
  ORDER BY expires_at desc, order_id LIMIT 1
) membership ON true
LEFT JOIN LATERAL (
  SELECT max(answered_at) AS last_practised_at FROM public.medicomm_member_attempts a
  WHERE a.app_key = state.key AND a.user_id = learner->>'id'
) activity ON true;

REVOKE ALL ON public.medicomm_reviews, public.medicomm_overview, public.medicomm_members,
  public.medicomm_member_sessions, public.medicomm_member_attempts, public.medicomm_member_progress
  FROM public, anon, authenticated;

GRANT SELECT ON public.medicomm_reviews, public.medicomm_overview, public.medicomm_members,
  public.medicomm_member_sessions, public.medicomm_member_attempts, public.medicomm_member_progress
  TO service_role;

COMMIT;
`;

  writeFileSync(path.join(stagingDir, "medulla_supabase_full_dump.sql"), sqlDump, "utf8");

  // 5. Add README_RESTORE.md with instructions
  const readmeContent = `# Medulla / Supabase Database Backup Package

This backup contains the complete data and schema of the Medulla application.

## Contents of this Archive

1. \`medulla_supabase_full_dump.sql\`:
   - Single-file monolithic SQL script.
   - Creates the tables (\`public.app_state\`, \`public.medicomm_paid_memberships\`).
   - Inserts the complete JSONB app state (users, sessions, reviews, duels, question progress).
   - Configures storage buckets, triggers, and all analytics/owner views.

2. \`raw_json/\`:
   - \`users.json\`: The raw application database JSON snapshot.
   - \`practice-question-bank.json\`: Full clinical practice questions.
   - \`fmge-question-bank.json\`: FMGE questions database.
   - \`usmle-module-bank.json\`: USMLE module bank.
   - \`fmge-editorial-notes.json\`: FMGE notes.

3. \`migrations/\`:
   - Individual migration scripts for incremental application.

---

## How to Restore on Your Server

### Option A: Restore to any PostgreSQL Database (Self-hosted or Cloud)
Run via \`psql\` terminal command:
\`\`\`bash
psql "postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>" -f medulla_supabase_full_dump.sql
\`\`\`

### Option B: Restore to another Supabase Project
1. Open the Supabase Dashboard $\\rightarrow$ **SQL Editor**.
2. Click **New Query**.
3. Copy and paste the contents of \`medulla_supabase_full_dump.sql\` (or open the file).
4. Click **Run**.

### Option C: Restore for Medulla Local Server
If running the Medulla node.js server directly without PostgreSQL:
1. Place \`raw_json/users.json\` into \`runtime-data/users.json\` (or \`data/users.json\`).
2. Start the server:
   \`\`\`bash
   npm run start
   \`\`\`
`;

  writeFileSync(path.join(stagingDir, "README_RESTORE.md"), readmeContent, "utf8");

  // 6. Create the ZIP archive using PowerShell Compress-Archive
  console.log("Compressing package into zipfile...");
  if (existsSync(zipOutputFile)) {
    rmSync(zipOutputFile, { force: true });
  }

  const psCommand = `Compress-Archive -Path "${stagingDir}\\*" -DestinationPath "${zipOutputFile}" -Force`;
  execSync(`powershell -Command "${psCommand}"`, { stdio: "inherit" });

  // Clean up temporary staging dir
  rmSync(stagingDir, { recursive: true, force: true });

  console.log("\n==========================================");
  console.log("  BACKUP COMPLETED SUCCESSFULLY!");
  console.log(`  Archive: ${zipOutputFile}`);
  console.log("==========================================");
}

run().catch((err) => {
  console.error("Error creating backup:", err);
  process.exit(1);
});
