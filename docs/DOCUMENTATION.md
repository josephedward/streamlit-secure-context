# streamlit-secure-context: Comprehensive Documentation

This folder contains all key documentation for this project, including setup, packaging, and extending the inference worker.

## 1. Project Overview

For a detailed project overview, usage examples, and API reference, see the root [README.md](../README.md).

## 2. Packaging & Distribution

Packaging and distribution instructions are provided in the root repository documentation (see `README.md`).

## 3. Extending the Worker for Real ML Inference

For extending the worker with TensorFlow.js or ONNX Runtime Web, refer to the inline comments in `frontend/public/worker.js` and the root documentation under "Extending the Worker".

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

## Under the Hood: Secure ML Inference Pipeline

When you run the example app with `streamlit run examples/basic_demo.py`, the component orchestrates a secure, client-side inference pipeline:

1. Streamlit one-liner
   - The Python call to `streamlit_secure_context(...)` invokes the low-level component implementation.

2. Bootstrapping a sandboxed iframe
   - A `<meta>` tag sets your Content Security Policy (CSP).
   - Cross-Origin Opener Policy (COOP) and Cross-Origin Embedder Policy (COEP) headers enable cross-origin isolation.
   - The iframe uses a sandbox attribute (`allow-scripts`, `allow-same-origin`) for strict isolation.

3. Spawning a Web Worker
   - Inside the iframe (`model_iframe.html`), a Worker is created for off-main-thread execution.
   - The parent frame sends `INIT` with the model URL to load the ML runtime.

4. Model loading & inference off-thread
   - Workers load one of:
     - TensorFlow.js GraphModel (`tf.loadGraphModel`)
     - TFLite via `@tensorflow/tfjs-tflite`
     - ONNX Runtime Web (`onnxruntime-web`)
   - Once loaded (`INIT_DONE`), the parent sends an `INFER` message with `inference_params`.
   - The Worker runs inference and posts back `RESULT` with the output data.

5. Round-trip back to Python
   - The React component listens for the Worker’s `RESULT` message.
   - It forwards the data via `Streamlit.setComponentValue(result)`.
   - Your Python app receives the tensor array and displays it with `st.write`.

Tips:
- Inspect DevTools → Application → Frames to verify iframe isolation.
- Use `console.log` in `worker.js` or `model_iframe.html` to trace messages.
- Plug in a real ML model URL and add a `shape` to `inference_params` to see real inference results.

## 6. Directory Structure
```
<project-root>/
├── docs/                        # Documentation folder
│   ├── README.md                # Index of documentation
│   └── DOCUMENTATION.md         # Comprehensive documentation
├── frontend/                    # React code & build config
├── scripts/                     # Build & release automation scripts
├── streamlit_secure_context/    # Python wrapper package
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