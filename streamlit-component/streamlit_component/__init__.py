"""
Python API for Secure ML Streamlit Component.
Provides `secure_ml_component()` to embed a secure ML inference widget in Streamlit apps.
"""
import os
import streamlit.components.v1 as components

# Toggle between development mode (local build) and release mode (CDN-hosted)
_RELEASE = False

# Compute path to the frontend build directory
_MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_MODULE_DIR, os.pardir))
_BUILD_DIR = os.path.join(_ROOT_DIR, "frontend", "build")

if not _RELEASE:
    # During development, serve the component assets from the local frontend build
    _secure_ml = components.declare_component(
        "secure_ml",
        path=_BUILD_DIR,
    )
else:
    # In release mode, load assets from the CDN (unpkg)
    _secure_ml = components.declare_component(
        "secure_ml",
        url="https://unpkg.com/secure-ml-component@1.0/dist/",
    )

def secure_ml_component(
    model_path: str,
    security_config: dict = None,
    inference_params: dict = None,
    key: str = None,
):
    """
    Embed a secure ML inference component in a Streamlit app.

    Parameters:
    - model_path (str): URL or file path to the ML model (HTTPS recommended in production).
    - security_config (dict): Security parameters for COOP, COEP, CSP, sandbox, and HTTPS enforcement.
    - inference_params (dict): Parameters for the ML inference worker.
    - key (str): Optional identifier for this component instance.

    Returns:
    - The result object returned by the frontend worker via `Streamlit.setComponentValue()`.
    """
    return _secure_ml(
        modelPath=model_path,
        securityConfig=security_config or {},
        inferenceParams=inference_params or {},
        key=key,
    )