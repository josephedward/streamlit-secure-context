import { analyzeNote } from './ai-utils.js';

// Use the hosted TensorFlow.js toxicity model for tag classification
let toxicityModel;

async function loadModel() {
  if (!window.isSecureContext) throw new Error('AI must run in secure context!');
  // Load the TensorFlow.js toxicity model from CDN with a 0.9 threshold
  toxicityModel = await toxicity.load(0.9);
}

window.addEventListener('message', async (event) => {
  if (event.origin !== window.location.origin || event.data.type !== 'analyze') return;
  if (!toxicityModel) {
    try {
      await loadModel();
    } catch (err) {
      console.warn('Toxicity model load failed, using basic analyzer:', err);
    }
  }
  // Derive summary via basic analyzer
  const summary = analyzeNote(event.data.note).summary;
  // Derive tags via toxicity classification if available
  let tags;
  if (toxicityModel) {
    try {
      const predictions = await toxicityModel.classify([event.data.note]);
      tags = predictions.filter(p => p.results[0].match).map(p => p.label);
    } catch (err) {
      console.warn('Toxicity classification failed:', err);
      tags = analyzeNote(event.data.note).tags;
    }
  } else {
    tags = analyzeNote(event.data.note).tags;
  }
  event.source.postMessage({ type: 'suggestions', summary, tags }, event.origin);
});