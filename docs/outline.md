# SecureAI Notes - Project Outline

This outline describes the structure and key features of the SecureAI Notes application.

## 1. Overview
- **Goal**: Provide on-device AI-powered note analysis entirely in the browser.
- **Security**: Enforce strict secure context (HTTPS/localhost), COOP/COEP headers, and sandboxed AI code via an iframe.

## 2. File Structure
```
docs/
  └── outline.md        # Project outline and file structure
  └── tutorial.md       # Step-by-step demo instructions
public/
  ├── index.html        # Main UI, security demos, and logs
  ├── ai-iframe.html    # Isolated sandbox for ML inference
  ├── ai-security-sw.js # Service worker for fetch interception
  └── style.css         # Custom styles and theme variables
src/
  ├── main.js           # UI logic & message passing
  ├── ai-iframe.js      # Model loading & inference in iframe
  └── ai-utils.js       # Fallback analyzer & security stubs
README.md
```

## 3. Key Features
- **Secure Context**: All code runs under HTTPS/localhost with COOP/COEP headers and strict CSP.
- **Sandboxed AI**: ML logic loads inside an isolated iframe; no direct DOM access.
- **On-Device Analysis**: Fallback summarization and tagging via regex in `ai-utils.js`.
- **Service Worker**: Monitors all fetch requests and logs anomalies in `ai-security-sw.js`.
- **Logging & Demo**: On-page logs, interactive security demo, and clear messaging API.