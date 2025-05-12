"""app.py

Demo Streamlit application showcasing the secure ML inference component.

Usage:
  streamlit run app.py

This app initializes the secure_ml_component with configurable security options:
 - COOP/COEP policies
 - Sandbox attributes
 - Content Security Policy for allowed sources
 - UI controls for uploading/fetching models and running inference
"""
import streamlit as st
from securecontext_component.secure_ml_component import secure_ml_component

# Demo app for Secure ML Inference Component
st.title("Secure ML Inference Demo")
st.write("This component runs a TensorFlow.js model in a sandboxed iframe.")

## Render the secure ML inference component with specified security settings
secure_ml_component(
    coop_enabled=False,  # COOP disabled by default
    coep_enabled=False,  # COEP disabled by default
    sandbox_opts="allow-scripts",  # Allow scripts only in sandbox
    allow_same_origin=False,  # Disallow same-origin for stronger isolation
    allowed_sources=[  # Domains allowed for fetching model files
        "cdn.jsdelivr.net",
        "storage.googleapis.com",
    ],
    message_types=[  # Message types to process from the iframe
        "sandbox-info",
        "fetch-log",
        "status",
        "model-loaded",
        "inference-result",
    ],
    height=600,  # Height of the iframe in pixels
)