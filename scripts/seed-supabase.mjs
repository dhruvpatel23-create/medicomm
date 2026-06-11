import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const runtimeDatabasePath = path.join(rootDir, "runtime-data", "users.json");
const legacyDatabasePath = path.join(rootDir, "data", "users.json");

const supabaseUrl = (process.env.SUPABASE_URL ?? "").replace(/\/$/, "");
const serviceRoleKey =
  process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_SECRET_KEY ?? process.env.SUPABASE_SERVICE_KEY ?? "";
const tableName = process.env.SUPABASE_STATE_TABLE ?? "app_state";
const stateKey = process.env.SUPABASE_STATE_KEY ?? "medicomm";
const isModernSupabaseApiKey = serviceRoleKey.startsWith("sb_");

if (!supabaseUrl || !serviceRoleKey) {
  console.error("Set SUPABASE_URL and SUPABASE_SECRET_KEY before running this script.");
  process.exit(1);
}

const databasePath = existsSync(runtimeDatabasePath) ? runtimeDatabasePath : legacyDatabasePath;
if (!existsSync(databasePath)) {
  console.error("No local database found at runtime-data/users.json or data/users.json.");
  process.exit(1);
}

const data = JSON.parse(readFileSync(databasePath, "utf8"));
const authHeaders = isModernSupabaseApiKey ? {} : { Authorization: `Bearer ${serviceRoleKey}` };
const response = await fetch(`${supabaseUrl}/rest/v1/${encodeURIComponent(tableName)}?on_conflict=key`, {
  method: "POST",
  headers: {
    apikey: serviceRoleKey,
    ...authHeaders,
    "Content-Type": "application/json",
    Prefer: "resolution=merge-duplicates,return=minimal",
  },
  body: JSON.stringify({
    key: stateKey,
    data,
    updated_at: new Date().toISOString(),
  }),
});

if (!response.ok) {
  const message = await response.text().catch(() => "");
  console.error(`Could not seed Supabase: ${message || response.statusText}`);
  process.exit(1);
}

console.log(`Seeded Supabase ${tableName}.${stateKey} from ${path.relative(rootDir, databasePath)}.`);
