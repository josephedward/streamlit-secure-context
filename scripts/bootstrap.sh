#!/usr/bin/env bash
set -euo pipefail

# Script to build the frontend and install the Python component locally
HERE="$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)"

echo "[bootstrap] Building frontend..."
cd "$HERE/frontend"
npm install
 npm run build

echo "[bootstrap] Copying frontend build assets into Python package..."
rm -rf "$HERE/streamlit_component/frontend"
mkdir -p "$HERE/streamlit_component/frontend"
cp -r "$HERE/frontend/build" "$HERE/streamlit_component/frontend"

echo "[bootstrap] Installing Python package..."
cd "$HERE"
pip install .

echo "[bootstrap] Done."