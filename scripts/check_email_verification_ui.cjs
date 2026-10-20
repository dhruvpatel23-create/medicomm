const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const { build } = require('esbuild');
const assert = require('node:assert/strict');
(async () => {
  const bundle = await build({ stdin: { contents: `import React from 'react'; import { createRoot } from 'react-dom/client';
    import EmailVerification from './src/components/EmailVerification.jsx';
    createRoot(document.getElementById('root')).render(<EmailVerification challenge={{ challengeId: 'test', email: 'learner@example.test', resendAfter: 1 }}
      onVerified={data => { window.verified = data.user.id; }} onCancel={() => { window.cancelled = true; }} />);`,
    resolveDir: process.cwd(), loader: 'jsx' }, bundle: true, write: false, jsx: 'automatic', define: { 'process.env.NODE_ENV': '"test"' } });
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage(); let resends = 0;
    await page.route('http://email.test/**', async route => {
      const url = route.request().url();
      if (url.endsWith('/api/auth/verify-email')) {
        const payload = route.request().postDataJSON(); assert.equal(payload.challengeId, 'test');
        return route.fulfill({ status: payload.code === '123456' ? 200 : 400, json: payload.code === '123456' ? { user: { id: 'learner' } } : { message: 'Incorrect verification code. Please try again.' } });
      }
      if (url.endsWith('/api/auth/resend-email')) { resends++; return route.fulfill({ json: { resendAfter: 60 } }); }
      return route.fulfill({ contentType: 'text/html', body: '<html><body><div id="root"></div></body></html>' });
    });
    await page.goto('http://email.test/'); await page.addScriptTag({ content: bundle.outputFiles[0].text });
    const input = page.getByLabel('Email verification code'); await input.fill('abc12'); assert.equal(await input.inputValue(), '12');
    await input.fill('000000'); await page.getByRole('button', { name: 'Verify email and continue' }).click();
    await page.getByRole('status').filter({ hasText: 'Incorrect verification code' }).waitFor();
    const resend = page.getByRole('button', { name: 'Resend code', exact: true }); await resend.click();
    await page.getByRole('status').filter({ hasText: 'A new code has been sent' }).waitFor();
    assert.equal(resends, 1); assert.equal(await input.inputValue(), '');
    await input.fill('123456'); await page.getByRole('button', { name: 'Verify email and continue' }).click();
    await page.waitForFunction(() => window.verified === 'learner');
    console.log('OTP UI passed: numeric input, errors, resend cooldown, and successful verification.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
