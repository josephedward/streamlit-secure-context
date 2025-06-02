"""
Interactive Iris Inference Demo (Page)

Demonstrates secure ML inference in the browser with adjustable Iris feature sliders
and security settings.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Iris Inference: Interactive Demo")

# Sidebar: Model configuration
model_url = st.sidebar.text_input(
    "Model URL",
    value="https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json",
    help="HTTPS URL to a TFJS GraphModel (e.g., Iris classifier)",
)

# Sidebar: Security settings
require_https = st.sidebar.checkbox(
    "Require HTTPS",
    value=False,
    help="Enforce HTTPS for model loading",
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
sepal_length = st.sidebar.slider("Sepal length (cm)", 0.0, 10.0, 5.1, 0.1)
sepal_width  = st.sidebar.slider("Sepal width (cm)",  0.0, 10.0, 3.5, 0.1)
petal_length = st.sidebar.slider("Petal length (cm)", 0.0, 10.0, 1.4, 0.1)
petal_width  = st.sidebar.slider("Petal width (cm)",  0.0, 10.0, 0.2, 0.1)
inference_params = {
    "input": [[sepal_length, sepal_width, petal_length, petal_width]],
    "shape": [1, 4],
}

# Display configuration and run inference
st.write("## Configuration")
st.write(f"- Model URL: {model_url}")
st.write(f"- requireHTTPS: {require_https}")
st.write(f"- Input: {inference_params['input']}")

if st.button("Run Inference"):
    with st.spinner("Running secure inference..."):
        result = streamlit_secure_context(
            model_path=model_url,
            security_config=security_config,
            inference_params=inference_params,
        )
    st.subheader("Result")
    st.write(result)
else:
    st.info("Adjust settings and click 'Run Inference'.")