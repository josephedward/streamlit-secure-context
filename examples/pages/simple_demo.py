"""
Simple Iris Inference Demo (Page)

Runs a single inference on the Iris TFJS GraphModel with hard-coded inputs.
Demonstrates secure context setup with minimal code.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Iris Inference: Simple Demo")

# Security config for simple demo
security_config = {"requireHTTPS": False}

# Inference params: one Iris example
inference_params = {"input": [[5.1, 3.5, 1.4, 0.2]], "shape": [1, 4]}

# Execute component and display result
result = streamlit_secure_context(
    model_path="https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json",
    security_config=security_config,
    inference_params=inference_params,
)
st.write("Inference result:", result)