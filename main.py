#!/usr/bin/env python3
import tkinter as tk
from printer_app import PrinterApp

def main():
    # Configuration
    TEST_MODE = True  # Set to False when printer is connected
    PRINTER_MODEL = 'QL-800'  # Update this to match your printer model

    # Create the main window
    root = tk.Tk()
    
    # Initialize the printer app
    app = PrinterApp(root, test_mode=TEST_MODE)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
