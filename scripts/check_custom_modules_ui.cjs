// Run against Vite preview on port 4190 with isolated prepared-question fixtures.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
    const errors = []; page.on('pageerror', error => errors.push(error.message));
    const makeQuestions = (subjectId, count) => Array.from({ length: count }, (_, index) => ({ id: `${subjectId}-${index}`, subjectId, source: 'ai', prompt: `${subjectId} prepared question ${index + 1}`, chapterTitle: index < 12 ? 'Chapter One' : 'Chapter Two', topic: 'Prepared topic', options: ['First choice', 'Second choice', 'Third choice', 'Fourth choice'], answerIndex: 0, answer: 'First choice', explanation: 'REVIEW_ONLY_EXPLANATION', imageUrls: [] }));
    const aiSubjects = [{ id: 'anatomy', title: 'Anatomy', questions: makeQuestions('anatomy', 24) }, { id: 'physiology', title: 'Physiology', questions: makeQuestions('physiology', 12) }, { id: 'general-surgery', title: 'General Surgery', questions: [] }];
    const library = { exam: { title: 'Practice' }, years: [], subjects: aiSubjects.map(subject => ({ ...subject, questions: [] })), aiSubjects, usmleSubjects: [], usmleModules: [], fmgeSessions: [] };
    const user = { id: 'custom-ui', name: 'Custom Tester', email: 'custom@example.test', hasPracticeAccess: true, questionBookmarks: [] };
    let attempts = 0;
    await page.route('**/api/**', route => {
      const pathname = new URL(route.request().url()).pathname;
      if (pathname === '/api/auth/session') return route.fulfill({ json: { user } });
      if (pathname === '/api/practice') return route.fulfill({ json: library });
      if (pathname === '/api/communities') return route.fulfill({ json: { communities: [] } });
      if (pathname === '/api/practice/attempts') {
        const body = route.request().postDataJSON();
        assert.equal(body.mode, 'ai'); assert.match(body.id, /^[a-zA-Z0-9_-]{10,100}$/);
        attempts++; return route.fulfill({ json: { user } });
      }
      return route.fulfill({ status: 503, json: { message: 'Outside this navigation test' } });
    });
    const openCustom = async () => {
      await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
      await page.getByRole('button', { name: /CUSTOM MODULES/ }).click();
    };
    await page.goto('http://127.0.0.1:4190', { waitUntil: 'domcontentloaded' });
    await openCustom();
    await page.getByRole('heading', { name: 'A test built around you.' }).waitFor();
    assert(await page.getByRole('button', { name: 'Start 10-question test' }).isDisabled());
    assert(await page.getByRole('checkbox', { name: 'Select all General Surgery chapters' }).isDisabled());
    const anatomy = page.locator('.custom-subject').filter({ hasText: 'Anatomy' });
    await anatomy.locator('summary').click();
    await anatomy.getByRole('checkbox', { name: /Chapter One/ }).check();
    await page.getByRole('radio', { name: '20 questions', exact: true }).check();
    assert(await page.getByRole('button', { name: 'Start 20-question test' }).isDisabled());
    await page.getByRole('checkbox', { name: 'Select all Physiology chapters' }).check();
    assert(await page.getByRole('button', { name: 'Start 20-question test' }).isEnabled());
    await page.getByRole('radio', { name: '10 questions', exact: true }).check();
    await fs.mkdir('output/custom-modules', { recursive: true });
    await page.screenshot({ path: 'output/custom-modules/setup-desktop.png', fullPage: true });
    await page.getByRole('button', { name: 'Start 10-question test' }).click();
    await page.getByRole('heading', { name: 'Your focused test' }).waitFor();
    assert.equal(await page.getByText('REVIEW_ONLY_EXPLANATION').count(), 0);
    assert.equal(await page.getByText('Correct answer', { exact: true }).count(), 0);
    assert.equal(attempts, 0);
    await page.getByRole('radio', { name: /First choice/ }).click();
    await page.getByRole('button', { name: 'Mark for review', exact: true }).click();
    await page.getByRole('button', { name: 'Next', exact: true }).click();
    await page.getByRole('button', { name: 'Previous', exact: true }).click();
    assert.equal(await page.getByRole('radio', { name: /First choice/ }).getAttribute('aria-checked'), 'true');
    assert.equal(attempts, 0);
    // Simulate returning to a two-minute-old test and check that the timer is not reset.
    await page.evaluate(() => {
      const key = 'medulla-custom-module:custom-ui'; const saved = JSON.parse(sessionStorage.getItem(key));
      saved.startedAt = Date.now() - 120000; sessionStorage.setItem(key, JSON.stringify(saved));
    });
    await page.reload({ waitUntil: 'domcontentloaded' }); await openCustom();
    await page.getByRole('heading', { name: 'Your focused test' }).waitFor();
    assert.match(await page.getByLabel('Elapsed time').innerText(), /02:/);
    assert.equal(await page.getByRole('radio', { name: /First choice/ }).getAttribute('aria-checked'), 'true');
    assert.equal(await page.getByRole('button', { name: 'Marked for review', exact: true }).getAttribute('aria-pressed'), 'true');
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.screenshot({ path: 'output/custom-modules/test-mobile.png', fullPage: true });
    await page.getByRole('button', { name: 'Submit test', exact: true }).click();
    await page.getByRole('button', { name: 'Keep working', exact: true }).click();
    assert.equal(await page.getByText('REVIEW_ONLY_EXPLANATION').count(), 0);
    await page.getByRole('button', { name: 'Submit test', exact: true }).click();
    await page.getByRole('button', { name: 'Submit and reveal answers' }).click();
    await page.getByRole('heading', { name: 'Your results, in focus.' }).waitFor();
    await page.locator('.custom-review').first().getByText('REVIEW_ONLY_EXPLANATION').waitFor();
    assert.equal(await page.locator('.custom-result-stats strong').first().innerText(), '1 / 10');
    assert.equal(await page.getByRole('radio').count(), 0);
    await page.screenshot({ path: 'output/custom-modules/results-mobile.png', fullPage: true });
    await page.waitForFunction(() => !JSON.parse(localStorage.getItem('medicomm-pending-attempts:custom-ui') || '[]').length);
    assert.equal(attempts, 1);
    for (const count of [20, 30]) {
      await page.getByRole('button', { name: 'Build another test' }).click();
      await page.getByRole('button', { name: 'Select all', exact: true }).click();
      await page.getByRole('radio', { name: `${count} questions`, exact: true }).check();
      await page.getByRole('button', { name: `Start ${count}-question test` }).click();
      assert.equal(await page.getByRole('navigation', { name: 'Question navigator' }).getByRole('button').count(), count);
      await page.getByRole('button', { name: 'Submit test', exact: true }).click();
      await page.getByRole('button', { name: 'Submit and reveal answers' }).click();
      await page.getByRole('heading', { name: 'Your results, in focus.' }).waitFor();
      assert.equal(await page.locator('.custom-result-stats strong').nth(2).innerText(), String(count));
    }
    assert.equal(attempts, 1);
    assert.deepEqual(errors, []);
    console.log('PASS: subject/chapter filters, 10/20/30 questions, timer and answer resume, mobile layout, delayed answers, scoring, and submission-only progress sync.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
