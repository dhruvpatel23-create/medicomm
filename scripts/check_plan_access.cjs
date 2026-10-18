const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { once } = require('node:events');
const assert = require('node:assert/strict');

(async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'medulla-plan-access-'));
  const { issueSession } = await import('../server/security.mjs');
  const { preview } = await import('vite');
  const plans = ['free', 'lite', 'ultra', 'premium'];
  const seed = { users: plans.map(plan => ({ id: plan, name: `${plan} Learner`, email: `${plan}@example.test`, medicalCollege: 'Test College', ...(plan === 'free' ? {} : { plan }) })), sessions: {}, paymentOrders: [] };
  const tokens = Object.fromEntries(plans.map(plan => [plan, issueSession(seed, plan)]));
  await fs.writeFile(path.join(root, 'users.json'), JSON.stringify(seed));
  let child, frontend, browser;
  try {
    const origin = 'http://127.0.0.1:4198';
    child = spawn(process.execPath, ['server.mjs'], { env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', RUNTIME_DATA_DIR: root, PORT: '0', HOST: '127.0.0.1', SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '', APP_ORIGINS: origin }, stdio: ['ignore', 'pipe', 'pipe'] });
    const backend = await new Promise((resolve, reject) => {
      let output = '';
      const timer = setTimeout(() => reject(new Error(output || 'Startup timed out')), 45000);
      child.on('error', reject);
      child.once('exit', code => { clearTimeout(timer); reject(new Error(`Server exited ${code}: ${output}`)); });
      child.stderr.on('data', c => { output += c; });
      child.stdout.on('data', c => { output += c; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); } });
    });
    frontend = await preview({ build: { outDir: 'output/plan-access-build' }, preview: { host: '127.0.0.1', port: 4198, strictPort: true, proxy: { '/api': backend } } });
    browser = await chromium.launch({ headless: true, channel: 'msedge' });
    await fs.mkdir('output/plan-access-ui', { recursive: true });
    for (const plan of plans) {
      const headers = { Cookie: `medicomm_session=${tokens[plan]}`, Origin: origin, 'Content-Type': 'application/json' };
      const bankResponse = await fetch(`${backend}/api/practice`, { headers });
      assert.equal(bankResponse.status, plan === 'free' ? 403 : 200);
      if (plan !== 'free') {
        const bank = await bankResponse.json();
        assert.equal(bank.usmleModules.length > 0, plan === 'premium');
        assert.ok(bank.fmgeSessions.length > 0);
      }
      const theory = await fetch(`${backend}/api/short-notes/custom`, { headers });
      assert.equal(theory.status === 403, ['free', 'lite'].includes(plan));
      const tests = await fetch(`${backend}/api/practice/fmge-tests`, { headers });
      assert.equal(tests.status, plan === 'premium' ? 200 : 403);
      const inbox = await fetch(`${backend}/api/direct-messages/open`, { method: 'POST', headers, body: JSON.stringify({ targetUserId: plan === 'premium' ? 'lite' : 'premium' }) });
      assert.equal(inbox.status, plan === 'free' ? 403 : 200);
      const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
      await context.addCookies([{ name: 'medicomm_session', value: tokens[plan], url: origin, httpOnly: true, sameSite: 'Lax' }]);
      const page = await context.newPage();
      page.setDefaultTimeout(45000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(origin);
      await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
      await page.locator('.practice-path-card').first().waitFor();
      assert.equal(await page.locator('.practice-path-card').count(), 8);
      assert.equal(await page.locator('.practice-path-action').filter({ hasText: 'Unlock practice' }).count(), { free: 8, lite: 4, ultra: 3, premium: 0 }[plan]);
      if (plan !== 'premium') {
        await page.locator('.practice-path-card').filter({ hasText: plan === 'free' ? 'NEET PG / INICET' : plan === 'lite' ? 'THEORY' : 'USMLE' }).click();
        await page.getByRole('dialog').waitFor();
        assert.match(await page.getByRole('dialog').innerText(), plan === 'ultra' ? /Premium/ : plan === 'lite' ? /Ultra or Premium/ : /Lite, Ultra, or Premium/);
        await page.getByRole('button', { name: 'Keep Exploring', exact: true }).click();
        assert.equal(await page.locator('.practice-path-card').count(), 8);
      }
      if (plan === 'free') {
        await page.setViewportSize({ width: 390, height: 844 });
        await page.screenshot({ path: 'output/plan-access-ui/free-mobile.png', fullPage: true });
        await page.locator('.practice-path-card').filter({ hasText: 'THEORY' }).click();
        await page.getByRole('dialog').waitFor();
        await page.screenshot({ path: 'output/plan-access-ui/free-unlock-mobile.png', fullPage: true });
        await page.getByRole('button', { name: 'Keep Exploring', exact: true }).click();
        await page.locator('.mobile-nav').getByRole('button', { name: 'Communities', exact: true }).click();
        await page.getByRole('button', { name: 'Unlock Personal Inbox', exact: true }).click();
        await page.getByRole('dialog').waitFor();
        await page.getByRole('button', { name: 'Keep Exploring', exact: true }).click();
      }
      assert.deepEqual(errors, [], plan);
      await context.close();
      console.log(`${plan}: API restrictions, visible features, and lock flow passed`);
    }
  } finally {
    await browser?.close();
    await new Promise(resolve => frontend ? frontend.httpServer.close(resolve) : resolve());
    if (child && child.exitCode === null) { child.kill(); await once(child, 'exit'); }
    // Remove only the isolated directory created above inside the OS temp directory.
    if (path.dirname(root) !== path.resolve(os.tmpdir())) throw new Error('Unexpected test directory');
    await fs.rm(root, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
