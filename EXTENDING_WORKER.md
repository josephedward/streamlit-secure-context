# Extending the Worker for Real ML Inference

By default, `worker.js` is a stub that doesn’t actually load or run a real model. This guide walks through productionizing it with popular web-based ML runtimes, covering:
  - TensorFlow.js (TFJS)
  - ONNX Runtime Web (ORT)
  - Security policy considerations (CSP, COEP, COOP)

---

## 1. TensorFlow.js

TensorFlow.js (TFJS) lets you run Keras, TensorFlow SavedModels, or even TFLite (via addons) in-browser.

### a) Include TFJS in the Worker
In `frontend/public/worker.js`, at the top:
```js
// Load TFJS runtime
importScripts(
  'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.6.0/dist/tf.min.js'
);
```

Ensure your CSP allows loading from the CDN (add its origin to `script-src` and `worker-src`).

### b) Loading the Model
In your `onmessage` handler:
```js
self.onmessage = async (e) => {
  const { type, modelPath, params } = e.data;
  if (type === 'INIT') {
    // Choose loader based on extension
    if (modelPath.endsWith('.tflite')) {
      // (Optional) Use tfjs-tflite: requires WASM binary and script
      importScripts('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite');
      self.model = await tflite.loadTFLiteModel({
        modelUrl: modelPath,
        wasmPath: '/worker/tflite.wasm'
      });
    } else {
      self.model = await tf.loadGraphModel(modelPath);
    }
    self.postMessage({ type: 'INIT_DONE' });
  }
  if (type === 'INFER') {
    // Preprocess input
    const inputTensor = tf.tensor(params.input, params.shape);
    // Run inference
    const outputTensor = await self.model.predict(inputTensor);
    const outputData = await outputTensor.array();
    self.postMessage({ type: 'RESULT', result: outputData });
  }
};
```

### c) Notes
- TFJS operations may be async (WASM/WebGL). Use `await` accordingly.
- Bundle TFJS locally if you need offline/locked-down environments, at the cost of payload size.

---

## 2. ONNX Runtime Web

ONNX Runtime Web (ORT) supports both WASM and WebGPU backends for ONNX models.

### a) Include ORT in the Worker
```js
importScripts(
  'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js'
);
```

### b) Loading the Model
```js
self.onmessage = async (e) => {
  const { type, modelPath, params } = e.data;
  if (type === 'INIT') {
    self.session = await ort.InferenceSession.create(modelPath, {
      executionProviders: ['wasm', 'webgl']
    });
    self.postMessage({ type: 'INIT_DONE' });
  }
  if (type === 'INFER') {
    // Construct feeds: adjust 'inputName' and shapes to your model
    const tensor = new ort.Tensor('float32', params.input, params.dims);
    const feeds = { inputName: tensor };
    const results = await self.session.run(feeds);
    const outputData = results.outputName.data;
    self.postMessage({ type: 'RESULT', result: outputData });
  }
};
```

### c) Notes
- You must know your model’s input/output names and shapes.
- ORT may compile WASM on-the-fly: ensure your CSP includes `'wasm-unsafe-eval'` under `script-src` or `worker-src`.

---

## 3. Security Policy Considerations

### Content Security Policy (CSP)
- Update your CSP directives to allow:
  - External CDNs (`cdn.jsdelivr.net`, `unpkg.com`, etc.) under `script-src`/`worker-src`.
  - WebAssembly: include `'wasm-unsafe-eval'` if needed.

### Cross-Origin Embedder Policy (COEP)
- If you can’t control model host headers, consider `COEP: credentialless` to load third-party resources without credentials.

### Cross-Origin Opener Policy (COOP)
- Typically `same-origin` is sufficient. Only change if you have special isolation requirements.

---

## 4. Putting It All Together
1. Choose a runtime (TFJS or ORT) based on your model format and performance needs.
2. Update `frontend/public/worker.js` with importScripts and handlers above.
3. Adjust your Streamlit/React component CSP settings to allow the chosen libraries and model hosts.
4. Build and deploy your component; test end-to-end inference in production-like environments.

Now your Streamlit Component carries real ML inference in a secure, sandboxed worker! 🎉