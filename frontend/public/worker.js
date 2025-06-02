// Web Worker script: handles model loading and inference off the main thread
// Load TensorFlow.js runtime
importScripts(
  'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.6.0/dist/tf.min.js'
);

let tfModel = null;
let ortSession = null;

self.onmessage = async (e) => {
  const { type, modelPath, params } = e.data;
  try {
    if (type === 'INIT') {
      // Signal readiness; no model preloading needed for image processing
      self.postMessage({ type: 'INIT_DONE' });
    } else if (type === 'INFER') {
      // Image processing path: handle imageURL in params
      if (params && params.imageURL) {
        const url = params.imageURL;
        const mode = params.processing || 'grayscale';
        // Fetch image and decode
        const resp = await fetch(url);
        const blob = await resp.blob();
        const bitmap = await createImageBitmap(blob);
        // Draw onto OffscreenCanvas
        const off = new OffscreenCanvas(bitmap.width, bitmap.height);
        const ctx = off.getContext('2d');
        ctx.drawImage(bitmap, 0, 0);
        // Pixel data
        const imgData = ctx.getImageData(0, 0, bitmap.width, bitmap.height);
        const data = imgData.data;
        // Apply filter
        for (let i = 0; i < data.length; i += 4) {
          const r = data[i], g = data[i+1], b = data[i+2];
          if (mode === 'invert') {
            data[i] = 255 - r;
            data[i+1] = 255 - g;
            data[i+2] = 255 - b;
          } else {
            const gray = (r + g + b) / 3;
            data[i] = data[i+1] = data[i+2] = gray;
          }
        }
        ctx.putImageData(imgData, 0, 0);
        // Convert to data URL
        const outBlob = await off.convertToBlob();
        const reader = new FileReaderSync();
        const result = reader.readAsDataURL(outBlob);
        self.postMessage({ type: 'RESULT', result });
        return;
      }
      let result;
      // ML inference path: initialize model on first call
      if (!tfModel && !ortSession) {
        // Initialize model or session based on file extension
        if (modelPath.endsWith('.onnx')) {
          importScripts('https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js');
          ortSession = await ort.InferenceSession.create(modelPath, { executionProviders: ['wasm', 'webgl'] });
        } else if (modelPath.endsWith('.tflite')) {
          importScripts('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite');
          tfModel = await tflite.loadTFLiteModel({ modelUrl: modelPath });
        } else {
          tfModel = await tf.loadGraphModel(modelPath);
        }
      }
      // ONNX inference
      if (ortSession) {
        // params.input: Array or TypedArray, params.shape: number[]
        const inputName = params.inputName || Object.keys(ortSession.inputNames || {})[0] || 'input';
        const tensor = new ort.Tensor('float32', params.input, params.shape);
        const feeds = { [inputName]: tensor };
        const outputs = await ortSession.run(feeds);
        const outputName = params.outputName || Object.keys(outputs)[0];
        result = outputs[outputName].data;
      }
      // TensorFlow.js inference
      else if (tfModel) {
        const tensor = tf.tensor(params.input, params.shape);
        let out;
        if (typeof tfModel.predict === 'function') {
          out = tfModel.predict(tensor);
        } else if (typeof tfModel.executeAsync === 'function') {
          out = await tfModel.executeAsync(tensor);
        } else {
          throw new Error('TFJS model has no predict or executeAsync method');
        }
        // Handle single tensor or array of tensors
        if (Array.isArray(out)) {
          result = await out[0].array();
        } else {
          result = await out.array();
        }
      } else {
        throw new Error('Model not initialized');
      }
      // Send inference result back
      self.postMessage({ type: 'RESULT', result });
    }
  } catch (err) {
    // Forward error to parent
    self.postMessage({ type: 'ERROR', error: err.message || String(err) });
  }
};