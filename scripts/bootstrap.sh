#!/usr/bin/env bash
set -euo pipefail

# Script to build the frontend and install the Python component locally
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[bootstrap] Building frontend..."
cd "$HERE/frontend"
# Ensure the upstream streamlit-component-lib CLI is available for build/start
if ! command -v streamlit-component-lib &>/dev/null; then
  echo "[bootstrap] streamlit-component-lib CLI not found; installing via tarball from upstream monorepo..."
  TMPDIR=$(mktemp -d)
  git clone https://github.com/streamlit/streamlit.git "$TMPDIR"
  cd "$TMPDIR/frontend/streamlit-component-lib"
  npm install
  npm pack
  mv streamlit-component-lib-*.tgz "$HERE/frontend/"
  cd "$HERE/frontend"
  npm install ./streamlit-component-lib-*.tgz
fi
npm install
npm run build
cd "$HERE"
echo "[bootstrap] Copying frontend build assets into Python package..."
rm -rf "$HERE/streamlit_secure_context/frontend"
mkdir -p "$HERE/streamlit_secure_context/frontend"
cp -r "$HERE/frontend/build" "$HERE/streamlit_secure_context/frontend"

echo "[bootstrap] Installing Python package..."
cd "$HERE"
pip install .

echo "[bootstrap] Done."
