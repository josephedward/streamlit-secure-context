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

## Running the Simple Demo

For a minimal one-line example that runs inference immediately:
```bash
streamlit run examples/simple_demo.py
```
This demo uses a fixed Iris TFJS model and hard-coded inputs to demonstrate secure ML inference with no extra UI.

### Capturing a Screenshot
After starting the demo in one terminal, from the project root run:
```bash
# Install Puppeteer if you haven't already:
npm install puppeteer

# Capture the running simple demo:
node scripts/capture_demo.js http://localhost:8501 screenshots/simple_demo_screenshot.png
```
The screenshot will be saved to `screenshots/simple_demo_screenshot.png`.