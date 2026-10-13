# Member administration and annual subscriptions

Apply `supabase/migrations/20261013000100_member_directory_and_subscriptions.sql`
in the project's SQL Editor, then deploy the updated backend/frontend. It assumes
the existing `public.app_state` table and revision migration. Do not seed or
replace production data. This migration is transactional and additive. It
backfills verified payments and increments the state revision; an in-flight
request may receive a conflict and need retrying. No question banks are changed.

Open these private views in Supabase Table Editor, or use SQL Editor:

```sql
-- All accounts, contact details, progress totals, membership and login status.
select * from public.medicomm_members where app_key = 'medicomm' order by joined_at desc;

-- Accounts with at least one unexpired login session (not live online presence).
select * from public.medicomm_members where app_key = 'medicomm' and is_logged_in;

-- Filter a particular member by user_id from the directory.
select * from public.medicomm_member_progress
where app_key = 'medicomm' and user_id = 'USER_ID' order by last_practised_at desc;
select * from public.medicomm_member_attempts
where app_key = 'medicomm' and user_id = 'USER_ID' order by answered_at desc;

-- Durable purchase records; amounts are in paise.
select * from public.medicomm_paid_memberships where app_key = 'medicomm' order by purchased_at desc;

-- Legacy accounts requiring confirmation of their original payment date.
select * from public.medicomm_members
where app_key = 'medicomm' and subscription_status = 'purchase_date_required';
```

Progress rows cover server-saved practice attempts, including custom modules.
Historical browser-only progress cannot be reconstructed from Supabase. Session
creation timestamps and last-login timestamps are recorded going forward; old
sessions can still be counted by expiry. Session hashes/tokens, password hashes,
password salts and payment signatures are not exposed in these reports.

An annual term ends at the same India-local time on the anniversary of purchase;
February 29 becomes February 28 in a non-leap year. Provider payment creation time
is used for new verified captured payments. For historical paid orders without a
purchase timestamp, the stored verification timestamp is used and explicitly
labelled `saved_verification`; it may need reconciliation to the original Razorpay
receipt if that historical timestamp was overwritten. No date is invented for
legacy access without payment evidence, and that access is preserved pending review.

Dates are saved on the order and user in app_state. The separate membership table
also retains them when an older app-state snapshot omits a payment. Its trigger
restores membership fields to existing user records on subsequent writes. Ordinary
server credentials can read/insert ledger records, but cannot update/delete them;
re-verifying an order does not restart its year. A new purchase creates a new
one-year term from that purchase; it does not add time to the previous expiry.
Legitimate expiry is enforced from the saved date, independently of legacy boolean flags.

This is protection against accidental state/flag loss, not against an owner
dropping tables, restoring the whole database, or deleting an account. Keep
Supabase backups. Intentional refunds/revocations need an explicit administrative
workflow; this change does not infer them from a missing JSON payment record.

The SQL uses security-invoker views and denies public/anon/authenticated access:
[Supabase view security](https://supabase.com/docs/guides/database/postgres/row-level-security#views).
Only project administrators and the server service role can inspect member data.
