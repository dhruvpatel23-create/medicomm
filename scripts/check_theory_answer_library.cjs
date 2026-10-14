const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const { createShortNotesHandler } = await import('../server/shortNotes.mjs');
  const { decodeImage } = await import('../server/uploads.mjs');
  const questions = [{ id: 'library-one', prompt: 'Describe the anatomy of the heart', kind: 'short-note', emphasis: 1 },
    { id: 'library-two', prompt: 'Describe the brachial plexus', kind: 'long-answer' }];
  let db = { shortNoteReviews: [] }, fail = false, serial = 0;
  const images = new Map();
  const handler = createShortNotesHandler({
    questions: new Map(questions.map(q => [q.id, { ...q, subjectTitle: 'Anatomy', topicTitle: 'Anatomy' }])),
    readDatabase: () => structuredClone(db), writeDatabase: async next => { db = next; },
    requireSessionUser: () => ({ id: 'gesture-user' }), parseRequestBody: async req => req.body,
    sendJson: (res, status, body) => Object.assign(res, { status, body }),
    parseAnswerImage: value => value ? { mimeType: value.slice(5, value.indexOf(';')), data: value.split(',')[1] } : null,
    saveAnswerImage: async data => { const name = `user-test-${++serial}.png`; images.set(name, decodeImage(data)); return name; },
    removeAnswerImage: async name => images.delete(name),
    evaluate: async () => {
      if (fail) throw new Error('Temporary AI failure');
      return { score: 8, feedback: 'A clear answer; add the applied anatomy.', strengths: ['Clear structure'], improvements: ['Add clinical relevance'],
        modelAnswerSections: [{ label: 'A', heading: 'Heart', points: ['Definition: The heart is a muscular pump.', 'Applied anatomy: Coronary arterial supply.'] }],
        textbookSources: [{ book: "B. D. Chaurasia's Human Anatomy", topic: 'Heart' }] };
    },
  });
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 1000 } });
    const errors = []; page.on('pageerror', error => errors.push(error.message));
    await page.route('**/answer-library-test*', route => route.fulfill({ contentType: 'text/html', body: `<html><body><div id="root"></div><script type="module">
      import RefreshRuntime from '/@react-refresh'; RefreshRuntime.injectIntoGlobalHook(window);
      window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => type => type;
      window.__vite_plugin_react_preamble_installed__ = true;
      await import('/scripts/notepad-gesture-harness.jsx');</script></body></html>` }));
    await page.route('**/short-notes.json', route => route.fulfill({ json: { source: { title: 'Bhalani PDF' }, subjects: [{ id: 'anatomy', title: 'Anatomy', topics: [{ id: 'topic', title: 'Anatomy', questions }] }] } }));
    await page.route('**/api/short-notes/reviews*', async route => {
      const request = route.request(), response = {};
      await handler({ method: request.method(), url: request.url(), body: request.method() === 'POST' ? request.postDataJSON() : {} }, response);
      await route.fulfill({ status: response.status, json: response.body });
    });
    await page.route('**/uploads/user-test-*', route => {
      const image = images.get(route.request().url().split('/').at(-1));
      return image ? route.fulfill({ contentType: image.mime, body: image.bytes }) : route.fulfill({ status: 404 });
    });
    await page.goto('http://127.0.0.1:4173/answer-library-test?review=1');
    const button = name => page.getByRole('button', { name, exact: true });
    const openFirst = async () => { await page.locator('.sn-topic-card').first().click(); await page.locator('.sn-question-row').first().click(); };
    const submit = async () => { await page.getByRole('checkbox').check(); await button('Submit for AI review').click(); };
    await openFirst();
    await page.getByRole('textbox', { name: 'Your theory answer' }).fill('My first answer with definition and anatomy.');
    await submit(); await page.getByRole('heading', { name: 'Your saved answer', exact: true }).waitFor();
    assert((await page.locator('.sn-saved-answer').innerText()).includes('My first answer'));
    assert(await page.evaluate(() => Boolean(document.querySelector('.sn-saved-answer').compareDocumentPosition(document.querySelector('.sn-review-top')) & Node.DOCUMENT_POSITION_FOLLOWING)));
    assert(!(await page.locator('body').innerText()).includes('Bhalani'));
    await button('Practise again').click();
    await page.getByRole('textbox', { name: 'Your theory answer' }).fill('An unfinished new draft');
    await button('Back to questions').click(); await page.locator('.sn-question-row').first().click();
    await page.getByRole('heading', { name: 'Your saved answer', exact: true }).waitFor();
    assert.equal(await page.getByRole('textbox', { name: 'Your theory answer' }).count(), 0, 'Saved response must open before an unfinished retry');
    await button('Practise again').click();
    assert.equal(await page.getByRole('textbox', { name: 'Your theory answer' }).inputValue(), 'An unfinished new draft');
    await page.getByRole('textbox', { name: 'Your theory answer' }).fill('');
    const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aWQAAAABJRU5ErkJggg==', 'base64');
    await page.locator('input[type=file][multiple]').setInputFiles([{ name: 'page-1.png', mimeType: 'image/png', buffer: png }, { name: 'page-2.png', mimeType: 'image/png', buffer: png }]);
    await page.getByAltText('Your handwritten answer page 2').waitFor();
    fail = true; await submit(); await page.getByRole('alert').filter({ hasText: 'Temporary AI failure' }).waitFor();
    assert.equal(images.size, 0); assert.equal(db.shortNoteReviews.length, 1);
    assert.equal(await page.locator('.sn-photo img').count(), 2);
    fail = false; await button('Submit for AI review').click();
    await page.getByAltText('Saved answer page 1', { exact: true }).waitFor();
    await page.getByRole('region', { name: 'Your saved answer' }).getByRole('button', { name: 'Next page' }).click();
    await page.getByAltText('Saved answer page 2').waitFor();
    await page.getByLabel('Saved attempt').selectOption('1');
    assert((await page.locator('.sn-saved-answer').innerText()).includes('My first answer'));
    await button('Practise again').click();
    await page.getByRole('button', { name: /^Notepad/ }).click();
    async function draw(offset) {
      const canvas = page.locator('.an-canvas'), bounds = await canvas.boundingBox();
      await page.mouse.move(bounds.x + 80, bounds.y + 100 + offset); await page.mouse.down();
      await page.mouse.move(bounds.x + 220, bounds.y + 130 + offset, { steps: 15 }); await page.mouse.up();
    }
    await draw(0); await button('Add page').click();
    await page.locator('.an-page-scale').evaluate(el => Promise.all(el.getAnimations().map(a => a.finished.catch(() => {}))));
    await draw(60); await button('Save answer').click(); await submit();
    await page.getByAltText('Saved answer page 1', { exact: true }).waitFor();
    assert.equal(db.shortNoteReviews[0].answerPages.length, 2);
    assert(db.shortNoteReviews[0].answerPages.every(item => item.source === 'notepad'));
    // Clearing local data simulates opening the account on another browser.
    await page.evaluate(() => localStorage.clear()); await page.reload(); await openFirst();
    await page.getByAltText('Saved answer page 1', { exact: true }).waitFor();
    assert.equal(await page.getByLabel('Saved attempt').locator('option').count(), 3);
    await page.getByRole('region', { name: 'Your saved answer' }).getByRole('button', { name: 'Next page' }).click();
    await page.getByAltText('Saved answer page 2').waitFor();
    fs.mkdirSync('output/answer-library', { recursive: true });
    await page.screenshot({ path: 'output/answer-library/desktop.png', fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: 'output/answer-library/mobile.png', fullPage: true });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await button('Back to questions').click(); await button('My answers').click();
    assert.equal(await page.locator('.sn-question-row').count(), 1);
    await button('All questions').click(); await page.locator('.sn-question-row').nth(1).click();
    await page.getByRole('textbox', { name: 'Your theory answer' }).waitFor();
    assert.equal(await page.getByRole('region', { name: 'Your saved answer' }).count(), 0);
    assert.deepEqual(errors, []);
    console.log('PASS: real library handler with mocked AI/storage; typed/photo/notepad answers, ordered pages, history, retry cleanup, saved-first reopening, cleared-browser recovery, My answers filter, mobile and question isolation.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
