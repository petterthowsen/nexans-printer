#!/bin/bash

# Exit on any error
set -e

echo "Installing Nexans Label Printer Application..."

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-venv git

# Clone repository
echo "Cloning repository..."
cd ~
rm -rf nexans-printer
git clone https://github.com/petter/nexans-printer.git
cd nexans-printer

# Setup Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make start script executable
echo "Setting up start script..."
chmod +x start.sh

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/Nexans\ Printer.desktop << EOL
[Desktop Entry]
Version=1.0
Name=Nexans Printer
Comment=Label printer application
Exec=~/nexans-printer/start.sh
Path=~/nexans-printer
Icon=~/nexans-printer/assets/Nexans_logo.svg.png
Terminal=false
Type=Application
Categories=Utility;
EOL

# Make desktop shortcut executable
chmod +x ~/Desktop/Nexans\ Printer.desktop

# Setup autostart
echo "Setting up autostart..."
mkdir -p ~/.config/autostart
cp ~/Desktop/Nexans\ Printer.desktop ~/.config/autostart/

echo "Installation complete!"
echo "Please reboot the system for all changes to take effect."
echo "The application will start automatically after reboot."
