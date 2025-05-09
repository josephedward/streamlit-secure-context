// Utility functions for AI processing and security

// Dummy AI: Summarize and tag note
export function analyzeNote(note) {
  const tags = Array.from(new Set(note.match(/\b\w{5,}\b/g) || []));
  const summary = note.split('. ')[0] || '';
  return { summary, tags };
}

// Placeholder: Extract features from a request for anomaly detection
export function featureVector(request) {
  // TODO: Implement feature extraction logic
  return {};
}

// Placeholder: Report anomaly to server endpoint
export function reportAnomaly(data) {
  console.warn('Anomaly reported:', data);
  // TODO: Send report to backend
}