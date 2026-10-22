const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
(async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'medulla-first-attempt-'));
  const { issueSession } = await import('../server/security.mjs');
  const seed = { users: [{ id: 'live-test', name: 'Live Tester', email: 'live@example.test', rating: 1480 }], sessions: {}, paymentOrders: [{ orderId: 'fixture', userId: 'live-test', status: 'paid', paymentId: 'paid', verifiedAt: new Date().toISOString() }] };
  const token = issueSession(seed, 'live-test');
  await fs.writeFile(path.join(root, 'users.json'), JSON.stringify(seed));
  const socket = require('node:net').createServer();
  await new Promise(resolve => socket.listen(0, '127.0.0.1', resolve));
  const port = socket.address().port; await new Promise(resolve => socket.close(resolve));
  const child = spawn(process.execPath, ['server.mjs'], { env: { ...process.env, NODE_ENV: 'test', LOAD_ENV_FILES: 'false', RUNTIME_DATA_DIR: root, PORT: String(port), APP_ORIGINS: `http://127.0.0.1:${port}`, HOST: '127.0.0.1', SUPABASE_URL: '', SUPABASE_SECRET_KEY: '', SUPABASE_SERVICE_ROLE_KEY: '', SUPABASE_SERVICE_KEY: '', SUPABASE_UPLOAD_BUCKET: '' }, stdio: ['ignore', 'pipe', 'pipe'] });
  let browser;
  try {
    const backend = await new Promise((resolve, reject) => {
      let output = ''; const timer = setTimeout(() => reject(new Error(output || 'Startup timeout')), 30000);
      child.on('error', reject); child.on('exit', code => { clearTimeout(timer); reject(new Error(`Exit ${code}: ${output}`)); });
      child.stderr.on('data', chunk => output += chunk);
      child.stdout.on('data', chunk => { output += chunk; const match = output.match(/listening on http:\/\/127.0.0.1:(\d+)/); if (match) { clearTimeout(timer); resolve(`http://127.0.0.1:${match[1]}`); } });
    });
    browser = await chromium.launch({ headless: true, channel: 'msedge' });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    await context.addCookies([{ name: 'medicomm_session', value: token, url: backend, httpOnly: true, sameSite: 'Lax' }]);
    const library = await (await context.request.get(`${backend}/api/practice`)).json();
    const subject = library.aiSubjects.find(s => s.id === 'anatomy');
    const questions = subject.questions.filter(q => !q.locked).slice(0, 2).map(q => ({ ...q, chapterTitle: 'First attempt check', topic: 'Live rewards' }));
    assert.equal(questions.length, 2);
    const fixture = { ...library, aiSubjects: [{ ...subject, questions }] };
    await context.route('**/api/practice', route => route.fulfill({ json: fixture }));
    const a = await context.newPage(), b = await context.newPage();
    const errors = []; for (const page of [a, b]) { page.setDefaultTimeout(30000); page.on('pageerror', e => { errors.push(e.message); console.error(e.message); }); }
    async function practice(page) {
      await page.goto(backend, { waitUntil: 'domcontentloaded' });
      await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click().catch(async e => { console.error((await page.locator('body').innerText()).slice(0,3000)); throw e; });
      await page.getByRole('button', { name: /TOPIC WISE questions/ }).click();
      await page.locator('.practice-subject-card').filter({ hasText: 'Anatomy' }).click();
      await page.locator('.chapter-directory-row').filter({ hasText: 'First attempt check' }).click();
      await page.locator('.topic-directory-row').filter({ hasText: 'Live rewards' }).click();
      await page.locator('.option-card').first().waitFor();
    }
    await practice(a); await practice(b);
    await a.getByRole('button', { name: questions[0].answer, exact: true }).click();
    for (const page of [a, b]) {
      await page.locator('.first-attempt-badge').waitFor();
      await page.locator('.practice-live-rating').filter({ hasText: '1481 Elo' }).waitFor();
      assert.match(await page.locator('.practice-question-status-first').innerText(), /1st attempt/);
    }
    await a.getByText('+1 Elo earned', { exact: true }).waitFor();
    await fs.mkdir('output/first-attempt-ui', { recursive: true });
    await a.evaluate(() => document.documentElement.dataset.theme = 'dark');
    await a.screenshot({ path: 'output/first-attempt-ui/question-dark.png', fullPage: true });
    await a.setViewportSize({ width: 390, height: 844 });
    await a.screenshot({ path: 'output/first-attempt-ui/question-mobile.png', fullPage: true });
    assert(await a.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await a.setViewportSize({ width: 1440, height: 1000 });
    await a.getByRole('button', { name: 'Next question', exact: true }).click();
    await Promise.all([a.waitForResponse(r => r.url().endsWith('/api/practice/attempts') && r.ok()), a.getByRole('button', { name: questions[1].options.find(o => o !== questions[1].answer), exact: true }).click()]);
    await practice(a); await a.getByRole('button', { name: 'Next question', exact: true }).click();
    await Promise.all([a.waitForResponse(r => r.url().endsWith('/api/practice/attempts') && r.ok()), a.getByRole('button', { name: questions[1].answer, exact: true }).click()]);
    assert.equal(await a.locator('.first-attempt-badge').count(), 0);
    assert.match(await a.locator('.practice-live-rating').innerText(), /1481 Elo/);
    await a.goto(backend, { waitUntil: 'domcontentloaded' });
    await a.getByRole('tab', { name: /Rating & Leaderboards/ }).click();
    await a.getByText('1st attempt · +1 Elo', { exact: true }).waitFor();
    await a.screenshot({ path: 'output/first-attempt-ui/home-rating.png', fullPage: true });
    assert.deepEqual(errors, []);
    console.log('PASS: visible first-attempt badge, immediate +1, live second-tab sync, persisted wrong-first rule, mobile layout, home explanation.');
  } finally { if (browser) await browser.close(); child.kill(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
