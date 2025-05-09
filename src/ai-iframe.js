import { analyzeNote } from './ai-utils.js';

// Simplified AI iframe: using fallback analyzer for summarization and tagging
console.log('AI iframe script loaded – using fallback fallback analyzer');

window.addEventListener('message', (event) => {
  console.log('AI iframe received message event:', event);
  console.log('Message origin and data type:', event.origin, event.data && event.data.type);
  if (event.origin !== window.location.origin) {
    console.warn('Ignored message from unknown origin:', event.origin);
    return;
  }
  if (event.data.type !== 'analyze') {
    console.warn('Ignored unsupported message type:', event.data.type);
    return;
  }
  const note = event.data.note || '';
  console.log('Extracted note for analysis:', note);
  const { summary, tags } = analyzeNote(note);
  console.log('Basic analyzer results - summary:', summary, 'tags:', tags);

  // Dummy toxicity score: ratio of tags to word count
  const words = note.trim().split(/\s+/).filter(Boolean).length;
  console.log('Word count for toxicity calculation:', words);
  const toxicityScore = words ? Math.min(1, tags.length / words) : 0;
  console.log('Calculated dummy toxicityScore:', toxicityScore);

  // Secure Context info
  const contextInfo = window.isSecureContext
    ? 'Running in Secure Context: isolation enforced.'
    : 'Not in a secure context; some features disabled.';
  console.log('Secure context status:', window.isSecureContext, contextInfo);

  // Posting suggestions back to main window
  const payload = { type: 'suggestions', summary, tags, toxicityScore, contextInfo };
  console.log('Posting suggestions payload to parent:', payload);
  event.source.postMessage(payload, event.origin);
  console.log('Posted suggestions back to parent');
});
