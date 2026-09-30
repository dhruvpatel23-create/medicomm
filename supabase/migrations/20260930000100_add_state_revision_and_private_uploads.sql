-- Apply to the existing production database before deploying the new backend.
-- Stop old API writers before cutover. Existing app_state data is preserved.
begin;

alter table public.app_state
  add column if not exists revision bigint not null default 0;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('medicomm-uploads', 'medicomm-uploads', false, 5242880,
        array['image/png', 'image/jpeg', 'image/webp', 'image/gif'])
on conflict (id) do nothing;

notify pgrst, 'reload schema';

commit;
