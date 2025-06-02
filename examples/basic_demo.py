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

st.title("Secure ML Inference Demo (Interactive)")
# Brief instructions for the demo
st.markdown(
    """
Use the sidebar on the left to:
- Enter your model URL (default: Iris classifier)
- Toggle HTTPS enforcement
- Adjust the four Iris feature values via sliders
Click **Run Inference** when ready.
"""
)


# Sidebar: Model configuration (default: TFJS Iris model)
model_url = st.sidebar.text_input(
    "Model URL",
    value="https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json",
    help="HTTPS URL to a TFJS GraphModel (e.g., Iris classifier)",
)

# Sidebar: Security settings
require_https = st.sidebar.checkbox(
    "Require HTTPS",
    value=False,
    help="Enforce HTTPS for model loading (recommended in production)",
)
security_config = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'wasm-unsafe-eval'"],
        "worker-src": ["'self'", "blob:"],
    },
    "requireHTTPS": require_https,
    "sandbox": ["allow-scripts", "allow-same-origin"],
}

# Sidebar: Inference parameters for Iris features
st.sidebar.header("Inference Parameters (Iris)")
sepal_length = st.sidebar.slider(
    "Sepal length (cm)", min_value=0.0, max_value=10.0, value=5.1, step=0.1
)
sepal_width = st.sidebar.slider(
    "Sepal width (cm)", min_value=0.0, max_value=10.0, value=3.5, step=0.1
)
petal_length = st.sidebar.slider(
    "Petal length (cm)", min_value=0.0, max_value=10.0, value=1.4, step=0.1
)
petal_width = st.sidebar.slider(
    "Petal width (cm)", min_value=0.0, max_value=10.0, value=0.2, step=0.1
)
# Prepare input as 2D array for TFJS GraphModel ([1,4])
inference_params = {
    "input": [[sepal_length, sepal_width, petal_length, petal_width]],
    "shape": [1, 4],
}

# Display current configuration
st.write("## Current Configuration")
st.write(f"- Model URL: {model_url}")
st.write(f"- requireHTTPS: {require_https}")
st.write(f"- Inference input (shape {inference_params['shape']}): {inference_params['input']}")

# Run inference on button click
if st.button("Run Inference"):
    with st.spinner("Running secure inference..."):
        result = streamlit_secure_context(
            model_path=model_url,
            security_config=security_config,
            inference_params=inference_params,
            key="interactive-demo",
        )
    if result is not None:
        st.success("Inference completed successfully!")
        st.write("Result:", result)
    else:
        st.error("No result returned. Check DevTools for errors.")
else:
    st.info("Adjust the inputs in the sidebar and click 'Run Inference' to start.")
# Related Projects section removed: external repos are empty and not relevant for this demo.
