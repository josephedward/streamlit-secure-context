---
title: SecureAI Notes Security Tutorial
---

# SecureAI Notes: Security & Isolation Testing Tutorial

This guide shows you how to test the SecureAI Notes demo’s core security features:
- Service Worker network interception
- Iframe sandbox DOM isolation
- Message-passing isolation

## Prerequisites
- Node.js (v14+) & npm
- Modern browser (Chrome/Firefox/Edge) with Service Worker & sandbox support

## 1. Run Locally
Install dependencies:
```bash
npm install
```
Start the app:
```bash
npm start
```
Open your browser at http://localhost:8080

## 2. Service Worker Logs
Expand the **Service Worker Logs** panel. You should see:
- `install` (skipWaiting)
- `activate` (clients.claim)
- A fetch event for the current page

## 3. Sandbox Isolation Test
In the **Sandbox Isolation Test** section, click **Attempt Parent DOM Access** inside the iframe.
Confirm the iframe logs:
```
✅ Access denied, sandbox isolation enforced.
```
and that your page background remains unchanged.

## 4. Network Interception Test
Click **Test Network Interception**.
The app will fetch `/`, and the SW log panel will record the event.

## 5. Message Isolation Test
Click **Test Message Isolation**.
A simulated message from `evil.com` is dispatched and ignored (no SW log).

## Troubleshooting
- No SW logs? Hard-reload (Ctrl+Shift+R) to let the SW activate.
- Sandbox test silent? Verify `sandbox="allow-scripts"` (no allow-same-origin).

---
*End of Security Testing Tutorial.*