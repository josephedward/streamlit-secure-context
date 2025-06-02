"""
Secure Image Processing Demo using the streamlit-secure-context component.

This demo loads an image by URL or file upload into a sandboxed iframe/Web Worker, applies a client-side
transformation (grayscale or invert), and returns the processed image as a Data URL without sending raw
bytes to the server.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context
import base64

st.title("🔒 Secure Image Processing Demo")
st.markdown(
    """
    Load an image (upload or URL), process it inside the secure sandbox, and display the result.
    """
)

# Image input: upload or URL
uploaded_file = st.file_uploader("Upload image file:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    b = uploaded_file.read()
    ext = uploaded_file.type.split("/")[-1]
    image_source = f"data:image/{ext};base64,{base64.b64encode(b).decode()}"
else:
    image_source = st.text_input(
        "Image URL:",
        value=(
            "https://upload.wikimedia.org/wikipedia/commons/4/47/"
            "PNG_transparency_demonstration_1.png"
        ),
        help="HTTPS URL to an image file.",
    )

mode = st.selectbox(
    "Processing Mode:",
    options=["grayscale", "invert"],
    help="Filter to apply inside the sandbox.",
)

# Security configuration
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

st.write("## Configuration")
st.write(f"- Source: {'[uploaded file]' if uploaded_file else image_source}")
st.write(f"- Mode: {mode}")

if st.button("Process Image"):
    with st.spinner("Processing image inside secure sandbox..."):
        try:
            result_data_url = streamlit_secure_context(
                model_path="",
                security_config=security_config,
                inference_params={"imageURL": image_source, "processing": mode},
                key="image-demo",
                height=600,
                width=600,
            )
        except Exception as e:
            st.error(f"Component error: {e}")
            st.stop()
    if result_data_url:
        st.success("Processing complete!")
        if not uploaded_file:
            st.image(image_source, caption="Original Image", use_column_width=True)
        st.image(result_data_url, caption="Processed Image", use_column_width=True)
    else:
        st.error("No result returned. Check browser console for errors.")
else:
    st.info("Upload an image or enter a URL, select mode, then click 'Process Image'.")