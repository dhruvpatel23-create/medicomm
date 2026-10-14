const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage({ viewport: { width: 1024, height: 1000 }, deviceScaleFactor: 2 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/notepad-ink-test', route => route.fulfill({ contentType: 'text/html', body: `
      <html><body><div id="root"></div><script type="module">
      import RefreshRuntime from '/@react-refresh';
      RefreshRuntime.injectIntoGlobalHook(window);
      window.$RefreshReg$ = () => {}; window.$RefreshSig$ = () => type => type;
      window.__vite_plugin_react_preamble_installed__ = true;
      await import('/scripts/notepad-gesture-harness.jsx');
      </script></body></html>` }));
    await page.goto(`${process.env.NOTEPAD_TEST_URL || 'http://127.0.0.1:4173'}/notepad-ink-test`);
    await page.getByRole('button', { name: /^Notepad/ }).click();
    const canvas = page.locator('.an-canvas');
    assert.deepEqual(await canvas.evaluate(el => [el.width, el.height]), [2400, 3200]);
    const settled = () => page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const pixels = () => canvas.evaluate(el => el.toDataURL());
    const blank = await pixels();
    for (const [index, style] of ['ballpoint', 'fountain', 'brush', 'pencil', 'highlighter'].entries()) {
      await page.getByLabel('Pen style', { exact: true }).selectOption(style);
      await canvas.evaluate((el, index) => {
        const bounds = el.getBoundingClientRect();
        el.closest('.an-workspace').setPointerCapture = () => {};
        const send = (type, x, y, pressure) => el.dispatchEvent(new PointerEvent(type, {
          pointerId: 91, pointerType: 'pen', clientX: bounds.x + x, clientY: bounds.y + y,
          pressure, bubbles: true, buttons: type === 'pointerup' ? 0 : 1,
        }));
        const y = 100 + index * 80;
        send('pointerdown', 70, y, .2);
        for (let i = 1; i < 120; i++) send('pointermove', 70 + i * 3, y + Math.sin(i / 8) * 20, i % 2 ? .2 : .9);
        send('pointerup', 460, y, 0);
      }, index);
      await settled();
      assert.notEqual(await pixels(), blank);
    }
    const strokes = await page.evaluate(() => JSON.parse(localStorage.getItem('medicomm-notepad:gesture-test')).pages[0].strokes);
    assert.equal(strokes.length, 5);
    for (const stroke of strokes) {
      assert(stroke.smooth);
      assert.equal(stroke.points.length, 121);
      assert(Math.abs(stroke.points[1].pressure - stroke.points[0].pressure) < .4, 'Pressure jumps must be softened');
      assert.equal(stroke.points.at(-1).pressure, stroke.points.at(-2).pressure, 'Pen lift must not add a pressure blob');
    }
    const endpoint = await canvas.evaluate(el => {
      const b = el.getBoundingClientRect();
      return el.getContext('2d').getImageData(Math.round(460 * el.width / b.width), Math.round(100 * el.height / b.height), 1, 1).data[3];
    });
    assert(endpoint > 0, 'The final pointer-up position must receive ink');
    const drawn = await pixels();
    await page.getByRole('button', { name: 'Pen', exact: true }).focus();
    await page.keyboard.press('Control+z'); await settled(); assert.notEqual(await pixels(), drawn);
    await page.keyboard.press('Control+Shift+z'); await settled(); assert.equal(await pixels(), drawn);
    await page.getByRole('button', { name: 'Close notepad' }).click();
    await page.getByRole('button', { name: /^Notepad/ }).click(); assert.equal(await pixels(), drawn);
    fs.mkdirSync('output/notepad', { recursive: true });
    await page.screenshot({ path: 'output/notepad/smooth-ink-tablet.png' });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.screenshot({ path: 'output/notepad/smooth-ink-mobile.png' });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.emulateMedia({ reducedMotion: 'reduce' });
    assert.equal(await page.locator('.an-ink-preview path').evaluate(el => getComputedStyle(el).animationName), 'none');
    assert.deepEqual(errors, []);
    console.log('PASS: Retina ink, all five pens, pressure smoothing, pen-lift endpoint, keyboard undo/redo, exact reload rendering, mobile controls and reduced motion.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
