 # Secure ML Inference Demo

 ## Overview
 This is a demo Streamlit application showcasing a secure machine learning inference component
 that runs TensorFlow.js models in a sandboxed iframe inside the browser. The component uses
 browser security features (COOP, COEP, CSP, and Permissions Policy) to enforce strict isolation
 and a secure context for loading and running untrusted model files.

 ## Features
 - Load models via file upload or HTTP fetch (HTTPS only).
 - Strict Content Security Policy (CSP) prevents unauthorized resource loading.
 - Cross-Origin-Opener-Policy (COOP) and Cross-Origin-Embedder-Policy (COEP) support.
 - Permissions Policy to disable camera, microphone, geolocation, and other powerful APIs.
 - Easy integration as a Streamlit component (`secure_ml_component`).

 ## Requirements
 - Python 3.7 or newer
 - pip
 - [Streamlit](https://streamlit.io/)

 ## Installation
 1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
 2. Set up the Python environment:
    ```bash
    bash scripts/setup_env.sh
    ```

 ## Running the App
 Activate the virtual environment (if not already active):
 ```bash
 source .venv/bin/activate
 ```
 Launch the Streamlit application:
 ```bash
 bash scripts/run_app.sh
 ```
 Then open `http://localhost:8501` in your browser.

 ## Component API
 `secure_ml_component` is a Streamlit component with the following signature:
 ```python
 secure_ml_component(
     coop_enabled: bool = False,
     coep_enabled: bool = False,
     sandbox_opts: str = "allow-scripts",
     allow_same_origin: bool = False,
     allowed_sources: list[str] = None,
     allow_inline_scripts: bool = False,
     message_types: list[str] = None,
     height: int = 600
 )
 ```
 - **coop_enabled**: Enable Cross-Origin-Opener-Policy.
 - **coep_enabled**: Enable Cross-Origin-Embedder-Policy.
 - **sandbox_opts**: Space-separated sandbox attributes for the iframe (e.g., `"allow-scripts allow-same-origin"`).
 - **allow_same_origin**: If `True`, adds `allow-same-origin` to the sandbox attributes.
 - **allowed_sources**: List of domains (e.g., `"cdn.jsdelivr.net"`) allowed to fetch model files.
 - **allow_inline_scripts**: If `True`, allows inline scripts in the iframe (reduces security).
 - **message_types**: List of iframe message types to handle (`"status"`, `"model-loaded"`, etc.).
 - **height**: Height of the component (iframe) in pixels.

 ## Project Structure
 ```
 .
 ├── app.py
 ├── README.md
 ├── requirements.txt
 ├── scripts
 │   ├── setup_env.sh
 │   └── run_app.sh
 └── securecontext_component
     ├── __init__.py
     └── secure_ml_component.py
 ```

 ## Development
 - Scripts in `scripts/` help set up and run the app.
 - Modify `secure_ml_component.py` to adjust policies or UI behavior.
 - Use `streamlit run app.py` for quick testing.

 ## License
 This project is open-source under the MIT License.