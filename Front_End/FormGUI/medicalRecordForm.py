import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys

# Import local modules
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import medicalRecord

class MedicalRecordForm:
    def __init__(self, root, id):
        """
        Initializes the medical record form with a fullscreen window, and prepares
        necessary configurations like colors and form variables.
        """
        self.root = root
        self.root.title("Medical Record Form")
        self.root.attributes('-fullscreen', True)  # Set window to full screen
        
        self.id = id  # Store the patient ID
        
        # Fetch patient names from database
        self.names = fnc.database_con().read("registration", "*")
        
        # Define color scheme for the UI
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }

        self.root.configure(bg=self.colors["bg"])  # Set background color
        self.form_vars = {
            "Check-up Form": {},
            "Normal Spontaneous Delivery Form": {}
        }

        self.create_widgets()  # Call method to create UI elements

    def create_widgets(self):
        """
        Create and organize the UI widgets such as header, forms, and scrollable canvas.
        """
        # Header frame with back button and title
        header_frame = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header_frame.pack(fill="x")

        back_btn = tk.Button(header_frame, text="⟵ Back", font=("Arial", 12),
                             command=self.back, bg=self.colors["accent"],
                             fg="white", bd=0, padx=10,
                             activebackground="#333333", activeforeground="white")
        back_btn.place(x=10, y=20)  # Positioning of back button

        title = tk.Label(header_frame, text="Medical Record Form", font=("Arial", 18, "bold"), bg=self.colors["accent"], fg="white")
        title.pack(pady=15)  # Title of the form

        # Container for scrollable content
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollable canvas setup
        self.canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind(
            "<Configure>",  # Adjust canvas size when content changes
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Resize canvas width when the window is resized
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(window_id, width=event.width))
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind_scroll()  # Enable mouse scroll functionality

        # Create forms for Check-up and Normal Delivery
        self.create_checkup_form()
        self.create_delivery_form()

    def bind_scroll(self):
        """
        Bind mouse scroll functionality to scroll the canvas.
        """
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling within the canvas.
        """
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def create_checkup_form(self):
        """
        Create and populate the Check-up Form fields and sections.
        """
        section_title = "Check-up Form"
        section = tk.LabelFrame(self.scrollable_frame, text=section_title, font=("Arial", 14, "bold"),
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        fields = ["Patient Name", "Date"]  # Fields for the check-up form
        for field in fields:
            self.create_entry_field(section, section_title, field)

        vital_header = tk.Label(section, text="Vital Signs", font=("Arial", 12, "bold"), bg=self.colors["section_bg"])
        vital_header.pack(fill="x", pady=5)

        vitals = ["Blood Pressure", "Heart Rate", "Respiratory Rate", "Temperature", "Oxygen Saturation"]
        for vital in vitals:
            self.create_entry_field(section, section_title, f"{vital}")

        # Diagnosis section with text input
        frame = tk.Frame(section, bg=self.colors["section_bg"])
        frame.pack(fill="x", pady=5)
        label = tk.Label(frame, text="Diagnosis:", font=("Arial", 12), bg=self.colors["section_bg"], anchor="w")
        label.pack(fill="x")
        text_frame = tk.Frame(frame)
        text_frame.pack(fill="x")
        text_widget = tk.Text(text_frame, height=4, font=("Arial", 11), wrap="word",
                              bd=0, highlightthickness=1,
                              highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
        text_widget.pack(side="left", fill="x", expand=True, ipady=6)
        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scroll.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scroll.set)
        self.form_vars[section_title]["Diagnosis"] = text_widget

        # Prescription field
        self.create_entry_field(section, section_title, "Prescription")

        # Submit button for the form
        submit_btn = tk.Button(section, text="Submit", font=("Arial", 12),
                               bg=self.colors["accent"], fg="white", padx=15, pady=6,
                               command=lambda: self.submit_section(section_title),
                               activebackground="#333333", activeforeground="white")
        submit_btn.pack(pady=10)

    def create_delivery_form(self):
        """
        Create and populate the Normal Spontaneous Delivery Form fields and sections.
        """
        section_title = "Normal Spontaneous Delivery Form"
        section = tk.LabelFrame(self.scrollable_frame, text=section_title, font=("Arial", 14, "bold"),
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        fields = ["Patient Name", "Date of Delivery", "Time of Delivery", "Delivery Notes", "Baby Weight", "Apgar Score"]
        for field in fields:
            self.create_entry_field(section, section_title, field)

        # Submit button for the delivery form
        submit_btn = tk.Button(section, text="Submit", font=("Arial", 12),
                               bg=self.colors["accent"], fg="white", padx=15, pady=6,
                               command=lambda: self.submit_section(section_title),
                               activebackground="#333333", activeforeground="white")
        submit_btn.pack(pady=10)

    def create_entry_field(self, parent, section_title, field):
        """
        Create an entry field for the form (either combobox or text entry).
        """
        frame = tk.Frame(parent, bg=self.colors["section_bg"])
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=field + ":", font=("Arial", 12), bg=self.colors["section_bg"], anchor="w")
        label.pack(fill="x")

        var = tk.StringVar()  # Variable to store input data
        
        if field == "Patient Name":
            # Combobox for patient name selection
            patient_names = [F"{name[2]} {name[3]}" for name in self.names]
            combobox = ttk.Combobox(frame, textvariable=var, values=patient_names, font=("Arial", 11), state="readonly")
            combobox.pack(fill="x", ipady=6)
        else:
            # Entry field for other data
            entry = tk.Entry(frame, textvariable=var, font=("Arial", 11), bd=0,
                             highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
            entry.pack(fill="x", ipady=6)

        # Store the variable in form_vars dictionary for later retrieval
        self.form_vars[section_title][field] = var

    def submit_section(self, section_name):
        """
        Submit the form data to the database and clear the section for next use.
        """
        values = self.form_vars[section_name].values()
        data = []

        for var in values:
            if isinstance(var, tk.Text):
                var = var.get("1.0", "end-1c")
            else:
                var = var.get()
            data.append(var)
        data.append(self.id)
        
        # Fetch patient ID from database based on patient name
        for names in self.names:
            if data[0] == f"{names[2]} {names[3]}":
                data.insert(0, names[0])
        
        print(data)
        
        # Insert data into corresponding table based on form
        if section_name == "Check-up Form":
            fnc.database_con().insert("checkup", ("patientID", "patientName", "date", "bloodPressure", "heartRate", "respiratoryRate", "temperature", "oxygenSaturation", "diagnosis", "prescription", "staffID"), data)
        elif section_name == "Normal Spontaneous Delivery Form":
            fnc.database_con().insert("nsd", ("patientID", "patientName", "dateofdelivery", "timeofdelivery", "deliveryNote", "Babyweight", "apgarScore", "staffID"), data)

        self.clear_section(section_name)

    def clear_section(self, section_name):
        """
        Clear all input fields in the specified form section.
        """
        for var in self.form_vars[section_name].values():
            if isinstance(var, tk.Text):
                var.delete("1.0", "end")
            else:
                var.set("")

    def back(self):
        """
        Navigate back to the medical record page.
        """
        self.root.destroy()
        medicalRecord.main(self.id)

def main(id=8):
    """
    Run the application with a default patient ID.
    """
    root = tk.Tk()
    app = MedicalRecordForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()  # Start the app with default patient ID
