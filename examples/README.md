<!-- examples/README.md -->
# Examples for streamlit-secure-context

This directory contains example apps demonstrating how to use the `streamlit-secure-context` Streamlit component.

## Prerequisites
- Node.js & npm
- Python 3.7+
- Streamlit 0.63+

## Setup
1. Build the frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```
   Alternatively, run the helper script from the project root to build, copy assets, and install:
   ```bash
   ./scripts/bootstrap.sh
   ```
2. Install the Python package (editable mode recommended):
   ```bash
   pip install -e .
   ```

## Running the Basic Demo
In one terminal, start the Streamlit app:
```bash
streamlit run examples/basic_demo.py
```
This will launch a web browser window showing a simple app that uses the secure context component to perform a dummy inference.

You can modify `basic_demo.py` to point at your own model URL or adjust inference parameters.

## Demo Modes

The `basic_demo.py` script supports two modes via the **Demo Mode** selector in the sidebar:
1. **Interactive**: Full UI with model URL input, HTTPS toggle, and four Iris feature sliders.
2. **Simple**: One-shot inference using fixed Iris inputs (`[5.1, 3.5, 1.4, 0.2]`) and no additional UI.

### Capturing Screenshots
After selecting your mode and running the app, capture a screenshot with Puppeteer:
```bash
# Install Puppeteer if needed
npm install puppeteer

# Capture the current mode of basic_demo
node scripts/capture_demo.js \
  http://localhost:8501 \
  screenshots/basic_demo_<mode>_screenshot.png
```
Replace `<mode>` with `interactive` or `simple`.  Screenshot files will be saved in `screenshots/`.
## Running the Image Classification Demo

In one terminal, start the secure image demo:
```bash
streamlit run examples/image_demo.py
```
This page lets you choose an image file; a MobileNet model loads from CDN inside a sandboxed iframe/Web Worker
and classifies the image entirely in-browser, displaying the top prediction.

### Capturing a Screenshot of the Image Demo
```bash
# Ensure Puppeteer is installed:
npm install puppeteer

# Capture the image demo:
node scripts/capture_demo.js \
  http://localhost:8501 \
  screenshots/image_demo_screenshot.png
```
The screenshot will be saved at `screenshots/image_demo_screenshot.png`.
