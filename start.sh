#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment and run app
source venv/bin/activate
python3 main.py
