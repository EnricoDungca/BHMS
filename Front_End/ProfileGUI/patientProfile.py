import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from PIL import ImageGrab  # For capturing screenshot

class PatientProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Profile")
        self.root.attributes("-fullscreen", True)  # Full screen
        self.root.configure(bg="white")

        self.logo_image = None
        self.logo_text = "VM"

        default_logo_path = "Z:/BHMS/Front_End/Pic/logo.png"
        try:
            self.logo_image = PhotoImage(file=default_logo_path)
        except Exception:
            print("Logo image not found, using text fallback.")

        self.create_header()
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(fill="both", expand=True)

        self.setup_ui()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(side='top', fill='x')

        profile_pic = tk.Canvas(header, width=60, height=60, bg="#ecf0f1", highlightthickness=0)
        profile_pic.create_text(30, 30, text="JD", font=('Arial', 24, 'bold'), fill="#2c3e50")
        profile_pic.pack(side='left', padx=20, pady=10)

        info = tk.Frame(header, bg="#2c3e50")
        info.pack(side='left', padx=10)
        tk.Label(info, text="Juan Dela Cruz", font=('Arial', 20, 'bold'), bg="#2c3e50", fg="white").pack(anchor='w')
        tk.Label(info, text="DOB: 1985-06-15   |   Gender: Male   |   Patient ID: PT-41323",
                 font=('Arial', 12), bg="#2c3e50", fg="white").pack(anchor='w')

        # Back Button - Top Right
        back_btn = tk.Button(header, text="Back", font=("Arial", 12, "bold"), fg="white",
                             bg="#e74c3c", relief="flat", command=self.root.destroy)
        back_btn.pack(side="right", padx=20)

    def setup_ui(self):
        sidebar = tk.Frame(self.main_container, bg="#f0f0f0", width=280)
        sidebar.pack(side="left", fill="y")
        self.quick_info(sidebar)

        content_area = tk.Frame(self.main_container, bg="white")
        content_area.pack(side="right", fill="both", expand=True)

        notebook = ttk.Notebook(content_area)
        notebook.pack(fill="both", expand=True)

        self.about_tab(notebook)
        self.medical_tab(notebook)
        self.billing_tab(notebook)

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#2c3e50", height=50)
        footer.pack(side="bottom", fill="x")

        container = tk.Frame(footer, bg="#2c3e50")
        container.pack(anchor='center', pady=5)

        if self.logo_image:
            small_logo = self.logo_image.subsample(3, 3)
            self.footer_logo_label = tk.Label(container, image=small_logo, bg="#2c3e50")
            self.footer_logo_label.image = small_logo
            self.footer_logo_label.pack(side='left', padx=5)
        else:
            self.footer_logo_label = tk.Label(container, text=self.logo_text, bg="white",
                                              font=('Arial', 12, 'bold'), width=4, height=2)
            self.footer_logo_label.pack(side='left', padx=5)

        title = tk.Label(container, text="VMUF Birthing Home", bg="#2c3e50",
                         fg="white", font=('Arial', 14, 'bold'))
        title.pack(side='left', padx=5)

    def upload_logo(self):
        path = filedialog.askopenfilename(title="Select Logo Image",
                                          filetypes=[('PNG Images', '*.png'), ('GIF Images', '*.gif'), ('All files', '*.*')])
        if path:
            try:
                self.logo_image = PhotoImage(file=path)
                self.footer_logo_label.configure(image=self.logo_image, text="")
                self.footer_logo_label.image = self.logo_image
            except Exception:
                messagebox.showerror("Error", "Could not load selected image.")

    def save_profile_as_image(self):
        self.root.update()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = x + self.root.winfo_width()
        h = y + self.root.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
                                                title="Save Profile Screenshot")
        if filepath:
            img.save(filepath)
            messagebox.showinfo("Success", f"Profile saved as PNG at:\n{filepath}")

    def quick_info(self, parent):
        tk.Label(parent, text="Quick Info", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=15)
        info = {
            "Contact": "(0917) 123-4567\njuan.delacruz@email.com",
            "Address": "Blk 12, Lot 9, Barangay Malinis,\nSan Fernando City, Pampanga",
            "Emergency Contact": "Maria Clara (Wife)\n(0918) 987-6543",
            "Insurance": "PhilHealth\nMembership No: 1234-5678-9012"
        }
        for title, text in info.items():
            tk.Label(parent, text=title, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
            tk.Label(parent, text=text, bg="#f0f0f0", justify="left", wraplength=250, font=("Arial", 11)).pack(anchor="w", padx=15)

        btn = tk.Button(parent, text="Save Profile as PNG", command=self.save_profile_as_image,
                        bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                        relief="flat", padx=12, pady=6, cursor="hand2")
        btn.pack(pady=20)

    def about_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="About")
        tk.Label(tab, text="Patient Profile", font=("Arial", 18, "bold")).pack(pady=20)
        personal_info = {
            "Full Name": "Juan Dela Cruz",
            "Gender": "Male",
            "Date of Birth": "1985-06-15",
            "Phone": "(0917) 123-4567",
            "Email": "juan.delacruz@email.com",
            "PhilHealth No.": "1234-5678-9012",
            "Occupation": "Software Developer"
        }
        for key, value in personal_info.items():
            frame = tk.Frame(tab)
            frame.pack(anchor="w", padx=30, pady=6)
            tk.Label(frame, text=f"{key}:", font=("Arial", 12, "bold"), width=20, anchor="w").pack(side="left")
            tk.Label(frame, text=value, font=("Arial", 12)).pack(side="left")

    def medical_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Medical Records")
        canvas = tk.Canvas(tab, bg="white")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        records = [
            {"Date": "2023-05-15", "Doctor": "Dr. Santos", "Diagnosis": "Hypertension",
             "Symptoms": "High BP, dizziness, fatigue", "Medications": "Losartan 50mg once daily"},
            {"Date": "2022-11-10", "Doctor": "Dr. Reyes", "Diagnosis": "Acid Reflux",
             "Symptoms": "Heartburn, bloating", "Medications": "Omeprazole 20mg"},
        ]
        for record in records:
            card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
            card.pack(fill="x", padx=20, pady=10)
            tk.Label(card, text=f"{record['Date']} - {record['Doctor']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
            tk.Label(card, text=f"Diagnosis: {record['Diagnosis']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
            tk.Label(card, text=f"Symptoms: {record['Symptoms']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
            tk.Label(card, text=f"Medications: {record['Medications']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)

    def billing_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Billing")

        # Main container for billing records
        container = tk.Frame(tab, bg="white", padx=30, pady=20)
        container.pack(fill="both", expand=True)

        # Example billing records
        billing_records = [
            {"Date": "2023-05-10", "Service": "General Check-up - Dr. Santos", "Amount": "₱1,500.00", "Insurance": "₱1,200.00", "Paid": "₱300.00", "Payment Date": "2023-05-12"},
            {"Date": "2023-05-15", "Service": "Routine Consultation - Dr. Reyes", "Amount": "₱2,000.00", "Insurance": "₱1,500.00", "Paid": "₱500.00", "Payment Date": "2023-05-16"},
            {"Date": "2023-06-01", "Service": "Labor and Delivery - Dr. Santos", "Amount": "₱10,000.00", "Insurance": "₱8,000.00", "Paid": "₱2,000.00", "Payment Date": "2023-06-03"}
        ]

        # Loop through each billing record and create a card for each
        for record in billing_records:
            card = tk.Frame(container, bg="white", bd=1, relief="solid", padx=20, pady=15, width=350)
            card.pack(fill="x", padx=20, pady=10)

            # Header with record date and service description
            tk.Label(card, text=f"Date: {record['Date']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
            tk.Label(card, text=f"Service: {record['Service']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)

            # Billing details inside the card
            billing_info = [
                ("Amount", record['Amount']),
                ("Insurance", record['Insurance']),
                ("Paid", record['Paid']),
                ("Payment Date", record['Payment Date'])
            ]

            for key, value in billing_info:
                row = tk.Frame(card, bg="white")
                row.pack(anchor="w", pady=3)
                tk.Label(row, text=f"{key}:", font=("Arial", 12, "bold"), width=15, anchor="w", bg="white").pack(side="left")
                tk.Label(row, text=value, font=("Arial", 12), bg="white").pack(side="left")

            # Optional: Add a horizontal divider if you want more visual separation between sections
            tk.Frame(card, bg="#bdc3c7", height=1).pack(fill="x", pady=10)




if __name__ == "__main__":
    root = tk.Tk()
    app = PatientProfileApp(root)
    root.mainloop()
