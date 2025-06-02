#!/usr/bin/env bash
set -euo pipefail

# Ensure screenshots directory exists
mkdir -p screenshots

# Helper function: start a Streamlit demo, capture a screenshot, then kill it
capture_demo() {
  demo_script="$1"
  out_path="$2"

  echo "Starting demo $demo_script on port 8501..."
  # Launch the demo
  streamlit run "$demo_script" --server.port=8501 &
  pid=$!
  # Wait for the app to fully start
  sleep 5
  echo "Capturing screenshot to $out_path"
  node scripts/capture_demo.js http://localhost:8501 "$out_path"
  echo "Stopping demo (PID $pid)"
  kill "$pid"
  # Give time for port to free up
  sleep 2
}

echo "Capturing all demos..."

# 1) Simple demo
capture_demo examples/simple_demo.py screenshots/simple_demo.png

# 2) Interactive Iris demo
capture_demo examples/basic_demo.py screenshots/basic_demo.png

# 3) Image processing demo
capture_demo examples/image_demo.py screenshots/image_demo.png#!/usr/bin/env bash
set -euo pipefail

# Ensure Puppeteer is installed at the repo root:
#   npm install puppeteer

# Make sure you’ve built the frontend and installed the component:
#   ./scripts/bootstrap.sh

# Directory for output
mkdir -p screenshots

capture_demo() {
  demo_script="$1"
  out_path="$2"

  echo "Starting $demo_script on :8501…"
  streamlit run "$demo_script" --server.port=8501 &
  pid=$!
  sleep 5
  echo "Capturing → $out_path"
  node scripts/capture_demo.js http://localhost:8501 "$out_path"
  echo "Stopping PID $pid"
  kill "$pid"
  sleep 2
}

echo "📸 Capturing all three demos…"

capture_demo examples/simple_demo.py    screenshots/simple_demo.png
capture_demo examples/basic_demo.py     screenshots/basic_demo.png
capture_demo examples/image_demo.py     screenshots/image_demo.png

echo "✅ Done. Screenshots in screenshots/"
