import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from datetime import datetime, timedelta

class PrinterApp:
    def __init__(self, root, test_mode=True):
        self.root = root
        self.root.title("Label Printer")
        self.test_mode = test_mode
        
        # Make the window fullscreen on Raspberry Pi
        self.root.attributes('-fullscreen', True)
        
        # Set white background
        self.root.configure(bg='white')
        
        # Create main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left side - Container for vertical centering
        left_frame = tk.Frame(main_container, bg='white')
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 20))
        
        # Center container vertically
        center_frame = tk.Frame(left_frame, bg='white')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Batch number display
        self.batch_display = tk.Entry(
            center_frame,
            font=('Nohemi-Bold', 36),
            justify='center',
            width=10,
            bg='white',
            fg='#ff1910',
            relief='flat',
            bd=2
        )
        self.batch_display.pack(pady=(0, 30))
        self.batch_display.insert(0, '000')  # Default prefix
        self.batch_display.config(state='readonly')
        
        # Button style configuration
        button_font = ('Nohemi-Bold', 24)
        button_color = '#ff1910'
        self.button_style = {
            'bg': button_color,
            'fg': 'white',
            'activebackground': '#cc140c',
            'activeforeground': 'white',
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 30,
            'pady': 15,
        }
        
        # Print button
        self.print_button = tk.Button(
            center_frame,
            text="PRINT LABEL",
            command=self.print_receipt,
            font=button_font,
            **self.button_style
        )
        self.print_button.pack()
        
        # Right side - Numpad
        numpad_frame = tk.Frame(main_container, bg='white')
        numpad_frame.pack(side='right', padx=(20, 0))
        
        # Create numpad
        self.create_numpad(numpad_frame)
        
        # Add a quit button in the corner
        quit_button = tk.Button(
            root,
            text="X",
            command=root.quit,
            font=('Nohemi-Bold', 16),
            **self.button_style
        )
        quit_button.place(x=10, y=10)
        
        # Initialize batch number and button state
        self.current_batch = '000'
        self.update_button_state()  # Initially disable button
        
    def create_numpad(self, parent):
        numpad_layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['C', '0', '⌫']
        ]
        
        for row_idx, row in enumerate(numpad_layout):
            for col_idx, key in enumerate(row):
                btn = tk.Button(
                    parent,
                    text=key,
                    font=('Nohemi-Bold', 24),
                    width=3,
                    command=lambda k=key: self.numpad_press(k),
                    **self.button_style
                )
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
    
    def update_button_state(self):
        current = self.batch_display.get()
        if len(current) == 10:  # Valid batch number (000 + 7 digits)
            self.print_button.configure(
                state='normal',
                bg=self.button_style['bg'],
                activebackground=self.button_style['activebackground']
            )
        else:
            self.print_button.configure(
                state='disabled',
                bg='#cccccc',
                activebackground='#cccccc'
            )
                
    def numpad_press(self, key):
        current = self.batch_display.get()
        
        if key == '⌫':  # Backspace
            if len(current) > 3:  # Don't delete the '000' prefix
                self.batch_display.config(state='normal')
                self.batch_display.delete(len(current)-1, tk.END)
                self.batch_display.config(state='readonly')
        elif key == 'C':  # Clear
            self.batch_display.config(state='normal')
            self.batch_display.delete(3, tk.END)  # Keep the '000' prefix
            self.batch_display.config(state='readonly')
        elif len(current) < 10:  # Max length is 10 (000 + 7 digits)
            self.batch_display.config(state='normal')
            self.batch_display.insert(tk.END, key)
            self.batch_display.config(state='readonly')
            
        # Update button state after any input change
        self.update_button_state()

    def create_receipt_image(self):
        # Create a new image with white background
        width = 800  # Width for 70mm tape
        height = 405  # ~36mm height (reduced by 10%)
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        try:
            title_font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 57)  # 52 * 1.1
            time_font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 44)   # 40 * 1.1
        except:
            title_font = time_font = ImageFont.load_default()
        
        # Get current time and finish time
        now = datetime.now()
        finish_time = now + timedelta(hours=19)
        
        # Format times
        start_str = now.strftime("%d/%m-%Y %H:%M")
        finish_str = finish_time.strftime("%d/%m-%Y %H:%M")
        
        # Get batch number
        batch = self.batch_display.get()
        
        # Add content
        y_spacing = 50  # Increased spacing for larger fonts
        draw.text((50, 50), f"START: {start_str}", font=time_font, fill='black')
        draw.text((50, 50 + y_spacing*2), f"FERDIG: {finish_str}", font=time_font, fill='black')
        draw.text((50, 50 + y_spacing*4), f"BATCH: {batch}", font=title_font, fill='black')
        
        return image

    def show_printing_feedback(self):
        # Disable and gray out the button
        self.print_button.configure(
            state='disabled',
            bg='#cccccc',
            activebackground='#cccccc'
        )
        
        # Create and show the printing message
        self.status_label = tk.Label(
            self.root,
            text="Printing...",
            font=('Nohemi-Bold', 28),
            fg='#cccccc',
            bg='white'
        )
        # Position it above the button
        button_x = self.print_button.winfo_rootx() - self.root.winfo_rootx()
        button_y = self.print_button.winfo_rooty() - self.root.winfo_rooty() - 50
        self.status_label.place(x=button_x, y=button_y)
        
        # Schedule the restoration
        self.root.after(5000, self.restore_button)

    def restore_button(self):
        # Remove the status label
        if hasattr(self, 'status_label'):
            self.status_label.destroy()
        
        # Reset input field
        self.batch_display.config(state='normal')
        self.batch_display.delete(3, tk.END)  # Keep the '000' prefix
        self.batch_display.config(state='readonly')
        
        # Update button state for the cleared input
        self.update_button_state()

    def print_receipt(self):
        try:
            # Create receipt image
            receipt_image = self.create_receipt_image()
            
            # Save temporary image
            temp_path = "temp_receipt.png"
            receipt_image.save(temp_path)
            
            # Show printing feedback
            self.show_printing_feedback()
            
            if self.test_mode:
                print("Test Mode: Receipt would be printed")
                print(f"Receipt image saved as {temp_path} for preview")
            else:
                # Real printing mode
                # Printer settings
                printer_model = 'QL-800'  # Update this to match your printer model
                label_size = '62'  # 62mm endless label
                
                # Create the label instructions
                qlr = BrotherQLRaster(printer_model)
                qlr.exception_on_warning = True
                
                # Convert image to label format
                convert(
                    qlr=qlr,
                    images=[temp_path],
                    label='62',  # 70mm endless label
                    rotate='auto',
                    threshold=70.0,
                    dither=False,
                    compress=False,
                    red=False,
                    dpi_600=False,
                    hq=True,
                    cut=True
                )
                
                # Send to printer using linux_kernel backend
                send(
                    instructions=qlr.data,
                    printer_identifier='/dev/usb/lp0',
                    backend_identifier='linux_kernel',
                    blocking=True
                )
                
                # Clean up temporary file after printing
                os.remove(temp_path)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error: {error_msg}")
            
            # Show error in GUI
            error_popup = tk.Toplevel(self.root)
            error_popup.title("Error")
            
            # Center the popup
            error_popup.geometry("400x150")
            error_popup.geometry(f"+{self.root.winfo_x() + 100}+{self.root.winfo_y() + 100}")
            
            # Add error message
            if "Permission denied" in error_msg and "/dev/usb/lp0" in error_msg:
                msg = "Printer permission denied.\nPlease run:\nsudo chmod 666 /dev/usb/lp0"
            else:
                msg = f"Error: {error_msg}"
                
            label = tk.Label(
                error_popup,
                text=msg,
                pady=20,
                font=('Nohemi-Bold', 14),
                fg='#ff1910'
            )
            label.pack()
            
            # Add OK button
            ok_button = tk.Button(
                error_popup,
                text="OK",
                command=error_popup.destroy,
                font=('Nohemi-Bold', 12),
                bg='#ff1910',
                fg='white',
                relief='flat',
                padx=20,
                pady=5
            )
            ok_button.pack(pady=10)
            
            # Restore the print button
            self.restore_button()
