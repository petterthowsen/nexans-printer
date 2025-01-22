# Nexans Receipt Printer

A simple GUI application for printing receipts using a Brother QL-800 label printer. Built with Python and Tkinter, designed for use on a Raspberry Pi with a touch screen.

## Features

- Clean, touch-friendly interface
- Large, easy-to-press print button
- Visual feedback during printing
- Test mode for development without printer
- Custom styling with Nohemi font

## Requirements

- Python 3.x
- Brother QL-800 printer (or compatible model)
- Linux system
- Python tkinter library (`python3-tk` package)

## Project Structure

```
nexans-printer/
├── assets/
│   └── Nohemi/            # Custom font files
├── venv/                  # Python virtual environment
├── main.py               # Application entry point
├── printer_app.py        # Main application logic
└── README.md            # This file
```

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd nexans-printer
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install brother_ql pillow tk
   ```

4. If tkinter is not installed on your system:
   ```bash
   sudo apt-get install python3-tk
   ```

## Running the Application

### Running the Application

The application can be run in two modes:

#### Test Mode (No Printer Required)
```bash
./main.py --test
```
When running in test mode:
- No printer connection is required
- Clicking print will save a preview image as temp_receipt.png
- A "Printing..." message will be shown
- The button returns to ready state after 5 seconds

#### Production Mode (With Printer)
1. Connect your Brother QL-800 printer via USB
2. Ensure the printer is recognized at `/dev/usb/lp0`
3. Set proper permissions:
   ```bash
   sudo chmod 666 /dev/usb/lp0
   ```
4. Run the application:
   ```bash
   ./main.py
   ```

## Configuration

The main configuration options are in `main.py`:
- `TEST_MODE`: Toggle between test mode and real printing
- `PRINTER_MODEL`: Set your Brother QL printer model

## Development

The application is split into two main files:
- `main.py`: Entry point and configuration
- `printer_app.py`: Core application logic and UI

To modify the receipt layout, edit the `create_receipt_image` method in `printer_app.py`.

## Troubleshooting

1. **Printer Not Found**: Ensure the printer is connected and `/dev/usb/lp0` exists
2. **Permission Denied**: Run `sudo chmod 666 /dev/usb/lp0`
3. **Font Issues**: Ensure the Nohemi font files are in the correct location under `assets/`
4. **Tkinter Missing**: Install with `sudo apt-get install python3-tk`

## Deployment

The application is designed to run on a Raspberry Pi. A deployment script `update-pi.sh` is provided to easily update the Pi with your latest changes:

1. Make your changes locally
2. Run the deployment script:
   ```bash
   ./update-pi.sh
   ```
   The script will:
   - Prompt for a commit message if there are changes
   - Commit and push your changes to the repository
   - SSH into the Pi and pull the latest changes

### Prerequisites for Deployment
- SSH access to the Raspberry Pi (configured at `pi@192.168.0.97`)
- Git repository cloned at `/home/pi/nexans-printer` on the Pi
- SSH key authentication set up (recommended)
- X server running on the Pi (for GUI display)

### Raspberry Pi Display Setup
1. Ensure your Raspberry Pi is properly configured for display output:
   ```bash
   sudo raspi-config
   ```
   Navigate to: Interface Options -> VNC/Desktop GUI and enable it

2. The display environment variable should be set automatically by the deployment script. If you still encounter display issues, manually set it:
   ```bash
   echo 'export DISPLAY=:0' >> ~/.bashrc
   source ~/.bashrc
   ```

3. If running the app manually on the Pi, ensure you're in a desktop session (not just SSH)

### Common Pi Setup Issues
- **No display name error**: This usually means the X server isn't running or `DISPLAY` isn't set
  - Solution: Follow the display setup steps above
  - Make sure you're running the app from the Pi's desktop environment
- **Cannot open display**: Check if X server is running and display variable is set correctly
  - Run `echo $DISPLAY` to verify it's set to `:0`
  - Ensure you're not trying to run the GUI over SSH without X forwarding

## License

This project uses the Nohemi font family. Please see `assets/Nohemi/License/` for font licensing details.
