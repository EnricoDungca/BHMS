import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys

# Import DateEntry for date picker
from tkcalendar import DateEntry

# import local modules
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import patientRegistration

class PatientRegistrationForm:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Patient Registration")
        self.root.attributes('-fullscreen', True)
        
        self.id = id
        
        # Modern color scheme with black accent
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",  # Black accent color
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }
        
        # Configure styles
        self.configure_styles()
        
        # Variables dictionary to store all form data
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
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_screenwidth()-80)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.bind_scroll_wheel()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_section("Personal Information", [
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
        
        submit_btn = tk.Button(button_frame, text="Submit", font=("Arial", 12), 
                              command=self.submit_data, bg=self.colors["accent"], 
                              fg="white", padx=20, pady=8, bd=0,
                              activebackground="#333333", activeforeground="white")
        submit_btn.pack(side="right", padx=20)
        
        exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 12), 
                            command=self.back, bg=self.colors["danger"], 
                            fg="white", padx=20, pady=8, bd=0,
                            activebackground="#c0392b", activeforeground="white")
        exit_btn.pack(side="right")

    def bind_scroll_wheel(self):
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        self.canvas.focus_set()
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        return "break"

    def create_section(self, section_name, fields):
        section_frame = ttk.Frame(self.scrollable_frame, style="Section.TFrame")
        section_frame.pack(fill="x", pady=10, padx=10, ipady=10)
        
        section_frame.bind("<MouseWheel>", self._on_mousewheel)
        section_frame.bind("<Button-4>", self._on_mousewheel)
        section_frame.bind("<Button-5>", self._on_mousewheel)
        
        header_font = Font(family="Arial", size=14, weight="bold")
        header = tk.Label(section_frame, text=section_name, font=header_font, 
                         bg=self.colors["section_bg"], fg=self.colors["accent"])
        header.pack(anchor="w", padx=15, pady=(10, 15))
        
        separator = ttk.Separator(section_frame, orient="horizontal")
        separator.pack(fill="x", padx=15, pady=(0, 15))
        
        fields_frame = ttk.Frame(section_frame, style="Section.TFrame")
        fields_frame.pack(fill="x", padx=15)
        
        fields_frame.bind("<MouseWheel>", self._on_mousewheel)
        fields_frame.bind("<Button-4>", self._on_mousewheel)
        fields_frame.bind("<Button-5>", self._on_mousewheel)
        
        row = 0
        col = 0
        max_cols = 2
        
        for field in fields:
            field_frame = ttk.Frame(fields_frame, style="Section.TFrame")
            field_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            fields_frame.columnconfigure(0, weight=1)
            fields_frame.columnconfigure(1, weight=1)
            
            label = tk.Label(field_frame, text=field, font=("Arial", 11), 
                            bg=self.colors["section_bg"], fg=self.colors["text"])
            label.pack(anchor="w", pady=(0, 5))
            
            var = tk.StringVar()
            
            if field == "Region":
                var.set("Select Region")
                regions = [
                    "National Capital Region (NCR)",
                    "Cordillera Administrative Region (CAR)",
                    "Ilocos Region (Region I)",
                    "Cagayan Valley (Region II)",
                    "Central Luzon (Region III)",
                    "CALABARZON (Region IV-A)",
                    "MIMAROPA (Region IV-B)",
                    "Bicol Region (Region V)",
                    "Western Visayas (Region VI)",
                    "Central Visayas (Region VII)",
                    "Eastern Visayas (Region VIII)",
                    "Zamboanga Peninsula (Region IX)",
                    "Northern Mindanao (Region X)",
                    "Davao Region (Region XI)",
                    "SOCCSKSARGEN (Region XII)",
                    "Caraga (Region XIII)",
                    "Bangsamoro (BARMM)"
                ]
                dropdown = ttk.Combobox(field_frame, textvariable=var, values=regions, 
                                       font=("Arial", 11), state="readonly")
                dropdown.pack(fill="x", ipady=4)
            elif field == "Date of Birth":
                entry = DateEntry(field_frame, textvariable=var, font=("Arial", 11),
                                  background=self.colors["accent"], foreground="white", 
                                  borderwidth=0, date_pattern='yyyy-mm-dd')
                entry.pack(fill="x", ipady=4)
            else:
                entry = tk.Entry(field_frame, textvariable=var, font=("Arial", 11), 
                                bd=0, highlightthickness=1, 
                                highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
                entry.pack(fill="x", ipady=8)
            
            self.form_vars[section_name][field] = var
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def submit_data(self):
        # Map the order of fields as expected by the database
        db_fields = [
            "fname", "lname", "dob", "gender", "phonenum", "email",
            "House/Building/Street", "barangay", "city/municipality", "province", "region", "zip",
            "ECname", "ECrelationship", "ECphone", "ECemail",
            "insuranceProvider", "Policynum", "GroupNum", "PrimaryInsured"
        ]

        # Define the order in which fields should be extracted
        form_field_order = [
            ("Personal Information", ["First Name", "Last Name", "Date of Birth", "Gender", "Phone", "Email"]),
            ("Address", ["House/Building No. and Street", "Barangay", "City/Municipality", "Province", "Region", "ZIP/Postal Code"]),
            ("Emergency Contact", ["Contact Name", "Relationship", "Phone", "Email"]),
            ("Insurance", ["Insurance Provider", "Policy Number", "Group Number", "Primary Insured"]),
        ]

        values = []
        empty_fields = []

        for section, fields in form_field_order:
            for field in fields:
                value = self.form_vars[section][field].get().strip()
                if not value or value == "Select Region":
                    empty_fields.append(f"{section} - {field}")
                values.append(value)

        if empty_fields:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in the following fields:\n• " + "\n• ".join(empty_fields)
            )
            return
        print(values)
        # Submit to database
        fnc.database_con().insert("registration", db_fields, values)

        # Clear form after submission
        self.clear_form()
    
    def clear_form(self):
        for section, fields in self.form_vars.items():
            for field, var in fields.items():
                if field == "Region":
                    var.set("Select Region")
                else:
                    var.set("")
    
    def back(self):
        self.root.destroy()
        patientRegistration.main(self.id)
    
def main(id):
    root = tk.Tk()
    app = PatientRegistrationForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
