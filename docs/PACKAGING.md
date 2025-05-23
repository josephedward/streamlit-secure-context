# Packaging & Distribution Guide

This document outlines the steps to package, distribute, and publish the streamlit-secure-context component under the MIT license with Edward Joseph as the author.

## 1. Update setup.py
- Ensure the following fields are set:
  ```python
  setup(
      name="streamlit-secure-context",
      version="0.1.0",
      packages=find_packages(),
      include_package_data=True,
      install_requires=["streamlit>=0.63"],
      description="Secure ML Inference Streamlit Component",
      author="Edward Joseph",
      license="MIT",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',  # optional
      url="https://github.com/your-organization/streamlit-secure-context",  # optional
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.7',  # optional
  )
  ```

## 2. Add an MIT LICENSE file
Create a `LICENSE` file at the project root with the standard MIT license text:
```text
MIT License

Copyright (c) 2025 Edward Joseph

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

... (rest of MIT text) ...
```

## 3. Include non-code files in the source distribution
Add a `MANIFEST.in` at the root:
```text
include LICENSE
include README.md
recursive-include streamlit_secure_context/frontend/build *
```

## 4. Bundle frontend assets in the Python package
Ensure the built React assets are copied into the Python package before installation.
 Update `scripts/bootstrap.sh` to include:
```bash
# Ensure the real CLI is available (the npm package v2.0.0 omits it):
if ! command -v streamlit-component-lib &>/dev/null; then
  # Clone Streamlit monorepo and link the component-lib package
  TMPDIR=$(mktemp -d)
  git clone https://github.com/streamlit/streamlit.git "$TMPDIR"
  cd "$TMPDIR/packages/frontend/streamlit-component-lib"
  npm install && npm link
  cd "$HERE/frontend"
  npm link streamlit-component-lib
fi

# After npm run build in frontend/
rm -rf streamlit_secure_context/frontend/build
cp -r frontend/build streamlit_secure_context/frontend/
```

Note: The published `streamlit-component-lib` (2.0.0) on npm does not ship the build/start CLI. The updated bootstrap script now automatically pulls and links the upstream CLI before building.

## 5. Release script
Create `scripts/release.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <new-version>"
  exit 1
fi

version=$1

# 1) Bump version in setup.py
sed -i -E "s/version=\"[0-9]+\.[0-9]+\.[0-9]+\"/version=\"$version\"/" setup.py

# 2) Commit & tag
git add setup.py
git commit -m "chore: bump version to $version"
git tag "v$version"

# 3) Build and bundle
./scripts/bootstrap.sh
python setup.py sdist bdist_wheel

# 4) Upload to PyPI (requires ~/.pypirc configured)
twine upload dist/*

# 5) Push commits + tags
git push
git push --tags
```

## 6. PyPI credentials
Configure `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: <your-username>
password: <your-password-or-token>
```

## 7. .gitignore updates
Add to `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*.egg-info/

# Build artifacts
build/
dist/

# Frontend
node_modules/
frontend/build/

# Virtualenv
.venv/
```

## 8. Continuous Integration (optional)
- Add a GitHub Actions workflow (e.g., `.github/workflows/ci.yml`) to:
  - Run tests and linters on push
  - On tag push, run `scripts/release.sh` or use `pypa/gh-action-pypi-publish`

## 9. Optional: Publish frontend to npm
* Package your React component under an npm name (e.g., `streamlit-secure-context`).
- Update your Python wrapper for release mode:
  ```python
  _streamlit_secure_context = components.declare_component(
      "streamlit_secure_context",
      url=f"https://unpkg.com/streamlit-secure-context@{version}/",
  )
  ```

## 10. Testing the end-to-end install
```bash
# Build & install locally
./scripts/bootstrap.sh

### In a fresh environment
```bash
pip uninstall streamlit-secure-context || true
pip install .
streamlit run examples/app.py
```
pip install .
streamlit run examples/app.py
```