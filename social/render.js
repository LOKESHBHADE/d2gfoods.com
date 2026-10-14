// Renders instagram-post.html to a 1080x1350 PNG. Usage: serve ../mirror on :8765, copy the html in, run node render.js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('http://localhost:8765/_yam.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[2] || 'yam-post.png' });
  await b.close();
})();
