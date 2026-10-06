const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 1000 }, hasTouch: true });
    page.setDefaultTimeout(60000);
    const errors = [];
    page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
    await page.route('**/notepad-gesture-test', route => route.fulfill({ contentType: 'text/html', body: `
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
    await session.detach();
    await button('Reset zoom').click(); await button('Pen').click(); await draw();
    assert.equal((await strokes()).at(-1).tool, 'pen');
    assert.deepEqual(errors, []);
    console.log('PASS: native pinch in/out with pen and eraser, no gesture marks, pointer capture released on tool switch, drawing resumes.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
