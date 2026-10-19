-- Apply before enabling NOTEPAD_ROW_STORAGE=true on every app process.
begin;
create table if not exists public.notepad_drafts (
  namespace text not null,
  user_id text not null,
  draft_id text not null,
  draft jsonb not null check (octet_length(draft::text) <= 3145728),
  revision bigint not null check (revision > 0),
  updated_at timestamptz not null default now(),
  primary key (namespace, user_id, draft_id)
);
create table if not exists public.notepad_reviews (
  namespace text not null,
  user_id text not null,
  id text not null,
  question_id text not null,
  submitted_at timestamptz not null,
  review jsonb not null,
  primary key (namespace, user_id, id)
);
create index if not exists notepad_reviews_user_date on public.notepad_reviews(namespace, user_id, submitted_at desc, id desc);
create index if not exists notepad_reviews_question on public.notepad_reviews(namespace, user_id, question_id, submitted_at desc);
create index if not exists notepad_reviews_images on public.notepad_reviews using gin ((review->'answerPages') jsonb_path_ops);
alter table public.notepad_drafts enable row level security;
alter table public.notepad_reviews enable row level security;
revoke all on public.notepad_drafts, public.notepad_reviews from anon, authenticated;
grant all on public.notepad_drafts, public.notepad_reviews to service_role;
-- Idempotent backfill. Keep the legacy copy for rollback until verified.
insert into public.notepad_reviews(namespace, user_id, id, question_id, submitted_at, review)
select s.key, r->>'userId', r->>'id', r->>'questionId', (r->>'submittedAt')::timestamptz, r
from public.app_state s cross join lateral jsonb_array_elements(coalesce(s.data->'shortNoteReviews', '[]'::jsonb)) r
where r->>'id' is not null and r->>'userId' is not null
on conflict do nothing;
create or replace view public.notepad_review_summaries with (security_invoker = true) as
select distinct on (namespace, user_id, question_id) namespace, user_id, question_id, id, submitted_at,
  count(*) over (partition by namespace, user_id, question_id) as attempt_count,
  jsonb_build_object('id', id, 'questionId', question_id, 'submittedAt', submitted_at, 'score', review->'score') as review
from public.notepad_reviews
order by namespace, user_id, question_id, submitted_at desc, id desc;
revoke all on public.notepad_review_summaries from anon, authenticated;
grant select on public.notepad_review_summaries to service_role;
commit;
notify pgrst, 'reload schema';
