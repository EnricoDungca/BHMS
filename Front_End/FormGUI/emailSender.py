import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import os
import sys
from dotenv import load_dotenv, dotenv_values

config = {
    **dotenv_values(r"Back_End\.env.secret")
}

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Dashboard

class CompactEmailSender:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Email Sender")
        self.root.geometry("600x1000")
        self.root.config(bg="#1e1e2f")  # Dark background
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.id = id
        
        # Colors and styling
        self.primary_color = "#4285F4"  # Google blue
        self.bg_color = "#1e1e2f"
        self.text_color = "#4285F4"
        self.entry_bg = "#2e2e3e"
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', font=('Arial', 10))
        self.style.map("TButton", background=[("active", self.primary_color)])
        
        # Email content
        self.message = MIMEMultipart()
        
        # Track attachments
        self.attachments = []
        
        self.create_widgets()
    def on_close(self):
        self.root.destroy()
        Dashboard.main(self.id)
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = ttk.Label(header_frame, text="Compose Email", font=('Arial', 14, 'bold'))
        header_label.pack(side=tk.LEFT)
        
        # Email form
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # To field
        self.to_entry = self._create_entry_field(form_frame, "To:")
        
        # Subject field
        self.subject_entry = self._create_entry_field(form_frame, "Subject:")
        
        # Attachments display area
        self.attachment_frame = ttk.Frame(form_frame)
        self.attachment_frame.pack(fill=tk.X, pady=5)
        
        attachment_label = ttk.Label(self.attachment_frame, text="Attachments:")
        attachment_label.pack(side=tk.LEFT, padx=(8, 0))
        
        self.attachment_display = ttk.Label(self.attachment_frame, text="None", foreground="gray", background=self.bg_color)
        self.attachment_display.pack(side=tk.LEFT, padx=5)
        
        # Message body
        message_frame = ttk.Frame(form_frame)
        message_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.message_text = scrolledtext.ScrolledText(
            message_frame, wrap=tk.WORD, bg=self.entry_bg, fg=self.text_color,
            insertbackground="white", font=("Arial", 10)
        )
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        # Bottom buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.send_button = ttk.Button(
            button_frame, 
            text="Send", 
            command=self.send_email
        )
        self.send_button.pack(side=tk.LEFT)
        
        attachment_button = ttk.Button(
            button_frame,
            text="Attach File",
            command=self.attach_file
        )
        attachment_button.pack(side=tk.LEFT, padx=10)
        
        discard_button = ttk.Button(
            button_frame,
            text="Discard",
            command=self.discard_draft
        )
        discard_button.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready")
    
    def _create_entry_field(self, parent, label_text):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        label = ttk.Label(frame, text=label_text, width=8)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, bg=self.entry_bg, fg=self.text_color, insertbackground="white")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return entry

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def attach_file(self):
        filetypes = [
            ("All files", "*.*"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Image files", "*.jpg *.jpeg *.png *.gif")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select file(s) to attach",
            filetypes=filetypes
        )
        
        if files:
            for file in files:
                if file not in self.attachments:
                    self.attachments.append(file)
            
            self.update_attachment_display()
            self.status_var.set(f"{len(files)} file(s) attached")
    
    def update_attachment_display(self):
        if not self.attachments:
            self.attachment_display.config(text="None", foreground="gray")
        else:
            file_names = [os.path.basename(f) for f in self.attachments]
            if len(file_names) <= 2:
                display_text = ", ".join(file_names)
            else:
                display_text = f"{', '.join(file_names[:2])} and {len(file_names)-2} more"
            
            self.attachment_display.config(text=display_text, foreground=self.text_color)
    
    def send_email(self):
        to_email = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not to_email:
            messagebox.showerror("Error", "Please enter a recipient email address")
            return
        
        if not self.validate_email(to_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        self.status_var.set("Sending email...")
        
        attachment_info = ""
        if self.attachments:
            attachment_info = f" with {len(self.attachments)} attachment(s)"
        
        messagebox.showinfo("Success", f"Email{attachment_info} sent successfully!")
        self.status_var.set(f"Email{attachment_info} sent")
        
        self.message["From"] = config["EMAIL"]
        self.message["to"] = to_email
        self.message["subject"] = subject
        self.message.attach(MIMEText(message, "plain"))
        
        for attachment in self.attachments:
            with open(attachment, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                self.message.attach(part)
        
        fnc.email(to_email, True).send_email(self.message)
        
    
    def discard_draft(self):
        if messagebox.askyesno("Discard", "Discard this draft?"):
            self.to_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.message_text.delete("1.0", tk.END)
            self.attachments = []
            self.update_attachment_display()
            self.status_var.set("Draft discarded")

def main(id):
    root = tk.Tk()
    app = CompactEmailSender(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
