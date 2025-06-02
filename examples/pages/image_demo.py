"""
Secure Image Processing Demo using the streamlit-secure-context component.

This demo loads an image by URL or file upload into a sandboxed iframe/Web Worker, applies a client-side
transformation (grayscale or invert), and returns the processed image as a Data URL without sending raw
bytes to the server.
"""
import streamlit as st
import base64
from streamlit_secure_context import streamlit_secure_context

def main():
    """
    Secure Image Processing Demo entrypoint.
    """
    st.title("🔒 Secure Image Processing Demo")
st.write(
    "Upload a PNG/JPG or enter its HTTPS URL, then apply a grayscale or invert filter "
    "inside a secure context in the browser."
)

# Image input: upload or URL
uploaded_file = st.file_uploader("Upload image:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    data = uploaded_file.read()
    ext = uploaded_file.type.split("/")[-1]
    img_src = f"data:image/{ext};base64,{base64.b64encode(data).decode()}"
else:
    img_src = st.text_input(
        "Image URL:",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    )

mode = st.selectbox("Processing Mode:", ["grayscale", "invert"])

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

    if st.button("Process Image"):
        with st.spinner("Processing image inside secure sandbox..."):
            result = streamlit_secure_context(
                model_path="",
                security_config=security_config,
                inference_params={"imageURL": img_src, "processing": mode},
                key="image-demo",
                height=600, width=600,
            )
        if result:
            if not uploaded_file:
                st.image(img_src, caption="Original Image", use_column_width=True)
            st.image(result, caption="Processed Image", use_column_width=True)
        else:
            st.error("Processing failed. Check browser console.")
    else:
        st.info("Upload or enter URL, select mode, then click 'Process Image'.")

if __name__ == '__main__':
    main()