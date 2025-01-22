import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import os
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

class PrinterApp:
    def __init__(self, root, test_mode=True):
        self.root = root
        self.root.title("Receipt Printer")
        self.test_mode = test_mode
        
        # Make the window fullscreen on Raspberry Pi
        self.root.attributes('-fullscreen', True)
        
        # Set white background
        self.root.configure(bg='white')
        
        # Create a frame to center the button with white background
        frame = tk.Frame(root, bg='white')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Button style configuration
        button_font = ('Nohemi-Bold', 24)
        button_color = '#ff1910'
        button_style = {
            'bg': button_color,
            'fg': 'white',
            'activebackground': '#cc140c',  # Slightly darker for pressed state
            'activeforeground': 'white',
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 30,
            'pady': 15,
        }
        
        # Create a large button suitable for touch screens
        self.print_button = tk.Button(
            frame,
            text="PRINT RECEIPT",
            command=self.print_receipt,
            font=button_font,
            **button_style
        )
        self.print_button.pack(pady=20)
        
        # Add a quit button in the corner with matching style
        quit_button = tk.Button(
            root,
            text="X",
            command=root.quit,
            font=('Nohemi-Bold', 16),
            **button_style
        )
        quit_button.place(x=10, y=10)

    def create_receipt_image(self):
        # Create a new image with white background
        width = 696  # Width for 62mm tape
        height = 500  # Adjust height as needed
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Add text to the image
        try:
            font = ImageFont.truetype("assets/Nohemi/OpenType-TT/Nohemi-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        # Add receipt content
        draw.text((50, 50), "Test Receipt", font=font, fill='black')
        draw.text((50, 150), "Date: 2025-01-22", font=font, fill='black')
        draw.text((50, 250), "Thank you!", font=font, fill='black')
        
        return image

    def show_printing_feedback(self):
        # Disable and fade out the button
        self.print_button.configure(state='disabled')
        
        # Create and show the printing message
        self.status_label = tk.Label(
            self.root,
            text="Printing...",
            font=('Nohemi-Bold', 28),
            fg='#ff1910',
            bg='white'
        )
        # Position it where the button is
        button_x = self.print_button.winfo_rootx() - self.root.winfo_rootx()
        button_y = self.print_button.winfo_rooty() - self.root.winfo_rooty()
        self.status_label.place(x=button_x, y=button_y)
        
        # Hide the button
        self.print_button.pack_forget()
        
        # Schedule the restoration of the button
        self.root.after(5000, self.restore_button)

    def restore_button(self):
        # Remove the status label
        if hasattr(self, 'status_label'):
            self.status_label.destroy()
        
        # Show and enable the button
        self.print_button.pack(pady=20)
        self.print_button.configure(state='normal')

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
                    label='62',  # 62mm endless label
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
