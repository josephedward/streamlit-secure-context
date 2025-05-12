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
      // Initialize model or session based on file extension
      if (modelPath.endsWith('.onnx')) {
        // ONNX Runtime Web
        importScripts('https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js');
        ortSession = await ort.InferenceSession.create(modelPath, {
          executionProviders: ['wasm', 'webgl'],
        });
      } else if (modelPath.endsWith('.tflite')) {
        // TFLite via tfjs-tflite
        importScripts('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite');
        tfModel = await tflite.loadTFLiteModel({ modelUrl: modelPath });
      } else {
        // TensorFlow.js GraphModel
        tfModel = await tf.loadGraphModel(modelPath);
      }
      self.postMessage({ type: 'INIT_DONE' });
    } else if (type === 'INFER') {
      let result;
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