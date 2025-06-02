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

## Running the Demo
Start the unified Streamlit app:

```bash
streamlit run examples/demo.py
```
You can modify `demo.py` to adjust model URLs or inference parameters.

### Capturing Screenshots
Capture a screenshot of the unified demo using Playwright:
```bash
# from repo root
pip install playwright
playwright install chromium
python3 scripts/capture_demo_screenshots.py \
  examples/demo.py --port 8501 --output screenshots/demo.png
```
The file `screenshots/demo.png` will be created.
<!-- Image classification demo removed; refer to Demo Mode in basic_demo.py -->
