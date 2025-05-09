import { analyzeNote } from './ai-utils.js';
console.log('AI iframe script loaded');
// Import the Transformers pipeline for summarization
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.3.1/dist/transformers.min.js';

// AI models and metrics storage
let toxicityModel;
let summarizer;
const modelMetrics = {};

/**
 * Load both toxicity classifier and summarization pipeline.
 * Records summarizer load time in modelMetrics.loadMs.
 */
async function loadModels() {
  console.log('loadModels: Checking secure context');
  if (!window.isSecureContext) throw new Error('AI must run in secure context!');
  console.log('loadModels: Loading TensorFlow.js toxicity model with threshold 0.9');
  toxicityModel = await toxicity.load(0.9);
  console.log('loadModels: Toxicity model loaded');
  console.log('loadModels: Loading summarization pipeline');
  const t0 = performance.now();
  summarizer = await pipeline('summarization', 'Xenova/distilbart-cnn-12-6');
  modelMetrics.loadMs = performance.now() - t0;
  console.log('loadModels: Summarization pipeline loaded in', modelMetrics.loadMs, 'ms');
}

/**
 * Handle 'analyze' messages: summarize and tag the note, returning performance metrics.
 */
window.addEventListener('message', async (event) => {
  console.log('AI iframe received message:', event);
  if (event.origin !== window.location.origin) {
    console.warn('Ignored message from unknown origin:', event.origin);
    return;
  }
  if (event.data.type !== 'analyze') {
    console.warn('Ignored message with unsupported type:', event.data.type);
    return;
  }
  // Ensure models are loaded
  if (!toxicityModel || !summarizer) {
    console.log('Models not loaded, invoking loadModels');
    try {
      await loadModels();
    } catch (err) {
      console.error('Model load failed, using fallback analyzer:', err);
    }
  }
  const note = event.data.note;
  console.log('AI iframe note content:', note);
  let summary;
  let tags;
  const metrics = {};

  // Summarization via Transformer pipeline, fallback to basic analyzer
  if (summarizer) {
    console.log('Starting summarization via Transformer pipeline');
    const infStart = performance.now();
    const results = await summarizer(note);
    metrics.inferenceMs = performance.now() - infStart;
    metrics.loadMs = modelMetrics.loadMs;
    summary = results[0].summary_text;
    metrics.confidence = results[0].score;
    console.log('Summarization complete:', summary, 'inferenceMs:', metrics.inferenceMs);
  } else {
    console.log('Summarizer unavailable, using basic analyzer');
    summary = analyzeNote(note).summary;
    console.log('Basic analyzer summary:', summary);
  }

  // Tagging via toxicity classifier, fallback to basic tags
  // Tagging via toxicity classifier, fallback to basic tags
  if (toxicityModel) {
    console.log('Starting toxicity classification');
    try {
      const tagStart = performance.now();
      const predictions = await toxicityModel.classify([note]);
      metrics.toxicityMs = performance.now() - tagStart;
      tags = predictions.filter(p => p.results[0].match).map(p => p.label);
      console.log('Toxicity classification complete:', tags, 'toxicityMs:', metrics.toxicityMs);
    } catch (err) {
      console.error('Toxicity classification failed, error:', err);
      tags = analyzeNote(note).tags;
      console.log('Fallback tags from basic analyzer:', tags);
    }
  } else {
    console.log('Toxicity model unavailable, using basic analyzer tags');
    tags = analyzeNote(note).tags;
    console.log('Basic analyzer tags:', tags);
  }

  // Send back summary, tags, and metrics
  console.log('Posting suggestions back to parent:', { summary, tags, metrics });
  event.source.postMessage({ type: 'suggestions', summary, tags, metrics }, event.origin);
});
