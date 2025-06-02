"""
Interactive Iris Inference Demo using streamlit-secure-context.

This demo allows users to adjust the four Iris features via sliders and run inference
on a TensorFlow.js GraphModel of the Iris dataset—all inside a secure, sandboxed iframe+Web Worker.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

def main():
    """
    Interactive Iris Inference Demo entrypoint.
    """
    st.title("🔒 Interactive Iris Inference Demo")
    st.write(
        "Use the sidebar sliders to specify sepal and petal measurements, then perform secure TFJS inference "
        "inside a browser sandbox without data ever touching your Streamlit server."
    )

# Sidebar: model URL & security settings
iris_url = "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"
model_url = st.sidebar.text_input("Model URL:", iris_url)
require_https = st.sidebar.checkbox("Require HTTPS", value=False)

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

st.sidebar.header("Iris Features")
sl = st.sidebar.slider
sepal_length = sl("Sepal length (cm)", 0.0, 10.0, 5.1, 0.1)
sepal_width = sl("Sepal width (cm)", 0.0, 10.0, 3.5, 0.1)
petal_length = sl("Petal length (cm)", 0.0, 10.0, 1.4, 0.1)
petal_width = sl("Petal width (cm)", 0.0, 10.0, 0.2, 0.1)

inference_params = {
    "input": [[sepal_length, sepal_width, petal_length, petal_width]],
    "shape": [1, 4],
}

    if st.button("Run Inference"):
        with st.spinner("Running secure inference..."):
            result = streamlit_secure_context(
                model_path=model_url,
                security_config=security_config,
                inference_params=inference_params,
                key="iris-demo",
                height=400,
            )
        st.subheader("Inference result")
        st.write(result)
    else:
        st.info("Adjust the sliders and click 'Run Inference' to begin.")

if __name__ == '__main__':
    main()