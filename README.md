## Integration Ideas
Here are some ways to integrate the `streamlit_secure_context` component into your own Streamlit applications:
- Data Annotation: Embed the component in a labeling UI to preview model inferences on user-uploaded data before finalizing annotations.
- Interactive Dashboards: Offload client-side inference to reduce server load, enabling live model predictions in real-time dashboards.
- Privacy-First Forms: Incorporate secure inference in forms that process sensitive inputs (e.g., images, documents) entirely in the browser.
- Model Comparison: Render multiple iframes side-by-side to compare outputs of different models or versions without server-side conflict.
- Edge Deployments: Package your app as a Progressive Web App (PWA) and run models on-device for offline or low-latency scenarios.
- Custom Workflows: Extend the Web Worker to support ONNX, TFLite, or other web-compatible runtimes for custom inference pipelines.
Use these ideas to build richer, more performant, and privacy-conscious Streamlit applications with client-side ML.
[![CI](https://github.com/josephedward/streamlit-secure-context/actions/workflows/ci.yml/badge.svg)](https://github.com/josephedward/streamlit-secure-context/actions)
# streamlit-secure-context

This repository provides a secure machine learning inference component for Streamlit, leveraging modern browser security features (HTTPS enforcement, Cross-Origin Isolation, and CSP) and a worker-based inference pipeline inside a sandboxed iframe.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Building the Frontend](#building-the-frontend)
- [Installing the Component](#installing-the-component)
- [Usage Example](#usage-example)
- [Directory Structure](#directory-structure)
- [Code Breakdown](#code-breakdown)
- [Python Wrapper (`streamlit_secure_context/__init__.py`)](#python-wrapper-streamlit_secure_contextinitpy)
  - [React Frontend (`frontend/src`)](#react-frontend-frontendsrc)
  - [Iframe Loader (`frontend/public/model_iframe.html`)](#iframe-loader-frontendorpublicmodel_iframehtml)
  - [Web Worker (`frontend/public/worker.js`)](#web-worker-frontendorpublicworkerjs)
- [Scripts](#scripts)
- [Next Steps](#next-steps)
- [Changelog](#changelog)

## Prerequisites
- Node.js & npm
- Python 3.7+
- Streamlit 0.63+
  - (Multipage) file watching disabled by default via `.streamlit/config.toml`

## Installation
```bash
git clone <repo_url>
cd streamlit-secure-context
scripts/bootstrap.sh    # Build frontend and install the component
```

## Building the Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

## Installing the Component
```bash
pip install .
```

## Usage Example
```python
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

# Basic usage with optional timeout
result = streamlit_secure_context(
    model_path="https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json",
    security_config={
        "coop": "same-origin",
        "coep": "require-corp",
        "csp": {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'wasm-unsafe-eval'"],
            "worker-src": ["'self'", "blob:"],
        },
        "sandbox": ["allow-scripts", "allow-same-origin"],
        "requireHTTPS": True,
    },
    inference_params={"input": [[5.1, 3.5, 1.4, 0.2]], "shape": [1, 4]},
    key="example1",
    height=600,    # optional: component height in px
    width=800,     # optional: component width in px
    timeout=30,    # optional: seconds to wait for component initialization
)
st.write("Inference result:", result)
```

## Directory Structure
```
streamlit-secure-context/
├── frontend/                # React code & build config
│   ├── public/              # Static assets for iframe & worker
│   └── src/                 # React component source (TypeScript)
├── scripts/                 # Helper scripts
│   └── bootstrap.sh         # Build & install automation
├── streamlit_secure_context/     # Python wrapper package
│   └── __init__.py
├── setup.py                 # Package setup
└── README.md                # This file
```

## Code Breakdown

### Python Wrapper (`streamlit_secure_context/__init__.py`)
Declares the Streamlit component and exposes `streamlit_secure_context()` for use in Python apps. Switches between local build and CDN modes based on `_RELEASE` flag.

### React Frontend (`frontend/src`)
Defines `StreamlitSecureContext`:
 - Configures CSP via a dynamic `<meta>` tag
 - Enforces COOP/COEP and verifies cross-origin isolation
 - Creates a sandboxed iframe to host the inference logic
 - Communicates with the iframe via `window.postMessage`

### Iframe Loader (`frontend/public/model_iframe.html`)
Loads inside an isolated iframe with COOP/COEP headers. Parses URL parameters for `modelPath`, instantiates a Web Worker (`worker.js`), and relays messages between the parent and the worker.

### Web Worker (`frontend/public/worker.js`)
Placeholder for inference logic. Responds to `INIT` (model loading) and `INFER` (dummy result) messages. Replace with real ML model loading and inference code.

## Scripts
```bash
./scripts/bootstrap.sh
```
Automates building the frontend and installing the Python package. 

## Next Steps

- Customize CSP and sandbox flags for your deployment.
- Integrate your actual ML model (ONNX/TFLite/TFJS) as shown in the worker guides.
- Consider CI/CD automation to publish releases automatically.

Happy building! 🎉


## Secure Deployment

- HTTPS everywhere: Configure your Streamlit server to use TLS certificates (see docs for `server.sslCert` and `server.key` options).
- Host all assets internally: The frontend is configured to bundle TFJS, ONNX Runtime Web, and TFLite scripts locally. Run `npm install` in `frontend/` and let the `postinstall` script copy these assets into `frontend/public`.
- Client-only PHI processing: Use in-browser inputs within the secure component (e.g., `<input type="file">`) so that raw PHI never leaves the user’s browser.
- Device security: Ensure end-user devices have disk encryption, updated browsers, and adhere to your organizational security policies.



## Demo

After installation and build (see above), start the multipage demo:

```bash
streamlit run examples/app.py
```
Use the **Pages** menu (☰) in the top-left to select:
  - **Image Processing** — apply grayscale/invert to an image entirely in-browser
  - **Iris Inference** — interactive TFJS GraphModel inference demo with sliders

### Capturing Screenshots & Videos
You can capture screenshots and videos of all demos with the helper script:
```bash
# Install Playwright & browser
pip install playwright
playwright install chromium

# Run the capture-all script
chmod +x scripts/capture_all_demos.sh
./scripts/capture_all_demos.sh
```
Screenshots will be in `screenshots/` and recordings in `videos/`.

## How It Works
When you run the demo with `streamlit run examples/app.py`, here's what happens:

**1. Streamlit one-liner**  
Your Python code invokes `streamlit_secure_context(...)`, which loads the low-level component.

**2. Bootstrapping a sandboxed iframe**  
A dynamic `<meta>` tag injects your CSP rules.  
COOP (`same-origin`) and COEP (`require-corp`) headers enforce cross-origin isolation.  
The iframe uses `sandbox="allow-scripts allow-same-origin"` to tightly control capabilities.

**3. Spawning a Web Worker**  
Inside the iframe (`model_iframe.html`), the component creates a Worker.  
The parent frame `postMessage({ type: 'INIT', modelPath })` to initialize the model loader.

**4. Model loading & inference off-thread**  
The Worker loads one of:  
- TFJS GraphModel via `tf.loadGraphModel(modelPath)`  
- TFLite via `@tensorflow/tfjs-tflite`  
- ONNX Runtime Web via `onnxruntime-web`  
After the Worker signals `INIT_DONE`, the component sends `{ type: 'INFER', params }`.  
The Worker runs inference (`predict` or `executeAsync`) and `postMessage({ type: 'RESULT', result })`.

**5. Round-trip back to Python**  
The React component receives the RESULT message.  
It calls `Streamlit.setComponentValue(result)`, returning the tensor data to Python.  
Your Streamlit app simply does `st.write("Inference result:", result)` to display it.

Tips:
- Open DevTools → Application → Frames → <iframe> to confirm sandbox/isolation.
- Add `console.log` in `worker.js` or `model_iframe.html` to debug message passing.
- Swap in a real model path and update `inference_params` (add a `shape` key) for genuine ML output.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.
