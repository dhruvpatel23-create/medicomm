begin;

-- Independent payment ledger: app-state replacement cannot delete membership dates.
create table if not exists public.medicomm_paid_memberships (
  app_key text not null,
  order_id text not null,
  user_id text not null,
  payment_id text not null,
  plan_id text,
  amount_paise bigint,
  currency text,
  purchased_at timestamptz not null,
  expires_at timestamptz generated always as
    (((purchased_at at time zone 'Asia/Kolkata') + interval '1 year') at time zone 'Asia/Kolkata') stored,
  purchase_date_source text not null,
  recorded_at timestamptz not null default now(),
  primary key (app_key, order_id)
);
create index if not exists medicomm_paid_memberships_user_idx
  on public.medicomm_paid_memberships (app_key, user_id, expires_at desc);
alter table public.medicomm_paid_memberships enable row level security;
revoke all on public.medicomm_paid_memberships from public, anon, authenticated, service_role;
grant select, insert on public.medicomm_paid_memberships to service_role;
drop policy if exists "server reads memberships" on public.medicomm_paid_memberships;
create policy "server reads memberships" on public.medicomm_paid_memberships
  for select to service_role using (true);
drop policy if exists "server records memberships" on public.medicomm_paid_memberships;
create policy "server records memberships" on public.medicomm_paid_memberships
  for insert to service_role with check (true);

create or replace function public.medicomm_preserve_memberships()
returns trigger language plpgsql security invoker set search_path = '' as $$
declare
  payment jsonb;
  learner jsonb;
  members jsonb := '[]'::jsonb;
  orders jsonb := '[]'::jsonb;
  term public.medicomm_paid_memberships%rowtype;
begin
  for payment in select value from jsonb_array_elements(coalesce(new.data->'paymentOrders', '[]'::jsonb)) loop
    if payment->>'status' = 'paid'
      and nullif(payment->>'paymentId', '') is not null
      and nullif(payment->>'verifiedAt', '') is not null
      and nullif(payment->>'userId', '') is not null
      and nullif(payment->>'orderId', '') is not null then
      insert into public.medicomm_paid_memberships
        (app_key, order_id, user_id, payment_id, plan_id, amount_paise, currency, purchased_at, purchase_date_source)
      values (new.key, payment->>'orderId', payment->>'userId', payment->>'paymentId',
        payment->>'planId', (payment->>'amount')::bigint, payment->>'currency',
        coalesce(nullif(payment->>'purchasedAt', ''), payment->>'verifiedAt')::timestamptz,
        coalesce(nullif(payment->>'purchaseDateSource', ''), 'saved_verification'))
      on conflict (app_key, order_id) do nothing;
      select * into term from public.medicomm_paid_memberships
        where app_key = new.key and order_id = payment->>'orderId';
      if found then
        payment := payment || jsonb_build_object('purchasedAt', term.purchased_at,
          'expiresAt', term.expires_at, 'purchaseDateSource', term.purchase_date_source);
      end if;
    end if;
    orders := orders || jsonb_build_array(payment);
  end loop;
  new.data := jsonb_set(new.data, '{paymentOrders}', orders);
  for learner in select value from jsonb_array_elements(coalesce(new.data->'users', '[]'::jsonb)) loop
    select * into term from public.medicomm_paid_memberships
      where app_key = new.key and user_id = learner->>'id'
      order by expires_at desc, order_id limit 1;
    if found then
      learner := learner || jsonb_build_object(
        'subscriptionPurchasedAt', term.purchased_at,
        'subscriptionExpiresAt', term.expires_at,
        'subscriptionOrderId', term.order_id,
        'plan', term.plan_id);
    end if;
    members := members || jsonb_build_array(learner);
  end loop;
  new.data := jsonb_set(new.data, '{users}', members);
  return new;
end;
$$;
revoke all on function public.medicomm_preserve_memberships() from public, anon, authenticated;
grant execute on function public.medicomm_preserve_memberships() to service_role;
drop trigger if exists medicomm_preserve_memberships on public.app_state;
create trigger medicomm_preserve_memberships before insert or update of data
  on public.app_state for each row execute function public.medicomm_preserve_memberships();

-- Backfill existing verified payments once, under the same transaction and CAS revision.
update public.app_state set data = data, revision = revision + 1, updated_at = now();

