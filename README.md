# medicomm

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
