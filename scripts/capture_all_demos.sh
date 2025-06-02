#!/usr/bin/env bash
set -euo pipefail

# capture_all_demos.sh - Capture screenshots and videos of all multipage demos

mkdir -p screenshots videos

PORT=8501

echo "Capturing Home page (app.py)..."
python3 scripts/capture_demo_screenshots.py \
  examples/app.py --port $PORT \
  --output screenshots/home.png \
  --video-output videos/home.webm

echo "Capturing Image Classification page..."
python3 scripts/capture_demo_screenshots.py \
  examples/pages/image_classification.py --port $((PORT+1)) \
  --output screenshots/image_classification.png \
  --video-output videos/image_classification.webm

echo "Capturing Iris Interactive page..."
python3 scripts/capture_demo_screenshots.py \
  examples/pages/1_interactive_iris_inference.py --port $((PORT+2)) \
  --output screenshots/iris_interactive.png \
  --video-output videos/iris_interactive.webm

echo "Capturing Iris Simple page..."
python3 scripts/capture_demo_screenshots.py \
  examples/pages/2_simple_iris_inference.py --port $((PORT+3)) \
  --output screenshots/iris_simple.png \
  --video-output videos/iris_simple.webm

echo "Screenshots saved in screenshots/ and videos saved in videos/"