#!/bin/bash

# Quick Start Script for Consciousness Simulator
# Sets up environment and runs the chatbot

echo "🧠 Consciousness Simulator - Quick Start"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python installation..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Downloading spaCy language model (medium model for better accuracy)..."
python -m spacy download en_core_web_md

# Run setup check
echo ""
echo "Running setup verification..."
python -c "
import torch
import transformers
import spacy
import numpy
print('✓ All core dependencies installed successfully')
"

if [ $? -ne 0 ]; then
    echo "❌ Dependency installation failed. Please check error messages above."
    exit 1
fi

# Offer to run demo or chatbot
echo ""
echo "========================================"
echo "Setup complete! Choose an option:"
echo "========================================"
echo "1) Run demo (showcases all features)"
echo "2) Run interactive chatbot"
echo "3) Exit"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting demo..."
        python demo.py
        ;;
    2)
        echo ""
        echo "Starting consciousness chatbot..."
        python consciousness_chatbot.py
        ;;
    3)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
