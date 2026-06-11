# medicomm

## Supabase database

The server stores the app database in Supabase when these environment variables are set:

- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`

Run `scripts/supabase-schema.sql` in the Supabase SQL editor first. On first startup, the server seeds Supabase from `runtime-data/users.json` if the `app_state` row does not exist. A local JSON copy is still written as a backup/fallback.
