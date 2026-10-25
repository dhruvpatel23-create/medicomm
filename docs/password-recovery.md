# Firebase authentication and password recovery

Firebase Authentication handles email/password credentials, verification links and password-reset emails. No Resend key, sender DNS changes or database reimport is required for authentication. Google sign-in and the website's secure HttpOnly session cookie remain supported.

## Existing accounts

- The current PBKDF2-SHA512 hashes cannot be imported directly. On the next successful legacy password sign-in, a missing Firebase identity is created with that password and original account ID. Profiles, paid memberships, progress and saved content stay intact.
- Firebase becomes authoritative after binding. Old application hashes never override an existing Firebase password or restore a password invalidated by recovery. A successful Firebase password sign-in removes the legacy hash from current app state; historical immutable chunks can still contain prior versions.
- Existing Firebase identities are reused only when UID bindings agree. Their passwords and Google providers are never overwritten. Users with Google-only identities can continue with Google or use Forgot password to add a Firebase password.
- Recovery before the first migrated login provisions a missing Firebase identity without a password. The user must complete the emailed reset before password sign-in can work. Requests have email/IP limits and generic responses. Delivery failures log no email, token or password.
- New email/password users and unverified legacy users must open the verification email before getting a website session. Google-proven emails stay verified. Firebase-bound website sessions are checked against identity deletion, disablement, email changes and Firebase token revocation, with a ten-second identity cache.

## Deploy

```sh
cd /var/www/medullaprep.com
git pull --ff-only origin main
npm run build
pm2 restart medullaprep
```

Keep the existing Firebase project, admin credentials and registered web app. In Firebase Console â†’ Authentication â†’ Sign-in method, keep Email/Password and Google enabled. Under Settings â†’ Authorized domains, retain medullaprep.com and www.medullaprep.com. Under Templates, review Password reset and Email address verification; retain the default Firebase hosted action handler. Users change passwords on that hosted page, then return to the website to sign in. Old custom recovery links open the request-new-link screen; the old custom reset API returns HTTP 410.

The Firebase project password policy was configured to require 8–128 characters, a number and a special character, matching signup. Forced upgrades on sign-in remain off. The hosted reset page follows this policy. Firebase quotas and abuse protection apply. No plan was upgraded and no live user email was sent during implementation. Verify inbox/spam delivery with your own account after deployment.

EMAIL_VERIFICATION_REQUIRED and EMAIL_OTP_SECRET are ignored for Firebase authentication. Optional Resend payment thank-you emails are a separate feature. Firebase's default authentication mailer cannot send arbitrary purchase receipts.

Official documentation: https://firebase.google.com/docs/auth/web/manage-users and https://firebase.google.com/docs/auth/admin/import-users
