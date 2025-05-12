#!/usr/bin/env bash
set -euo pipefail

# Script to build the frontend and install the Python component locally
HERE="$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)"

if [ ! -d "$HERE/frontend/build" ]; then
  echo "ERROR: frontend/build not found. Please add a prebuilt frontend/build directory to your repo and commit it."
  exit 1
fi

echo "[bootstrap] Copying frontend build assets into Python package..."
    rm -rf "$HERE/streamlit_secure_context/frontend"
    mkdir -p "$HERE/streamlit_secure_context/frontend"
    cp -r "$HERE/frontend/build" "$HERE/streamlit_secure_context/frontend"

echo "[bootstrap] Installing Python package..."
cd "$HERE"
pip install .

echo "[bootstrap] Done."
