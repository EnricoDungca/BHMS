import tkinter as tk
from tkinter import ttk, font, messagebox
import sys, os
import re  # <-- added for regex

from PIL import Image, ImageTk

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import accountManagement

class AccountForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Register New Account")
        self.root.attributes('-fullscreen', True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.primary_color = "#34495e"
        self.secondary_color = "#2c3e50"
        self.bg_color = "#f4f4f4"
        self.text_color = "#2c3e50"
        self.accent_color = "#e74c3c"
        self.required_color = "#c0392b"

        self.root.configure(bg=self.bg_color)

        self.init_fonts()
        self.create_header()
        self.create_form()
        self.create_exit_button()

    def init_fonts(self):
        self.title_font = font.Font(family="Arial", size=26, weight="bold")
        self.header_font = font.Font(family="Arial", size=18, weight="bold")
        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = font.Font(family="Arial", size=13)
        self.button_font = font.Font(family="Arial", size=13, weight="bold")

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=90)
        header_frame.pack(fill="x")

        title_label = tk.Label(
            header_frame,
            text="Register New Account",
            font=self.title_font,
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=25)

    def create_form(self):
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill="both", expand=True)

        form = tk.Frame(container, bg="white", padx=40, pady=30, width=650)
        form.place(relx=0.5, rely=0.5, anchor="center")

        # Full Name
        tk.Label(form, text="Full Name *", font=self.label_font,
                 bg="white", fg=self.required_color).grid(row=0, column=0, sticky="w", pady=5)
        self.fullname_entry = tk.Entry(form, font=self.entry_font, width=45)
        self.fullname_entry.grid(row=1, column=0, pady=5)

        # Position
        tk.Label(form, text="Position *", font=self.label_font,
                 bg="white", fg=self.required_color).grid(row=2, column=0, sticky="w", pady=5)
        self.position_entry = tk.Entry(form, font=self.entry_font, width=45)
        self.position_entry.grid(row=3, column=0, pady=5)

        # Email
        tk.Label(form, text="Email *", font=self.label_font,
                 bg="white", fg=self.required_color).grid(row=4, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form, font=self.entry_font, width=45)
        self.email_entry.grid(row=5, column=0, pady=5)

        # Password
        tk.Label(form, text="Password *", font=self.label_font,
                 bg="white", fg=self.required_color).grid(row=6, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form, font=self.entry_font, show="*", width=45)
        self.password_entry.grid(row=7, column=0, pady=5)

        # Verify Password
        tk.Label(form, text="Verify Password *", font=self.label_font,
                 bg="white", fg=self.required_color).grid(row=8, column=0, sticky="w", pady=5)
        self.verify_password_entry = tk.Entry(form, font=self.entry_font, show="*", width=45)
        self.verify_password_entry.grid(row=9, column=0, pady=5)

        # Show Password checkbox
        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(form, text="Show Password", font=self.label_font,
                       bg="white", variable=self.show_password_var,
                       command=self.toggle_password_visibility).grid(row=10, column=0, sticky="w", pady=5)

        # Account Status (optional)
        tk.Label(form, text="Account Status (Optional)", font=self.label_font,
                 bg="white", fg=self.text_color).grid(row=11, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(
            form, textvariable=self.status_var,
            values=["Active", "Disabled"],
            state="readonly", font=self.entry_font, width=43
        )
        self.status_combobox.current(0)
        self.status_combobox.grid(row=12, column=0, pady=5)

        # Buttons
        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(row=13, column=0, pady=20)
        tk.Button(button_frame, text="Cancel", font=self.button_font,
                  command=self.cancel_form, bg="white", fg=self.text_color,
                  bd=1, relief="solid", padx=15, pady=8).pack(side="left", padx=10)
        tk.Button(button_frame, text="Register", font=self.button_font,
                  command=self.submit_form, bg=self.primary_color,
                  fg="white", padx=15, pady=8).pack(side="right", padx=10)

    def toggle_password_visibility(self):
        show = "" if self.show_password_var.get() else "*"
        self.password_entry.config(show=show)
        self.verify_password_entry.config(show=show)

    def create_exit_button(self):
        tk.Button(
            self.root, text="✕", font=self.button_font, bg=self.accent_color, fg="white",
            command=self.exit_application, bd=0
        ).place(x=self.screen_width - 50, y=10)

    def submit_form(self):
        fullname = self.fullname_entry.get().strip()
        position = self.position_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        verify_password = self.verify_password_entry.get().strip()
        status = self.status_var.get()

        # 1) Required fields
        if not all([fullname, position, email, password, verify_password]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # 2) Full Name & Position: only letters/spaces
        name_pattern = r"^[A-Za-z\s]+$"
        if not re.fullmatch(name_pattern, fullname):
            messagebox.showerror("Error", "Full Name may only contain letters and spaces.")
            return
        if not re.fullmatch(name_pattern, position):
            messagebox.showerror("Error", "Position may only contain letters and spaces.")
            return

        # 3) Email format
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.fullmatch(email_pattern, email):
            messagebox.showerror("Error", "Invalid email address format.")
            return

        # 4) Password strength (min 8 chars, letters & numbers)
        pwd_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
        if not re.fullmatch(pwd_pattern, password):
            messagebox.showerror(
                "Error",
                "Password must be at least 8 characters and include both letters and numbers."
            )
            return

        # 5) Password match
        if password != verify_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Encrypt & insert
        encoded_password = fnc.Security().Encrypt_str(password)
        try:
            fnc.database_con().insert(
                "accounts",
                ["fullname", "position", "email", "password", "accountStatus"],
                (fullname, position, email, encoded_password, status)
            )
            messagebox.showinfo("Success", "Account registered!")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Registration failed: {e}")

    def cancel_form(self):
        if messagebox.askyesno("Cancel", "Discard all entered data?"):
            self.clear_form()

    def clear_form(self):
        self.fullname_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.verify_password_entry.delete(0, tk.END)
        self.status_combobox.current(0)

    def exit_application(self):
        if messagebox.askyesno("Exit", "Exit to account management?"):
            self.root.destroy()
            accountManagement.main()

def main():
    root = tk.Tk()
    app = AccountForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
