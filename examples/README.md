<!-- examples/README.md -->
# Examples for streamlit-secure-context

This directory contains example apps demonstrating how to use the `streamlit-secure-context` Streamlit component.

## Prerequisites
- Node.js & npm
- Python 3.7+
- Streamlit 0.63+

## Setup
1. Build the frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```
   Alternatively, run the helper script from the project root to build, copy assets, and install:
   ```bash
   ./scripts/bootstrap.sh
   ```
2. Install the Python package (editable mode recommended):
   ```bash
   pip install -e .
   ```

## Running the Basic Demo
In one terminal, start the Streamlit app:
```bash
streamlit run examples/basic_demo.py
```
This will launch a web browser window showing a simple app that uses the secure context component to perform a dummy inference.

You can modify `basic_demo.py` to point at your own model URL or adjust inference parameters.