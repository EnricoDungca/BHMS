import tkinter as tk
from tkinter import ttk, font
import time
from threading import Thread
import sys

# import local modules
sys.path.insert(0,'\\BHMS')
from Back_End.systemfnc import email
from Front_End.PagesGUI import Dashboard
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import accountManagement

class OTPVerificationScreen:
    def __init__(self, root, email, id, verify, mode, digits=6, timeout=60):
        self.root = root
        self.root.title("OTP Verification")
        
        # Make it full screen
        self.root.attributes('-fullscreen', True)
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Number of OTP digits
        self.digits = digits
        
        # OTP timeout in seconds
        self.timeout = timeout
        self.time_remaining = timeout
        self.timer_running = False
        
        # Store email and verification data, etc.
        self.email = email
        self.id = id
        self.verify = verify
        self.mode = mode
        self.code = self.send_otp()
        
        # Create custom fonts
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=14)
        self.input_font = font.Font(family="Arial", size=20, weight="bold")
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        self.timer_font = font.Font(family="Arial", size=12)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white', font=self.subtitle_font)
        self.style.configure('Title.TLabel', font=self.title_font)
        self.style.configure('Timer.TLabel', font=self.timer_font, foreground='#666666')
        self.style.configure('TButton', font=self.button_font)
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create centered content frame
        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Add close button in top-right corner
        self.close_button = ttk.Button(
            self.main_frame, 
            text="×", 
            command=self.root.destroy,
            style='TButton'
        )
        self.close_button.place(x=self.screen_width-50, y=20, width=30, height=30)
        
        # Create UI elements
        self.create_ui()
        
        # Start the timer
        self.start_timer()
        
        # Store references to entry widgets
        self.entries = []
        
        # Create OTP input fields
        self.create_otp_inputs()
    
    def send_otp(self):
        """Send the OTP and return the code"""
        otp_code = email(self.email, self.verify).otp_send()
        return otp_code
    
    def create_ui(self):
        """Create the UI elements"""
        # Title
        title_label = ttk.Label(
            self.content_frame,
            text="Verification Code",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(
            self.content_frame,
            text="Enter the verification code sent to your device",
            style='TLabel'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # OTP input container (will be filled in create_otp_inputs)
        self.otp_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.otp_frame.pack(pady=(0, 30))
        
        # Timer label
        self.timer_label = ttk.Label(
            self.content_frame,
            text=f"Code expires in: {self.format_time(self.timeout)}",
            style='Timer.TLabel'
        )
        self.timer_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.content_frame, style='TFrame')
        buttons_frame.pack(pady=(10, 0))
        
        # Verify button
        self.verify_button = ttk.Button(
            buttons_frame,
            text="Verify",
            command=self.verify_otp,
            style='TButton',
            width=15
        )
        self.verify_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Resend button
        self.resend_button = ttk.Button(
            buttons_frame,
            text="Resend Code",
            command=self.resend_otp,
            style='TButton',
            width=15
        )
        self.resend_button.pack(side=tk.LEFT)
        
        # Error message label (hidden initially)
        self.error_label = ttk.Label(
            self.content_frame,
            text="",
            foreground="red",
            style='TLabel'
        )
        self.error_label.pack(pady=(20, 0))
        self.error_label.pack_forget()  # Hide initially
    
    def create_otp_inputs(self):
        """Create the OTP input fields"""
        # Clear any existing entries
        for widget in self.otp_frame.winfo_children():
            widget.destroy()
        
        self.entries = []
        
        # Calculate the width based on screen size
        digit_width = min(70, self.screen_width // (self.digits * 2))
        
        # Create entry widgets for each digit
        for i in range(self.digits):
            entry_var = tk.StringVar()
            entry = ttk.Entry(
                self.otp_frame,
                font=self.input_font,
                width=2,
                justify='center',
                textvariable=entry_var
            )
            
            # Position the entry
            entry.grid(row=0, column=i, padx=8)
            
            # Configure validation and behavior
            entry.configure(validate="key", validatecommand=(self.root.register(self.validate_digit), '%P', '%d', i))
            
            # Bind events
            entry.bind("<FocusIn>", lambda e, idx=i: self.on_entry_focus(e, idx))
            entry.bind("<KeyPress>", lambda e, idx=i: self.on_key_press(e, idx))
            entry.bind("<KeyRelease>", lambda e, idx=i: self.on_key_release(e, idx))
            
            self.entries.append(entry)
        
        # Focus on the first entry
        if self.entries:
            self.entries[0].focus_set()
    
    def validate_digit(self, new_value, action_type, index):
        """Validate input to ensure only one digit is entered"""
        if action_type == '1':  # Insert
            # Only allow digits
            if not new_value.isdigit():
                return False
            
            # Only allow one character
            if len(new_value) > 1:
                return False
            
            # Move focus to next entry if available
            if int(index) < len(self.entries) - 1:
                self.root.after(10, lambda: self.entries[int(index) + 1].focus_set())
            
            return True
        return True
    
    def on_entry_focus(self, event, index):
        """Handle entry focus event"""
        # Select all text when focused
        event.widget.select_range(0, tk.END)
    
    def on_key_press(self, event, index):
        """Handle key press events"""
        # Handle backspace
        if event.keysym == 'BackSpace' and not event.widget.get() and index > 0:
            # Move to previous entry
            self.entries[index - 1].focus_set()
            self.entries[index - 1].delete(0, tk.END)
            return 'break'
        
        # Handle left/right arrow keys
        if event.keysym == 'Left' and index > 0:
            self.entries[index - 1].focus_set()
            return 'break'
        elif event.keysym == 'Right' and index < len(self.entries) - 1:
            self.entries[index + 1].focus_set()
            return 'break'
    
    def on_key_release(self, event, index):
        """Handle key release events"""
        # Check if all entries are filled
        all_filled = all(entry.get() for entry in self.entries)
        if all_filled:
            # Auto-submit or just enable the verify button
            self.verify_button.focus_set()
    
    def get_otp(self):
        """Get the complete OTP from all entries"""
        return ''.join(entry.get() for entry in self.entries)
    
    def verify_otp(self):
        """Verify the entered OTP"""
        otp = self.get_otp()
        
        # Check if all digits are entered
        if len(otp) != self.digits:
            self.show_error("Please enter all digits")
            return
        
        # Here you would typically validate the OTP against your backend
        if int(otp) == self.code:
            self.show_success()
        else:
            self.show_error("Invalid verification code")
    
    def resend_otp(self):
        """Resend the OTP"""
        # Send a new OTP and update the code
        self.code = self.send_otp()  # <--- FIX: save the new code!

        # Reset the timer
        self.time_remaining = self.timeout
        if not self.timer_running:
            self.start_timer()

        # Clear all entries
        for entry in self.entries:
            entry.delete(0, tk.END)

        # Focus on the first entry
        if self.entries:
            self.entries[0].focus_set()

        # Enable the verify button again
        self.verify_button.config(state="enabled")

        # Show confirmation message
        self.show_message("A new code has been sent")

    
    def start_timer(self):
        """Start the countdown timer"""
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display"""
        if self.time_remaining > 0:
            self.timer_label.config(text=f"Code expires in: {self.format_time(self.time_remaining)}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Code expired. Please request a new one.")
            self.verify_button.config(state="disabled")
            self.code = 0
            self.timer_running = False
    
    def format_time(self, seconds):
        """Format seconds into MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def show_error(self, message):
        """Show an error message"""
        self.error_label.config(text=message, foreground="red")
        self.error_label.pack(pady=(20, 0))
        
        # Hide the message after 3 seconds
        self.root.after(3000, lambda: self.error_label.pack_forget())
    
    def show_message(self, message):
        """Show an informational message"""
        self.error_label.config(text=message, foreground="green")
        self.error_label.pack(pady=(20, 0))
        
        # Hide the message after 3 seconds
        self.root.after(3000, lambda: self.error_label.pack_forget())
    
    def show_success(self):
        """Show success message and close after delay"""
        # Clear the UI
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show success message
        success_label = ttk.Label(
            self.content_frame,
            text="✓",
            font=font.Font(family="Arial", size=48, weight="bold"),
            foreground="green",
            style='TLabel'
        )
        success_label.pack(pady=(0, 20))

        message_label = ttk.Label(
            self.content_frame,
            text="Verification Successful",
            style='Title.TLabel'
        )
        message_label.pack()

        # Close after 2 seconds and redirect properly
        self.root.after(2000, self.redirect)

    
    def redirect(self):
        """Redirect after success"""
        if self.mode == "user":
            if self.verify:
                self.root.destroy()
                Dashboard.main(self.id)
            else:
                self.root.destroy()
                Login.LoginUI()    
        else:
            if self.verify:
                self.root.destroy()
                accountManagement.main(self.id)
            else:
                self.root.destroy()
                Login.LoginUI() 
        

def main(email, id, verify, mode):
    """Main function to initiate the OTP Verification Screen"""
    root = tk.Tk()
    otp_screen = OTPVerificationScreen(root, email, id, verify, mode)
    root.mainloop()


if __name__ == "__main__":
    main("your_email@example.com", "verification_data")
