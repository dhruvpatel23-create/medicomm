# Medulla: verified stack, dependencies and API inventory

Verified against repository source and package-lock.json on 2026-10-16. This describes checked-in implementation/configuration, not a live production audit. This source-based inventory corrects inaccuracies in the existing PDF, including the reviews write method, session implementation and installed dependency versions.

## Architecture

- React single-page frontend, primarily JavaScript/JSX with a small TypeScript utility. Vite builds static assets into `dist`; custom CSS and Tailwind provide styling.
- Node.js native HTTP server (`server.mjs`), ES modules, manual routing, native fetch. Package engine specifies Node 22.x; this workstation currently runs 20.17.0.
- Development: Vite on 127.0.0.1:4173 proxies `/api` and `/uploads` to Node on 4174. Production Node serves the frontend and API together.
- React hooks handle most application state. TanStack Query's provider is configured, but no useQuery/useMutation calls were found in src. Navigation is managed within the application rather than a React Router dependency.
- Community, messaging and duel updates use HTTP polling. Canvas/pointer handling supports the answer notepad. Browser localStorage/sessionStorage hold selected UI/progress state.
- Deployment configuration: Render Node web service, starter plan, `npm ci --include=dev && npm run build`, `npm start`, readiness at `/health/ready`. Configured domains: medullaprep.com and www.medullaprep.com.

## Persistence and authentication

Supabase PostgreSQL is accessed using native fetch and PostgREST, without a Supabase JavaScript SDK or ORM. Main application state is a JSONB snapshot in `public.app_state`, with key, data, revision and updated_at columns. Revision-conditional writes provide optimistic concurrency checks. SQL migrations also define owner views and member/subscription structures.

Local development state is in `runtime-data/users.json`; question banks are JSON files in data/public. Production requires Supabase and a private upload bucket. Storage failures are surfaced rather than silently switching production writes to a local database. Private user images pass through authenticated Node handlers; public educational images live under public/uploads.

Authentication is custom: salted PBKDF2-SHA512 passwords (220,000 iterations), random opaque session tokens stored as SHA256 hashes, and HttpOnly/SameSite=Lax cookies (Secure in production). Sessions are not JWTs or Supabase Auth. Server code includes origin checks, request limits, rate limiting and upload signature/size validation.

## Direct npm dependencies

Versions below are resolved lockfile versions. The complete transitive graph is in package-lock.json (261 package entries excluding the root, including platform/optional packages).

| Package | Locked version | Role / observed usage |
| --- | --- | --- |
| react | 18.3.1 | Components and hooks |
| react-dom | 18.3.1 | DOM rendering and portals |
| @radix-ui/react-dialog | 1.1.17 | Dialog primitives |
| @radix-ui/react-dropdown-menu | 2.1.18 | Dropdown primitives |
| @radix-ui/react-tabs | 1.1.15 | Tabs primitives |
| @radix-ui/react-tooltip | 1.2.10 | Tooltip provider and components |
| @radix-ui/react-progress | 1.1.10 | Declared; no src import found |
| @radix-ui/react-switch | 1.3.1 | Declared; no src import found |
| @tanstack/react-query | 5.101.2 | QueryClient/provider configured |
| framer-motion | 12.42.0 | Motion components/transitions |
| lucide-react | 1.21.0 | SVG icons |
| class-variance-authority | 0.7.1 | Button variants |
| clsx | 2.1.1 | Conditional classes |
| tailwind-merge | 3.6.0 | Tailwind class merging |
| tailwindcss | 3.4.17 | CSS utilities |
| tailwindcss-animate | 1.0.7 | Tailwind animation plugin |
| postcss | 8.5.28 | CSS processing |
| autoprefixer | 10.5.2 | CSS prefixes |
| typescript | 6.0.3 | TypeScript tooling/configuration |
| react-hook-form | 7.80.0 | Declared; no src import found |
| @hookform/resolvers | 5.4.0 | Declared; no src import found |
| zod | 4.4.3 | Declared; no src import found |
| razorpay | 2.9.8 | Server payment SDK |
| @vitejs/plugin-react | 4.7.0 | Development dependency: React build plugin |
| vite | 5.4.21 | Development dependency: build/dev server |

Node built-ins include http, crypto, fs, path, url, util and zlib; tests use node:test and assertions. These require no separate npm installation. There is no direct Express, Next.js, Axios, Prisma, MongoDB, Redis or Socket.IO dependency.

## External calls

| Service | Call | Purpose |
| --- | --- | --- |
| Gemini | POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent | MCQ generation, Viva questions/evaluation, clinical cases, theory/short-note evaluation and prompts; native fetch with server API key |
| Supabase PostgREST | GET /rest/v1/{stateTable}?key=eq.{stateKey} | Load app snapshot |
| Supabase PostgREST | PATCH /rest/v1/{stateTable}?key=eq.{stateKey}&revision=eq.{revision} | Revision-checked state persistence |
| Supabase Storage | POST /storage/v1/object/{bucket}/{name} | Upload image |
| Supabase Storage | GET or DELETE /storage/v1/object/{bucket}/{name} | Retrieve/remove image |
| Supabase Storage | GET /storage/v1/bucket/{bucket} | Validate bucket readiness/privacy |
| Razorpay SDK | orders.create; payments.fetch | Create orders and verify payment status |
| Razorpay browser script | https://checkout.razorpay.com/v1/checkout.js | Hosted checkout |
| Google Fonts | fonts.googleapis.com / fonts.gstatic.com | Inter font |

