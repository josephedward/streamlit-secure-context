import { analyzeNote } from './ai-utils.js';

console.log('AI iframe loaded – using fallback analyzer');

window.addEventListener('message', (event) => {
  console.log('AI iframe received:', event.data);
  if (event.origin !== window.location.origin) return;
  if (event.data.type !== 'analyze') return;

  const note = event.data.note || '';
  const { summary, tags } = analyzeNote(note);

  // Dummy toxicity score = tags count / word count
  const words = note.trim().split(/\s+/).filter(Boolean).length;
  const toxicityScore = words
    ? Math.min(1, tags.length / words)
    : 0;

  const contextInfo = window.isSecureContext
    ? 'Running in Secure Context: isolation is enabled.'
    : 'Not in a secure context (some features may be disabled).';

  // Send it all back in one go
  event.source.postMessage({
    type: 'suggestions',
    summary,
    tags,
    toxicityScore,
    contextInfo
  }, event.origin);
});
