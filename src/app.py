import tkinter as tk
from src.screens.printer_screen import PrinterScreen
from src.screens.settings_screen import SettingsScreen
from src.config_manager import ConfigManager

class App(tk.Tk):
    def __init__(self, test_mode=True):
        super().__init__()
        
        self.test_mode = test_mode
        self.config_manager = ConfigManager()
        
        # Configure window
        self.title("Label Printer")
        
        # Set explicit geometry for Raspberry Pi's 800x480 screen
        self.geometry("800x480+0+0")
        self.minsize(800, 480)
        self.maxsize(800, 480)
        
        # Force fullscreen
        self.attributes('-fullscreen', True)
        self.wm_attributes('-topmost', True)
        
        self.configure(bg='white')
        
        # Initialize screens dictionary
        self.screens = {}
        
        # Create screens
        self.create_screens()
        
        # Bind ESC key to quit
        self.bind('<Escape>', lambda e: self.quit())
        
        # Show initial screen
        self.show_printer_screen()
        
    def create_screens(self):
        # Create printer screen
        self.screens['printer'] = PrinterScreen(
            self,
            self.config_manager,
            self.show_settings_screen
        )
        
        # Create settings screen
        self.screens['settings'] = SettingsScreen(
            self,
            self.config_manager,
            self.show_printer_screen
        )
    
    def show_screen(self, screen_name):
        # Hide all screens
        for screen in self.screens.values():
            screen.pack_forget()
        
        # Show requested screen
        self.screens[screen_name].pack(expand=True, fill='both')
    
    def show_printer_screen(self):
        self.show_screen('printer')
    
    def show_settings_screen(self):
        self.show_screen('settings')
