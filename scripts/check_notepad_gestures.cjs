const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 1000 }, hasTouch: true });
    page.setDefaultTimeout(60000);
    const errors = [];
    page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
    await page.route('**/notepad-gesture-test*', route => route.fulfill({ contentType: 'text/html', body: `
      <html><body><div id="root"></div><script type="module">
      import RefreshRuntime from '/@react-refresh';
      RefreshRuntime.injectIntoGlobalHook(window);
      window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => type => type;
      window.__vite_plugin_react_preamble_installed__ = true;
      await import('/scripts/notepad-gesture-harness.jsx');
      </script></body></html>` }));
    await page.goto(`${process.env.NOTEPAD_TEST_URL || 'http://127.0.0.1:4173'}/notepad-gesture-test`);
    await page.getByRole('button', { name: /Notepad Write/ }).click();
    const canvas = page.locator('.an-canvas');
    const workspace = page.locator('.an-workspace');
    const button = name => page.getByRole('button', { name, exact: true });
    const settled = () => page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const pixels = () => canvas.evaluate(el => el.toDataURL());
    const strokes = () => page.evaluate(() => JSON.parse(localStorage.getItem('medicomm-notepad:gesture-test'))?.pages[0].strokes || []);
    const bounds = await canvas.boundingBox();
    const x = bounds.x + 200, y = bounds.y + 200;
    async function draw() {
      await page.mouse.move(x - 60, y); await page.mouse.down();
      await page.mouse.move(x + 60, y, { steps: 12 }); await page.mouse.up(); await settled();
    }
    await draw();
    const ink = await pixels();
    await button('Eraser').click(); await draw();
    assert.notEqual(await pixels(), ink);
    await button('Undo').click(); await settled(); assert.equal(await pixels(), ink);

    // Switching while a pointer is captured must release it and preserve the old stroke's tool.
    await page.mouse.move(x, y); await page.mouse.down();
    assert(await workspace.evaluate(el => el.hasPointerCapture(1)));
    await button('Pen').evaluate(el => el.click());
    assert.equal(await workspace.evaluate(el => el.hasPointerCapture(1)), false);
    await page.mouse.up(); await draw();
    assert.deepEqual((await strokes()).slice(-2).map(stroke => stroke.tool), ['eraser', 'pen']);

    const session = await page.context().newCDPSession(page);
    const fingers = distance => [{ id: 11, x: x - distance / 2, y }, { id: 12, x: x + distance / 2, y }];
    for (const tool of ['Pen', 'Eraser']) {
      await button(tool).click(); await button('Reset zoom').click(); await settled();
      const before = await pixels(), saved = await strokes();
      await session.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: fingers(100).slice(0, 1) });
      await session.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: fingers(100) });
      await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: fingers(200) });
      await page.waitForFunction(() => document.querySelector('[aria-label="Reset zoom"]').textContent === '200%');
      await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: fingers(80) });
      await page.waitForFunction(() => document.querySelector('[aria-label="Reset zoom"]').textContent === '80%');
      await session.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: fingers(80).slice(0, 1) });
      await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ id: 11, x, y: y + 20 }] });
      await session.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await settled();
      assert.equal(await pixels(), before, `${tool}: pinch must preserve ink`);
      assert.deepEqual(await strokes(), saved, `${tool}: pinch must preserve history`);
    }
    await button('Reset zoom').click(); await button('Pen').click(); await draw();
    assert.equal((await strokes()).at(-1).tool, 'pen');
    const firstPage = await pixels();
    await page.locator('.an-page-scale').evaluate(el => {
      window.pageAnimations = [];
      const original = el.animate.bind(el);
      el.animate = (frames, options) => { window.pageAnimations.push(frames); return original(frames, options); };
    });
    const finishAnimation = () => page.locator('.an-page-scale').evaluate(el => Promise.all(el.getAnimations().map(animation => animation.finished.catch(() => {}))));
    await button('Add page').click(); await finishAnimation();
    assert.equal(await page.locator('.an-page-navigation > span').textContent(), '2/2');
    assert.equal(await page.evaluate(() => window.pageAnimations.length), 1);
    await draw(); const secondPage = await pixels();
    await button('Previous page').click(); await finishAnimation();
    assert.equal(await pixels(), firstPage);
    async function swipe(right) {
      const view = await workspace.boundingBox();
      const startX = right ? view.x + 16 : view.x + view.width - 16;
      const touchY = view.y + 200;
      await session.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ id: 21, x: startX, y: touchY }] });
      await session.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ id: 21, x: startX + (right ? 180 : -180), y: touchY + 5 }] });
      await session.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await settled(); await finishAnimation();
    }
    const savedPages = await page.evaluate(() => localStorage.getItem('medicomm-notepad:gesture-test'));
    await swipe(true);
    assert.equal(await page.locator('.an-page-navigation > span').textContent(), '2/2');
    assert.equal(await pixels(), secondPage);
    await swipe(true); // Last page must not create an extra page.
    assert.equal(await page.locator('.an-page-navigation > span').textContent(), '2/2');
    await swipe(false);
    assert.equal(await pixels(), firstPage);
    assert.equal(await page.evaluate(() => localStorage.getItem('medicomm-notepad:gesture-test')), savedPages);
    await button('Close notepad').click();
    await button('Question two').click(); await page.getByRole('button', { name: /^Notepad/ }).click();
    assert.equal(await button('Undo').isDisabled(), true);
    await button('Close notepad').click(); await button('Question one').click();
    await page.getByRole('button', { name: /Notepad Continue your 2 saved pages/ }).click();
    assert.equal(await pixels(), firstPage);
    await button('Next page').click(); await finishAnimation();
    await page.reload(); await page.getByRole('button', { name: /^Notepad/ }).click();
    assert.equal(await page.locator('.an-page-navigation > span').textContent(), '2/2');
    assert.equal(await pixels(), secondPage);
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await button('Previous page').click();
    assert.equal(await page.locator('.an-page-scale').evaluate(el => el.getAnimations().length), 0);
    await session.detach();
    // A signed-in learner can review saved pages and reopen them with the same question.
    const fixtureQuestion = { id: 'question-one', prompt: 'Triangles of the neck', kind: 'short-note', sourcePage: 1 };
    const fixtureReview = { questionId: fixtureQuestion.id, answer: '', hasImage: true, score: 8, feedback: 'A clear answer; add the relevant boundaries.', strengths: ['Clear structure'], improvements: ['Add boundaries'],
      modelAnswerSections: [{ heading: 'Triangles of the neck', points: ['Definition: Anatomical subdivisions of the neck.', 'Applied anatomy: Include relevant clinical relations.'] }],
      textbookSources: [{ book: "B. D. Chaurasia's Human Anatomy", topic: 'Triangles of the neck' }] };
    let reviews = [];
    await page.route('**/short-notes.json', route => route.fulfill({ json: { source: { title: 'Test questions' }, subjects: [{ id: 'anatomy', title: 'Anatomy', topics: [{ id: 'neck', title: 'Neck', questions: [fixtureQuestion, { ...fixtureQuestion, id: 'question-two', prompt: 'Another question' }] }] }] } }));
    await page.route('**/api/short-notes/reviews', route => {
      if (route.request().method() === 'GET') return route.fulfill({ json: { reviews } });
      const submitted = route.request().postDataJSON();
      assert.equal(submitted.questionId, fixtureQuestion.id);
      assert(submitted.answerImageDataUrl.startsWith('data:image/png;'));
      reviews = [fixtureReview];
      return route.fulfill({ status: 201, json: { review: fixtureReview } });
    });
    await page.evaluate(() => localStorage.setItem('medicomm-notepad:short-notes:gesture-user:question-one', localStorage.getItem('medicomm-notepad:gesture-test')));
    await page.goto(`${process.env.NOTEPAD_TEST_URL || 'http://127.0.0.1:4173'}/notepad-gesture-test?review=1`);
    const openFirstQuestion = async () => { await page.locator('.sn-topic-card').first().click(); await page.locator('.sn-question-row').first().click(); };
    await openFirstQuestion();
    await page.getByRole('button', { name: /^Notepad/ }).click();
    assert.equal(await pixels(), firstPage);
    await button('Save answer').click();
    await page.getByRole('checkbox').check(); await button('Submit for AI review').click();
    await page.getByRole('region', { name: 'Textbook references' }).waitFor();
    assert(await page.getByText("B. D. Chaurasia's Human Anatomy", { exact: true }).isVisible());
    await page.getByRole('button', { name: /Notepad Continue your 2 saved pages/ }).click();
    assert.equal(await pixels(), firstPage); await button('Done').click();
    await button('Next question').click(); await page.getByRole('button', { name: /^Notepad/ }).click();
    assert.equal(await button('Undo').isDisabled(), true); await button('Close notepad').click();
    await page.reload(); await openFirstQuestion();
    await page.getByRole('region', { name: 'Textbook references' }).waitFor();
    await page.getByRole('button', { name: /Notepad Continue your 2 saved pages/ }).click();
    assert.equal(await pixels(), firstPage);
    assert.deepEqual(errors, []);
    console.log('PASS: pinch, tools, animated page swipes, boundaries, question isolation, reload recovery, reduced motion, signed-in image review, textbook references, saved pages reopened after review. Review API mocked.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
