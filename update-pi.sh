./#!/bin/bash

# Load environment variables
if [ -f .local.env ]; then
    source .local.env
else
    echo "Error: .local.env file not found"
    echo "Please create .local.env with PI_PASSWORD=\"your_password\""
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print with color
print_status() {
    echo -e "${GREEN}==>${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}==>${NC} $1"
}

# Check if there are any changes to commit
if [[ -n $(git status -s) ]]; then
    print_status "Changes detected, preparing to commit..."
    
    # Prompt for commit message
    read -p "Enter commit message: " commit_message
    
    # Commit changes
    print_status "Committing changes..."
    git add .
    git commit -m "$commit_message"
else
    print_warning "No changes detected, proceeding with push and deploy..."
fi

# Push to remote
print_status "Pushing to remote repository..."
git push

# SSH into Pi and update
print_status "Connecting to Raspberry Pi and updating..."
sshpass -p "$PI_PASSWORD" ssh -o StrictHostKeyChecking=no pi@192.168.0.97 "
cd /home/pi/nexans-printer && \
git pull && \
# Create virtual environment if it doesn't exist
if [ ! -d \"venv\" ]; then
    print_status 'Creating virtual environment...'
    python3 -m venv venv
fi && \
# Activate virtual environment and install dependencies
source venv/bin/activate && \
pip install brother_ql pillow tk
"

print_status "Update complete! 🚀"

print_warning "To run the app on the Pi:"
print_warning "1. Open a terminal on the Pi"
print_warning "2. cd /home/pi/nexans-printer"
print_warning "3. source venv/bin/activate"
print_warning "4. ./main.py"
