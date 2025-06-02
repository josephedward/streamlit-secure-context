#!/usr/bin/env bash
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

echo "Bumping version to $version..."
sed -i '' -E "s/version=\"[0-9]+\.[0-9]+\.[0-9]+\"/version=\"$version\"/" setup.py

# Clean out any old distributions so we only upload the new build
echo "Cleaning old distributions..."
rm -rf dist

echo "Building distributions..."
# Build source and wheel distributions
python3 -m pip install --upgrade --user build wheel twine >/dev/null
python3 -m build --sdist --wheel

echo "Uploading to PyPI..."
twine upload dist/* -u __token__ -p "$PYPI_TOKEN"

echo "✅ streamlit-secure-context@$version published!"
