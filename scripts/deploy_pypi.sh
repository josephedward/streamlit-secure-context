#!/usr/bin/env bash
# Ensure PYPI_TOKEN is set for authentication
if [ -z "${PYPI_TOKEN:-}" ]; then
  echo "Error: PYPI_TOKEN environment variable not set" >&2
  exit 1
fi

set -euo pipefail

# Clone upstream CLI for build scripts if missing
TMP_CLI=/tmp/streamlit
if [ ! -d "$TMP_CLI" ]; then
  echo "Cloning upstream Streamlit CLI into $TMP_CLI..."
  git clone https://github.com/streamlit/streamlit.git "$TMP_CLI"
else
  echo "Upstream Streamlit CLI already present; skipping clone"
fi

if [ $# -ne 1 ]; then
  echo "Usage: $0 <new-version>"
  exit 1
fi
version=$1

# Bundle frontend build assets (if available)
echo "Bundling frontend assets..."
if [ -d "frontend/build" ]; then
  rm -rf streamlit_secure_context/frontend
  mkdir -p streamlit_secure_context/frontend
  cp -r frontend/build streamlit_secure_context/frontend
else
  echo "Warning: frontend/build not found; skipping asset bundling"
fi

echo "[2/4] Bumping Python package version to $version..."
# Bump version in setup.py
echo "Updating package version to $version..."
sed -i '' -E "s/version=\"[0-9]+\.[0-9]+\.[0-9]+\"/version=\"$version\"/" setup.py

# Clean out any old distributions so we only upload the new build
echo "[*] Cleaning old distributions..."
rm -rf dist

echo "[3/4] Building sdist & wheel..."
# Build source and wheel distributions
echo "Building source and wheel packages..."
python3 -m pip install --upgrade --user build wheel twine >/dev/null
python3 -m build --sdist --wheel

echo "[4/4] Uploading to PyPI..."
twine upload dist/* -u __token__ -p "$PYPI_TOKEN"
echo "Uploading packages to PyPI..."
twine upload dist/* -u __token__ -p "$PYPI_TOKEN"

echo "✅ streamlit-secure-context@$version published!"
