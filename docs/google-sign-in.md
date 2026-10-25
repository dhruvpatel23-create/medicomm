# Google sign-in

Google login complements the existing email/password and OTP flows. It does not
import, replace or reset existing accounts. Google credentials are exchanged for
the existing HttpOnly Medulla session cookie; Firebase browser authentication is
memory-only and is signed out after the exchange. Tokens and Google passwords are
never persisted in browser storage or application logs.

The backend verifies Firebase ID tokens against this Firebase project, checking
revocation and the current Firebase user. Google must be the sign-in provider,
the token and current user must both have verified matching email addresses, the
Google provider identity must match, and authentication must be within ten minutes.
Client-supplied emails and verification flags are not trusted.

Existing password accounts require a one-time original-password confirmation
before their first Google link (or an existing authenticated session for that same
account). Existing passwords, IDs, subscriptions and progress are preserved. Later
Google logins use the stored Google UID; UID/email conflicts are rejected rather
than merging different accounts. Duplicate existing emails require support.

New Google users finish the normal username, batch, college/country and ten-digit
phone profile before a Medulla account/session is created. They are verified through
Google and do not need a local password or a redundant email OTP. Password-only
login does not itself prove email ownership; its existing OTP setting remains in
effect. Google-only accounts cannot authenticate with a fabricated local password.

## Configuration and deployment

The server uses its existing Firebase Admin credential. It discovers the registered
web-app configuration through the Firebase Management API and returns only the
public SDK fields from `/api/auth/google/config`. No server key is exposed.
For multiple web apps, pin `FIREBASE_WEB_APP_ID`. If discovery is unavailable, set
`FIREBASE_WEB_API_KEY`, `FIREBASE_WEB_APP_ID` and optionally `FIREBASE_AUTH_DOMAIN`
on the server. These are web SDK configuration values, not the Admin private key.

Enable Google in Firebase Authentication, and authorize `medullaprep.com` and
`www.medullaprep.com` under Authentication → Settings → Authorized domains.
The existing Firebase domain remains the OAuth handler domain. Existing authorized
domains must be retained. Local development needs its own authorized hostname.

Deploy with `git pull --ff-only origin main`, `npm ci`, `npm run build`, then
`pm2 restart medullaprep` to retain the saved Firebase server environment. This
does not require database re-import, migration replay, or user password resets.

Firebase browser modules are pinned to Node-22-compatible versions; compatibility
dependency overrides prevent transitive updates to Node-24-only packages.

Verify by signing in with a real Google account manually: existing accounts should
link once and keep their subscription/progress; new accounts should finish profile
details and enter without another email code. Popup blocking, unauthorized domains
and Firebase provider conflicts show actionable errors without changing accounts.

References:
- https://firebase.google.com/docs/auth/web/google-signin
- https://firebase.google.com/docs/auth/admin/verify-id-tokens
- https://firebase.google.com/docs/reference/firebase-management/rest/v1beta1/projects.webApps/getConfig
