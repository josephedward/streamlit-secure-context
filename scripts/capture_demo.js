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
 *   3. Run this script (default capture for the basic demo):
 *        node scripts/capture_demo.js
 *   4. Optional: specify URL and output path for other demos:
 *        node scripts/capture_demo.js http://localhost:8501 screenshots/basic_demo_screenshot.png
 *        node scripts/capture_demo.js http://localhost:8501 screenshots/simple_demo_screenshot.png
 *
 * Output:
 *   - screenshots/demo_screenshot.png      (default basic demo)
 *   - screenshots/basic_demo_screenshot.png
 *   - screenshots/simple_demo_screenshot.png
 */
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  // Allow overriding URL and output path via CLI args:
  //   node scripts/capture_demo.js [url] [output_path]
  const [, , urlArg, outputArg] = process.argv;
  const url = urlArg || 'http://localhost:8501';
  const screenshotPath = outputArg || 'screenshots/demo_screenshot.png';
  // Ensure output directory exists
  const outDir = path.dirname(screenshotPath);
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
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
