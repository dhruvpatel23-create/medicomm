create table if not exists public.app_state (
  key text primary key,
  data jsonb not null default '{}'::jsonb,
  revision bigint not null default 0,
  updated_at timestamptz not null default now()
);

-- Safe additive migration for existing installations. Stop old API instances
-- before deploying revision-aware writers; old binaries bypass this guard.
alter table public.app_state add column if not exists revision bigint not null default 0;

alter table public.app_state enable row level security;

drop policy if exists "service role manages app state" on public.app_state;

create policy "service role manages app state"
on public.app_state
for all
to service_role
using (true)
with check (true);

-- Learner uploads are served through the authenticated Node API.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('medicomm-uploads', 'medicomm-uploads', false, 5242880,
        array['image/png','image/jpeg','image/webp','image/gif'])
on conflict (id) do nothing;
