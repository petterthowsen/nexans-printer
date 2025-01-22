# Nexans Printer

Label printer application for Brother QL-800.

## Requirements

- Python 3.10 or higher
- Brother QL-800 printer connected via USB
- sshpass (for deployment)

## Development Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

```bash
# Test mode (no actual printing)
./main.py --test

# Production mode
./main.py
```

## Features

- Print labels with start and finish times
- Optional batch number
- Configurable number of copies
- Adjustable drying time
- Touch-friendly interface
- Settings persistence
- ESC to quit

## Deployment

1. Install sshpass:
```bash
sudo apt-get install sshpass
```

2. Create `.local.env` with Pi password:
```bash
PI_PASSWORD="your_password"
```

3. Run update script:
```bash
./update-pi.sh
```

4. Copy desktop icon to Pi:
```bash
scp "Nexans Printer.desktop" pi@192.168.0.97:~/Desktop/
ssh pi@192.168.0.97 "chmod +x ~/Desktop/\"Nexans Printer.desktop\""
