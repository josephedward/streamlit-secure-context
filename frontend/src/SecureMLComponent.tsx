// Frontend entrypoint for Secure ML Streamlit Component
import React from "react";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";

// Security configuration interface matching Python API options
interface SecurityConfig {
  coop?: "same-origin" | "same-origin-allow-popups";
  coep?: "require-corp" | "credentialless";
  csp?: { [directive: string]: string | string[] };
  sandbox?: string[];
  requireHTTPS?: boolean;
}

// Default security parameters (COOP, COEP, CSP, sandbox, HTTPS enforcement)
const defaultSecurityConfig: SecurityConfig = {
  coop: "same-origin",
  coep: "require-corp",
  csp: {
    "default-src": "'self'",
    // Allow loading TFJS and ORT from CDN
    "script-src": ["'self'", "'wasm-unsafe-eval'", "https://cdn.jsdelivr.net"],
    "worker-src": ["'self'", "blob:", "https://cdn.jsdelivr.net"],
  },
  sandbox: ["allow-scripts", "allow-same-origin"],
  requireHTTPS: true,
};

// Inject a dynamic Content Security Policy meta tag into document head
function applyCSP(directives: { [directive: string]: string | string[] }): void {
  const content = Object.entries(directives)
    .map(([k, v]) => `${k} ${Array.isArray(v) ? v.join(" ") : v}`)
    .join("; ");
  const meta = document.createElement("meta");
  meta.httpEquiv = "Content-Security-Policy";
  meta.content = content;
  document.head.appendChild(meta);
}

// Ensure Cross-Origin Isolation is enabled via COOP/COEP headers
function verifyIsolation(): void {
  if (!crossOriginIsolated) {
    throw new Error(
      "Cross-Origin Isolation failed. Required headers:\n" +
        "- Cross-Origin-Embedder-Policy: require-corp\n" +
        "- Cross-Origin-Opener-Policy: same-origin"
    );
  }
}

// Create a sandboxed iframe for hosting the ML model and inference worker
function createSecureIframe(
  modelPath: string,
  config: SecurityConfig
): HTMLIFrameElement {
  const iframe = document.createElement("iframe");
  iframe.sandbox = (config.sandbox || defaultSecurityConfig.sandbox)!.join(" ");
  iframe.allow = "";
  iframe.src = `model_iframe.html?modelPath=${encodeURIComponent(
    modelPath
  )}`;
  iframe.style.border = "none";
  return iframe;
}

// Manage a dedicated Web Worker for ML inference
class WorkerManager {
  private worker: Worker;
  private readyPromise: Promise<void>;

  constructor(private modelPath: string) {
    const workerCode = `
      self.onmessage = async (e) => {
        const { type, modelPath, params } = e.data;
        if (type === 'INIT') {
          self.postMessage({ type: 'INIT_DONE' });
        } else if (type === 'INFER') {
          const result = { output: 'dummy inference result' };
          self.postMessage({ type: 'RESULT', result });
        }
      };
    `;
    const blob = new Blob([workerCode], { type: "application/javascript" });
    const url = URL.createObjectURL(blob);
    this.worker = new Worker(url);
    this.readyPromise = new Promise((resolve) => {
      this.worker.onmessage = (e) => {
        if (e.data.type === "INIT_DONE") {
          resolve();
        }
      };
    });
    this.worker.postMessage({ type: "INIT", modelPath });
  }

  public ready(): Promise<void> {
    return this.readyPromise;
  }

  public infer(params: any): Promise<any> {
    return new Promise((resolve) => {
      this.worker.onmessage = (e) => {
        if (e.data.type === "RESULT") {
          resolve(e.data.result);
        }
      };
      this.worker.postMessage({ type: "INFER", params });
    });
  }
}

// Main component implementing the Streamlit component lifecycle
class SecureMLComponent extends StreamlitComponentBase {
  private containerRef = React.createRef<HTMLDivElement>();
  private iframeWindow?: Window;

  public componentDidMount(): void {
    // Initialize security, iframe, and worker communication
    try {
      const args = this.props.args as Record<string, any>;
      const modelPath: string = args["modelPath"];
      const securityConfig: SecurityConfig =
        args["securityConfig"] || defaultSecurityConfig;
      const inferenceParams: any = args["inferenceParams"] || {};

      // Enforce HTTPS if requested
      if (securityConfig.requireHTTPS && location.protocol !== "https:") {
        throw new Error("HTTPS required for secure context.");
      }
      // Apply CSP and verify cross-origin isolation
      applyCSP(securityConfig.csp || defaultSecurityConfig.csp!);
      verifyIsolation();

      // Create and embed the secure iframe
      const iframe = createSecureIframe(modelPath, securityConfig);
      iframe.style.width = "100%";
      iframe.style.height = "500px";
      const container = this.containerRef.current;
      if (container) {
        container.innerHTML = "";
        container.appendChild(iframe);
      }
      // Listen for messages from the iframe
      window.addEventListener("message", (e) =>
        this.handleIframeMessage(e, inferenceParams)
      );
      this.iframeWindow = iframe.contentWindow!;
    } catch (err: any) {
      Streamlit.setComponentValue({ error: err.message });
    }
  }

  private handleIframeMessage(
    event: MessageEvent,
    inferenceParams: any
  ): void {
    // Route messages between parent and the iframe worker
    const data = event.data;
    if (data.type === "IFRAME_READY") {
      this.iframeWindow!.postMessage(
        { type: "INIT", modelPath: this.props.args["modelPath"] },
        "*"
      );
    } else if (data.type === "INIT_DONE") {
      this.iframeWindow!.postMessage(
        { type: "INFER", params: inferenceParams },
        "*"
      );
    } else if (data.type === "RESULT") {
      Streamlit.setComponentValue(data.result);
    } else if (data.type === "ERROR") {
      // Forward worker error to Python side
      Streamlit.setComponentValue({ error: data.error });
    }
  }

  public render(): React.ReactNode {
    // Placeholder container for dynamic iframe insertion
    return <div ref={this.containerRef}>Initializing Secure ML...</div>;
  }
}

export default withStreamlitConnection(SecureMLComponent);