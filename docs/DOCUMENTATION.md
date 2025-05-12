# streamlit-secure-context: Comprehensive Documentation

This folder contains all key documentation for this project, including setup, packaging, and extending the inference worker.

## 1. Project Overview

For a detailed project overview, usage examples, and API reference, see the root [README.md](../README.md).

## 2. Packaging & Distribution

Full packaging and PyPI distribution instructions are in [PACKAGING.md](PACKAGING.md).

## 3. Extending the Worker for Real ML Inference

Guides and code samples for integrating TensorFlow.js and ONNX Runtime Web into `worker.js` are in [EXTENDING_WORKER.md](EXTENDING_WORKER.md).

## 4. Security Policy Considerations

- **Content Security Policy (CSP)**: Configure `script-src` and `worker-src` to allow CDN origins (e.g., `https://cdn.jsdelivr.net`) and include `'wasm-unsafe-eval'` if deploying WASM-based runtimes.
- **Cross-Origin Embedder Policy (COEP)**: Use `require-corp` for strict isolation or `credentialless` for third-party model hosting without credentials.
- **Cross-Origin Opener Policy (COOP)**: Use `same-origin` to maintain isolation.

## 5. Build & Development Workflow

1. Build the frontend and install locally:
   ```bash
   ./scripts/bootstrap.sh
   ```
2. During development, the Python wrapper serves assets from `frontend/build/`.
3. To test in a fresh environment:
   ```bash
   pip uninstall streamlit-secure-context || true
   pip install .
   streamlit run examples/app.py
   ```

## 6. Directory Structure
```
<project-root>/
├── docs/                        # Documentation folder
│   ├── DOCUMENTATION.md         # This summary file
│   ├── PACKAGING.md             # Packaging & distribution guide
│   └── EXTENDING_WORKER.md      # Worker extension guide
├── frontend/                    # React code & build config
├── scripts/                     # Build & release automation scripts
├── streamlit_secure_context/         # Python wrapper package
├── setup.py                     # Python package setup
└── README.md                    # Project overview & API reference
```

## 7. Next Steps

- Customize CSP and sandbox flags for your deployment.
- Integrate your actual ML model (ONNX/TFLite/TFJS) as shown in the worker guides.
- Consider CI/CD automation to publish releases automatically.
  
Happy building! 🎉
  
## HIPAA-Conscious Deployment

Follow these guidelines to deploy in a HIPAA-compliant manner and minimize ePHI exposure:

- HTTPS everywhere: Configure Streamlit’s `server` section in `~/.streamlit/config.toml`:
  ```toml
  [server]
  enableXsrfProtection = true
  headless = true
  enableCORS = false
  sslCert = "/path/to/fullchain.pem"
  sslKey = "/path/to/privkey.pem"
  ```
- Host all assets internally: Ensure `frontend/public` contains `tf.min.js`, `ort.min.js`, and `tf-tflite.js`—the `postinstall` script in `frontend/package.json` will copy them from `node_modules`.
- Client-only PHI processing: Build UI elements inside the component (e.g., file `<input>`) so that raw PHI never reaches the Streamlit server.
- Secure server environment: Use a HIPAA-certified cloud or on-prem environment, enforce role-based access controls, encryption at rest, and audit logs for any stored data.
- Device security: Require disk encryption, OS patches, and up-to-date browsers on client devices.

By keeping inference and PHI processing within the user’s browser and enforcing strict server security, you simplify compliance and reduce ePHI risks.