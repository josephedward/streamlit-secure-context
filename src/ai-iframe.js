import { analyzeNote } from './ai-utils.js';

// Simplified AI iframe: using fallback analyzer for summarization and tagging
console.log('AI iframe loaded – using fallback analyzer');

window.addEventListener('message', (event) => {
  console.log('AI iframe received message:', event.data);
  if (event.origin !== window.location.origin) {
    console.warn('Ignored message from origin:', event.origin);
    return;
  }
  if (event.data.type !== 'analyze') {
    console.warn('Ignored unsupported message type:', event.data.type);
    return;
  }
  const note = event.data.note || '';
  const { summary, tags } = analyzeNote(note);

  // Dummy toxicity score: ratio of tags to word count
  const words = note.trim().split(/\s+/).filter(Boolean).length;
  const toxicityScore = words ? Math.min(1, tags.length / words) : 0;

  // Secure Context info
  const contextInfo = window.isSecureContext
    ? 'Running in Secure Context: isolation enforced.'
    : 'Not in a secure context; some features disabled.';

  // Post suggestions back to main window
  event.source.postMessage({
    type: 'suggestions',
    summary,
    tags,
    toxicityScore,
    contextInfo
  }, event.origin);
});
