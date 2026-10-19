const { chromium } = require('C:/Users/Hp/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const page = await browser.newPage();
    await page.route('http://compression.test/**', route => route.fulfill({ contentType: route.request().url().endsWith('.js') ? 'text/javascript' : 'text/html',
      body: route.request().url().endsWith('.js') ? fs.readFileSync('src/lib/theoryImages.js', 'utf8') : '<html><body>Compression test</body></html>' }));
    await page.goto('http://compression.test/');
    const result = await page.evaluate(async () => {
      const { encodeTheoryPage, prepareTheoryImage, imageBytes } = await import('/theoryImages.js');
      const canvas = document.createElement('canvas'); canvas.width = 1200; canvas.height = 1600;
      const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 1200, 1600);
      ctx.fillStyle = '#243959'; ctx.font = '24px serif';
      for (let line = 0; line < 45; line++) ctx.fillText(`${line + 1}. Cardiac output = heart rate x stroke volume. Na+, K+, Ca2+`, 45, 60 + line * 32);
      ctx.strokeStyle = '#7950b8'; ctx.lineWidth = 2;
      for (let line = 0; line < 5; line++) {
        ctx.beginPath(); ctx.moveTo(50, 1500 + line * 15);
        for (let i = 1; i < 1000; i++) ctx.lineTo(50 + i, 1500 + line * 15 + Math.sin(i / 8) * 4);
        ctx.stroke();
      }
      const original = canvas.toDataURL('image/png');
      const encoded = encodeTheoryPage(canvas);
      const img = new Image(); img.src = encoded.dataUrl; await img.decode();
      const comparison = document.createElement('canvas'); comparison.width = 1200; comparison.height = 1600;
      const cc = comparison.getContext('2d'); cc.drawImage(img, 0, 0);
      const before = ctx.getImageData(0, 0, 1200, 1600).data, after = cc.getImageData(0, 0, 1200, 1600).data;
      let error = 0;
      for (let i = 0; i < before.length; i++) if (i % 4 !== 3) error += (before[i] - after[i]) ** 2;
      const mse = error / (1200 * 1600 * 3);
      const psnr = mse ? 10 * Math.log10(255 ** 2 / mse) : 100;
      const blob = await (await fetch(encoded.dataUrl)).blob();
      const prepared = await prepareTheoryImage(new File([blob], 'answer.webp', { type: blob.type }));
      const alreadySmallPreserved = prepared.dataUrl === encoded.dataUrl;
      const unsupportedCanvas = { width: 1, height: 1, toDataURL: () => 'data:image/png;base64,YQ==' };
      const fallback = encodeTheoryPage(unsupportedCanvas);
      canvas.width = 3200; canvas.height = 2400;
      ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 3200, 2400); ctx.fillStyle = '#000'; ctx.fillText('Large answer photo', 40, 80);
      const large = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
      const resized = await prepareTheoryImage(new File([large], 'large.png', { type: 'image/png' }));
      let invalidRejected = false;
      try { await prepareTheoryImage(new File(['invalid'], 'bad.txt', { type: 'text/plain' })); } catch { invalidRejected = true; }
      return { originalBytes: imageBytes(original), compressedBytes: encoded.bytes, format: encoded.extension, psnr,
        dimensions: [img.naturalWidth, img.naturalHeight], resized: [resized.width, resized.height], alreadySmallPreserved,
        fallback: fallback.extension, paddedBytes: imageBytes('data:image/png;base64,YQ=='), invalidRejected };
    });
    assert.deepEqual(result.dimensions, [1200, 1600]);
    assert(result.compressedBytes < result.originalBytes, 'Text sample should compress');
    assert(result.psnr > 35, 'Full-size sample must retain high pixel fidelity');
    assert.deepEqual(result.resized, [2560, 1920]);
    assert(result.alreadySmallPreserved, 'Do not recompress already-efficient uploads');
    assert.equal(result.fallback, 'png'); assert.equal(result.paddedBytes, 1); assert(result.invalidRejected);
    console.log(JSON.stringify(result, null, 2));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
