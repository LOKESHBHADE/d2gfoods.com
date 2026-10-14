// Renders an HTML design to PNG. Usage: serve ../mirror on :8765 with the html + fonts/ + images/ copied in,
// then: node render.js <page.html> <out.png> <width> <height>
const { chromium } = require('playwright');
(async () => {
  const [page, out, w, h] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('http://localhost:8765/' + page);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  await p.screenshot({ path: out });
  await b.close();
})();
