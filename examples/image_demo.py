"""
Image Classification Demo using the streamlit-secure-context component.

This demo lets users select a local image file and classifies it with a MobileNet model
running entirely in the browser (inside a sandboxed iframe/Web Worker). No image data or model
execution ever leaves the user's browser.
"""
import streamlit as st
from streamlit_secure_context import streamlit_secure_context as secure_context

st.title("🔒 Secure Inference Demo")
st.write(
    "This demo classifies an image using a MobileNet model running entirely in the browser."
)

# HTML+JS snippet embedded inside a secure iframe
html_code = """
<input type="file" id="imginput" accept="image/*"/>
<br/><br/>
<img id="imgpreview" width="224" style="display:none;" />
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
"""

# Embed the HTML snippet in a secure iframe (height can be adjusted)
secure_context(
    html_code,
    height=600,
)"""
Example Streamlit app demonstrating secure in-browser image classification with MobileNet.
"""
import streamlit as st
from streamlit_secure_context import secure_context

st.title("🔒 Secure Image Classification Demo")
st.write("Classify an image using a MobileNet model running entirely in the browser.")

# HTML and JS snippet for file input and inference
html_code = """
<input type="file" id="imginput" accept="image/*"/>
<br/><br/>
<img id="imgpreview" width="224" style="display:none;"/>
<p id="prediction">No image selected.</p>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet"></script>
<script>
// Load image into <img> element and classify
document.getElementById('imginput').onchange = async function(evt) {
    const file = evt.target.files[0];
    if (!file) return;
    const img = document.getElementById('imgpreview');
    img.src = URL.createObjectURL(file);
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
"""

# Render the snippet inside the secure context component
secure_context(html_code, height=500)
