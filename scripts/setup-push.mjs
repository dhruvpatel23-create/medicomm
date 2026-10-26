import { readFileSync, appendFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import webpush from 'web-push';

const target = fileURLToPath(new URL('../.env.local', import.meta.url));
const files = ['../.env.local', '../.env'].map(file => new URL(file, import.meta.url));
const existing = files.filter(file => existsSync(file)).map(file => readFileSync(file, 'utf8')).join('\n');
if (/^VAPID_(?:PUBLIC|PRIVATE)_KEY=\S+/m.test(existing) || process.env.VAPID_PUBLIC_KEY || process.env.VAPID_PRIVATE_KEY) {
  console.log('Existing VAPID configuration found. Keeping the current keys.');
} else {
  const keys = webpush.generateVAPIDKeys();
  appendFileSync(target, `\n# Stable Web Push identity. Never commit or rotate casually.\nVAPID_PUBLIC_KEY=${keys.publicKey}\nVAPID_PRIVATE_KEY=${keys.privateKey}\nVAPID_SUBJECT=https://medullaprep.com\nPUSH_REMINDER_HOUR_IST=18\n`);
  console.log('Web Push keys saved to .env.local. Copy the VAPID values to your production server environment; restart the backend to activate.');
}
