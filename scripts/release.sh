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

# 3) Build distributions
./scripts/bootstrap.sh
python setup.py sdist bdist_wheel

# 4) Upload to PyPI (requires ~/.pypirc configured)
twine upload dist/*

# 5) Push commits + tags
git push
git push --tags