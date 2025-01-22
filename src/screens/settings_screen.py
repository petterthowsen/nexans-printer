import tkinter as tk
from tkinter import ttk, messagebox

class SettingsScreen(tk.Frame):
    def __init__(self, parent, config_manager, on_back):
        super().__init__(parent, bg='white')
        self.config_manager = config_manager
        self.on_back = on_back
        
        # Style configuration
        self.style = {
            'bg': 'white',
            'button_color': '#ff1910',
            'button_active': '#cc140c',
            'font': 'Nohemi-Bold'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(
            self,
            text="Settings",
            font=(self.style['font'], 36),
            bg=self.style['bg'],
            fg=self.style['button_color']
        )
        title.pack(pady=20)
        
        # Settings container
        settings_frame = tk.Frame(self, bg=self.style['bg'])
        settings_frame.pack(expand=True, fill='both', padx=50)
        
        # Number of copies setting
        copies_label = tk.Label(
            settings_frame,
            text="Number of copies:",
            font=(self.style['font'], 24),
            bg=self.style['bg']
        )
        copies_label.pack(anchor='w', pady=(20, 5))
        
        # Number of copies controls
        copies_controls = tk.Frame(settings_frame, bg=self.style['bg'])
        copies_controls.pack(anchor='w', pady=(0, 20))
        
        minus_btn = tk.Button(
            copies_controls,
            text="-",
            command=lambda: self.adjust_copies(-1),
            font=(self.style['font'], 24),
            width=2,
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat'
        )
        minus_btn.pack(side='left', padx=5)
        
        self.copies_var = tk.StringVar(value=str(self.config_manager.get_num_copies()))
        copies_label = tk.Label(
            copies_controls,
            textvariable=self.copies_var,
            font=(self.style['font'], 24),
            width=3,
            bg='white'
        )
        copies_label.pack(side='left', padx=10)
        
        plus_btn = tk.Button(
            copies_controls,
            text="+",
            command=lambda: self.adjust_copies(1),
            font=(self.style['font'], 24),
            width=2,
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat'
        )
        plus_btn.pack(side='left', padx=5)
        
        # Drying time setting
        drying_label = tk.Label(
            settings_frame,
            text="Tørketid (hours):",
            font=(self.style['font'], 24),
            bg=self.style['bg']
        )
        drying_label.pack(anchor='w', pady=(20, 5))
        
        # Drying time controls
        drying_controls = tk.Frame(settings_frame, bg=self.style['bg'])
        drying_controls.pack(anchor='w', pady=(0, 20))
        
        minus_btn = tk.Button(
            drying_controls,
            text="-",
            command=lambda: self.adjust_drying(-1),
            font=(self.style['font'], 24),
            width=2,
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat'
        )
        minus_btn.pack(side='left', padx=5)
        
        self.drying_var = tk.StringVar(value=str(self.config_manager.get_drying_time()))
        drying_label = tk.Label(
            drying_controls,
            textvariable=self.drying_var,
            font=(self.style['font'], 24),
            width=3,
            bg='white'
        )
        drying_label.pack(side='left', padx=10)
        
        plus_btn = tk.Button(
            drying_controls,
            text="+",
            command=lambda: self.adjust_drying(1),
            font=(self.style['font'], 24),
            width=2,
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat'
        )
        plus_btn.pack(side='left', padx=5)
        
        # Save button
        save_button = tk.Button(
            settings_frame,
            text="Save",
            command=self.save_settings,
            font=(self.style['font'], 24),
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat',
            padx=30,
            pady=15
        )
        save_button.pack(pady=20)
        
        # Back button
        back_button = tk.Button(
            settings_frame,
            text="Back",
            command=self.on_back,
            font=(self.style['font'], 24),
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat',
            padx=30,
            pady=15
        )
        back_button.pack(pady=20)
    
    def adjust_copies(self, delta):
        try:
            current = int(self.copies_var.get())
            new_value = max(1, current + delta)  # Ensure minimum of 1
            self.copies_var.set(str(new_value))
            self.config_manager.set_num_copies(new_value)
        except ValueError:
            self.copies_var.set('1')
            self.config_manager.set_num_copies(1)
    
    def adjust_drying(self, delta):
        try:
            current = int(self.drying_var.get())
            new_value = max(1, current + delta)  # Ensure minimum of 1
            self.drying_var.set(str(new_value))
            self.config_manager.set_drying_time(new_value)
        except ValueError:
            self.drying_var.set('19')
            self.config_manager.set_drying_time(19)
    
    def save_settings(self):
        # Settings are saved immediately when adjusted
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.on_back()
