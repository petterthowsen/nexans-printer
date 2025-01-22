#!/usr/bin/env python3
import argparse
from src.app import App

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Label Printer')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()
    
    # Create and run app
    app = App(test_mode=args.test)
    app.mainloop()

if __name__ == '__main__':
    main()
