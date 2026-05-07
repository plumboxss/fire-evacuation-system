#!/usr/bin/env bash
# setup_env.sh — Create a virtual environment and install all dependencies.
# Usage: bash scripts/setup_env.sh

set -euo pipefail

PYTHON=${PYTHON:-python3}
VENV_DIR=".venv"

echo "=== Fire Evacuation System — Environment Setup ==="

# Check Python version >= 3.10
PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_MAJOR=3
REQUIRED_MINOR=10

MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$MAJOR" -lt "$REQUIRED_MAJOR" ] || { [ "$MAJOR" -eq "$REQUIRED_MAJOR" ] && [ "$MINOR" -lt "$REQUIRED_MINOR" ]; }; then
    echo "ERROR: Python $REQUIRED_MAJOR.$REQUIRED_MINOR+ required, found $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION  [OK]"

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at $VENV_DIR — skipping creation."
else
    echo "Creating virtual environment at $VENV_DIR ..."
    "$PYTHON" -m venv "$VENV_DIR"
fi

# Activate
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip ..."
pip install --upgrade pip --quiet

# Install requirements
echo "Installing requirements.txt ..."
pip install -r requirements.txt

# Install project in editable mode so 'from src.*' imports work
echo "Installing project in editable mode ..."
pip install -e . --quiet

echo ""
echo "=== Setup complete ==="
echo ""
echo "To activate the environment:"
echo "    source $VENV_DIR/bin/activate"
echo ""
echo "To verify the installation:"
echo "    python -m src.shared.constants"
echo "    python -m src.shared.normalization"
echo "    pytest tests/test_constants.py tests/test_normalization.py -v"
