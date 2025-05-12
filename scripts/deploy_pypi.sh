#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <new-version>"
  exit 1
fi
version=$1

# 1) Prepare frontend build (must exist under frontend/build); skip if missing
echo "[1/4] Preparing frontend build..."
echo "[1/4] Packing & installing upstream CLI..."
rm -rf /tmp/streamlit
git clone https://github.com/streamlit/streamlit.git /tmp/streamlit
cd /tmp/streamlit/packages/frontend/streamlit-component-lib
npm install
npm pack
mv streamlit-component-lib-*.tgz "$OLDPWD"/frontend/
cd "$OLDPWD"
(cd frontend && npm install && npm install ./streamlit-component-lib-*.tgz)
if [ -d "frontend/build" ]; then
  rm -rf streamlit_secure_context/frontend
  mkdir -p streamlit_secure_context/frontend
  cp -r frontend/build streamlit_secure_context/frontend
else
  echo "[1/4] Warning: frontend/build not found; skipping static asset bundling"
fi

# 2) Bump version in setup.py
echo "[2/4] Bumping Python package version to $version..."
sed -i '' -E "s/version=\"[0-9]+\.[0-9]+\.[0-9]+\"/version=\"$version\"/" setup.py

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
