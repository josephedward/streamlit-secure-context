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

Since we can’t bundle a real browser screenshot here, you can generate one yourself in two minutes:

1. Start the simple demo  
   ```bash
   streamlit run examples/simple_demo.py
   ```
2. In a second terminal, install Puppeteer and capture the screenshot  
   ```bash
   npm install puppeteer
   node scripts/capture_demo.js http://localhost:8501 screenshots/simple_demo_screenshot.png
   ```
   The script will auto-create the `screenshots/` folder if needed.

3. Open `screenshots/simple_demo_screenshot.png` to see the result:  
   ![Simple Demo Screenshot](screenshots/simple_demo_screenshot.png)

If you prefer Playwright instead of Puppeteer:

```bash
pip install playwright
playwright install chromium
python scripts/capture_demo_screenshots.py
```

Either approach will give you a PNG of the simple demo for your docs or slides.
