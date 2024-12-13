#!/bin/bash

# Set repository URL and directory name
REPO_URL="https://github.com/atelier-it-ro/metrics-collector"
REPO_DIR="metrics-collector"

# Clone the repository
if [ ! -d "$REPO_DIR" ]; then
    echo "Cloning repository from $REPO_URL..."
    git clone $REPO_URL
else
    echo "Repository already exists. Pulling latest changes..."
    cd $REPO_DIR
    git pull
    cd ..
fi

# Enter the repository directory
cd $REPO_DIR || { echo "Failed to enter directory $REPO_DIR"; exit 1; }

# Create a Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install required modules
if [ -f "requirements.txt" ]; then
    echo "Installing required modules..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping module installation."
fi

# Run the Python script in background mode
if [ -f "main.py" ]; then
    echo "Running main.py in background mode..."
    nohup python main.py > output.log 2>&1 &
    echo $! > pidfile
    echo "Process started with PID $(cat pidfile). Output redirected to output.log."
else
    echo "main.py not found. Aborting."
    exit 1
fi
