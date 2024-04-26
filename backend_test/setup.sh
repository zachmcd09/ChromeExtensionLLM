#!/bin/bash
set -e

command -v python3 &>/dev/null || { echo "Python is not installed"; exit 1; }
command -v node &>/dev/null || { echo "Node.js is not installed"; exit 1; }

command -v poetry &>/dev/null || { echo "Installing Poetry..."; pip install poetry; }
echo "Installing Python dependencies with Poetry..."
poetry install

command -v npm &>/dev/null || { echo "npm is not installed"; exit 1; }
echo "Installing JavaScript dependencies with npm..."
npm install

# Additional configuration checks or setups from manifest.json
# echo "Configuring application..."

echo "Setup completed successfully!"
