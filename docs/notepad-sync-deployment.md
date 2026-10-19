# Notepad cloud sync deployment

The handwriting notepad now syncs signed-in users' drafts to `notepad_drafts`, one row per account/question. Each save uses a revision check. Conflicting edits require the user to choose; the losing copy is retained in that browser under a `:conflict:` key. Browser drafts are retained offline and uploaded when their sheet is opened. Guests remain local-only. A draft syncs after a pause in writing; the open sheet checks for remote edits every 15 seconds. Wait for “Synced across devices” before switching devices. Closing the browser before a network save finishes leaves the local copy pending for the next visit.

This change covers handwritten notepad drafts. The separate typed-answer field and locally attached, unsubmitted photos are not cloud drafts.

## Theory image compression

New theory photo attachments and exported notepad pages are compressed in the browser before submission. The encoder compares PNG, high-quality WebP and JPEG (quality 0.94), retaining PNG when lossy savings are less than 10%. Already-efficient original photos are preserved when no resizing is needed. Notepad exports keep 1200 × 1600 pixels per page; photos keep their aspect ratio and are capped at a 2560-pixel long edge, without upscaling. The preview, AI review and saved full-size viewer use the same prepared image. Opening an image decodes that stored file; it cannot recover detail lost during resizing or lossy encoding. Original notepad stroke drafts remain separately editable.

This reduces Supabase **Storage** usage for new submissions, not the number of database rows. Existing uploads are untouched. Savings vary by content; noisy photos may remain large. The 5 MB combined answer limit still applies. Direct API clients must prepare their own images; the server validates size and format but does not re-encode them. No new VPS dependency or database migration is required specifically for compression.

## Production rollout

1. Back up Supabase and the VPS environment configuration. Run `supabase/migrations/20261019000100_notepad_rows.sql` in the configured Supabase project's SQL editor. It creates private tables, indexes and a summary view, and copies legacy reviews without deleting them. It is safe to rerun. PostgreSQL 15+ is required for the security-invoker view. The backfill assumes the default `public.app_state` table; adapt that table name if using `SUPABASE_STATE_TABLE`.
2. Deploy the code, install dependencies, and build. Stop **all** app processes that can write this database (including any old Render deployment) briefly for the final cutover. Rerun the migration to capture reviews submitted since the initial copy.
3. Add `NOTEPAD_ROW_STORAGE=true` to the VPS `.env`, preserving the existing Supabase URL, server secret and `SUPABASE_STATE_KEY`. Restart every active app process using this configuration. `pm2 restart medullaprep` restarts the previously configured VPS app; inspect the other PM2 entries before changing them.
4. Check `/health/ready`, then open a notepad while signed in, draw, and wait for “Synced across devices”. Sign into the **same account** on another device, open the same question, and confirm the draft. Submit an answer, refresh, and check its history and private page images. Confirm another account cannot read the image URL.
5. Test concurrent edits: leave a pending edit on device A offline, edit on B, reconnect A. A must display the conflict choices instead of silently replacing either draft. Test clearing a page, undo/redo, multiple pages, and reopening the sheet.

Draft sync errors leave the browser copy intact. Missing tables produce a visible waiting-to-sync status; they do not silently fall back to storing drafts in the shared app JSON. The row-storage flag controls reviews only. With it off, reviews continue using legacy storage during migration.

## Review storage and scale

New submitted reviews go to indexed `notepad_reviews` rows; their images remain in the private Supabase Storage bucket. Requests are scoped by the server-authenticated user, with 100-row pagination. The library fetches small latest-review summaries, and the selected question fetches its history. Browser clients have no direct table permissions. The service-role key stays on the server.

The migration deliberately keeps old `shortNoteReviews` in `app_state` for rollback. After verifying the row counts and contents, stop all writers, back up `app_state`, rerun the backfill, and remove only that legacy JSON field using the following SQL. Restart all writers afterwards so no cached state restores the field:

```sql
begin;
-- Restrict to your SUPABASE_STATE_KEY (default medicomm).
select key from public.app_state where key = 'medicomm' for update;
do $$
begin
  if exists (
    select 1 from public.app_state s,
      lateral jsonb_array_elements(coalesce(s.data->'shortNoteReviews', '[]'::jsonb)) r
    where s.key = 'medicomm' and not exists (
      select 1 from public.notepad_reviews n
      where n.namespace = s.key and n.user_id = r->>'userId'
        and n.id = r->>'id' and n.review = r
    )
  ) then raise exception 'Review backfill is incomplete; do not remove legacy data'; end if;
end $$;
update public.app_state set data = data - 'shortNoteReviews', revision = revision + 1,
  updated_at = now() where key = 'medicomm';
commit;
```

Do not simply disable row storage after new submissions: first merge the row reviews into a backed-up legacy state during a maintenance window. Otherwise those submissions will disappear from the old UI even though the rows are still safe.

Notepad drafts/reviews no longer grow the shared JSON after cutover and cleanup. Authentication, token charging and other existing features still use `app_state`; this change does not remove those broader scaling limits. Per-draft payloads are limited to 2 MB and eight pages. Storage quotas, observability and overall capacity planning remain deployment responsibilities.
