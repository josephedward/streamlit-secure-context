// Extensive logging enabled
console.log('App initialization started');
// Register secure service worker for AI-powered security
if ('serviceWorker' in navigator && window.isSecureContext) {
  console.log('Registering service worker: /ai-security-sw.js');
  navigator.serviceWorker.register('/ai-security-sw.js')
    .then(registration => console.log('Service worker registered with scope:', registration.scope))
    .catch(error => console.error('Service worker registration failed:', error));
} else {
  console.warn('Service worker not supported or not in secure context');
}

// Send note to isolated AI iframe for processing
const analyzeBtn = document.getElementById('analyzeBtn');
const noteArea = document.getElementById('note');
const aiFrame = document.getElementById('aiFrame');
const suggestionsDiv = document.getElementById('suggestions');

analyzeBtn.addEventListener('click', () => {
  console.log('Analyze button clicked. Note:', noteArea.value);
  aiFrame.contentWindow.postMessage({
    type: 'analyze',
    note: noteArea.value
  }, window.location.origin);
  console.log('Posted analyze message to AI iframe');
});

window.addEventListener('message', (event) => {
  console.log('Received message in main window:', event);
  if (event.origin !== window.location.origin) {
    console.warn('Ignored message from unknown origin:', event.origin);
    return;
  }
  if (event.data.type === 'suggestions') {
    console.log('Processing suggestions:', event.data);
    const { summary, tags, metrics } = event.data;
    let html = `
      <p><strong>Summary:</strong> ${summary}</p>
      <p><strong>Tags:</strong> ${tags.join(', ')}</p>
    `;
    if (metrics) {
      html += `<p><small>Model Load: ${metrics.loadMs.toFixed(0)} ms | Inference: ${metrics.inferenceMs.toFixed(0)} ms | Classification: ${metrics.toxicityMs ? metrics.toxicityMs.toFixed(0) + ' ms' : 'n/a'} | Confidence: ${metrics.confidence.toFixed(2)}</small></p>`;
    }
    suggestionsDiv.innerHTML = html;
    console.log('Updated suggestions DOM with metrics');
  }
});
