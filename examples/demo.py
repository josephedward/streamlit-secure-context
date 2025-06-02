"""Unified Demo for streamlit-secure-context Component.

This single Streamlit app provides two demos:
  1. Secure Image Classification using a MobileNet model in a sandboxed iframe + Web Worker
  2. Secure Iris model inference via TFJS GraphModel with interactive sliders or a simple one-shot mode
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.set_page_config(page_title="Secure Context Demos")
st.title("🔒 Streamlit Secure Context Demos")

# Top-level demo selector
demo_choice = st.sidebar.selectbox(
    "Select Demo",
    ["Image Classification", "Iris Inference"]
)

if demo_choice == "Image Classification":
    st.header("🔒 Secure Image Classification Demo")
    st.write(
        "Classify a local image using a pretrained MobileNet model "
        "running entirely in the browser (sandboxed iframe + Web Worker)."
    )
    html_code = '''
<input type="file" id="imginput" accept="image/*"/>
<br/><br/>
<img id="imgpreview" width="224" style="display:none;"/>
<p id="prediction">No image selected.</p>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet"></script>
<script>
document.getElementById('imginput').onchange = async function(evt) {
    const file = evt.target.files[0];
    if (!file) return;
    const img = document.getElementById('imgpreview');
    img.src = URL.createObjectURL(file);
    img.style.display = 'block';
    img.onload = async () => {
        document.getElementById('prediction').innerText = "Loading model...";
        const model = await mobilenet.load();
        const predictions = await model.classify(img);
        if (predictions.length > 0) {
            document.getElementById('prediction').innerText =
                `Prediction: ${predictions[0].className} (prob=${predictions[0].probability.toFixed(3)})`;
        } else {
            document.getElementById('prediction').innerText = "No prediction.";
        }
    };
};
</script>
'''
    streamlit_secure_context(html_code, height=600)

else:
    st.header("🔒 Secure Iris Inference Demo")
    mode = st.radio(
        "Mode",
        ["Interactive", "Simple"],
        index=0,
    )
    # Common model URL
    iris_model = (
        "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"
    )
    if mode == "Simple":
        st.write("## Simple Mode")
        st.write(
            "Running single inference on Iris TFJS model with default inputs: [5.1, 3.5, 1.4, 0.2]."
        )
        security_config = {"requireHTTPS": False}
        inference_params = {"input": [[5.1, 3.5, 1.4, 0.2]], "shape": [1, 4]}
        result = streamlit_secure_context(
            model_path=iris_model,
            security_config=security_config,
            inference_params=inference_params,
        )
        st.write("Inference result:", result)
    else:
        # Interactive mode
        st.write("## Interactive Mode")
        model_url = st.text_input(
            "Model URL",
            value=iris_model,
            help="HTTPS URL to a TFJS GraphModel (e.g., Iris classifier)",
        )
        require_https = st.checkbox(
            "Require HTTPS",
            value=False,
            help="Enforce HTTPS for model loading (recommended)",
        )
        security_config = {
            "coop": "same-origin",
            "coep": "require-corp",
            "csp": {
                "default-src": ["'self'"],
                "script-src": ["'self'", "'wasm-unsafe-eval'"],
                "worker-src": ["'self'", "blob:"],
            },
            "sandbox": ["allow-scripts", "allow-same-origin"],
            "requireHTTPS": require_https,
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
        st.write("### Configuration")
        st.write(f"- HTTPS required: {require_https}")
        st.write(f"- Input: {inference_params['input']}")
        if st.button("Run Inference"):
            with st.spinner("Running secure inference..."):
                result = streamlit_secure_context(
                    model_path=model_url,
                    security_config=security_config,
                    inference_params=inference_params,
                    key="iris-interactive",
                )
            if result is not None:
                st.success("Inference completed successfully!")
                st.write("Result:", result)
            else:
                st.error("No result returned. Check DevTools for errors.")