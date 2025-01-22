#!/usr/bin/env python3
import tkinter as tk
import argparse
from printer_app import PrinterApp

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Nexans Receipt Printer')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no printer required)')
    args = parser.parse_args()

    # Create the main window
    root = tk.Tk()
    
    # Initialize the printer app
    app = PrinterApp(root, test_mode=args.test)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
