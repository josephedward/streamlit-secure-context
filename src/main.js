// Register secure service worker for AI-powered security
if ('serviceWorker' in navigator && window.isSecureContext) {
  navigator.serviceWorker.register('/ai-security-sw.js');
}

// Send note to isolated AI iframe for processing
const analyzeBtn = document.getElementById('analyzeBtn');
const noteArea = document.getElementById('note');
const aiFrame = document.getElementById('aiFrame');
const suggestionsDiv = document.getElementById('suggestions');

analyzeBtn.addEventListener('click', () => {
  aiFrame.contentWindow.postMessage({
    type: 'analyze',
    note: noteArea.value
  }, window.location.origin);
});

window.addEventListener('message', (event) => {
  if (event.origin !== window.location.origin) return;
  if (event.data.type === 'suggestions') {
    suggestionsDiv.innerHTML = `
      <p><strong>Summary:</strong> ${event.data.summary}</p>
      <p><strong>Tags:</strong> ${event.data.tags.join(', ')}</p>
    `;
  }
});