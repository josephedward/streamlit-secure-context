<!-- examples/README.md -->
# Streamlit Secure Context Demos

This directory provides a multipage Streamlit demo for the `streamlit-secure-context` component:

- **app.py**: Entrypoint with a landing page and sidebar **Pages** menu.
* **pages/**: Contains individual demo pages:
  - `image_demo.py`: Secure Image Processing Demo (grayscale/invert filter).
  - `iris_demo.py`: Interactive Iris Inference Demo (adjustable sliders).

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
Use the **☰ Pages** menu in the top-left to switch between:
- Simple Iris inference
- Interactive Iris inference

## Capturing Screenshots

```bash
# Install Playwright & browser
pip install playwright
playwright install chromium


# Capture Image Processing demo
python3 scripts/capture_demo_screenshots.py \
  examples/pages/image_demo.py --port 8501 --output screenshots/image_demo.png

# Capture Iris Inference demo
python3 scripts/capture_demo_screenshots.py \
  examples/pages/iris_demo.py --port 8501 --output screenshots/iris_demo.png
```

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for detailed release notes.