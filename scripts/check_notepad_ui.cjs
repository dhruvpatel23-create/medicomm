const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true });
    page.setDefaultTimeout(90000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    let submitted;
    let fail = true;
    await page.route('**/api/**', route => {
      if (route.request().url().endsWith('/api/practice')) return route.fulfill({ path: 'public/practice-question-bank.json', contentType: 'application/json' });
      if (route.request().url().endsWith('/api/short-notes/reviews')) {
        if (route.request().method() === 'GET') return route.fulfill({ json: { reviews: [] } });
        submitted = route.request().postDataJSON();
        if (fail) return route.fulfill({ status: 502, json: { message: 'Temporary review failure' } });
        return route.fulfill({ json: { review: { questionId: submitted.questionId, hasImage: true, score: 8, feedback: 'Good answer', strengths: ['Clear'], improvements: ['More detail'], modelAnswerSections: [] } } });
      }
      return route.fulfill({ json: {} });
    });
    await page.goto(process.env.NOTEPAD_TEST_URL || 'http://127.0.0.1:4174', { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: 'Explore as guest' }).click();
    await page.evaluate(() => localStorage.setItem('medicomm-session-token', 'notepad-test'));
    async function openQuestion() {
      await page.locator('.shell-nav').getByRole('button', { name: 'Practice', exact: true }).click();
      await page.locator('.practice-path-card').filter({ hasText: 'THEORY' }).click();
      await page.locator('.practice-subject-card').filter({ has: page.locator('.practice-subject-label', { hasText: /^Anatomy$/ }) }).click();
      await page.getByRole('button', { name: /NOTE.*Short Notes/ }).click();
      await page.locator('.sn-topic-card').first().click();
      await page.locator('.sn-question-row').first().click();
    }
    await openQuestion();
    await page.getByRole('button', { name: /Notepad Write/ }).click();
    fs.mkdirSync('output/notepad', { recursive: true });
    for (const viewport of [{ width: 1270, height: 587 }, { width: 1440, height: 1000 }, { width: 1024, height: 1366 }]) {
      await page.setViewportSize(viewport);
      const workspace = await page.locator('.an-workspace').boundingBox();
      const paper = await page.locator('.an-canvas').boundingBox();
      const visibleWidth = Math.min(workspace.x + workspace.width, paper.x + paper.width) - Math.max(workspace.x, paper.x);
      const visibleHeight = Math.min(workspace.y + workspace.height, paper.y + paper.height) - Math.max(workspace.y, paper.y);
      assert(visibleWidth >= viewport.width * 0.8, 'Visible writable sheet must occupy at least 80% of viewport width');
      assert(visibleHeight >= viewport.height * 0.8, 'Visible writable sheet must occupy at least 80% of viewport height');
      if (viewport.width === 1270) {
        await page.evaluate(() => document.documentElement.dataset.theme = 'dark');
        await page.screenshot({ path: 'output/notepad/short-screen.png' });
      }
    }
    await page.getByRole('button', { name: 'Save answer', exact: true }).click();
    await page.getByRole('alert').filter({ hasText: 'Write your answer' }).waitFor();
    const canvas = page.locator('.an-canvas');
    async function stroke(type = 'pen', id = 1) {
      await canvas.evaluate((element, { type, id }) => {
        const bounds = element.getBoundingClientRect();
        const send = (name, x, y) => element.dispatchEvent(new PointerEvent(name, { pointerId: id, pointerType: type, clientX: bounds.x + x, clientY: bounds.y + y, pressure: 0.6, bubbles: true }));
        // Synthetic pointer events cannot capture, but exercise the same drawing handlers.
        element.closest('.an-workspace').setPointerCapture = () => {};
        send('pointerdown', 70, 80);
        for (let i = 0; i < 40; i++) send('pointermove', 70 + i * 5, 80 + Math.sin(i / 3) * 15);
        send('pointerup', 265, 80);
      }, { type, id });
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    }
    const inkCount = () => canvas.evaluate(el => {
      const pixels = el.getContext('2d').getImageData(0, 0, el.width, el.height).data;
      let count = 0; for (let i = 3; i < pixels.length; i += 4) if (pixels[i]) count++;
      return count;
    });
    await stroke();
    const ink = await inkCount(); assert(ink > 100);
    assert(await page.getByRole('checkbox', { name: /Pencil only/ }).isChecked());
    await stroke('touch', 2); assert.equal(await inkCount(), ink);
    await page.getByRole('button', { name: 'Undo', exact: true }).click(); assert.equal(await inkCount(), 0);
    await page.getByRole('button', { name: 'Redo', exact: true }).click(); assert.equal(await inkCount(), ink);
    await page.getByRole('button', { name: 'Eraser', exact: true }).click(); await stroke(); assert((await inkCount()) < ink);
    await page.getByRole('button', { name: 'Undo', exact: true }).click(); assert.equal(await inkCount(), ink);
    await page.getByRole('button', { name: 'Clear sheet', exact: true }).click();
    await page.getByRole('button', { name: 'Clear', exact: true }).click(); assert.equal(await inkCount(), 0);
    await page.getByRole('button', { name: 'Undo', exact: true }).click(); assert.equal(await inkCount(), ink);
    await page.getByLabel('Paper style').selectOption('dotted');
    fs.mkdirSync('output/notepad', { recursive: true });
    await page.screenshot({ path: 'output/notepad/ipad.png' });
    await page.getByRole('button', { name: 'Close notepad' }).click();
    await page.getByRole('button', { name: 'Next question' }).click();
    await page.getByRole('button', { name: /Notepad Write/ }).click(); assert.equal(await inkCount(), 0);
    await page.getByRole('button', { name: 'Close notepad' }).click();
    await page.getByRole('button', { name: 'Previous question' }).click();
    await page.getByRole('button', { name: /Notepad Write/ }).click(); assert.equal(await inkCount(), ink);
    await page.getByRole('button', { name: 'Close notepad' }).click();
    // Restore a legacy single-page draft, including its original eraser semantics.
    await page.evaluate(() => {
      for (const key of Object.keys(localStorage).filter(key => key.startsWith('medicomm-notepad:'))) {
        const draft = JSON.parse(localStorage.getItem(key));
        if (draft.version === 2 && draft.pages.length === 1) localStorage.setItem(key, JSON.stringify({ version: 1, ...draft.pages[0] }));
      }
    });
    await page.reload(); await page.getByRole('button', { name: 'Explore as guest' }).click();
    await page.evaluate(() => localStorage.setItem('medicomm-session-token', 'notepad-test'));
    await openQuestion(); await page.getByRole('button', { name: /Notepad Write/ }).click();
    assert.equal(await inkCount(), ink); assert.equal(await page.getByLabel('Paper style').inputValue(), 'dotted');
    // Tool switching must not leave a captured eraser stroke or change ink into erasing.
    await page.getByRole('button', { name: 'Pen', exact: true }).click();
    await page.getByLabel('Pen style', { exact: true }).selectOption('brush');
    await page.getByRole('slider', { name: 'Tip thickness' }).fill('9');
    assert.equal(await page.getByRole('slider', { name: 'Tip thickness' }).inputValue(), '9');
    await page.getByRole('button', { name: 'Eraser', exact: true }).click();
    await page.getByRole('slider', { name: 'Eraser size' }).fill('64');
    await page.getByRole('button', { name: 'Blue ink', exact: true }).click();
    assert.equal(await page.getByRole('button', { name: 'Eraser', exact: true }).getAttribute('aria-pressed'), 'true');
    await page.getByRole('button', { name: 'Pen', exact: true }).click();
    assert.equal(await page.getByRole('slider', { name: 'Tip thickness' }).inputValue(), '9');
    await page.getByRole('button', { name: 'Add page', exact: true }).click();
    assert.equal(await inkCount(), 0);
    for (const style of ['ballpoint', 'fountain', 'brush', 'pencil', 'highlighter']) {
      await page.getByLabel('Pen style', { exact: true }).selectOption(style);
      await stroke(); assert((await inkCount()) > 0);
      await page.getByRole('button', { name: 'Undo', exact: true }).click(); assert.equal(await inkCount(), 0);
    }
    await page.getByLabel('Pen style', { exact: true }).selectOption('ballpoint'); await stroke();
    const secondPageInk = await inkCount();
    await page.getByRole('button', { name: 'Previous page', exact: true }).click(); assert.equal(await inkCount(), ink);
    await page.getByRole('button', { name: 'Next page', exact: true }).click(); assert.equal(await inkCount(), secondPageInk);
    await page.getByRole('button', { name: 'Zoom in', exact: true }).click();
    assert.equal(await page.getByRole('button', { name: 'Reset zoom' }).textContent(), '125%');
    await page.getByRole('button', { name: 'Move page', exact: true }).click();
    const workspace = page.locator('.an-workspace');
    await workspace.evaluate(el => delete el.setPointerCapture);
    await workspace.evaluate(el => el.scrollTop = 0);
    const touchSession = await page.context().newCDPSession(page);
    const view = await workspace.boundingBox();
    const touchX = Math.round(view.x + view.width / 2);
    const touchY = Math.round(view.y + Math.min(view.height - 30, 350));
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: touchX, y: touchY }] });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: touchX, y: touchY - 150 }] });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    assert((await workspace.evaluate(el => el.scrollTop)) >= 140, 'A finger drag must actually move the page');
    assert.equal(await inkCount(), secondPageInk, 'Panning must not add ink');
    // Native two-finger gestures must zoom in both directions without changing the draft.
    await page.getByRole('button', { name: 'Pen', exact: true }).click();
    await page.getByRole('checkbox', { name: /Pencil only/ }).uncheck();
    const draftBeforePinch = await page.evaluate(() => JSON.stringify(Object.entries(localStorage).filter(([key]) => key.startsWith('medicomm-notepad:'))));
    const fingers = distance => [{ id: 11, x: touchX - distance / 2, y: touchY }, { id: 12, x: touchX + distance / 2, y: touchY }];
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: fingers(120).slice(0, 1) });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: fingers(120) });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: fingers(240) });
    await page.waitForFunction(() => document.querySelector('[aria-label="Reset zoom"]').textContent === '250%');
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: fingers(96) });
    await page.waitForFunction(() => document.querySelector('[aria-label="Reset zoom"]').textContent === '100%');
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: fingers(96).slice(0, 1) });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ id: 11, x: touchX, y: touchY - 30 }] });
    await touchSession.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    assert.equal(await inkCount(), secondPageInk, 'Pinching and lifting one finger must not leave a mark');
    assert.equal(await page.evaluate(() => JSON.stringify(Object.entries(localStorage).filter(([key]) => key.startsWith('medicomm-notepad:')))), draftBeforePinch);
    await touchSession.detach();
    await page.getByRole('button', { name: 'Zoom out', exact: true }).click();
    await page.getByRole('button', { name: 'Reset zoom', exact: true }).click();
    await page.getByRole('button', { name: 'Close notepad' }).click();
    await page.getByRole('button', { name: /Notepad Write/ }).click(); assert.equal(await inkCount(), secondPageInk);
    await page.getByRole('button', { name: 'Previous page', exact: true }).click(); assert.equal(await inkCount(), ink);
    await page.evaluate(() => document.documentElement.dataset.theme = 'dark');
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: 'output/notepad/mobile-dark.png' });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    const dialog = await page.getByRole('dialog').boundingBox(); assert(dialog.width <= 390 && dialog.height <= 844);
    await page.getByRole('button', { name: 'Save answer', exact: true }).click();
    await page.getByAltText('Your handwritten answer').waitFor();
    const image = await page.getByAltText('Your handwritten answer').getAttribute('src');
    assert(image.startsWith('data:image/png;base64,'));
    const dimensions = await page.getByAltText('Your handwritten answer').evaluate(async el => { await el.decode(); return [el.naturalWidth, el.naturalHeight]; });
    assert.deepEqual(dimensions, [2400, 1632], 'Both pages must be included in the attachment');
    await page.getByRole('checkbox').check();
    await page.getByRole('button', { name: 'Submit for AI review' }).click();
    await page.getByRole('alert').filter({ hasText: 'Temporary review failure' }).waitFor();
    assert.equal(submitted.answerImageDataUrl, image); assert.equal(submitted.answer, '');
    assert.equal(await page.getByAltText('Your handwritten answer').getAttribute('src'), image);
    fail = false;
    await page.getByRole('button', { name: 'Submit for AI review' }).click();
    await page.getByRole('heading', { name: 'Exam-ready model answer' }).waitFor();
    assert.deepEqual(errors, []);
    console.log('PASS: ink, eraser, undo/redo, clear/undo, palm touch rejection, two-finger zoom, question isolation, reload recovery, tablet/mobile layouts, PNG attachment, image-only review failure/retry/success. Review API mocked.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
