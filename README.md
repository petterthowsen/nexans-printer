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

### Test Mode (No Printer Required)
```bash
./main.py
```
The application will run in test mode by default. When the print button is pressed, it will:
- Save a preview image as temp_receipt.png
- Show a "Printing..." message
- Return to ready state after 5 seconds

### Production Mode (With Printer)
1. Connect your Brother QL-800 printer via USB
2. Ensure the printer is recognized at `/dev/usb/lp0`
3. Set proper permissions:
   ```bash
   sudo chmod 666 /dev/usb/lp0
   ```
4. Edit `main.py` and set `TEST_MODE = False`
5. Run the application:
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

## License

This project uses the Nohemi font family. Please see `assets/Nohemi/License/` for font licensing details.
