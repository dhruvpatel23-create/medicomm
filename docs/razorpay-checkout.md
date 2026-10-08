# Razorpay Standard Checkout

React/Vite calls the existing Node HTTP backend. `razorpay` is server-only.
Local credentials belong in ignored `.env`; production ignores local env files.
Set `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in Render's Environment settings.
No frontend secret or build-time Vite credential is needed: create-order returns
the public key ID associated with the order.

## Test

1. Use Node 22, run `npm install`, then `npm run dev`.
2. Sign in, open Pricing, select Lite, Ultra or Premium, then click Pay securely
   with Razorpay. Annual prices are defined in `src/data/paymentPlans.js`.
3. Complete a Razorpay test-mode payment. Check cancellation and failed-payment
   messages too. Real money is not collected using test keys.
4. The server verifies the HMAC against its saved order, checks account ownership,
   and fetches the payment to confirm amount, currency and capture status. A valid
   signature with only authorization is shown as pending, not paid. Use Check
   payment status to retry verification without paying again.
5. Run `node --test server/payments.test.mjs server/backend-api.test.mjs`.

POST `/api/create-order` takes `{ planId, amount, currency }`; amount is integer
paise, at least 100, and must match the server catalog. Receipts are server-generated.
It returns `{ order_id, amount, currency, key_id, test_mode }`.
POST `/api/verify-payment` accepts the three Razorpay checkout callback fields.
Both endpoints require the existing authenticated session and allowed origin.
Orders and verification status use `paymentOrders` inside the existing database;
there are no new database tables or migrations.

## Production setup

Add the two credentials to Render, enable automatic payment capture in Razorpay,
and redeploy. For real payments, replace both test credentials with the matching
live pair. Never put the secret in a VITE_ variable or commit `.env`.

Apply PRELAUNCH on Pricing to reduce any plan's total to ₹9 (900 paise).
POST `/api/payment-quote` validates the code; order creation validates it again.
Only a captured payment with a verified signature grants Practice access and a
golden avatar. Access is derived from saved orders on each session/API request;
pending, failed and forged payments do not unlock Practice. This also applies to
test payments while testing with the configured test keys.

Practice, theory APIs and raw practice JSON require paid access. Annual checkout
is a one-time payment; automatic renewals, refunds and expiry are not implemented.
Pending callbacks received by this tab are kept in sessionStorage for verification
retries after reload. Webhook reconciliation for callbacks lost before reaching the
browser is not yet implemented; verify the payment from the original checkout tab.

Reference: https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/integration-steps/
