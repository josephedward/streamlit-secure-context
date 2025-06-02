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

## Demo Details

Here’s what each demo is doing, and why they’re useful illustrations of the secure-context component:

1. Image Classification Demo
   • Purpose: Show how to run a full ML pipeline (load model, preprocess, infer, postprocess) entirely in the browser—no image bytes ever reach your Streamlit server.  
   • How it works:  
     – The component renders a small HTML/JS snippet (file input + image preview + TensorFlow.js/MobileNet scripts) inside a sandboxed iframe.  
     – When you pick or enter an image URL, the JS loads MobileNet in a Web Worker, classifies the image, and returns the top prediction back to Python via `Streamlit.setComponentValue`.  
   • Why it’s valuable: Great for demos of privacy-sensitive workloads (e.g. PHI images) or to offload heavy model downloads/execution from your server to the client.

2. Iris Inference Demo  
   We actually ship two pages to show two common UX patterns for numeric models:  
   a) Simple Mode  
     – Hard-coded 4-dim Iris input `[5.1, 3.5, 1.4, 0.2]`  
     – One call to the secure-context component doing TFJS GraphModel inference in-browser  
     – Illustrates the minimal boilerplate you need to embed the component when inputs are static.  
   b) Interactive Mode  
     – Sidebar sliders let you tweak each Iris feature in real time  
     – You can also swap in your own TFJS model URL or toggle HTTPS enforcement for loading.  
     – When you hit **Run Inference**, the component spins up (or re-uses) its iframe + Worker, loads the model off-thread, and does inference with your chosen values.  
   • Why it’s valuable: Demonstrates how to build rich parameterized UIs in Streamlit while offloading all compute to the browser—perfect for live demos, teaching, or low-latency client-only inference.

In both cases the core pattern is the same:

– You declare `streamlit_secure_context(…)` in Python, passing  
  • `model_path` or inline JS/HTML  
  • `security_config` (COOP/COEP/CSP/sandbox rules)  
  • `inference_params` for the Worker  
  • Optional layout hints (`height`/`width`)  
– Under the hood the React wrapper injects CSP headers, boots an isolated iframe, spins up a Worker (via `postMessage`), and returns the result back to Python.

By splitting them into pages in the multipage app you get a clean, focused demo for each use case—image classification vs. numeric (Iris) inference—so your users can immediately grasp the pattern they care about.

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
