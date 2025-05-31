"""
Python API for streamlit-secure-context Component.
Provides `streamlit_secure_context()` to embed a secure context widget in Streamlit apps.
"""
import os
import streamlit.components.v1 as components
from streamlit.errors import StreamlitAPIException

# Toggle between development mode (local build) and release mode (CDN-hosted)
_RELEASE = False

# Compute path to the frontend build directory
_MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_MODULE_DIR, os.pardir))
_BUILD_DIR = os.path.join(_ROOT_DIR, "frontend", "build")

if not _RELEASE:
    # During development, serve the component assets from the local frontend build
    if not os.path.isdir(_BUILD_DIR):
        raise StreamlitAPIException(f"Frontend build not found at {_BUILD_DIR}. Please run 'npm install && npm run build' in the frontend directory.")
    _streamlit_secure_context = components.declare_component(
        "streamlit_secure_context",
        path=_BUILD_DIR,
    )
else:
    # In release mode, load assets from the CDN (unpkg)
    _streamlit_secure_context = components.declare_component(
        "streamlit_secure_context",
        url="https://unpkg.com/streamlit-secure-context@0.1.0/dist/",
    )

def streamlit_secure_context(
    model_path: str,
    security_config: dict = None,
    inference_params: dict = None,
    key: str = None,
):
    """
    Embed a secure context component in a Streamlit app.

    Parameters:
    - model_path (str): URL or file path to the ML model (HTTPS recommended in production).
    - security_config (dict): Security parameters for COOP, COEP, CSP, sandbox, and HTTPS enforcement.
    - inference_params (dict): Parameters for the ML inference worker.
    - key (str): Optional identifier for this component instance.

    Returns:
    - The result object returned by the frontend worker via `Streamlit.setComponentValue()`.
    - For HIPAA compliance, ensure `requireHTTPS` is enabled, host assets locally, and keep PHI processing within the client browser.
    """
    return _streamlit_secure_context(
        modelPath=model_path,
        securityConfig=security_config or {},
        inferenceParams=inference_params or {},
        key=key,
    )
