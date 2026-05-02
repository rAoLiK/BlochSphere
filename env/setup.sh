#!/bin/bash
# Bloch Sphere - One-click environment setup (Linux / WSL)
set -e

echo "=== Bloch Sphere Environment Setup ==="

# Check for conda
if ! command -v conda &> /dev/null; then
    echo "ERROR: conda not found. Please install Miniforge or Anaconda first."
    exit 1
fi

ENV_NAME="bloch"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "Environment '${ENV_NAME}' already exists."
    read -p "Remove and recreate? [y/N]: " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        conda env remove -n "${ENV_NAME}" -y
    else
        echo "Activating existing environment..."
        conda activate "${ENV_NAME}"
        echo "Done. Run: streamlit run app.py"
        exit 0
    fi
fi

echo "Creating conda environment '${ENV_NAME}'..."
conda env create -f "${SCRIPT_DIR}/environment.yml"

echo ""
echo "=== Setup Complete ==="
echo "Activate:  conda activate ${ENV_NAME}"
echo "Run:       streamlit run app.py"
