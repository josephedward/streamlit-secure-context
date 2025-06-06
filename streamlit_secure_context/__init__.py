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
# Possible local build locations
_PKG_BUILD_DIR = os.path.join(_MODULE_DIR, "frontend", "build")
_ROOT_BUILD_DIR = os.path.join(_ROOT_DIR, "frontend", "build")

if not _RELEASE:
    # During development, serve component assets from local build
    if os.path.isdir(_PKG_BUILD_DIR):
        _component_path = _PKG_BUILD_DIR
    elif os.path.isdir(_ROOT_BUILD_DIR):
        _component_path = _ROOT_BUILD_DIR
    else:
        raise StreamlitAPIException(
            f"Could not find component build directory at '{_PKG_BUILD_DIR}' or '{_ROOT_BUILD_DIR}'. "
            "Please run 'npm install && npm run build' in the 'frontend' folder, "
            "or use './scripts/bootstrap.sh'."
        )
    _streamlit_secure_context = components.declare_component(
        "streamlit_secure_context",
        path=_component_path,
    )
else:
    # In release mode, load assets from the CDN (unpkg)
    _streamlit_secure_context = components.declare_component(
        "streamlit_secure_context",
        url="https://unpkg.com/streamlit-secure-context@0.1.5/dist/",
    )

def streamlit_secure_context(
    model_path: str,
    security_config: dict = None,
    inference_params: dict = None,
    key: str = None,
    timeout: int = 0,
    **component_kwargs
):
    """
    Embed a secure context component in a Streamlit app.

    Parameters:
    - model_path (str): URL or file path to the ML model (HTTPS recommended in production).
    - security_config (dict, optional): Security parameters (COOP, COEP, CSP, sandbox, HTTPS enforcement).
    - inference_params (dict, optional): Parameters to pass to the ML inference worker.
    - key (str, optional): Identifier for this component instance (required if multiple on one page).
    - timeout (int, optional): Seconds to wait for component initialization before raising an error. Default is 0 (no timeout).
    - **component_kwargs: Additional kwargs (e.g., height, width) forwarded to the Streamlit component.

    Returns:
    - The result object from the frontend worker via `Streamlit.setComponentValue()`.

    Usage:
    ```python
    result = streamlit_secure_context(
        model_path="https://.../model.json",
        security_config={"requireHTTPS": True},
        inference_params={"input": [[1,2,3,4]]},
        key="demo1",
        height=400,
        width=600,
        timeout=30,  # wait up to 30 seconds for the component to load
    )
    ```
    """
    # Only forward timeout if non-zero (0 = no timeout)
    if timeout:
        component_kwargs['timeout'] = timeout
    # Forward additional kwargs (e.g., height, width) to the Streamlit component
    try:
        return _streamlit_secure_context(
            modelPath=model_path,
            securityConfig=security_config or {},
            inferenceParams=inference_params or {},
            key=key,
            **component_kwargs,
        )
    except Exception as e:
        # Provide a clearer error message on timeout or component failure
        raise StreamlitAPIException(
            f"streamlit_secure_context failed or timed out: {e}\n"
            "Ensure the frontend is built (npm run build), modelPath is reachable, and security settings are correct."
        )
