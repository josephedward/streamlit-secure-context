#!/usr/bin/env python3
"""
capture_demo_screenshots.py

Automates screenshot capture of Streamlit demos using Playwright.

Usage:
  pip install playwright
  playwright install chromium
  python3 scripts/capture_demo_screenshots.py <demo_script.py> [--port PORT] [--output OUTPUT_PATH]
"""
import subprocess
import time
import os
import argparse
from playwright.sync_api import sync_playwright

import shutil

def capture(demo_script: str,
            port: int,
            screenshot_path: str,
            mode: str = None,
            video_path: str = None):
    """
    Launches the given Streamlit demo on the specified port,
    captures a full-page screenshot (to screenshot_path),
    optionally records a video (to video_path), then terminates the demo process.
    """
    # Determine temp video directory if video recording is desired
    temp_video_dir = None
    if video_path:
        video_dir = os.path.dirname(video_path) or os.getcwd()
        temp_video_dir = os.path.join(video_dir, ".tmp_playwright_videos")
        os.makedirs(temp_video_dir, exist_ok=True)
    # Start the Streamlit demo
    cmd = ["streamlit", "run", demo_script, f"--server.port={port}", "--server.headless=true"]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        # Wait for the server to start
        time.sleep(5)
        # Capture via Playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            # Create context with video recording if requested
            if temp_video_dir:
                context = browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    record_video_dir=temp_video_dir
                )
                page = context.new_page()
            else:
                page = browser.new_page(viewport={"width": 1280, "height": 800})
            # Navigate and select mode if provided
            page.goto(f"http://localhost:{port}", wait_until="networkidle")
            if mode:
                try:
                    page.click(f"text={mode.capitalize()}")
                    page.wait_for_selector(f"text={mode.capitalize()} Mode", timeout=5000)
                except Exception:
                    pass
            # Take screenshot
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
            # Close context to finalize video, if any
            if temp_video_dir:
                context.close()
                # Move the generated video file
                for fname in os.listdir(temp_video_dir):
                    if fname.endswith('.webm'):
                        src = os.path.join(temp_video_dir, fname)
                        os.makedirs(os.path.dirname(video_path), exist_ok=True)
                        shutil.move(src, video_path)
                # Clean up temp video directory
                shutil.rmtree(temp_video_dir, ignore_errors=True)
            browser.close()
    finally:
        proc.terminate()

def main():
    parser = argparse.ArgumentParser(description="Capture Streamlit demo screenshots.")
    parser.add_argument("demo_script", help="Path to the Streamlit Python script to run.")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the demo on.")
    parser.add_argument("--output", default="screenshots/demo.png", help="Output screenshot path.")
    parser.add_argument("--mode", choices=["interactive", "simple"],
                        help="Demo mode to select before screenshot (e.g., simple or interactive)")
    parser.add_argument("--video-output", default=None,
                        help="Path to save a recording of the demo (WebM format)")
    args = parser.parse_args()
    capture(
        args.demo_script,
        args.port,
        args.output,
        args.mode,
        args.video_output,
    )

if __name__ == "__main__":
    main()
