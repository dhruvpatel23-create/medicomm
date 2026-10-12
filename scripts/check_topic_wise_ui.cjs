// Run against Vite preview on port 4190; uses isolated API fixtures.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
    const question = (id, chapterTitle, prompt) => ({ id, chapterTitle, prompt, topic: 'Shared topic', source: 'ai', subjectId: 'anatomy', options: ['A', 'B', 'C', 'D'], answer: 'A', answerIndex: 0, explanation: 'Explanation', imageUrls: [] });
    const library = {
      exam: { title: 'NEET PG PYQs' },
      years: [{ id: 'first-year', title: '1st Year', subjectIds: ['anatomy'] }, { id: 'final-year', title: 'Final Year', subjectIds: ['general-surgery'] }],
      subjects: [{ id: 'anatomy', title: 'Anatomy', questions: [] }, { id: 'general-surgery', title: 'General Surgery', questions: [] }],
      aiSubjects: [{ id: 'anatomy', title: 'Anatomy', questions: [question('a', 'Chapter A', 'Prepared question from chapter A'), question('b', 'Chapter B', 'Prepared question from chapter B')] }, { id: 'general-surgery', title: 'General Surgery', questions: [] }],
      usmleSubjects: [], usmleModules: [], fmgeSessions: [],
    };
    await page.route('**/api/**', route => {
      const pathname = new URL(route.request().url()).pathname;
      if (!['/api/auth/session', '/api/practice', '/api/communities'].includes(pathname)) return route.fulfill({ status: 503, json: { message: 'Not part of this isolated navigation test' } });
      const json = pathname === '/api/auth/session' ? { user: { id: 'topic-test', name: 'Topic Tester', email: 'topic@example.test', hasPracticeAccess: true, questionBookmarks: [] } }
        : pathname === '/api/practice' ? library : pathname === '/api/communities' ? { communities: [] } : {};
      return route.fulfill({ json });
    });
    await page.goto('http://127.0.0.1:4190', { waitUntil: 'domcontentloaded' });
    await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
    await page.getByRole('button', { name: /TOPIC WISE questions/ }).click();
    await page.getByRole('heading', { name: 'Topic-wise questions by subject', exact: true }).waitFor();
    const unavailable = page.locator('.practice-subject-card').filter({ hasText: 'General Surgery' });
    assert(await unavailable.isDisabled());
    assert.match(await unavailable.innerText(), /Coming soon/i);
    assert.equal(await page.getByText('Previous Year Questions', { exact: true }).count(), 0);
    await page.locator('.practice-subject-card').filter({ hasText: 'Anatomy' }).click();
    await page.getByRole('heading', { name: 'Choose a chapter', exact: true }).waitFor();
    assert.equal(await page.locator('.practice-choice-grid-formats').count(), 0);
    await page.locator('.chapter-directory-row').filter({ hasText: 'Chapter A' }).click();
    await page.getByRole('heading', { name: 'Chapter A', exact: true }).waitFor();
    await page.locator('.topic-directory-row').filter({ hasText: 'Shared topic' }).click();
    await page.getByText('Prepared question from chapter A', { exact: true }).waitFor();
    assert.equal(await page.getByRole('button', { name: /^Question 2,/ }).count(), 0);
    await page.getByRole('button', { name: 'Back to topics', exact: true }).click();
    await page.getByRole('button', { name: 'Back to chapters', exact: true }).click();
    await page.locator('.chapter-directory-row').filter({ hasText: 'Chapter B' }).click();
    await page.locator('.topic-directory-row').filter({ hasText: 'Shared topic' }).click();
    await page.getByText('Prepared question from chapter B', { exact: true }).waitFor();
    assert.deepEqual(errors, []);
    console.log('PASS: direct subject/chapter/topic/question navigation, Coming soon subjects, chapter isolation, and back navigation.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
