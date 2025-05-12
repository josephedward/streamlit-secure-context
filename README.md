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

## Prerequisites
- Node.js & npm
- Python 3.7+
- Streamlit 0.63+

## Installation
```bash
git clone <repo_url>
cd streamlit-secure-context
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

result = streamlit_secure_context(
    model_path="https://example.com/model.tflite",
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
    inference_params={"input": [1,2,3]},
    key="example1",
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
`./scripts/bootstrap.sh` automates building the frontend and installing the Python package:
```bash
./scripts/bootstrap.sh
```

## Next Steps
1. Integrate real model loading and inference in `worker.js`.
2. Extend the Python API for parameter validation and error handling.
3. Customize CSP directives and sandbox flags per your deployment requirements.
   
## HIPAA-Conscious Deployment

To deploy in a HIPAA-compliant environment and minimize ePHI exposure:

- HTTPS everywhere: Configure your Streamlit server to use TLS certificates (see docs for `server.sslCert` and `server.key` options).
- Host all assets internally: The frontend is configured to bundle TFJS, ONNX Runtime Web, and TFLite scripts locally. Run `npm install` in `frontend/` and let the `postinstall` script copy these assets into `frontend/public`.
- Client-only PHI processing: Use in-browser inputs within the secure component (e.g., `<input type="file">`) so that raw PHI never leaves the user’s browser.
- Secure server environment: If you collect logs or results, ensure your hosting platform enforces strict access controls, audit logging, and is a HIPAA-certified environment.
- Device security: Ensure end-user devices have disk encryption, updated browsers, and adhere to your organizational security policies.

By running inference entirely in the user’s browser and enforcing strict security policies, you minimize ePHI exposure and simplify HIPAA compliance.
4. Add unit and integration tests with Jest and Cypress.