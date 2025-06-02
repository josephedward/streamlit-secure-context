#!/usr/bin/env python3
# scripts/capture_demo_screenshots.py
import subprocess
import time
import os
from playwright.sync_api import sync_playwright

DEMO_CMD = [
    "streamlit",
    "run",
    "examples/basic_demo.py",
    "--server.port=8501",
    "--server.headless=true",
]

def main():
    # 1) Launch the Streamlit demo as a background process
    proc = subprocess.Popen(DEMO_CMD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        # 2) Wait for the server to start
        time.sleep(5)

        # 3) Launch Playwright and navigate
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto("http://localhost:8501", wait_until="networkidle")

            # 4) Full-page screenshot
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path="screenshots/demo_full.png", full_page=True)

            # 5) Crop the sidebar
            sidebar = page.query_selector("aside[data-testid='stSidebar']")
            if sidebar:
                box = sidebar.bounding_box()
                page.screenshot(
                    path="screenshots/demo_sidebar.png",
                    clip={
                        "x": box["x"],
                        "y": box["y"],
                        "width": box["width"],
                        "height": box["height"],
                    },
                )

            browser.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()
