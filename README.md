# medicomm

## Website ratings and reviews

Home and the Reviews page show public 1–5 star ratings, an overall average, and learner comments. Signed-in users can save, edit, or delete one rating per account; comments are optional and limited to 1,000 characters. Guest users can browse reviews.

`GET /api/reviews?page=1` returns 12 reviews per page and the overall rating summary. Authenticated `PUT /api/reviews` accepts `{ "rating": 5, "comment": "..." }`; `DELETE /api/reviews` deletes the caller's own review. Reviews use the existing `websiteReviews` database field and follow the app's local/Supabase storage configuration.

Run `node scripts/check-website-reviews.mjs` to check authentication, validation, ownership, persistence, rating calculations, and pagination with isolated test data.

## Local Gemini setup

The local API automatically loads `.env.local` and then `.env` from the project root. Add a Gemini API key to `.env.local`:

```env
GEMINI_API_KEY=your_key_from_google_ai_studio
GEMINI_MODEL=gemini-2.5-flash
VIVA_QUESTION_MODEL=gemini-3.5-flash-lite
CLINICAL_CASE_MODEL=gemini-3.5-flash-lite
CLINICAL_CASE_EVALUATION_MODEL=gemini-3.5-flash
VIVA_AI_PROVIDER=gemini
```

`VIVA_QUESTION_MODEL` uses the stable, lower-latency Gemini 3.5 Flash-Lite model for preparing a Viva while `GEMINI_MODEL` remains the default for answer review. Remove the question-specific override if you prefer to use the same model for both operations.
`CLINICAL_CASE_MODEL` controls fast generation of the applied theory cases. `CLINICAL_CASE_EVALUATION_MODEL` independently uses the higher-quality model for grading and structured exam-ready answers.

Keep `.env.local` private. Restart `npm run dev` after adding or changing the key because an already-running API process will not reload environment variables.

## Supabase database

The server stores the app database in Supabase when these environment variables are set:

- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`

Run `scripts/supabase-schema.sql` in the Supabase SQL editor first. On first startup, the server seeds Supabase from `runtime-data/users.json` if the `app_state` row does not exist. A local JSON copy is still written as a backup/fallback.
