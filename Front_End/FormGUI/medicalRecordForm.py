import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys
from tkcalendar import DateEntry
import datetime
import sys, os

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc
from Front_End.PagesGUI import medicalRecord

class MedicalRecordForm:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Medical Record Form")
        self.root.attributes('-fullscreen', True)

        self.id = id
        self.names = fnc.database_con().read("registration", "*")

        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }

        self.root.configure(bg=self.colors["bg"])
        self.form_vars = {
            "Check-up Form": {},
            "Normal Spontaneous Delivery Form": {}
        }

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header_frame.pack(fill="x")

        back_btn = tk.Button(header_frame, text="⟵ Back", font=("Arial", 12),
                             command=self.back, bg=self.colors["accent"],
                             fg="white", bd=0, padx=10,
                             activebackground="#333333", activeforeground="white")
        back_btn.place(x=10, y=20)

        title = tk.Label(header_frame, text="Medical Record Form", font=("Arial", 18, "bold"), bg=self.colors["accent"], fg="white")
        title.pack(pady=15)

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(window_id, width=event.width))
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind_scroll()
        self.create_checkup_form()
        self.create_delivery_form()

    def bind_scroll(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
            
    def create_checkup_form(self):
        section_title = "Check-up Form"
        section = tk.LabelFrame(self.scrollable_frame, text=section_title, font=("Arial", 14, "bold"),
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        fields = ["Patient Name", "Date"]
        for field in fields:
            self.create_entry_field(section, section_title, field)

        vital_header = tk.Label(section, text="Vital Signs", font=("Arial", 12, "bold"), bg=self.colors["section_bg"])
        vital_header.pack(fill="x", pady=5)

        vitals = ["Blood Pressure", "Heart Rate", "Respiratory Rate", "Temperature", "Oxygen Saturation"]
        for vital in vitals:
            self.create_entry_field(section, section_title, f"{vital}")
            
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

        self.create_entry_field(section, section_title, "Prescription")

        submit_btn = tk.Button(section, text="Submit", font=("Arial", 12),
                            bg=self.colors["accent"], fg="white", padx=15, pady=6,
                            command=lambda: self.submit_section(section_title),
                            activebackground="#333333", activeforeground="white")
        submit_btn.pack(pady=10)

    def create_delivery_form(self):
        section_title = "Normal Spontaneous Delivery Form"
        section = tk.LabelFrame(self.scrollable_frame, text=section_title, font=("Arial", 14, "bold"),
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        fields = ["Patient Name", "Date of Delivery", "Time of Delivery", "Delivery Notes", "Baby Weight", "Apgar Score"]
        for field in fields:
            self.create_entry_field(section, section_title, field)

        submit_btn = tk.Button(section, text="Submit", font=("Arial", 12),
                            bg=self.colors["accent"], fg="white", padx=15, pady=6,
                            command=lambda: self.submit_section(section_title),
                            activebackground="#333333", activeforeground="white")
        submit_btn.pack(pady=10)

    def create_entry_field(self, parent, section_title, field):
        frame = tk.Frame(parent, bg=self.colors["section_bg"])
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=field + ":", font=("Arial", 12), bg=self.colors["section_bg"], anchor="w")
        label.pack(fill="x")

        var = tk.StringVar()

        if field == "Patient Name":
            patient_names = [f"{name[2]} {name[3]}" for name in self.names]
            combobox = ttk.Combobox(frame, textvariable=var, values=patient_names, font=("Arial", 11), state="readonly")
            combobox.pack(fill="x", ipady=6)
        elif "Date" in field:
            date_entry = DateEntry(frame, textvariable=var, font=("Arial", 11), background="darkblue",
                                foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd',
                                maxdate=datetime.date.today())
            date_entry.pack(fill="x", ipady=6)
        elif "Time" in field:
            hours = [f"{h:02d}:{m:02d}" for h in range(24) for m in (range(60))]
            time_combobox = ttk.Combobox(frame, textvariable=var, values=hours, font=("Arial", 11), state="writeonly")
            time_combobox.pack(fill="x", ipady=6)
        else:
            entry = tk.Entry(frame, textvariable=var, font=("Arial", 11), bd=0,
                            highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
            entry.pack(fill="x", ipady=6)

        self.form_vars[section_title][field] = var

    def submit_section(self, section_name):
        values = self.form_vars[section_name].values()
        data = []

        for var in values:
            if isinstance(var, tk.Text):
                var = var.get("1.0", "end-1c")
            else:
                var = var.get()
            data.append(var)
        data.append(self.id)

        for names in self.names:
            if data[0] == f"{names[2]} {names[3]}":
                data.insert(0, names[0])

        print(data)

        if section_name == "Check-up Form":
            fnc.database_con().insert("checkup", ("patientID", "patientName", "date", "bloodPressure", "heartRate", "respiratoryRate", "temperature", "oxygenSaturation", "diagnosis", "prescription", "staffID"), data)
        elif section_name == "Normal Spontaneous Delivery Form":
            fnc.database_con().insert("nsd", ("patientID", "patientName", "dateofdelivery", "timeofdelivery", "deliveryNote", "Babyweight", "apgarScore", "staffID"), data)

        self.clear_section(section_name)

    def clear_section(self, section_name):
        for var in self.form_vars[section_name].values():
            if isinstance(var, tk.Text):
                var.delete("1.0", "end")
            else:
                var.set("")

    def back(self):
        self.root.destroy()
        medicalRecord.main(self.id)

def main(id=8):
    root = tk.Tk()
    app = MedicalRecordForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
