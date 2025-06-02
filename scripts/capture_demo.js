#!/usr/bin/env node
/**
 * capture_demo.js
 *
 * Automates screenshot capture of the Streamlit demo using Puppeteer.
 *
 * Usage:
 *   1. Ensure the demo is running:
 *        streamlit run examples/basic_demo.py
 *   2. Install Puppeteer:
 *        npm install puppeteer
 *   3. Run this script:
 *        node scripts/capture_demo.js
 *
 * Output:
 *   - scripts/demo_screenshot.png
 */
const puppeteer = require('puppeteer');

(async () => {
  const url = 'http://localhost:8501';
  const screenshotPath = 'scripts/demo_screenshot.png';
  try {
    console.log(`Launching headless browser to capture screenshot of ${url}`);
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.goto(url, { waitUntil: 'networkidle2' });
    // Give Streamlit time to render
    await page.waitForTimeout(2000);
    console.log(`Saving screenshot to ${screenshotPath}`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log('Screenshot captured successfully.');
    await browser.close();
  } catch (err) {
    console.error('Error capturing screenshot:', err);
    process.exit(1);
  }
})();