#!/bin/bash

echo "Starting Fedora environment setup for AI Command Center..."

# 1. Update package list and install required system dependencies
echo "Installing Python 3 and pip (if not present)..."
sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++

# 2. Create the virtual environment
echo "Creating venv_linux..."
python3 -m venv venv_linux

# 3. Activate the virtual environment
echo "Activating virtual environment..."
source venv_linux/bin/activate

# 4. Install project dependencies
echo "Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create necessary directories
echo "Ensuring required directories exist..."
mkdir -p src/data

echo "================================================="
echo "Setup Complete!"
echo "To activate the environment and run the dashboard, use:"
echo "source venv_linux/bin/activate"
echo "streamlit run src/api/dashboard.py"
echo "================================================="
