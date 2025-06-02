"""
Example Streamlit app demonstrating usage of streamlit-secure-context
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

inference_params = {"input": [1, 2, 3]}

result = streamlit_secure_context(
    model_path=model_url,
    security_config=security_config,
    inference_params=inference_params,
    key="demo1",
)

st.write("Inference result:", result)