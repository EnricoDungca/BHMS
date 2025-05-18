import sys
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import re

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc  # type: ignore
from Front_End.PagesGUI import patientRegistration  # type: ignore


def main(staff_id: int):
    root = tk.Tk()
    app = PatientRegistrationForm(root, staff_id)
    root.mainloop()


class PatientRegistrationForm:
    def __init__(self, root: tk.Tk, staff_id: int) -> None:
        self.root = root
        self.staff_id = staff_id
        # form_vars now stores dicts with var and required flag
        self.form_vars = {}
        self._init_window()
        self._build_ui()

    def _init_window(self):
        self.root.title("Patient Registration")
        icon_file = Path(BASE_DIR) / 'resources' / 'app.ico'
        if icon_file.exists():
            try:
                self.root.iconbitmap(icon_file)
            except Exception:
                pass

        self.root.attributes('-fullscreen', True)
        self.colors = {
            'bg': '#ffffff',
            'accent': '#000000',
            'section_bg': '#f9f9f9',
            'required': '#e74c3c',
            'optional': '#7f8c8d',
            'button_fg': '#ffffff',
            'success': '#2ecc71',
            'danger': '#e74c3c'
        }
        self.root.configure(bg=self.colors['bg'])

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Section.TFrame', background=self.colors['section_bg'])
        style.configure('TLabel', background=self.colors['section_bg'], foreground=self.colors['accent'], font=('Arial', 14))
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TEntry', fieldbackground='white', padding=5)
        style.configure('TCombobox', padding=5)

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        header.pack(fill='x')
        tk.Label(
            header, text="Patient Registration",
            font=("Arial", 22, "bold"),
            bg=self.colors['accent'], fg=self.colors['button_fg']
        ).pack(pady=15)

        legend = tk.Frame(self.root, bg=self.colors['bg'])
        legend.pack(fill='x', padx=20)
        tk.Label(
            legend, text='* Required fields',
            font=("Arial", 12), fg=self.colors['required'], bg=self.colors['bg']
        ).pack(side='left')
        tk.Label(
            legend, text='(optional)',
            font=("Arial", 12, 'italic'), fg=self.colors['optional'], bg=self.colors['bg']
        ).pack(side='left', padx=10)

        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill='both', expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        win = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        self._bind_scroll(canvas, scroll_frame)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        sections = [
            ("Personal Information", [
                ("First Name", True), ("Middle Name", True), ("Last Name", True), ("Date of Birth", True),
                ("Gender", True), ("Phone", True), ("Email", False)
            ]),
            ("Address", [
                ("Street", True), ("Barangay", True), ("City/Municipality", True),
                ("Province", True), ("Region", True), ("ZIP/Postal Code", True)
            ]),
            ("Emergency Contact", [
                ("Emergency Contact Name", True), ("Emergency Contact Relationship", True), 
                ("Emergency Contact Phone", True), ("Emergency Contact Email", False)
            ]),
            ("Insurance", [
                ("Insurance Provider", False), ("Policy Number", False),
                ("Group Number", False), ("Primary Insured", False)
            ])
        ]

        for title, fields in sections:
            self._create_section(scroll_frame, title, fields)

        btn_frame = tk.Frame(self.root, bg=self.colors['bg'], pady=15)
        btn_frame.pack(fill='x', side='bottom')
        tk.Button(
            btn_frame, text='🔙 Exit', font=("Arial", 14, "bold"),
            bg=self.colors['danger'], fg=self.colors['button_fg'], bd=0,
            padx=30, pady=12, command=self._back
        ).pack(side='right', padx=10)
        tk.Button(
            btn_frame, text='✔ Submit', font=("Arial", 14, "bold"),
            bg=self.colors['success'], fg=self.colors['button_fg'], bd=0,
            padx=30, pady=12, command=self._submit
        ).pack(side='right')

    def _bind_scroll(self, canvas, widget):
        for target in (canvas, widget):
            target.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
            target.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
            target.bind('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))

    def _create_section(self, parent, title, fields):
        sf = ttk.Frame(parent, style='Section.TFrame')
        sf.pack(fill='x', pady=14, padx=5)
        tk.Label(
            sf, text=title, font=("Arial", 18, "bold"),
            bg=self.colors['section_bg'], fg=self.colors['accent']
        ).pack(anchor='w', padx=10, pady=(10, 0))
        ttk.Separator(sf, orient='horizontal').pack(fill='x', padx=10, pady=8)

        content = ttk.Frame(sf, style='Section.TFrame')
        content.pack(fill='x', padx=10, pady=8)
        cols = 2
        for idx, (label, required) in enumerate(fields):
            frame = ttk.Frame(content, style='Section.TFrame')
            frame.grid(row=idx//cols, column=idx%cols, sticky='ew', padx=8, pady=8)
            display_label = f"{'* ' if required else ''}{label}{'' if required else ' (optional)'}"
            fg = self.colors['required'] if required else self.colors['optional']
            tk.Label(frame, text=display_label, font=("Arial", 13), fg=fg, bg=self.colors['section_bg']).pack(anchor='w', pady=(0,6))

            var = tk.StringVar()
            # store each field's variable and required flag
            self.form_vars[label] = {'var': var, 'required': required}

            if label == "Date of Birth":
                DateEntry(frame, textvariable=var, date_pattern='yyyy-mm-dd', font=("Arial",14), width=40).pack(fill='x', pady=4)
            elif label == "Gender":
                cb = ttk.Combobox(frame, textvariable=var, values=["Male","Female"], state='readonly', font=("Arial",14), width=40)
                cb.pack(fill='x', pady=4); cb.current(0)
            elif label == "Region":
                regions = [
                    "NCR","CAR","Region I","Region II","Region III","Region IV-A",
                    "Region IV-B","Region V","Region VI","Region VII","Region VIII",
                    "Region IX","Region X","Region XI","Region XII","Region XIII","BARMM"
                ]
                cb = ttk.Combobox(frame, textvariable=var, values=regions, state='readonly', font=("Arial",14), width=40)
                cb.pack(fill='x', pady=4); cb.set('Select Region')
            else:
                entry = tk.Entry(
                    frame, textvariable=var, font=("Arial", 14), bd=1,
                    highlightthickness=1, highlightcolor=self.colors['accent'], width=50
                )
                entry.pack(fill='x', pady=4, ipady=8)

    def get_field_value(self, label: str) -> str:
        """Helper to retrieve and strip a field's value."""
        field = self.form_vars.get(label)
        if field:
            return field['var'].get().strip()
        return ''

    def _submit(self):
        # Validation for required fields
        missing = []
        for label, data in self.form_vars.items():
            if data['required'] and not data['var'].get().strip():
                missing.append(label)

        if missing:
            messagebox.showwarning("Missing Fields",
                                   f"Please complete all required fields: {', '.join(missing)}.",
                                   parent=self.root)
            return

        # Regular expression patterns
        name_pattern = re.compile(r'^[A-Za-z\s]+$')
        phone_pattern = re.compile(r'^\d{10,11}$')
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')
        zip_pattern = re.compile(r'^\d{4}$')

        # Validate names
        for fld in ["First Name", "Middle Name", "Last Name"]:
            val = self.get_field_value(fld)
            if val and not name_pattern.match(val):
                messagebox.showerror("Invalid Input",
                                     f"{fld} may only contain letters and spaces.",
                                     parent=self.root)
                return

        # Validate phone numbers
        for fld in ["Phone", "Emergency Contact Phone"]:
            val = self.get_field_value(fld)
            if val and not phone_pattern.match(val):
                messagebox.showerror("Invalid Input",
                                     f"Invalid {fld.lower()} format. Use 10 or 11 digits.",
                                     parent=self.root)
                return

        # Validate emails
        for fld in ["Email", "Emergency Contact Email"]:
            val = self.get_field_value(fld)
            if val and not email_pattern.match(val):
                messagebox.showerror("Invalid Input",
                                     f"Invalid {fld.lower()} format.",
                                     parent=self.root)
                return

        # Validate ZIP code
        zip_val = self.get_field_value("ZIP/Postal Code")
        if zip_val and not zip_pattern.match(zip_val):
            messagebox.showerror("Invalid Input",
                                 "Invalid ZIP/Postal Code. Must be 4 digits.",
                                 parent=self.root)
            return

        # Field mapping for DB insert
        field_mapping = {
            "First Name": "fname",
            "Middle Name": "mname",
            "Last Name": "lname",
            "Date of Birth": "dob",
            "Gender": "gender",
            "Phone": "phonenum",
            "Email": "email",
            "Street": "Street",
            "Barangay": "barangay",
            "City/Municipality": "cityMunicipality",
            "Province": "province",
            "Region": "region",
            "ZIP/Postal Code": "zip",
            "Emergency Contact Name": "ECname",
            "Emergency Contact Relationship": "ECrelationship",
            "Emergency Contact Phone": "ECphone",
            "Emergency Contact Email": "ECemail",
            "Insurance Provider": "insuranceProvider",
            "Policy Number": "Policynum",
            "Group Number": "GroupNum",
            "Primary Insured": "PrimaryInsured"
        }

        db_fields = list(field_mapping.values()) + ["staffID"]

        # Collect data
        data = []
        for fld in field_mapping:
            data.append(self.get_field_value(fld))
        data.append(self.staff_id)

        # Insert into database
        try:
            fnc.database_con().insert("registration", db_fields, data)
            messagebox.showinfo("Success", "Patient registered successfully!", parent=self.root)
            self._clear()
        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"An error occurred while saving to the database:\n{e}",
                                 parent=self.root)

    def _clear(self):
        for label, data in self.form_vars.items():
            var = data['var']
            if label == "Region":
                var.set('Select Region')
            elif label == "Gender":
                var.set('Male')
            else:
                var.set('')

    def _back(self):
        self.root.destroy()
        patientRegistration.main(self.staff_id)


if __name__ == '__main__':
    main(0)
