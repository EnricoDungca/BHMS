import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys, os

from tkcalendar import DateEntry

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import patientRegistration

class PatientRegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Registration")
        self.root.attributes('-fullscreen', True)

        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }

        self.configure_styles()

        self.form_vars = {
            "Personal Information": {},
            "Address": {},
            "Emergency Contact": {},
            "Insurance": {}
        }

        self.create_widgets()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Section.TFrame", background=self.colors["section_bg"])
        style.configure("TScrollbar", background=self.colors["bg"],
                        troughcolor=self.colors["light_bg"],
                        arrowcolor=self.colors["text"])

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header_frame.pack(fill="x")

        title_font = Font(family="Arial", size=18, weight="bold")
        title = tk.Label(header_frame, text="Patient Registration",
                         font=title_font, bg=self.colors["accent"], fg="white")
        title.pack(pady=15)

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw",
                                  width=self.canvas.winfo_screenwidth() - 80)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.bind_scroll_wheel()

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_section("Personal Information", [
            "ID",  # For retrieve/edit
            "First Name", "Last Name", "Date of Birth", "Gender", "Phone", "Email"
        ])

        self.create_section("Address", [
            "House/Building No. and Street",
            "Barangay",
            "City/Municipality",
            "Province",
            "Region",
            "ZIP/Postal Code"
        ])

        self.create_section("Emergency Contact", [
            "Contact Name", "Relationship", "Phone", "Email"
        ])

        self.create_section("Insurance", [
            "Insurance Provider", "Policy Number", "Group Number", "Primary Insured"
        ])

        button_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_frame.pack(side="bottom", fill="x")

        tk.Button(button_frame, text="Submit", font=("Arial", 12),
                  command=self.submit_data, bg=self.colors["accent"],
                  fg="white", padx=20, pady=8, bd=0,
                  activebackground="#333333", activeforeground="white").pack(side="right", padx=20)

        tk.Button(button_frame, text="Edit", font=("Arial", 12),
                  command=self.edit_data, bg="#f39c12",
                  fg="white", padx=20, pady=8, bd=0,
                  activebackground="#d68910", activeforeground="white").pack(side="left", padx=10)

        tk.Button(button_frame, text="Retrieve", font=("Arial", 12),
                  command=self.retrieve_data, bg="#2980b9",
                  fg="white", padx=20, pady=8, bd=0,
                  activebackground="#2471a3", activeforeground="white").pack(side="left")

        tk.Button(button_frame, text="Exit", font=("Arial", 12),
                  command=self.back, bg=self.colors["danger"],
                  fg="white", padx=20, pady=8, bd=0,
                  activebackground="#c0392b", activeforeground="white").pack(side="right")

    def bind_scroll_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        return "break"

    def create_section(self, section_name, fields):
        section_frame = ttk.Frame(self.scrollable_frame, style="Section.TFrame")
        section_frame.pack(fill="x", pady=10, padx=10, ipady=10)

        header_font = Font(family="Arial", size=14, weight="bold")
        tk.Label(section_frame, text=section_name, font=header_font,
                 bg=self.colors["section_bg"], fg=self.colors["accent"]).pack(anchor="w", padx=15, pady=(10, 15))

        ttk.Separator(section_frame, orient="horizontal").pack(fill="x", padx=15, pady=(0, 15))

        fields_frame = ttk.Frame(section_frame, style="Section.TFrame")
        fields_frame.pack(fill="x", padx=15)

        row = 0
        col = 0
        max_cols = 2

        for field in fields:
            field_frame = ttk.Frame(fields_frame, style="Section.TFrame")
            field_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            fields_frame.columnconfigure(col, weight=1)

            tk.Label(field_frame, text=field, font=("Arial", 11),
                     bg=self.colors["section_bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 5))

            var = tk.StringVar()

            if field == "Region":
                var.set("Select Region")
                regions = [
                    "National Capital Region (NCR)", "Cordillera Administrative Region (CAR)",
                    "Ilocos Region (Region I)", "Cagayan Valley (Region II)",
                    "Central Luzon (Region III)", "CALABARZON (Region IV-A)",
                    "MIMAROPA (Region IV-B)", "Bicol Region (Region V)",
                    "Western Visayas (Region VI)", "Central Visayas (Region VII)",
                    "Eastern Visayas (Region VIII)", "Zamboanga Peninsula (Region IX)",
                    "Northern Mindanao (Region X)", "Davao Region (Region XI)",
                    "SOCCSKSARGEN (Region XII)", "Caraga (Region XIII)", "Bangsamoro (BARMM)"
                ]
                ttk.Combobox(field_frame, textvariable=var, values=regions,
                             font=("Arial", 11), state="readonly").pack(fill="x", ipady=4)
            elif field == "Date of Birth":
                DateEntry(field_frame, textvariable=var, font=("Arial", 11),
                          background=self.colors["accent"], foreground="white",
                          borderwidth=0, date_pattern='yyyy-mm-dd').pack(fill="x", ipady=4)
            else:
                tk.Entry(field_frame, textvariable=var, font=("Arial", 11),
                         bd=0, highlightthickness=1,
                         highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"]).pack(fill="x", ipady=8)

            self.form_vars[section_name][field] = var

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def submit_data(self):
        all_data = {section: {k: v.get() for k, v in fields.items()}
                    for section, fields in self.form_vars.items()}

        empty_fields = [f"{section} - {field}" for section, fields in all_data.items()
                        for field, value in fields.items()
                        if not value.strip() or value == "Select Region"]

        if empty_fields:
            messagebox.showwarning("Missing Information", "Please fill in the following fields:\n• " + "\n• ".join(empty_fields))
            return

        values = [value for values in all_data.values() for value in values.values()][1:]
        fnc.database_con().insert("registration", (
            "fname", "lname", "dob", "gender", "phonenum", "email",
            "House/Building/Street", "barangay", "city/municipality", "province", "region", "zip",
            "ECname", "ECrelationship", "ECphone", "ECemail",
            "insuranceProvider", "Policynum", "GroupNum", "PrimaryInsured"
        ), values)

        messagebox.showinfo("Success", "Data submitted successfully.")
        self.clear_form()

    def retrieve_data(self):
        patient_id = self.form_vars["Personal Information"]["ID"].get()
        if not patient_id:
            messagebox.showwarning("Missing ID", "Please enter a patient ID to retrieve data.")
            return

        result = fnc.database_con().read("registration", "*")
        for row in result:
            if str(row[0]) == patient_id:
                flat_fields = [field for section in self.form_vars.values() for field in section.values()]
                for i, field_var in enumerate(flat_fields):
                    if i < len(row):
                        field_var.set(str(row[i]))
                break
        else:
            messagebox.showinfo("Not Found", "No record found with the given ID.")

    def edit_data(self):
        patient_id = self.form_vars["Personal Information"]["ID"].get()
        if not patient_id:
            messagebox.showwarning("Missing ID", "Please enter a patient ID to edit data.")
            return

        all_data = {section: {k: v.get() for k, v in fields.items()}
                    for section, fields in self.form_vars.items()}

        values = [value for values in all_data.values() for value in values.values()][1:]  # Skip ID
        columns = [
            "fname", "lname", "dob", "gender", "phonenum", "email",
            "House/Building/Street", "barangay", "city/municipality", "province", "region", "zip",
            "ECname", "ECrelationship", "ECphone", "ECemail",
            "insuranceProvider", "Policynum", "GroupNum", "PrimaryInsured"
        ]

        try:
            fnc.database_con().Record_edit(
                "registration",
                columns,
                values,
                "id",
                patient_id
            )
            messagebox.showinfo("Success", "Patient record updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient data.\n\n{str(e)}")

    def clear_form(self):
        for section, fields in self.form_vars.items():
            for field, var in fields.items():
                var.set("Select Region" if field == "Region" else "")

    def back(self):
        self.root.destroy()
        patientRegistration.main()

def main():
    root = tk.Tk()
    app = PatientRegistrationForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
