#!/usr/bin/env bash
set -e

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Create wheel
"${PYTHON_CMD:-python3}" -m pip install --upgrade pip build
"${PYTHON_CMD:-python3}" -m build

echo "Build completed successfully!"

# Optional: Install locally for testing
# "${PYTHON_CMD:-python3}" -m pip install dist/*.whl 