"""
Simple demo of streamlit-secure-context.

Runs a single inference on the Iris TFJS GraphModel with hard-coded inputs.
Demonstrates secure context setup with minimal code.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Simple Secure Context Demo")

# Security config: disable HTTPS enforcement for local development
security_config = {"requireHTTPS": False}

# Inference parameters: one example of four Iris features
inference_params = {
    "input": [[5.1, 3.5, 1.4, 0.2]],
    "shape": [1, 4],
}

# Run inference and display result
result = streamlit_secure_context(
    model_path="https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json",
    security_config=security_config,
    inference_params=inference_params,
    key="simple-demo",
)

st.write("Inference result:", result)#!/usr/bin/env python3
"""
Simple Streamlit app demonstrating secure ML inference with no UI extras.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Secure ML Inference: Simple Demo")

# Default Iris TFJS GraphModel URL
model_url = "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"

# Security configuration (disable HTTPS enforcement for local demo)
security_config = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'wasm-unsafe-eval'"],
        "worker-src": ["'self'", "blob:"],
    },
    "requireHTTPS": False,
    "sandbox": ["allow-scripts", "allow-same-origin"],
}

# Hard-coded inference parameters ([1,4] for Iris model)
inference_params = {
    "input": [[5.1, 3.5, 1.4, 0.2]],
    "shape": [1, 4],
}

# Run secure inference and display result
result = streamlit_secure_context(
    model_path=model_url,
    security_config=security_config,
    inference_params=inference_params,
    key="simple-demo",
)

st.write("Inference result:", result)
