const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');
const bank = require('../data/fmge-question-bank.json');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
    page.setDefaultTimeout(45000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://127.0.0.1:4173');
    await page.getByRole('button', { name: 'Explore as guest' }).click();
    const openYears = async () => {
      await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
      await page.getByRole('button', { name: /Medical licensing.*FMGE/ }).click();
      await page.getByRole('button', { name: 'Explore 2018', exact: true }).waitFor();
    };
    const openSession = async (session) => {
      await page.getByRole('button', { name: `Explore ${session.year}`, exact: true }).click();
      if (bank.sessions.filter(s => s.year === session.year).length > 1) {
        await page.getByRole('button', { name: `Start ${session.month} ${session.year}`, exact: true }).click();
      }
      await page.locator('.fmge-session').waitFor();
    };
    await openYears();
    assert.equal(await page.locator('.usmle-module-card').count(), 8);
    await page.screenshot({ path: 'output/fmge-years-desktop.png', fullPage: true });
    for (const session of bank.sessions) {
      await openSession(session);
      assert.equal(await page.locator('.practice-question-status').count(), session.questions.length);
      assert.equal(await page.locator('.option-card').count(), 4);
      assert((await page.locator('.fmge-session h3').first().innerText()).includes(session.questions[0].prompt));
      await page.getByRole('button', { name: 'Back to years', exact: true }).click();
    }
    const january = bank.sessions.find(s => s.id === 'fmge-2025-january');
    await page.getByRole('button', { name: 'Explore 2025', exact: true }).click();
    assert.equal(await page.locator('.usmle-module-card').count(), 2);
    assert((await page.locator('.usmle-module-card').first().innerText()).includes('Parts 1 & 2'));
    await page.screenshot({ path: 'output/fmge-months-desktop.png', fullPage: true });
    await page.getByRole('button', { name: 'Start January 2025', exact: true }).click();
    const imageIndex = january.questions.findIndex(q => q.imageUrls.length && q.explanationImageUrls.length);
    assert(imageIndex >= 0);
    const question = january.questions[imageIndex];
    await page.locator('.practice-question-status').nth(imageIndex).click();
    assert.equal(await page.locator('.practice-question-image').count(), question.imageUrls.length);
    await page.locator('.practice-question-image').first().evaluate(img => img.decode());
    await page.getByRole('button', { name: /Save question/ }).click();
    await page.locator('.option-card').nth(question.answerIndex).click();
    await page.getByRole('button', { name: /Check answer/ }).click();
    await page.locator('.feedback-good').waitFor();
    assert.equal(await page.locator('.practice-question-image').count(), question.imageUrls.length + question.explanationImageUrls.length);
    assert((await page.locator('.feedback-box').innerText()).replace(/\s+/g, ' ').includes(question.explanation.replace(/\s+/g, ' ').slice(0, 80)));
    await page.screenshot({ path: 'output/fmge-question-explanation.png', fullPage: true });
    const partTwoIndex = january.questions.findIndex(q => q.part === 2);
    await page.locator('.practice-question-status').nth(partTwoIndex).click();
    assert((await page.locator('.quiz-meta').innerText()).includes('Part 2'));
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({ path: 'output/fmge-question-mobile.png', fullPage: true });
    await page.getByRole('button', { name: 'Back to years', exact: true }).click();
    assert((await page.locator('.usmle-module-card').last().innerText()).includes('1 / 443 answered'));
    await page.screenshot({ path: 'output/fmge-years-mobile.png', fullPage: true });
    await page.setViewportSize({ width: 1440, height: 1050 });
    await page.locator('.shell-nav').getByRole('button', { name: 'Bookmarks', exact: true }).click();
    await page.getByRole('button', { name: /Review question/ }).first().click();
    await page.getByRole('button', { name: 'Back to years', exact: true }).waitFor();
    assert((await page.locator('.fmge-session h3').first().innerText()).includes(question.prompt));
    await page.reload();
    await page.getByRole('button', { name: 'Explore as guest' }).click();
    await openYears();
    assert((await page.locator('.usmle-module-card').last().innerText()).includes('1 / 443 answered'));
    await page.getByRole('button', { name: 'Back', exact: true }).click();
    await page.locator('.practice-path-red').click();
    assert.equal(await page.locator('.usmle-module-card').count(), 10);
    assert.deepEqual(errors, []);
    console.log('PASS: all 12 sessions, 8 years, month groups, both January parts, image loading, hidden solution images, answer review, bookmarks, persisted progress, mobile overflow, and USMLE regression.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