create or replace view public.medicomm_member_sessions with (security_invoker = true) as
select state.key as app_key, session.value->>'userId' as user_id,
  nullif(session.value->>'createdAt', '')::timestamptz as logged_in_at,
  to_timestamp((session.value->>'expiresAt')::double precision / 1000) as session_expires_at,
  to_timestamp((session.value->>'expiresAt')::double precision / 1000) > now() as is_valid
from public.app_state state
cross join lateral jsonb_each(coalesce(state.data->'sessions', '{}'::jsonb)) session
where jsonb_typeof(session.value) = 'object' and jsonb_typeof(session.value->'expiresAt') = 'number';

create or replace view public.medicomm_member_attempts with (security_invoker = true) as
select state.key as app_key, item->>'id' as attempt_id, item->>'userId' as user_id,
  item->>'questionId' as question_id, item->>'subjectId' as subject_id,
  item->>'subject' as subject, item->>'topic' as topic, item->>'mode' as mode,
  (item->>'correct')::boolean as correct,
  coalesce((item->>'durationSeconds')::integer, 0) as duration_seconds,
  (item->>'answeredAt')::timestamptz as answered_at
from public.app_state state
cross join lateral jsonb_array_elements(coalesce(state.data->'practiceResults', '[]'::jsonb)) item;

create or replace view public.medicomm_member_progress with (security_invoker = true) as
select app_key, user_id, subject_id, subject, topic, mode, count(*) as attempts,
  count(*) filter (where correct) as correct_answers,
  round(100.0 * count(*) filter (where correct) / nullif(count(*), 0), 1) as accuracy_percent,
  sum(duration_seconds) as study_seconds, max(answered_at) as last_practised_at
from public.medicomm_member_attempts
group by app_key, user_id, subject_id, subject, topic, mode;

create or replace view public.medicomm_members with (security_invoker = true) as
select state.key as app_key, learner->>'id' as user_id, learner->>'name' as name,
  learner->>'email' as email, learner->>'contactNumber' as contact_number,
  learner->>'medicalCollege' as medical_college,
  nullif(learner->>'createdAt', '')::timestamptz as joined_at,
  nullif(learner->>'lastLoginAt', '')::timestamptz as last_login_at,
  coalesce(sessions.active_sessions, 0) as active_sessions,
  coalesce(sessions.active_sessions, 0) > 0 as is_logged_in,
  sessions.latest_session_expiry,
  coalesce(membership.plan_id, learner->>'plan', learner->>'subscription') as plan,
  membership.purchased_at, membership.expires_at,
  case when membership.expires_at > now() then 'active'
       when membership.expires_at is not null then 'expired'
       when learner->>'hasPracticeAccess' = 'true' or learner->>'isSubscribed' = 'true'
         or nullif(learner->>'plan', '') is not null or nullif(learner->>'subscription', '') is not null
         then 'purchase_date_required'
       else 'free' end as subscription_status,
  membership.purchase_date_source,
  coalesce((learner->>'attemptedQuestions')::bigint, 0) as total_attempted,
  coalesce((learner->>'correctAnswers')::bigint, 0) as total_correct,
  coalesce((learner->>'streak')::integer, 0) as streak_days,
  learner->'studyGoal' as study_goal,
  activity.last_practised_at
from public.app_state state
cross join lateral jsonb_array_elements(coalesce(state.data->'users', '[]'::jsonb)) learner
left join lateral (
  select count(*) filter (where is_valid) as active_sessions,
    max(session_expires_at) filter (where is_valid) as latest_session_expiry
  from public.medicomm_member_sessions s where s.app_key = state.key and s.user_id = learner->>'id'
) sessions on true
left join lateral (
  select * from public.medicomm_paid_memberships m
  where m.app_key = state.key and m.user_id = learner->>'id'
  order by expires_at desc, order_id limit 1
) membership on true
left join lateral (
  select max(answered_at) as last_practised_at from public.medicomm_member_attempts a
  where a.app_key = state.key and a.user_id = learner->>'id'
) activity on true;

revoke all on public.medicomm_members, public.medicomm_member_sessions,
  public.medicomm_member_attempts, public.medicomm_member_progress from public, anon, authenticated;
grant select on public.medicomm_members, public.medicomm_member_sessions,
  public.medicomm_member_attempts, public.medicomm_member_progress to service_role;
comment on view public.medicomm_members is 'Private owner directory. Logged in means an unexpired session, not live presence. No password or session credentials.';
notify pgrst, 'reload schema';
commit;
