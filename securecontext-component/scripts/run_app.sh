#!/usr/bin/env bash
set -e

# Activate virtual environment if it exists
if [ -f .venv/bin/activate ]; then
  echo "Activating virtual environment..."
  source .venv/bin/activate
fi

# Launch Streamlit app
echo "Launching Streamlit app..."
streamlit run app.py