"""
Secure Image Classification Demo (Page)

Classify an image using a pretrained MobileNet model inside a sandboxed
iframe + Web Worker. Image data never leaves the browser.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context

st.title("Secure Image Classification Demo")

# HTML & JS for file input and image preview
html_code = '''
<input type="file" id="imginput" accept="image/*"/>
<br/><br/>
<img id="imgpreview" width="224" style="display:none;"/>
<p id="prediction">No image selected.</p>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet"></script>
<script>
document.getElementById('imginput').onchange = async function(evt) {
    const file = evt.target.files[0]; if (!file) return;
    const img = document.getElementById('imgpreview');
    img.src = URL.createObjectURL(file); img.style.display = 'block';
    img.onload = async () => {
        document.getElementById('prediction').innerText = 'Loading model...';
        const model = await mobilenet.load();
        const preds = await model.classify(img);
        document.getElementById('prediction').innerText =
            preds.length > 0
                ? `Prediction: ${preds[0].className} (prob=${preds[0].probability.toFixed(3)})`
                : 'No prediction.';
    };
};
</script>
'''

# Render inside the secure context component
streamlit_secure_context(html_code, height=600)