"""Secure Context Demo: in-browser ML inference across two modes."""
import base64
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

# Page configuration
st.set_page_config(page_title="Secure Context Demo", layout="wide")
st.title("🔒 Secure Context Demo")

# ============ Image Classification ============
st.header("Secure Image Classification")
st.write(
    "Process an uploaded or linked image (grayscale/invert) entirely in-browser "
    "within a sandboxed iframe + Web Worker."
)
file = st.file_uploader("Upload an image (PNG/JPG):", type=["png", "jpg", "jpeg"])
if file:
    data = file.read()
    ext = file.type.split("/")[-1]
    img_src = f"data:image/{ext};base64,{base64.b64encode(data).decode()}"
else:
    img_src = st.text_input(
        "Or enter image URL:",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/"
        "PNG_transparency_demonstration_1.png",
    )
mode = st.selectbox("Processing mode:", ["grayscale", "invert"])

security_cfg = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {"default-src": ["'self'"], "script-src": ["'self'", "'wasm-unsafe-eval'"], "worker-src": ["'self'", "blob:"], "img-src": ["'self'", "data:", "https:"]},
    "sandbox": ["allow-scripts", "allow-same-origin"],
    "requireHTTPS": True,
}

if st.button("Process Image"):
    st.info("Processing... look below for results.")
    output = streamlit_secure_context(
        model_path="",
        security_config=security_cfg,
        inference_params={"imageURL": img_src, "action": mode},
        height=600,
    )
    if output:
        st.image(img_src, caption="Original", use_column_width=True)
        st.image(output, caption="Processed", use_column_width=True)
    else:
        st.error("Processing failed. Check DevTools for errors.")

st.markdown("---")

# ============ Iris Inference ============
st.header("Secure Iris Feature Inference")
st.write(
    "Enter Iris feature values below and perform secure TFJS GraphModel inference "
    "inside a sandboxed iframe + Web Worker."
)
iris_url = "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"
url = st.text_input("Model URL:", value=iris_url)

st.sidebar.subheader("Iris Features")
sl = st.sidebar.slider
f1 = sl("Sepal length (cm)", 0.0, 10.0, 5.1, 0.1)
f2 = sl("Sepal width (cm)", 0.0, 10.0, 3.5, 0.1)
f3 = sl("Petal length (cm)", 0.0, 10.0, 1.4, 0.1)
f4 = sl("Petal width (cm)", 0.0, 10.0, 0.2, 0.1)

sec_cfg = {
    "coop": "same-origin",
    "coep": "require-corp",
    "csp": {"default-src": ["'self'"], "script-src": ["'self'", "'wasm-unsafe-eval'"], "worker-src": ["'self'", "blob:"]},
    "sandbox": ["allow-scripts", "allow-same-origin"],
    "requireHTTPS": False,
}
params = {"input": [[f1, f2, f3, f4]], "shape": [1, 4]}

if st.button("Run Iris Inference"):
    st.info("Running inference... result below.")
    res = streamlit_secure_context(
        model_path=url,
        security_config=sec_cfg,
        inference_params=params,
        height=300,
    )
    st.write("Result:", res)