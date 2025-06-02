"""
Example Streamlit app demonstrating usage of streamlit-secure-context.

Under the hood, when you run:
    streamlit run examples/basic_demo.py

1. Your code calls `streamlit_secure_context(...)`, invoking the low-level component.
2. The component creates a sandboxed iframe with your CSP, COOP, and COEP settings.
3. The iframe loader spins up a Web Worker and posts an INIT message with the model path.
4. The Worker loads the model (TFJS, TFLite, or ONNX) off the main thread.
5. After INIT_DONE, the component sends an INFER message with `inference_params`.
6. The Worker runs inference, posts back RESULT, and the component returns the result to Python.
7. You simply call `st.write("Inference result:", result)` to display the array.

Tips:
- Inspect DevTools → Application → Frames to verify the sandbox.
- Add `console.log` in `worker.js` or `model_iframe.html` to debug messages.
- Swap in a real model URL and update `inference_params` (e.g., add a `shape` key) to see genuine ML outputs.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Secure ML Inference Demo")

# Sample model URL (replace with your own model path)
model_url = "https://example.com/model.tflite"

security_config = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'wasm-unsafe-eval'"],
        "worker-src": ["'self'", "blob:"],
    },
    # For local development, allow HTTP; set to True in production
    "requireHTTPS": False,
    "sandbox": ["allow-scripts", "allow-same-origin"],
}

st.sidebar.header("Inference Params")
user_input = st.sidebar.text_input("Input array (comma-separated)", "1,2,3")
input_list = [int(x.strip()) for x in user_input.split(",") if x.strip().isdigit()]
inference_params = {"input": input_list}

if st.sidebar.button("Run Inference"):
    result = streamlit_secure_context(
        model_path=model_url,
        security_config=security_config,
        inference_params=inference_params,
        key="demo1",
    )
    st.write("Inference result:", result)
else:
    st.write("Change input in sidebar and click 'Run Inference'")
