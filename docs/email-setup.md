# Optional subscription emails and legacy local verification

For production Firebase authentication, follow [Firebase authentication and recovery](password-recovery.md). Firebase sends password-reset and verification links directly. Legacy OTP instructions below apply only to non-Firebase deployments. Resend is optional for payment thank-you messages.

Email is disabled until configured. This implementation uses Resend over HTTPS (no SMTP package or mail server). It does not send real email during tests. Password sign-in remains; email OTP is a one-time verification step for new users and for existing users without `emailVerifiedAt`. It is not passwordless login or an OTP challenge on every login.

## Set up the sender

1. Create a Resend account at https://resend.com and add a sending domain you control, preferably a subdomain such as `mail.medullaprep.com`.
2. Add **exactly** the DNS records Resend shows at the authoritative DNS provider for the domain (Cloudflare if that is where its nameservers point). Wait for domain verification. Do not replace your website's A records or an existing mailbox's MX records. See https://resend.com/docs/dashboard/domains/introduction.
3. Create a sending API key limited to this domain. A sender could be `Medulla <noreply@mail.medullaprep.com>`. Resend is the sending service; this does not create an inbox for receiving replies.
4. Add these values to the VPS environment. Do not commit real keys or paste them into chat:

```env
RESEND_API_KEY=your_real_resend_key
EMAIL_FROM="Medulla <noreply@mail.medullaprep.com>"
EMAIL_OTP_SECRET=your_random_secret_at_least_32_characters
EMAIL_VERIFICATION_REQUIRED=true
RAZORPAY_WEBHOOK_SECRET=your_separate_random_webhook_secret
```

Generate each secret separately using `openssl rand -hex 32` in the VPS terminal. Keep the OTP secret identical on every app process using the database. Changing it invalidates pending codes. Existing verified accounts continue working. Enabling verification without complete mail configuration fails startup instead of bypassing verification.

## Payment confirmation even when checkout closes

In Razorpay's dashboard, add a webhook with URL `https://medullaprep.com/api/payments/webhook`, event **payment.captured**, and the same secret as `RAZORPAY_WEBHOOK_SECRET`. Configure and test it in the appropriate Test/Live mode. The secret is separate from `RAZORPAY_KEY_SECRET`. Requests are checked against the signature of the raw body, and payment amount/currency/order are rechecked with Razorpay before activation. See https://razorpay.com/docs/webhooks/validate-test/.

Both checkout verification and this webhook queue the same thank-you message. Duplicate events do not create additional messages. If the webhook is not configured, delivery depends on the browser completing payment verification.

## Deployment and verification

Deploy the updated files, run `npm ci --include=dev`, `npm run build`, and restart the app with the new environment. The existing server skips loading `.env` files when `NODE_ENV=production` is already inherited, so ensure PM2 actually supplies all new variables or uses a startup command with Node's `--env-file=.env` option. Do not assume editing `.env` always updates an already configured PM2 environment.

Every app process that writes this database must run the updated code: old versions normalize away the new OTP state fields. Retire stale PM2/Render writers before enabling verification. No SQL migration is required; the existing server database persists pending challenges and limits, and the payment order holds its email delivery state.

1. Check `/health/ready` and sign up using an email address you control. No session or permanent account is created before verification. Confirm the actual code arrives, then verify it. Test a wrong code and a resend as well.
2. Sign in with an existing unverified account; after its password is validated it must complete email verification once. Previously verified accounts use normal password login. Existing sessions are not revoked, but new checkout requires verified email; an old session will be asked to sign out and in to verify.
3. Make a Razorpay **test-mode** purchase. Confirm activation and one thank-you email with plan, actual paid amount, order/payment reference and expiry. Test emails are clearly labelled. Repeat the webhook and check that no duplicate is sent. Test the browser-close case too.
4. Check Resend delivery/bounce logs before switching to live payments. Provider acceptance is not a guarantee of inbox delivery.

## Behaviour and recovery

- Codes: six digits, 10-minute validity, at most five attempts, 60-second resend cooldown and five sends per email per hour. IP limits also cover all auth endpoints. Only keyed hashes of codes are stored; pending signup passwords are hashed. Challenge IDs are random and codes are consumed atomically with account/session creation.
- A resend replaces the earlier code. The email challenges survive restart. Expired challenges are removed on subsequent requests. Limits expire after an hour.
- A paid order queues mail only for a verified account. Authorized/pending/failed payments do not. Existing purchases are not automatically bulk-emailed.
- Every 30 seconds the app retries due queued messages. A persisted lease prevents simultaneous workers from sending independently. Retries use the same saved message and provider idempotency key. Resend retains keys for 24 hours: https://resend.com/docs/dashboard/emails/idempotency-keys.
- After 10 attempts or 23 hours since the first attempt, the job becomes `needs_review` instead of risking a duplicate after the provider's idempotency window. Inspect `paymentOrders[].thankYouEmail` in the app-state database and the Resend logs. `sent` means the provider accepted the message. Do not blindly clear a sent/uncertain job or change its idempotency key; verify delivery before manually retrying.
- Mail outages do not undo a confirmed subscription. A failed OTP send does not create an account; the user can retry after the cooldown.

Tests: `node --test server/email.test.mjs server/email-http.test.mjs server/payments.test.mjs server/backend-api.test.mjs`. Optional browser check: `node scripts/check_email_verification_ui.cjs` (uses the same local Playwright installation as existing UI scripts).