Model strings in code/configuration: general generation and Viva review default `gemini-2.5-flash`; Render config specifies `gemini-3.5-flash-lite` for Viva questions/clinical generation and `gemini-3.5-flash` for clinical evaluation. Short-note evaluation and review fallback have separate overrides. These are repository configuration values, not independently verified model availability.

Payment verification checks an HMAC-SHA256 checkout signature and fetches payment details. No payment webhook route was found.

## Internal HTTP routes

`:id` represents a dynamic identifier. Requests generally use JSON and same-origin cookies; protected routes enforce authentication and, where applicable, access/token rules.

| Area | Methods and paths |
| --- | --- |
| Auth | POST /api/auth/signup; POST /api/auth/login; GET /api/auth/session; POST /api/auth/logout |
| Profile | PATCH /api/profile; PATCH /api/profile/stats; PATCH /api/profile/question-bookmarks |
| Users | GET /api/users/search; GET /api/users/:id |
| Dashboard | GET /api/dashboard; PATCH /api/dashboard/goal; POST /api/practice/attempts |
| Practice | GET /api/practice; POST /api/generate-question; POST /api/generate-questions |
| Viva | POST /api/viva/sessions; POST /api/viva/sessions/:id/answers; POST /api/viva/sessions/:id/advance |
| Clinical cases | POST /api/clinical-cases/sessions; GET /api/clinical-cases/sessions/:id; POST /api/clinical-cases/sessions/:id/answers; POST /api/clinical-cases/sessions/:id/advance |
| Short notes | GET/POST /api/short-notes/reviews; GET/POST/DELETE /api/short-notes/custom; POST /api/short-notes/generate-prompt |
| Rankings/tokens | GET /api/leaderboard; GET /api/tokens |
| Duels | GET /api/duels/questions; POST /api/duels/answer; GET /api/duels/status; POST /api/duels/complete |
| Challenges | POST /api/duels/challenge/create; GET /api/duels/challenge/status; POST /api/duels/challenge/accept; POST /api/duels/challenge/decline; POST /api/duels/challenge/cancel |
| Ranked queue | GET/POST/DELETE /api/duels/rated/queue |
| Friends | GET/POST /api/friends; POST /api/friends/request; POST /api/friends/accept; POST /api/friends/decline; POST /api/friends/cancel |
| Messaging | GET /api/direct-messages; POST /api/direct-messages/open; POST /api/direct-messages/:id/messages |
| Communities | GET/POST /api/communities; POST /api/communities/:id/join; POST /api/communities/:id/messages; DELETE /api/communities/:id/members/:memberId |
| Payments | POST /api/payment-quote; POST /api/create-order; POST /api/verify-payment |
| Reviews | GET/PUT/DELETE /api/reviews |
| Operations | GET /api/summary; GET /api/storage/status; GET /health/live; GET /health/ready |
| Images | GET /uploads/:filename |

The frontend's src/lib/api.js wraps native fetch with JSON parsing, credentials: same-origin, an AbortController and an 8-second default timeout (callers may override). It dispatches token-refresh events after relevant calls.

Example authenticated frontend calls:

```js
await apiRequest('/api/dashboard');
await apiRequest('/api/reviews', {
  method: 'PUT',
  body: JSON.stringify({ rating: 5, comment: 'Helpful explanations.' }),
});
```

## Supporting tools and configuration

- Python content scripts use pypdf and PyMuPDF (fitz) for PDFs, Pillow for images and NumPy for image/numerical work. No pinned Python requirements manifest was found.
- UI verification scripts use Playwright/Chromium, but Playwright is not declared in package.json; several scripts reference a local npm cache path or PLAYWRIGHT_MODULE.
- Backend tests: `npm run test:backend`; duel tests: `npm run test:duels`. Other scripts check reviews, payments, Supabase, practice order and theory features.
- `npm run dev` starts local development; `npm run build` first synchronizes AI questions into practice banks, then invokes Vite; `npm start` runs Node. The build command does not run a separate TypeScript type-check.
- Server configuration includes GEMINI_API_KEY, GEMINI_MODEL, VIVA_AI_PROVIDER, VIVA_QUESTION_MODEL, CLINICAL_CASE_MODEL, CLINICAL_CASE_EVALUATION_MODEL, SHORT_NOTES_EVALUATION_MODEL, GEMINI_REVIEW_FALLBACK_MODEL, SUPABASE_URL, a Supabase server key, SUPABASE_STATE_TABLE, SUPABASE_STATE_KEY, SUPABASE_UPLOAD_BUCKET, APP_ORIGINS, TRUST_PROXY, RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET. Secrets belong in environment configuration, not browser code.

Sources: package.json, package-lock.json, server.mjs, server/*.mjs, src/main.jsx, src/lib/api.js, src/components, vite.config.js, tailwind.config.js, tsconfig.json, render.yaml, scripts/supabase-schema.sql and supabase/migrations.
