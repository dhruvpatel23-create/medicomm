# Password recovery

Sign in → Forgot password sends a single-use recovery link to the account email. It expires in 15 minutes. Resetting preserves the user ID, subscription, progress and saved content, updates the password, verifies the email and invalidates all existing application sessions. Linked Google refresh tokens are revoked too. Google-only accounts may use recovery to add a password.

The existing email service must be configured on the server: `RESEND_API_KEY` and `EMAIL_FROM` (a sender verified in Resend). Keep credentials outside Git. If they are already configured, no additional email settings are needed. Delivery has not been verified against the production provider by this change.

Links use a trusted application origin from `APP_ORIGINS`, preferring `https://medullaprep.com`. Set optional `PASSWORD_RESET_ORIGIN=https://medullaprep.com` to choose another allowed origin. Tokens travel in the URL fragment, are removed from the browser address bar, and are stored only as hashes on the server. Requests use generic responses and email/IP rate limits.

Deploy on the VPS:

```sh
cd /var/www/medullaprep.com
git pull --ff-only origin main
npm run build
pm2 restart medullaprep
```

If adding email environment variables through the PM2 configuration, load that configuration and save it with `pm2 save`, preserving the existing Firebase environment. Ordinary code deployment uses the restart above. No database import or migration rerun is needed.
