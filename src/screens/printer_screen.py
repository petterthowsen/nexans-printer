import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from datetime import datetime, timedelta

class PrinterScreen(tk.Frame):
    def __init__(self, parent, config_manager, show_settings):
        super().__init__(parent, bg='white')
        self.config_manager = config_manager
        self.show_settings = show_settings
        
        # Style configuration
        self.style = {
            'bg': 'white',
            'button_color': '#ff1910',
            'button_active': '#cc140c',
            'font': 'Nohemi-Bold'
        }
        
        # Easter egg tracking
        self.backspace_times = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        main_container = tk.Frame(self, bg='white')
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
            font=(self.style['font'], 36),
            justify='center',
            width=10,
            bg='white',
            fg=self.style['button_color'],
            relief='flat',
            bd=2
        )
        self.batch_display.pack(pady=(0, 30))
        self.batch_display.insert(0, '000')  # Default prefix
        self.batch_display.config(state='readonly')
        
        # Print button
        self.print_button = tk.Button(
            center_frame,
            text="PRINT LABEL",
            command=self.print_receipt,
            font=(self.style['font'], 24),
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat',
            padx=30,
            pady=15
        )
        self.print_button.pack()
        
        # Right side - Numpad
        numpad_frame = tk.Frame(main_container, bg='white')
        numpad_frame.pack(side='right', padx=(20, 0))
        
        # Create numpad
        self.create_numpad(numpad_frame)
        
        # Load and create logo for GUI
        logo_image = Image.open("assets/Nexans_logo.svg.png")
        # Resize logo to height of 40px while maintaining aspect ratio
        logo_ratio = logo_image.width / logo_image.height
        logo_image = logo_image.resize((int(40 * logo_ratio), 40), Image.Resampling.LANCZOS)
        # Save temporarily and load as PhotoImage
        logo_image.save("temp_logo.png")
        self.logo_photo = tk.PhotoImage(file="temp_logo.png")
        os.remove("temp_logo.png")
        
        # Add logo to bottom left of window
        logo_label = tk.Label(self, image=self.logo_photo, bg='white')
        logo_label.place(relx=0.02, rely=0.95, anchor='sw')
        
        # Settings button in top right
        settings_button = tk.Button(
            self,
            text="⚙",  # Gear emoji
            command=self.show_settings,
            font=(self.style['font'], 24),
            bg=self.style['button_color'],
            fg='white',
            activebackground=self.style['button_active'],
            activeforeground='white',
            relief='flat',
            width=2
        )
        settings_button.place(x=self.winfo_screenwidth()-100, y=20)
        
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
                    font=(self.style['font'], 24),
                    width=3,
                    command=lambda k=key: self.numpad_press(k),
                    bg=self.style['button_color'],
                    fg='white',
                    activebackground=self.style['button_active'],
                    activeforeground='white',
                    relief='flat'
                )
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
    
    def update_button_state(self):
        # Button is always enabled since batch number is optional
        self.print_button.configure(
            state='normal',
            bg=self.style['button_color'],
            activebackground=self.style['button_active']
        )
                
    def numpad_press(self, key):
        current = self.batch_display.get()
        
        if key == '⌫':  # Backspace
            if current == '000':  # Easter egg check
                now = datetime.now()
                # Remove old timestamps (older than 3 seconds)
                self.backspace_times = [t for t in self.backspace_times 
                                      if (now - t).total_seconds() <= 3]
                # Add new timestamp
                self.backspace_times.append(now)
                
                # Check if we have 5 presses within 3 seconds
                if len(self.backspace_times) >= 5:
                    self.print_easter_egg()
                    self.backspace_times = []  # Reset after showing
            
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
        height = 365  # ~32mm height
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        try:
            title_font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 63)
            time_font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 48)
        except:
            title_font = time_font = ImageFont.load_default()
        
        # Get current time and finish time
        now = datetime.now()
        drying_hours = self.config_manager.get_drying_time()
        finish_time = now + timedelta(hours=drying_hours)
        
        # Format times
        start_str = now.strftime("%d/%m-%Y %H:%M")
        finish_str = finish_time.strftime("%d/%m-%Y %H:%M")
        
        # Get batch number
        batch = self.batch_display.get()
        
        # Calculate positions
        y_spacing = 55  # Spacing between lines
        left_margin = 50
        right_margin = width - 50  # 50px from right edge
        
        # Draw times
        draw.text((left_margin, 50), "START:", font=time_font, fill='black')
        draw.text((left_margin, 50 + y_spacing*2), "FERDIG:", font=time_font, fill='black')
        
        # Right-align time values
        start_width = time_font.getlength(start_str)
        finish_width = time_font.getlength(finish_str)
        draw.text((right_margin - start_width, 50), start_str, font=time_font, fill='black')
        draw.text((right_margin - finish_width, 50 + y_spacing*2), finish_str, font=time_font, fill='black')
        
        # Only show batch if entered
        if batch.strip() != '000':  # If there's more than just the prefix
            draw.text((left_margin, 50 + y_spacing*4), "BATCH:", font=title_font, fill='black')
            batch_width = title_font.getlength(batch)
            draw.text((right_margin - batch_width, 50 + y_spacing*4), batch, font=title_font, fill='black')
        
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
            self,
            text="Printing...",
            font=(self.style['font'], 28),
            fg='#cccccc',
            bg='white'
        )
        # Position it above the button
        button_x = self.print_button.winfo_rootx() - self.winfo_rootx()
        button_y = self.print_button.winfo_rooty() - self.winfo_rooty() - 50
        self.status_label.place(x=button_x, y=button_y)
        
        # Schedule the restoration after 3 seconds
        self.after(3000, self.restore_button)

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
            
            if self.winfo_toplevel().test_mode:
                print("Test Mode: Labels would be printed")
                print(f"Receipt preview saved as {temp_path}")
            else:
                # Real printing mode
                # Printer settings
                printer_model = 'QL-800'
                
                # Create the label instructions
                qlr = BrotherQLRaster(printer_model)
                qlr.exception_on_warning = True
                
                # Convert image to label format once
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
                
                # Store instructions
                instructions = qlr.data
                
                # Print the configured number of copies
                num_copies = self.config_manager.get_num_copies()
                for _ in range(num_copies):
                    # Send to printer using linux_kernel backend
                    send(
                        instructions=instructions,
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
            error_popup = tk.Toplevel(self)
            error_popup.title("Error")
            
            # Center the popup
            error_popup.geometry("400x150")
            error_popup.geometry(f"+{self.winfo_x() + 100}+{self.winfo_y() + 100}")
            
            # Add error message
            if "Permission denied" in error_msg and "/dev/usb/lp0" in error_msg:
                msg = "Printer permission denied.\nPlease run:\nsudo chmod 666 /dev/usb/lp0"
            else:
                msg = f"Error: {error_msg}"
                
            label = tk.Label(
                error_popup,
                text=msg,
                pady=20,
                font=(self.style['font'], 14),
                fg=self.style['button_color']
            )
            label.pack()
            
            # Add OK button
            ok_button = tk.Button(
                error_popup,
                text="OK",
                command=error_popup.destroy,
                font=(self.style['font'], 12),
                bg=self.style['button_color'],
                fg='white',
                relief='flat',
                padx=20,
                pady=5
            )
            ok_button.pack(pady=10)
            
            # Restore the print button
            self.restore_button()
            
    def create_easter_egg_image(self):
        # Create a new image with white background - shorter height for single line
        width = 800  # Width for 70mm tape
        height = 150  # Shorter height for single line
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        

        message = "Slutt å tull!"
        
        # Center the text
        text_width = font.getlength(message)
        x = (width - text_width) / 2
        y = (height - 48) / 2  # Vertically center based on font size
        
        # Draw the message
        draw.text((x, y), message, font=font, fill='black')
        
        return image
            
    def print_easter_egg(self):
        try:
            # Create easter egg image
            easter_egg_image = self.create_easter_egg_image()
            
            # Save temporary image
            temp_path = "temp_easter_egg.png"
            easter_egg_image.save(temp_path)
            
            # Show printing feedback
            self.show_printing_feedback()
            
            if self.winfo_toplevel().test_mode:
                print("Test Mode: Easter egg would be printed")
                print(f"Easter egg preview saved as {temp_path}")
            else:
                # Real printing mode
                # Printer settings
                printer_model = 'QL-800'
                
                # Create the label instructions
                qlr = BrotherQLRaster(printer_model)
                qlr.exception_on_warning = True
                
                # Convert image to label format
                convert(
                    qlr=qlr,
                    images=[temp_path],
                    label='62',
                    rotate='auto',
                    threshold=70.0,
                    dither=False,
                    compress=False,
                    red=False,
                    dpi_600=False,
                    hq=True,
                    cut=True
                )
                
                # Send to printer
                send(
                    instructions=qlr.data,
                    printer_identifier='/dev/usb/lp0',
                    backend_identifier='linux_kernel',
                    blocking=True
                )
                
                # Clean up
                os.remove(temp_path)
            
        except Exception as e:
            print(f"Easter egg error: {str(e)}")
