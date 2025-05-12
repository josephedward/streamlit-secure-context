#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <new-version>"
  exit 1
fi
version=$1

# 1) Build frontend & copy into Python package
echo "[1/4] Building frontend..."
npm --prefix frontend install
npm --prefix frontend run build
rm -rf streamlit_secure_context/frontend
mkdir -p streamlit_secure_context/frontend
cp -r frontend/build streamlit_secure_context/frontend

# 2) Bump version in setup.py
echo "[2/4] Bumping Python package version to $version..."
sed -i -E "s/version=\"[0-9]+\.[0-9]+\.[0-9]+\"/version=\"$version\"/" setup.py

# 3) Build distributions
echo "[3/4] Building sdist & wheel..."
python3 -m pip install --upgrade build wheel twine >/dev/null
python3 -m build --sdist --wheel

# 4) Upload to PyPI
echo "[4/4] Uploading to PyPI..."
if [ -z "${PYPI_TOKEN:-}" ]; then
  echo "Error: set PYPI_TOKEN to your PyPI API token"
  exit 1
fi
twine upload dist/* -u __token__ -p "$PYPI_TOKEN"

echo "✅ streamlit-secure-context@$version published!"
