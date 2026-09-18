import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function main() {
  for (const filename of [".env.local", ".env"]) {
    const envPath = path.join(rootDir, filename);
    if (existsSync(envPath)) process.loadEnvFile(envPath);
  }

  const projectUrl = process.env.SUPABASE_URL?.trim();
  const secret = process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_SECRET_KEY ?? process.env.SUPABASE_SERVICE_KEY;
  if (!projectUrl || !secret) {
    throw new Error("Add SUPABASE_URL and SUPABASE_SECRET_KEY to .env.local, then run npm run check:supabase again.");
  }

  const baseUrl = new URL(projectUrl);
  if (baseUrl.protocol !== "https:" && !(baseUrl.protocol === "http:" && ["localhost", "127.0.0.1"].includes(baseUrl.hostname))) {
    throw new Error("SUPABASE_URL must use HTTPS (HTTP is allowed only for localhost).");
  }
  const stateKey = process.env.SUPABASE_STATE_KEY ?? "medicomm";
  const table = process.env.SUPABASE_STATE_TABLE ?? "app_state";
  const headers = { apikey: secret };
  if (!secret.startsWith("sb_secret_")) headers.Authorization = `Bearer ${secret}`;

  async function readRows(tableName, select, keyColumn) {
    const url = new URL(`/rest/v1/${encodeURIComponent(tableName)}`, baseUrl);
    url.searchParams.set("select", select);
    url.searchParams.set(keyColumn, `eq.${stateKey}`);
    const response = await fetch(url, { headers, signal: AbortSignal.timeout(15000) });
    if (!response.ok) {
      if ([401, 403].includes(response.status)) throw new Error("Supabase rejected the credentials. Use the project's server secret or service_role key.");
      if (response.status === 404) throw new Error(`Supabase cannot find ${tableName}. Run the SQL setup files listed in docs/supabase-owner-guide.md.`);
      throw new Error(`Supabase returned HTTP ${response.status} while reading ${tableName}.`);
    }
    const rows = await response.json();
    if (!Array.isArray(rows)) throw new Error(`Unexpected response from ${tableName}.`);
    return rows;
  }

  const stateRows = await readRows(table, "key,updated_at", "key");
  console.log("Supabase connection: OK (read access verified; no data changed).");
  if (!stateRows.length) {
    throw new Error(`No ${stateKey} row yet. Configure the live server and restart it to initialize Supabase from that server's data.`);
  }
  console.log(`App state: ${table}.${stateKey}; last saved: ${stateRows[0].updated_at}`);

  const overviewRows = await readRows("medicomm_overview", "*", "app_key");
  await readRows("medicomm_reviews", "review_id", "app_key");
  if (!overviewRows.length) throw new Error("The owner overview returned no app row.");
  console.table(overviewRows);
  console.log("Owner reviews view: OK.");
}

main().catch((error) => {
  // Network errors can include request details; keep diagnostics free of credentials.
  console.error(error instanceof TypeError || error?.name === "TimeoutError"
    ? "Connection failed. Check SUPABASE_URL and network access."
    : error.message);
  process.exitCode = 1;
});
