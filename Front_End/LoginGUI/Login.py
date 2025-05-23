import tkinter as tk
from tkinter import messagebox, font, ttk
import sys, os
from dotenv import dotenv_values
import re

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End.systemfnc import authentication
from Front_End.LoginGUI import OTPverificationUI

class LoginUI(tk.Tk):
    def __init__(self, mode="user"):
        super().__init__()
        self.mode = mode  # Store mode ("user" or "admin")
        self.title("Birthing Home Management System")
        self.geometry("1200x700")
        self.configure(bg="#f0f2f5")
        self.attributes('-fullscreen', True)  # Start fullscreen
        self.bind('<Escape>', self.exit_fullscreen)  # Bind ESC to exit fullscreen
        self.bind('<F11>', self.toggle_fullscreen)  # Bind F11 to toggle fullscreen
        
        self.setup_fonts()
        self.build_gui()

    def setup_fonts(self):
        """Configure fonts used in the GUI."""
        self.title_font = font.Font(family="Arial", size=28, weight="bold")
        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = ("Arial", 14)
        self.btn_font = font.Font(family="Arial", size=14, weight="bold")
        self.link_font = font.Font(family="Arial", size=12, underline=True)
        self.instr_font = font.Font(family="Arial", size=10)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode."""
        self.attributes('-fullscreen', False)
        return "break"

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        current = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current)
        return "break"

    def build_gui(self):
        """Construct the GUI layout based on the mode."""
        # Main container frame, centered
        main_frame = tk.Frame(self, bg="#f0f2f5")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Header frame for logo and title
        header_frame = tk.Frame(main_frame, bg="#f0f2f5")
        header_frame.pack(pady=(0, 50))
        
        # Load and display the logo image - FIX PATH HANDLING
        logo_path = resource_path(os.path.join("Front_End", "Pic", "logo.png"))
        try:
            self.logo_image = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(header_frame, image=self.logo_image, bg="#f0f2f5")
            logo_label.image = self.logo_image  # Prevent garbage collection
            logo_label.grid(row=0, column=0, padx=(0, 15))
        except Exception as e:
            print(f"Error loading logo image from {logo_path}: {str(e)}")
            # Create a placeholder if image fails to load
            placeholder = tk.Label(header_frame, text="LOGO", font=self.title_font, bg="#f0f2f5", 
                                  width=10, height=5)
            placeholder.grid(row=0, column=0, padx=(0, 15))
        
        # Title label changes based on mode
        if self.mode == "admin":
            title_text = "Birthing Home Management System\nAdmin"
        else:
            title_text = "Birthing Home Management System"
        title_label = tk.Label(header_frame, text=title_text, font=self.title_font, bg="#f0f2f5")
        title_label.grid(row=0, column=1)

        # Frame for the login form
        login_frame = tk.Frame(main_frame, bg="#f0f2f5", padx=40, pady=20)
        login_frame.pack()
        
        # Username label and entry
        tk.Label(login_frame, text="Email:", font=self.label_font, bg="#f0f2f5").grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        self.username_entry = tk.Entry(login_frame, width=30, font=self.entry_font)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Password label and entry
        tk.Label(login_frame, text="Password:", font=self.label_font, bg="#f0f2f5").grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        self.password_entry = tk.Entry(login_frame, width=30, font=self.entry_font, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Login button with validation callback
        login_button = tk.Button(
            login_frame,
            text="Login",
            command=self.validate_login,  # Call validate_login on click
            width=15,
            height=2,
            bg="#1877f2",
            fg="white",
            font=self.btn_font,
            relief=tk.FLAT
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=(30, 15))
        
        # Link button for toggling modes:
        # In user mode, shows "Admin" link; in admin mode, shows "Back" link.
        link_text = "Admin" if self.mode == "user" else "Back"
        link_button = tk.Label(
            login_frame,
            text=link_text,
            font=self.link_font,
            fg="#1877f2",
            bg="#f0f2f5",
            cursor="hand2"
        )
        link_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        # Clicking the link toggles the mode and rebuilds the GUI.
        link_button.bind("<Button-1>", lambda e: self.switch_mode())
        
        # Exit button to close the application
        exit_button = tk.Button(
            login_frame,
            text="Exit",
            command=self.destroy,
            width=15,
            height=1,
            bg="#e4e6eb",
            fg="#050505",
            font=("Arial", 12),
            relief=tk.FLAT
        )
        exit_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Instruction label for exiting fullscreen
        instr_label = tk.Label(
            login_frame,
            text="Press ESC to exit fullscreen mode",
            font=self.instr_font,
            fg="#65676b",
            bg="#f0f2f5"
        )
        instr_label.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        # Set focus to the username entry field
        self.username_entry.focus_set()

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return

        # Regex validation for username and password
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"

        if not re.match(email_pattern, username):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not re.match(password_pattern, password):
            messagebox.showerror("Error", "Invalid password format. Password must be at least 8 characters long and include uppercase, lowercase, and a digit.")
            return

        # Continue with your existing authentication logic...
        if self.mode == "admin":
            id, valid = authentication(username, password).main(self.mode)
            if valid:
                self.destroy()
                OTPverificationUI.main(username, id, valid, self.mode, "Active")
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        else:
            id, status, valid = authentication(username, password).main(self.mode)
            if valid:
                self.destroy()
                OTPverificationUI.main(username, id, valid, self.mode, status)
            else:
                messagebox.showerror("Error", "Invalid email, password, or account is disabled.")

    def switch_mode(self):
        """
        Toggle between user and admin modes.
        Destroys current window and re-launches LoginUI in the alternate mode.
        """
        self.destroy()
        new_mode = "admin" if self.mode == "user" else "user"
        LoginUI(mode=new_mode).mainloop()

def main():
    # Start the login UI in user mode (pass mode="admin" to start in admin mode)
    app = LoginUI(mode="user")
    app.mainloop()

if __name__ == "__main__":
    main()
