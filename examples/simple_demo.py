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

st.write("Inference result:", result)