#!/usr/bin/env bash
set -e

# Create a Python virtual environment in .venv/
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment and upgrade pip
echo "Activating virtual environment and installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

echo "Setup complete. Activate the environment with: source .venv/bin/activate"