// Override console methods to also log to on-page log container
(() => {
  if (typeof document.getElementById !== 'function') return;
  const logContainer = document.getElementById('log');
  if (!logContainer) return;
  const origLog = console.log;
  const origWarn = console.warn;
  const origError = console.error;
  console.log = (...args) => { origLog.apply(console, args); const d = document.createElement('div'); d.textContent = args.join(' '); logContainer.appendChild(d); };
  console.warn = (...args) => { origWarn.apply(console, args); const d = document.createElement('div'); d.style.color='orange'; d.textContent = args.join(' '); logContainer.appendChild(d); };
  console.error = (...args) => { origError.apply(console, args); const d = document.createElement('div'); d.style.color='red'; d.textContent = args.join(' '); logContainer.appendChild(d); };
})();

console.log('App initialization started');

// Theme toggle (light/dark)
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
  });
}

// Register service worker for security monitoring
if ('serviceWorker' in navigator && window.isSecureContext) {
  console.log('Registering service worker');
  navigator.serviceWorker.register('/ai-security-sw.js')
    .then(reg => console.log('SW scope:', reg.scope))
    .catch(err => console.error('SW registration failed:', err));
} else {
  console.warn('Service worker unsupported or insecure context');
}

// Main elements
const analyzeBtn = document.getElementById('analyzeBtn');
const noteArea = document.getElementById('note');
const suggestionsDiv = document.getElementById('suggestions');
const aiFrame = document.getElementById('aiFrame');

// Click handler
if (analyzeBtn && noteArea && aiFrame) {
  analyzeBtn.addEventListener('click', () => {
    console.log('Analyze button clicked. Note:', noteArea.value);
    // Show simple loading state
    suggestionsDiv.innerHTML = '<p>Analyzing…</p>';
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing…';
    aiFrame.contentWindow.postMessage({ type: 'analyze', note: noteArea.value }, window.location.origin);
  });
}

// Receive suggestions
window.addEventListener('message', (event) => {
  console.log('Main window received message:', event.data);
  // Handle Service Worker logs
  if (event.data.type === 'sw-log') {
    const sw = document.getElementById('swLogs');
    if (sw) { sw.textContent += event.data.message + '\n'; sw.scrollTop = sw.scrollHeight; }
    return;
  }
  console.log('Main window origin and type:', event.origin, event.data && event.data.type);
  if (event.origin !== window.location.origin) {
    console.warn('Ignored message from unknown origin:', event.origin);
    return;
  }
  if (event.data.type !== 'suggestions') return;

  const { summary, tags, toxicityScore, contextInfo } = event.data;
  console.log('Suggestions payload unpacked:', { summary, tags, toxicityScore, contextInfo });
  let html = `
    <p><strong>Summary:</strong> ${summary}</p>
    <p><strong>Tags:</strong> ${tags.join(', ') || '—'}</p>
    <p><strong>Toxicity Score:</strong> ${toxicityScore.toFixed(2)}</p>
    <p><em>${contextInfo}</em></p>`;
  suggestionsDiv.innerHTML = html;
  analyzeBtn.disabled = false;
  analyzeBtn.textContent = 'AI Suggest';
  console.log('Updated suggestions segment, reset analyze button');
});
