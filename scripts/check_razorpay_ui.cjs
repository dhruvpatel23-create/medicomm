// Run against the Vite preview on port 4190. PLAYWRIGHT_MODULE may point to a local installation.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { once } = require('node:events');
const assert = require('node:assert/strict');

(async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'medulla-account-ui-'));
  await fs.writeFile(path.join(root, 'users.json'), JSON.stringify({ users: [], sessions: {} }));
  const child = spawn(process.execPath, ['server.mjs'], { env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', RUNTIME_DATA_DIR: root, PORT: '0', HOST: '127.0.0.1', SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '', APP_ORIGINS: 'http://127.0.0.1:4190' }, stdio: ['ignore', 'pipe', 'pipe'] });
  let browser;
  try {
    const backend = await new Promise((resolve, reject) => {
      let output = ''; const timer = setTimeout(() => reject(new Error(output || 'Backend start timed out')), 20000);
      child.on('error', reject); child.on('exit', code => { clearTimeout(timer); reject(new Error(`Backend exited ${code}: ${output}`)); });
      child.stderr.on('data', chunk => output += chunk);
      child.stdout.on('data', chunk => { output += chunk; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); } });
    });
    browser = await chromium.launch({ headless: true, channel: 'msedge' });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1050 } });
    const signup = await context.request.post(`${backend}/api/auth/signup`, { data: { name: 'Aanya Learner', email: 'account-ui@example.test', medicalCollege: 'Test Medical College, Kerala', contactNumber: '9000000088', password: 'Secure-test-password-123' } });
    assert.equal(signup.status(), 201);
    const page = await context.newPage(); page.setDefaultTimeout(30000);
    const errors = []; page.on('pageerror', error => errors.push(error.message));
    // Forward to a real isolated backend; do not mock account data or mutations.
    await page.route('**/api/**', async route => route.fulfill({ response: await route.fetch({ url: backend + new URL(route.request().url()).pathname + new URL(route.request().url()).search }) }));
    await page.route('**/uploads/user-*', async route => route.fulfill({ response: await route.fetch({ url: backend + new URL(route.request().url()).pathname }) }));
    await page.goto('http://127.0.0.1:4190', { waitUntil: 'domcontentloaded' });
    const navigate = title => page.locator('.shell-nav').getByRole('button', { name: title, exact: true }).click();
    await page.evaluate(() => {
      window.checkoutMode = 'cancel';
      window.Razorpay = class {
        constructor(options) { this.options = options; window.checkoutOptions = options; }
        on(name, callback) { this.failed = callback; }
        close() { this.options.modal.ondismiss(); }
        open() {
          if (window.checkoutMode === 'cancel') this.options.modal.ondismiss();
          if (window.checkoutMode === 'failure') { this.failed({ error: { description: 'Test bank declined payment' } }); this.options.modal.ondismiss(); }
          if (window.checkoutMode === 'success') this.options.handler({ razorpay_order_id: this.options.order_id, razorpay_payment_id: 'pay_browser123', razorpay_signature: 'a'.repeat(64) });
        }
      };
    });
    let orderRequests = 0;
    let verifyRequests = 0;
    await page.route('**/api/create-order', async route => {
      orderRequests++;
      const body = route.request().postDataJSON();
      assert.equal(body.currency, 'INR'); assert.equal(body.planId, 'lite'); assert.equal(body.amount, 49900);
      await route.fulfill({ json: { order_id: 'order_browser123', amount: body.amount, currency: body.currency, key_id: 'rzp_test_browser', test_mode: true } });
    });
    await page.route('**/api/verify-payment', async route => {
      verifyRequests++;
      const body = route.request().postDataJSON();
      assert.equal(body.razorpay_order_id, 'order_browser123'); assert.equal(body.razorpay_payment_id, 'pay_browser123'); assert.equal(body.razorpay_signature, 'a'.repeat(64));
      await route.fulfill(verifyRequests === 1 ? { status: 500, json: { message: 'Temporary verification outage' } } : { json: { success: true, paid: true, test_mode: true, payment_id: 'pay_browser123' } });
    });
    await navigate('Pricing');
    await page.getByRole('button', { name: 'Get Lite', exact: true }).click();
    const pay = page.getByRole('button', { name: 'Pay securely with Razorpay', exact: true });
    await pay.click();
    await page.getByText('Checkout cancelled. No payment was confirmed.', { exact: true }).waitFor();
    const options = await page.evaluate(() => ({ key: window.checkoutOptions.key, amount: window.checkoutOptions.amount, email: window.checkoutOptions.prefill.email }));
    assert.equal(options.key, 'rzp_test_browser'); assert.equal(options.amount, 49900); assert.equal(options.email, 'account-ui@example.test');
    await page.evaluate(() => window.checkoutMode = 'failure'); await pay.click();
    await page.getByText('Test bank declined payment', { exact: true }).waitFor();
    await page.evaluate(() => window.checkoutMode = 'success'); await pay.click();
    await page.getByText(/Temporary verification outage/).waitFor();
    assert(await pay.isDisabled());
    await page.getByRole('button', { name: 'Check payment status', exact: true }).click();
    await page.getByText('Test payment confirmed. Reference: pay_browser123.', { exact: true }).waitFor();
    assert.equal(orderRequests, 3); assert.equal(verifyRequests, 2);
    assert.deepEqual(errors, []);
    await fs.mkdir('output/razorpay', { recursive: true });
    await page.screenshot({ path: 'output/razorpay/checkout.png', fullPage: true, animations: 'disabled' });
    console.log('PASS: browser checkout options, price selection, cancellation, failure, verification retry without another order, and confirmation (Razorpay simulated).');
  } finally {
    if (browser) await browser.close();
    if (child.exitCode === null) { child.kill(); await once(child, 'exit'); }
    const resolved = path.resolve(root);
    if (!resolved.startsWith(path.resolve(os.tmpdir()) + path.sep) || !path.basename(resolved).startsWith('medulla-account-ui-')) throw new Error('Unexpected cleanup path');
    await fs.rm(resolved, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exit(1); });
