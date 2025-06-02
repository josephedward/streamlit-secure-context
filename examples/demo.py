"""Secure Context Demo: in-browser ML inference."""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

# Page configuration
st.set_page_config(page_title="Secure Context Demo", layout="wide")
st.title("🔒 Secure Context Demo")

# -- Image Classification Section --
st.header("Secure Image Classification")
st.write(
    "Classify a local image using MobileNet in a sandboxed iframe + Web Worker."
)
image_html = '''
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
        document.getElementById('prediction').innerText =
            predictions.length > 0
                ? `Prediction: ${predictions[0].className} (prob=${predictions[0].probability.toFixed(3)})`
                : "No prediction.";
    };
};
</script>
'''
streamlit_secure_context(image_html, height=600)

st.markdown("---")

# -- Iris Inference Section --
st.header("Secure Iris Inference")
st.write("Use TFJS GraphModel to classify Iris features securely in-browser.")
iris_model_url = "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"

st.sidebar.subheader("Model & Security Settings")
model_url = st.sidebar.text_input("Model URL", value=iris_model_url)
require_https = st.sidebar.checkbox("Require HTTPS", value=False)
security_conf = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {"default-src": ["'self'"], "script-src": ["'self'", "'wasm-unsafe-eval'"], "worker-src": ["'self'", "blob:"]},
    "sandbox": ["allow-scripts", "allow-same-origin"],
    "requireHTTPS": require_https,
}

st.sidebar.subheader("Iris Features")
sl = st.sidebar.slider
feat1 = sl("Sepal length (cm)", 0.0, 10.0, 5.1, 0.1)
feat2 = sl("Sepal width (cm)", 0.0, 10.0, 3.5, 0.1)
feat3 = sl("Petal length (cm)", 0.0, 10.0, 1.4, 0.1)
feat4 = sl("Petal width (cm)", 0.0, 10.0, 0.2, 0.1)
params = {"input": [[feat1, feat2, feat3, feat4]], "shape": [1, 4]}

if st.button("Run Iris Inference"):
    with st.spinner("Running secure inference..."):
        iris_result = streamlit_secure_context(
            model_path=model_url,
            security_config=security_conf,
            inference_params=params,
        )
    st.write("Inference result:", iris_result)