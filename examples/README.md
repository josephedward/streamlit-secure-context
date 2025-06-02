<!-- examples/README.md -->
# Streamlit Secure Context Demos

This directory provides a multipage Streamlit demo for the `streamlit-secure-context` component:

- **app.py**: Entrypoint with a landing page and sidebar **Pages** menu.
- **pages/**: Contains individual demo pages:
  - `image_demo.py`: Secure Image Processing Demo (grayscale/invert filters inside a sandbox).
  - `interactive_demo.py`: Interactive Iris Inference Demo (adjustable sliders).
  - `simple_demo.py`: Simple Iris Inference Demo (one-shot inference).

## Setup

From the project root:
```bash
./scripts/bootstrap.sh
pip install -e .
pip install streamlit
```

## Running the Demos

```bash
cd examples
streamlit run app.py
```
Use the **☰ Pages** menu in the top-left to switch between the two demos.

## Capturing Screenshots

```bash
# Install Playwright & browser
pip install playwright
playwright install chromium

# Capture Secure Image Processing demo
python3 scripts/capture_demo_screenshots.py \
  examples/pages/image_demo.py --port 8501 --output screenshots/image_demo.png

# Capture Interactive Iris demo
python3 scripts/capture_demo_screenshots.py \
  examples/pages/interactive_demo.py --port 8501 --output screenshots/interactive_demo.png

# Capture Simple Iris demo
python3 scripts/capture_demo_screenshots.py \
  examples/pages/simple_demo.py --port 8501 --output screenshots/simple_demo.png
```