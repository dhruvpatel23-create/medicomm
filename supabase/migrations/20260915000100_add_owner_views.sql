begin;

create or replace view public.medicomm_reviews
with (security_invoker = true) as
select
  state.key as app_key,
  review.item->>'id' as review_id,
  review.item->>'userId' as user_id,
  coalesce(nullif(learner.item->>'name', ''), 'MediComm learner') as name,
  (review.item->>'rating')::integer as rating,
  review.item->>'comment' as comment,
  (review.item->>'createdAt')::timestamptz as created_at,
  (review.item->>'updatedAt')::timestamptz as updated_at
from public.app_state as state
cross join lateral jsonb_array_elements(coalesce(state.data->'websiteReviews', '[]'::jsonb)) as review(item)
left join lateral jsonb_array_elements(coalesce(state.data->'users', '[]'::jsonb)) as learner(item)
  on learner.item->>'id' = review.item->>'userId';

create or replace view public.medicomm_overview
with (security_invoker = true) as
select
  state.key as app_key,
  state.updated_at as last_saved_at,
  jsonb_array_length(coalesce(state.data->'users', '[]'::jsonb)) as users,
  jsonb_array_length(coalesce(state.data->'websiteReviews', '[]'::jsonb)) as reviews,
  jsonb_array_length(coalesce(state.data->'communities', '[]'::jsonb)) as communities,
  jsonb_array_length(coalesce(state.data->'practiceResults', '[]'::jsonb)) as practice_results,
  jsonb_array_length(coalesce(state.data->'duelResults', '[]'::jsonb)) as duel_results,
  jsonb_array_length(coalesce(state.data->'vivaSessions', '[]'::jsonb)) as viva_sessions,
  jsonb_array_length(coalesce(state.data->'clinicalCaseSessions', '[]'::jsonb)) as clinical_case_sessions
from public.app_state as state;

revoke all on public.medicomm_reviews, public.medicomm_overview from public, anon, authenticated;
grant select on public.medicomm_reviews, public.medicomm_overview to service_role;

comment on view public.medicomm_reviews is 'Owner review report. Read with SELECT and sort by created_at descending.';
comment on view public.medicomm_overview is 'Owner counts and last saved time from the current app state.';

commit;
