// Main script: communicate with AI iframe and update UI
window.addEventListener('DOMContentLoaded', () => {
  // Mirror console logs in the on-page log panel
  const logDiv = document.getElementById('log');
  if (logDiv) {
    ['log', 'warn', 'error'].forEach(level => {
      const orig = console[level].bind(console);
      console[level] = (...args) => {
        orig(...args);
        const entry = document.createElement('div');
        entry.className = level === 'warn'
          ? 'ui yellow message'
          : level === 'error'
            ? 'ui red message'
            : 'ui message';
        entry.textContent = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
        logDiv.appendChild(entry);
        logDiv.scrollTop = logDiv.scrollHeight;
      };
    });
  }

  console.log('App loaded in secure context:', window.isSecureContext);
  // Service Worker registration & log forwarding
  const swLogsEl = document.getElementById('swLogs');
  function swLog(msg) {
    if (swLogsEl) swLogsEl.textContent += msg + '\n';
  }
  if ('serviceWorker' in navigator && window.isSecureContext) {
    navigator.serviceWorker.register('/ai-security-sw.js')
      .then(reg => {
        console.log('Service Worker registered with scope:', reg.scope);
        swLog(`Service Worker registered: ${reg.scope}`);
        // Trigger a dummy fetch so SW fetch listener fires and logs
        console.log('Triggering test fetch so SW can log it');
        fetch(window.location.href)
          .then(() => console.log('Test fetch done'))
          .catch(err => console.error('Test fetch error:', err));
      })
      .catch(err => {
        console.error('Service Worker registration failed:', err);
        swLog(`Service Worker registration failed: ${err}`);
      });
    navigator.serviceWorker.addEventListener('message', event => {
      if (event.data && event.data.type === 'sw-log') {
        console.log('SW log:', event.data.message);
        swLog(event.data.message);
      }
    });
  } else {
    swLog('Service Worker not supported or not in secure context');
  }
  // Populate security status indicators
  const secureSpan = document.getElementById('secureContextStatus');
  if (secureSpan) secureSpan.textContent = window.isSecureContext ? '✅ yes' : '❌ no';
  const coiSpan = document.getElementById('crossOriginIsolatedStatus');
  if (coiSpan) {
    const isolated = typeof navigator.crossOriginIsolated === 'boolean' && navigator.crossOriginIsolated;
    coiSpan.textContent = isolated ? '✅ yes' : '❌ no';
  }

  const analyzeBtn = document.getElementById('analyzeBtn');
  const noteArea = document.getElementById('note');
  const suggestionsDiv = document.getElementById('suggestions');
  const aiFrame = document.getElementById('aiFrame');
  // Wire up example note loader dropdown
  const exampleSelector = document.getElementById('exampleSelector');
  if (exampleSelector && noteArea && suggestionsDiv) {
    exampleSelector.addEventListener('change', () => {
      console.log('Loading example note:', exampleSelector.value);
      noteArea.value = exampleSelector.value;
      suggestionsDiv.innerHTML = '';
    });
  }

  if (analyzeBtn && noteArea && suggestionsDiv && aiFrame) {
    analyzeBtn.addEventListener('click', () => {
      console.log('Analyze button clicked. Note:', noteArea.value);
      suggestionsDiv.innerHTML = '<p>Analyzing…</p>';
      aiFrame.contentWindow.postMessage(
        { type: 'analyze', note: noteArea.value },
        window.location.origin
      );
      console.log('Posted analyze message to AI iframe');
    });
  }
  // Add interactive security demo buttons
  const testNetworkBtn = document.getElementById('testNetworkBtn');
  const testMessageBtn = document.getElementById('testMessageBtn');
  const securityDemoResults = document.getElementById('securityDemoResults');
  if (testNetworkBtn && securityDemoResults) {
    testNetworkBtn.addEventListener('click', () => {
      securityDemoResults.innerHTML = '<p>Sending request to example.com…</p>';
      fetch('https://example.com')
        .then(() => {
          securityDemoResults.innerHTML += '<p class="ui green message">✅ Intercepted by Service Worker—check logs.</p>';
        })
        .catch(err => {
          securityDemoResults.innerHTML += `<p class="ui red message">❌ Fetch failed: ${err.message}</p>`;
        });
    });
  }
  if (testMessageBtn && securityDemoResults) {
    testMessageBtn.addEventListener('click', () => {
      securityDemoResults.innerHTML = '<p>Dispatching malicious message from evil.com…</p>';
      window.dispatchEvent(new MessageEvent('message', {
        data: { type: 'analyze', note: 'attack' },
        origin: 'http://evil.com'
      }));
      setTimeout(() => {
        securityDemoResults.innerHTML += '<p class="ui green message">✅ Malicious message ignored by our handler.</p>';
      }, 500);
    });
  }

  window.addEventListener('message', (event) => {
    console.log('Received message in main window:', event);
    if (event.origin !== window.location.origin) {
      console.warn('Ignored message from unknown origin:', event.origin);
      return;
    }
    if (event.data.type !== 'suggestions') return;
    const { summary, tags, toxicityScore, contextInfo } = event.data;
    const html = `
      <p><strong>Summary:</strong> ${summary}</p>
      <p><strong>Tags:</strong> ${tags.join(', ') || '—'}</p>
      <p><strong>Toxicity Score:</strong> ${toxicityScore.toFixed(2)}</p>
      <p><em>${contextInfo}</em></p>`;
    suggestionsDiv.innerHTML = html;
    console.log('Updated suggestions with summary, tags, toxicity score, and context info');
  });
});