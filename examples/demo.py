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

# 1) Sidebar selector for page
page = st.sidebar.selectbox("Select Demo", ["Image Processing", "Iris Inference"])
st.sidebar.markdown("---")

if page == "Image Processing":
    st.title("🔒 Secure Image Processing Demo")
    st.write("Upload or URL ➔ sandboxed iframe + Worker ➔ grayscale/invert filter ➔ back as Data-URL")

    # Image input: upload or URL
    uploaded_file = st.file_uploader("Upload image:", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        data = uploaded_file.read()
        ext = uploaded_file.type.split("/")[-1]
        image_source = f"data:image/{ext};base64,{base64.b64encode(data).decode()}"
    else:
        image_source = st.text_input(
            "Image URL:",
            "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
        )

    mode = st.selectbox("Processing Mode", ["grayscale", "invert"])

    security_config = {
        "coop": "same-origin",
        "coep": "require-corp",
        "csp": {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'wasm-unsafe-eval'"],
            "worker-src": ["'self'", "blob:"],
            "img-src": ["'self'", "data:", "https:"],
        },
        "requireHTTPS": True,
        "sandbox": ["allow-scripts", "allow-same-origin"],
    }

    if st.button("Process Image", key="process_image"):
        res = streamlit_secure_context(
            model_path="",
            security_config=security_config,
            inference_params={"imageURL": image_source, "processing": mode},
            key="image-demo",
            height=600,
            width=600,
        )
        if res:
            if not uploaded_file:
                st.image(image_source, caption="Original", use_column_width=True)
            st.image(res, caption="Processed", use_column_width=True)
        else:
            st.error("Failed: see console.")

else:  # Iris Inference
    st.title("🔒 Secure Iris Inference Demo")
    st.write("Adjust sliders in the sidebar and click ‘Run Inference’.")

    # Model URL and HTTPS option in sidebar
    iris_url = "https://storage.googleapis.com/tfjs-models/tfjs/iris_v1/model.json"
    model_url = st.sidebar.text_input("Model URL", iris_url)
    https_req = st.sidebar.checkbox("Require HTTPS", False)
    st.sidebar.markdown("---")
    st.sidebar.header("Iris Features")

    # Feature sliders
    sl = st.sidebar.slider
    feats = [
        sl("Sepal length", 0.0, 10.0, 5.1, 0.1),
        sl("Sepal width", 0.0, 10.0, 3.5, 0.1),
        sl("Petal length", 0.0, 10.0, 1.4, 0.1),
        sl("Petal width", 0.0, 10.0, 0.2, 0.1),
    ]

    security_conf = {
        "coop": "same-origin",
        "coep": "require-corp",
        "csp": {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'wasm-unsafe-eval'"],
            "worker-src": ["'self'", "blob:"],
        },
        "sandbox": ["allow-scripts", "allow-same-origin"],
        "requireHTTPS": https_req,
    }
    params = {"input": [feats], "shape": [1, 4]}

    if st.button("Run Inference"):
        result = streamlit_secure_context(
            model_path=model_url,
            security_config=security_conf,
            inference_params=params,
            key="iris-inference",
            height=400,
        )
        st.write("Result:", result)
    else:
        st.info("Set features and click to run.")
