const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

(async () => {
  const source = fs.readFileSync('server.mjs', 'utf8');
  const context = vm.createContext({ normalizeQuestion: q => q, readFmgeSessions: () => [], readUsmleModules: () => [] });
  vm.runInContext(source.slice(source.indexOf('function buildPracticeLibrary('), source.indexOf('function collectQuestionImageUrls(')), context);
  const question = { id: 'pyq', source: 'official', year: 2024, examTitle: 'NEET PG 2024', prompt: 'PYQ fixture question', options: ['One', 'Two', 'Three', 'Four'], answer: 'One', explanation: 'Explanation', topic: 'Anatomy', subjectId: 'anatomy' };
  const sources = ['official', 'ai', 'usmle', 'topic-wise', 'fmge', 'unknown'];
  const bank = { exam: { title: 'NEET PG / INI-CET', questionCount: 7 }, years: [{ id: 'first-year', title: 'First year', subtitle: 'Basic sciences', subjectIds: ['anatomy', 'empty'] }],
    subjects: [{ id: 'anatomy', title: 'Anatomy', questions: [...sources.map(s => ({ ...question, id: s, source: s })), { ...question, id: 'legacy', source: undefined }] }, { id: 'empty', title: 'Empty subject', questions: [] }] };
  const library = context.buildPracticeLibrary(bank);
  assert.deepEqual(Array.from(library.subjects[0].questions, q => q.id), ['official', 'legacy']);
  assert.equal(library.aiSubjects[0].questions[0].source, 'ai');
  const { filterPracticeLibraryForUi } = await import('../src/lib/practiceImageVisibility.js');
  assert.deepEqual(filterPracticeLibraryForUi(bank).subjects[0].questions.map(q => q.id), ['official', 'legacy']);
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const errors = []; page.on('pageerror', error => { errors.push(error.message); console.error('Browser error:', error.stack); });
    await page.route('**/api/**', route => {
      const url = new URL(route.request().url());
      if (url.pathname === '/api/auth/session') return route.fulfill({ json: { user: { id: 'pyq-test', name: 'Learner', email: 'learner@example.test', rating: 1480, hasPracticeAccess: true } } });
      // Include polluted cached-style subjects to exercise the client guard too.
      if (url.pathname === '/api/practice') return route.fulfill({ json: { ...library, subjects: bank.subjects } });
      if (url.pathname === '/api/dashboard') return route.fulfill({ status: 503, json: { message: 'Dashboard not needed for this test' } });
      return route.fulfill({ json: {} });
    });
    await page.goto('http://127.0.0.1:4173', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
    await page.locator('.practice-path-card').filter({ hasText: 'NEET PG / INICET' }).click();
    const directory = page.getByTestId('practice-subject-directory');
    await directory.waitFor();
    const text = await directory.innerText();
    assert(!/topic-wise|more subjects|practice format/i.test(text));
    assert.equal(await directory.getByRole('button', { name: 'Practice Empty subject', exact: true }).count(), 0);
    await page.getByRole('button', { name: 'Practice Anatomy', exact: true }).click();
    const chooser = page.getByRole('dialog');
    await chooser.getByRole('heading', { name: 'Anatomy PYQs' }).waitFor();
    assert(!/Topic Wise|USMLE|Mind Maps|AI Viva|Clinical Cases|All practice modes/.test(await chooser.innerText()));
    assert((await chooser.innerText()).includes('2 official questions'));
    await chooser.getByRole('button', { name: /All subjects/ }).click();
    assert.equal(await page.getByRole('dialog').count(), 0);
    await page.getByRole('button', { name: 'Practice Anatomy', exact: true }).click();
    await page.locator('.practice-year-choice-card').first().click();
    await page.getByText('PYQ fixture question', { exact: true }).waitFor();
    await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
    await page.locator('.practice-path-card').filter({ hasText: 'THEORY' }).click();
    await page.locator('.practice-subject-card').filter({ hasText: 'Anatomy' }).click();
    await page.getByRole('button', { name: /NOTE.*Short Notes/ }).waitFor();
    assert.deepEqual(errors, []);
    console.log('PASS: API and cache exclude non-PYQs; PYQ counts, direct year picker, subject navigation and question opening; separate Theory path remains available.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
