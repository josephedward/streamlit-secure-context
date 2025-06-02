"""Multipage Secure Context Demos"""
import streamlit as st
from pages.image_demo import main as run_image_demo
from pages.iris_demo import main as run_iris_demo

# App layout
st.set_page_config(page_title="Secure Context Demos", layout="wide")
st.title("🔒 Streamlit Secure Context Demos")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Demo:",
    ["Image Processing", "Iris Inference"]
)
st.sidebar.markdown("---")

if page == "Image Processing":
    run_image_demo()
else:
    run_iris_demo()