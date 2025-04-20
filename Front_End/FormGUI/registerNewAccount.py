import tkinter as tk
from tkinter import ttk, font, messagebox
import sys
from PIL import Image, ImageTk  # For handling images

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import accountManagement


class AccountForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Register New Account")
        
        # Make fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Set theme colors
        self.primary_color = "black"  # Blue
        self.secondary_color = "black"  # Darker blue
        self.bg_color = "#f5f5f5"  # Light gray
        self.text_color = "#333333"  # Dark gray
        self.accent_color = "#e74c3c"  # Red for exit button
        
        self.root.configure(bg=self.bg_color)
        
        self.init_fonts()
        self.create_header()
        self.create_form()
        self.create_exit_button()

    def init_fonts(self):
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.header_font = font.Font(family="Arial", size=16, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.entry_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

    def create_header(self):
        # Create header frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill="x")
        
        # Add title
        title_label = tk.Label(
            header_frame, 
            text="Register New Account", 
            font=self.title_font, 
            bg=self.primary_color, 
            fg="white"
        )
        title_label.pack(pady=20)

    def create_form(self):
        # Create main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True)
        
        # Create form container with fixed width
        form_width = 600
        form_container = tk.Frame(
            main_container, 
            bg="white", 
            width=form_width,
            highlightbackground=self.primary_color,
            highlightthickness=1,
            padx=40, 
            pady=30
        )
        
        # Center the form
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Form title
        form_title = tk.Label(
            form_container, 
            text="Register New Account", 
            font=self.header_font, 
            bg="white", 
            fg=self.text_color
        )
        form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Full Name
        tk.Label(
            form_container, 
            text="Full Name:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", pady=(10, 5))
        
        self.fullname_entry = tk.Entry(
            form_container, 
            font=self.entry_font, 
            width=40, 
            bd=1, 
            relief="solid"
        )
        self.fullname_entry.grid(row=2, column=0, sticky="ew", padx=5)

        # Position
        tk.Label(
            form_container, 
            text="Position:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=3, column=0, sticky="w", pady=(10, 5))
        
        self.position_entry = tk.Entry(
            form_container, 
            font=self.entry_font, 
            width=40, 
            bd=1, 
            relief="solid"
        )
        self.position_entry.grid(row=4, column=0, sticky="ew", padx=5)

        # Email
        tk.Label(
            form_container, 
            text="Email:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=5, column=0, sticky="w", pady=(10, 5))
        
        self.email_entry = tk.Entry(
            form_container, 
            font=self.entry_font, 
            width=40, 
            bd=1, 
            relief="solid"
        )
        self.email_entry.grid(row=6, column=0, sticky="ew", padx=5)

        # Password
        tk.Label(
            form_container, 
            text="Password:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=7, column=0, sticky="w", pady=(10, 5))
        
        self.password_entry = tk.Entry(
            form_container, 
            show="*", 
            font=self.entry_font, 
            width=40, 
            bd=1, 
            relief="solid"
        )
        self.password_entry.grid(row=8, column=0, sticky="ew", padx=5)

        # Verify Password
        tk.Label(
            form_container, 
            text="Verify Password:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=9, column=0, sticky="w", pady=(10, 5))
        
        self.verify_password_entry = tk.Entry(
            form_container, 
            show="*", 
            font=self.entry_font, 
            width=40, 
            bd=1, 
            relief="solid"
        )
        self.verify_password_entry.grid(row=10, column=0, sticky="ew", padx=5)

        # Account Status
        tk.Label(
            form_container, 
            text="Account Status:", 
            font=self.label_font, 
            bg="white", 
            fg=self.text_color
        ).grid(row=11, column=0, sticky="w", pady=(10, 5))
        
        self.status_var = tk.StringVar()
        
        style = ttk.Style()
        style.configure('TCombobox', font=self.entry_font)
        
        self.status_combobox = ttk.Combobox(
            form_container, 
            textvariable=self.status_var, 
            font=self.entry_font,
            values=["Active", "Disabled"], 
            state="readonly", 
            width=38
        )
        self.status_combobox.current(0)
        self.status_combobox.grid(row=12, column=0, sticky="ew", padx=5, pady=(0, 20))

        # Buttons frame
        buttons_frame = tk.Frame(form_container, bg="white")
        buttons_frame.grid(row=13, column=0, sticky="ew", pady=20)
        
        # Cancel Button
        tk.Button(
            buttons_frame, 
            text="Cancel", 
            font=self.button_font, 
            bg="white", 
            fg=self.text_color,
            relief=tk.FLAT, 
            padx=20, 
            pady=10, 
            command=self.cancel_form,
            bd=1,
            highlightbackground=self.text_color,
            highlightthickness=1
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Submit Button
        tk.Button(
            buttons_frame, 
            text="Register", 
            font=self.button_font, 
            bg=self.primary_color, 
            fg="white",
            activebackground=self.secondary_color,
            activeforeground="white",
            relief=tk.FLAT, 
            padx=20, 
            pady=10, 
            command=self.submit_form
        ).pack(side=tk.RIGHT)

    def create_exit_button(self):
        # Create exit button in top-right corner
        exit_button = tk.Button(
            self.root, 
            text="✕", 
            font=font.Font(family="Arial", size=16, weight="bold"),
            bg=self.accent_color, 
            fg="white",
            relief=tk.FLAT, 
            padx=10, 
            pady=5, 
            command=self.exit_application
        )
        exit_button.place(x=self.screen_width-50, y=10)

    def submit_form(self):
        fullname = self.fullname_entry.get().strip()
        position = self.position_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        verify_password = self.verify_password_entry.get().strip()
        encoded_password = fnc.Security().Encrypt_str(password)
        status = self.status_var.get()

        if not all([fullname, position, email, password, verify_password, status]):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if password != verify_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Validate email format (basic validation)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            # Insert into database
            fnc.database_con().insert(
                "accounts", 
                ["fullname", "position", "email", "password", "accountStatus"], 
                (fullname, position, email, encoded_password, status)
            )
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to register account: {str(e)}")

    def cancel_form(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel? All entered data will be lost."):
            self.clear_form()

    def clear_form(self):
        self.fullname_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.verify_password_entry.delete(0, tk.END)
        self.status_combobox.current(0)

    def exit_application(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            accountManagement.main()
            

def main():
    root = tk.Tk()
    app = AccountForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()