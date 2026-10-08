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
    await navigate('Dashboard');
    await page.getByText('Your next question awaits', { exact: true }).waitFor();
    assert(await page.getByTestId('dashboard-summary').getByText('0 days', { exact: true }).isVisible());
    await page.getByLabel('Exam name', { exact: true }).fill('My university exam');
    await page.getByLabel('Target exam date').fill('2027-03-01');
    await page.getByLabel('Weekly question target').fill('150');
    await page.getByRole('button', { name: 'Save goal', exact: true }).click();
    await page.getByRole('heading', { name: 'My university exam' }).waitFor();
    const bank = await (await context.request.get(`${backend}/api/practice`)).json();
    const subject = bank.subjects.find(subject => subject.questions.length > 1);
    const question = subject.questions[0];
    const recorded = await context.request.post(`${backend}/api/practice/attempts`, { headers: { Origin: 'http://127.0.0.1:4190' }, data: { id: 'browser-attempt-001', mode: 'pyq', subjectId: subject.id, questionId: question.id, selectedAnswer: question.answer, durationSeconds: 90 } });
    assert.equal(recorded.status(), 200, await recorded.text());
    await page.getByRole('button', { name: 'Refresh dashboard' }).click();
    await page.getByText('1 day', { exact: true }).first().waitFor();
    await page.getByRole('button', { name: 'Resume practice', exact: true }).click();
    await page.getByRole('button', { name: /Check answer/ }).waitFor().catch(async error => { console.error((await page.locator('.app-view').innerText()).slice(0, 3000)); console.error(errors); throw error; });
    await page.locator('.option-card').first().click();
    await Promise.all([page.waitForResponse(response => response.url().endsWith('/api/practice/attempts') && response.status() === 200), page.getByRole('button', { name: /Check answer/ }).click()]);
    await navigate('Dashboard'); await page.getByText('2 answered today', { exact: true }).waitFor();
    await fs.mkdir('output/account-ui', { recursive: true });
    await page.evaluate(() => { document.documentElement.dataset.theme = 'dark'; window.scrollTo(0, 0); });
    await page.screenshot({ path: 'output/account-ui/dashboard-dark.png', fullPage: true });
    await navigate('Profile'); await page.getByTestId('profile-overview').getByText('#1', { exact: true }).first().waitFor();
    await page.screenshot({ path: 'output/account-ui/profile-dark.png', fullPage: true });
    const image = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=', 'base64');
    await page.getByLabel('Change profile photo').setInputFiles({ name: 'avatar.png', mimeType: 'image/png', buffer: image });
    await page.getByRole('button', { name: 'Save photo', exact: true }).click();
    await page.getByTestId('profile-overview').getByText('Profile photo saved.', { exact: true }).waitFor();
    const saved = await (await context.request.get(`${backend}/api/auth/session`)).json();
    assert(saved.user.profileImageUrl.startsWith('/uploads/user-'));
    await page.getByLabel('Name', { exact: true }).fill('Aanya Updated');
    await page.getByRole('button', { name: 'Save profile', exact: true }).click();
    await page.getByTestId('profile-overview').getByRole('heading', { name: 'Aanya Updated' }).waitFor();
    await page.reload(); await navigate('Profile');
    assert.equal(await page.getByLabel('Name', { exact: true }).inputValue(), 'Aanya Updated');
    await page.route('**/uploads/user-*', route => route.abort());
    await page.reload(); await navigate('Profile');
    await page.getByTestId('profile-overview').getByText('AU', { exact: true }).waitFor();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => document.documentElement.dataset.theme = 'light');
    await page.screenshot({ path: 'output/account-ui/profile-mobile.png', fullPage: true });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.setViewportSize({ width: 1440, height: 1050 });
    await navigate('Dashboard'); await page.getByRole('heading', { name: 'My university exam' }).waitFor();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: 'output/account-ui/dashboard-mobile.png', fullPage: true });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
    console.log('PASS: real backend account stats, practice submission, resume, goal persistence, photo upload, profile save/reload, broken-photo fallback, dark/light mobile layouts.');
  } finally {
    if (browser) await browser.close();
    if (child.exitCode === null) { child.kill(); await once(child, 'exit'); }
    const resolved = path.resolve(root);
    if (!resolved.startsWith(path.resolve(os.tmpdir()) + path.sep) || !path.basename(resolved).startsWith('medulla-account-ui-')) throw new Error('Unexpected cleanup path');
    await fs.rm(resolved, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exit(1); });
