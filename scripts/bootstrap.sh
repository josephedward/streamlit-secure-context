#!/usr/bin/env bash
set -euo pipefail

# Script to build the frontend and install the Python component locally
HERE="$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)"

if [ ! -d "$HERE/frontend/build" ]; then
  echo "[bootstrap] Warning: frontend/build not found; skipping asset copy"
else
  echo "[bootstrap] Copying frontend build assets into Python package..."
  rm -rf "$HERE/streamlit_secure_context/frontend"
  mkdir -p "$HERE/streamlit_secure_context/frontend"
  cp -r "$HERE/frontend/build" "$HERE/streamlit_secure_context/frontend"
fi

echo "[bootstrap] Installing Python package..."
cd "$HERE"
pip install .

echo "[bootstrap] Done."
