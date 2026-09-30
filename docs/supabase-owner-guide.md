# Medulla Supabase setup

## Connect the website

1. In your Supabase project's SQL Editor, run `scripts/supabase-schema.sql`.
2. Run `supabase/migrations/20260915000100_add_owner_views.sql` in a new SQL query. It adds reports without changing existing app data.
3. Put the project URL and server secret key in your Render service's Environment settings as `SUPABASE_URL` and `SUPABASE_SECRET_KEY`. Save and restart/redeploy the service. These credentials belong on the server; never use a `VITE_` prefix.
4. Follow [the backend rollout guide](backend-production.md) to configure origins and private uploads before starting production. Visit `https://YOUR-WEBSITE/health/ready`; expect HTTP 200 with `{"status":"ready"}`. Internal storage details are no longer public.

If the `medicomm` row already exists, the server loads it. Missing state now stops startup. For a new database only, explicitly initialize a reviewed source with `npm run seed:supabase`; this command now rejects an existing row instead of replacing it.

For a local connection check, add the same two variables to `.env.local` and run `npm run check:supabase`. This command only reads data and reports counts; it does not start the app or replace its local database. The owner views use the default `public.app_state` table; adjust the SQL if you configured another table.

## Read reviews

Open the website's Reviews page, or run this in Supabase SQL Editor:

```sql
select name, rating, comment, created_at, updated_at
from public.medicomm_reviews
where app_key = 'medicomm'
order by created_at desc;
```

The report reads directly from saved app data, so new reviews appear when you run the query again. It includes reviews whose user account no longer exists, labelled "Medulla learner". The public website only shows reviews with an existing account.

## Check activity

```sql
select *
from public.medicomm_overview
where app_key = 'medicomm';
```

This shows saved counts for users, reviews, communities, practice results, duel results, Viva sessions, and clinical case sessions. These are stored totals, not a count of people currently online.

## Where data lives

Medulla currently stores its database in `public.app_state`, inside the `data` column of the `medicomm` row. Accounts are in `data.users`; this app does not use Supabase Authentication for its website accounts. The two owner views display selected information from that JSON. They are restricted to database administrators and the server's service role.

Use website controls to make changes. The server caches committed app data in memory and uses revision checks to reject stale writes. Direct SQL edits and old binaries bypass this protection. Keep only one running app server; connecting a local dev server to production creates another writer.

Local development without Supabase uses `runtime-data/users.json`. Production does not fall back to or mirror that file. Production uploads use the configured private Supabase Storage bucket; existing local uploads need the migration in the rollout guide. Database backups and object backups must both be maintained independently of the app host.

Supabase view permissions: https://supabase.com/docs/guides/database/postgres/row-level-security#views
