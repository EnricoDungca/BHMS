import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys
from tkcalendar import DateEntry
import datetime
import re
import os

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc
from Front_End.PagesGUI import medicalRecord


class AutocompleteCombobox(ttk.Combobox):
    """
    A ttk.Combobox with autocompletion: filters suggestions as the user types.
    """
    def __init__(self, master=None, completevalues=None, **kwargs):
        self.all_values = completevalues or []
        super().__init__(master, **kwargs)

        # allow typing
        self.config(state='normal')
        # bind key release to update suggestions
        self.bind('<KeyRelease>', self._on_keyrelease)

    def _on_keyrelease(self, event):
        value = self.get()
        # filter list case-insensitive
        filtered = [v for v in self.all_values if value.lower() in v.lower()]
        # update dropdown
        self['values'] = filtered
        # show if matches
        if filtered:
            self.event_generate('<Down>')


class MedicalRecordForm:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Medical Record Form")
        self.root.attributes('-fullscreen', True)

        self.id = id
        # fetch all registrations
        self.names = fnc.database_con().read("registration", "*")

        self.colors = {
            "bg": "#ffffff",
            "accent": "#007acc",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#d60000",
            "section_bg": "#f9f9f9"
        }

        self.root.configure(bg=self.colors["bg"])
        self.form_vars = {
            "Check-up Form": {},
            "Normal Spontaneous Delivery Form": {}
        }

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="black", height=70)
        header_frame.pack(fill="x")

        back_btn = tk.Button(
            header_frame, text="⟵ Back", font=("Arial", 12),
            command=self.back, bg="black",
            fg="white", bd=0, padx=10,
            activebackground="#333333", activeforeground="white"
        )
        back_btn.place(x=10, y=20)

        title = tk.Label(
            header_frame, text="Medical Record Form", font=("Arial", 18, "bold"),
            bg="black", fg="white"
        )
        title.pack(pady=15)

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(window_id, width=event.width)
        )
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
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def create_checkup_form(self):
        title = "Check-up Form"
        section = self.create_section_frame(title)

        required_fields = [
            "Patient Name*", "Date*", "Blood Pressure*",
            "Heart Rate*", "Respiratory Rate*", "Temperature*",
            "Oxygen Saturation*", "Diagnosis*", "Prescription*"
        ]

        for field in required_fields:
            self.create_entry_field(section, title, field)

        self.create_textarea(section, title, "Diagnosis")
        self.create_submit_button(section, title)
        self.create_field_note(section)

    def create_delivery_form(self):
        title = "Normal Spontaneous Delivery Form"
        section = self.create_section_frame(title)

        required_fields = [
            "Patient Name*", "Date of Delivery*", "Time of Delivery*",
            "Delivery Notes*", "Baby Weight (Kg)*", "Apgar Score (0-10)*"
        ]

        for field in required_fields:
            self.create_entry_field(section, title, field)

        self.create_submit_button(section, title)
        self.create_field_note(section)

    def create_section_frame(self, title):
        section = tk.LabelFrame(
            self.scrollable_frame,
            text=title,
            font=("Arial", 14, "bold"),
            bg=self.colors["section_bg"],
            fg=self.colors["text"],
            bd=2,
            relief="groove",
            padx=15,
            pady=15
        )
        section.pack(fill="x", padx=30, pady=15)
        return section

    def create_entry_field(self, parent, section_title, field):
        frame = tk.Frame(parent, bg=self.colors["section_bg"])
        frame.pack(fill="x", pady=5)

        is_required = field.endswith("*")
        label_color = self.colors["danger"] if is_required else self.colors["text"]
        clean_field = field.rstrip("*").strip()

        label = tk.Label(
            frame,
            text=clean_field + (" *" if is_required else ""),
            font=("Arial", 12), fg=label_color,
            bg=self.colors["section_bg"], anchor="w"
        )
        label.pack(fill="x")

        var = tk.StringVar()
        self.form_vars.setdefault(section_title, {})

        # Autocomplete-enabled combobox for patient name
        if clean_field == "Patient Name":
            patient_names = [f"{n[2]} {n[3]} {n[4]}" for n in self.names]
            combobox = AutocompleteCombobox(
                frame,
                textvariable=var,
                completevalues=patient_names,
                values=patient_names,
                font=("Arial", 11)
            )
            combobox.pack(fill="x", ipady=6)

        elif "Date" in clean_field:
            date_entry = DateEntry(
                frame,
                textvariable=var,
                font=("Arial", 11),
                background="darkblue",
                foreground="white",
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                maxdate=datetime.date.today()
            )
            date_entry.pack(fill="x", ipady=6)

        elif "Time" in clean_field:
            hours = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 15, 30, 45)]
            time_combobox = ttk.Combobox(
                frame,
                textvariable=var,
                values=hours,
                font=("Arial", 11),
                state="readonly"
            )
            time_combobox.pack(fill="x", ipady=6)

        else:
            entry = tk.Entry(
                frame,
                textvariable=var,
                font=("Arial", 11),
                bd=0,
                highlightthickness=1,
                highlightbackground="#e0e0e0",
                highlightcolor=self.colors["accent"]
            )
            entry.pack(fill="x", ipady=6)

        self.form_vars[section_title][clean_field] = var

    def create_textarea(self, parent, section_title, field):
        frame = tk.Frame(parent, bg=self.colors["section_bg"])
        frame.pack(fill="x", pady=5)

        label = tk.Label(
            frame,
            text=field + ":",
            font=("Arial", 12),
            bg=self.colors["section_bg"],
            anchor="w"
        )
        label.pack(fill="x")

        text_frame = tk.Frame(frame)
        text_frame.pack(fill="x")

        text_widget = tk.Text(
            text_frame,
            height=4,
            font=("Arial", 11),
            wrap="word",
            bd=0,
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            highlightcolor=self.colors["accent"]
        )
        text_widget.pack(side="left", fill="x", expand=True, ipady=6)

        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scroll.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scroll.set)

        self.form_vars[section_title][field] = text_widget

    def create_submit_button(self, parent, section_title):
        submit_btn = tk.Button(
            parent,
            text="Submit",
            font=("Arial", 12),
            bg=self.colors["accent"],
            fg="white",
            padx=15,
            pady=6,
            command=lambda: self.submit_section(section_title),
            activebackground="#333333",
            activeforeground="white"
        )
        submit_btn.pack(pady=10)

    def create_field_note(self, parent):
        note = tk.Label(
            parent,
            text="* Required fields",
            font=("Arial", 10, "italic"),
            bg=self.colors["section_bg"],
            fg=self.colors["danger"],
            anchor="w"
        )
        note.pack(fill="x", pady=(0, 5), padx=5)

    def validate_field(self, field_name, value):
        patterns = {
            "Blood Pressure": r"^\d{2,3}/\d{2,3}$",
            "Heart Rate": r"^\d{2,3}$",
            "Respiratory Rate": r"^\d{1,2}$",
            "Temperature": r"^\d{2}(\.\d)?$",
            "Oxygen Saturation": r"^\d{2,3}%?$",
            "Baby Weight": r"^\d{1,2}(\.\d{1,2})?$",
            "Apgar Score": r"^\d{1,2}$",
        }
        pattern = patterns.get(field_name)
        if pattern and not re.match(pattern, value):
            return False
        return True

    def submit_section(self, section_name):
        raw_values = self.form_vars[section_name]
        data = []

        for field, var in raw_values.items():
            if isinstance(var, tk.Text):
                value = var.get("1.0", "end-1c").strip()
            else:
                value = var.get().strip()

            if field.endswith("*") and not value:
                messagebox.showerror("Validation Error", f"The field '{field}' is required.")
                return

            clean_field = field.rstrip("*").strip()
            if not self.validate_field(clean_field, value):
                messagebox.showerror("Validation Error", f"Invalid format for '{clean_field}'.")
                return

            data.append(value)

        data.append(self.id)

        # insert patientID from registration
        for names in self.names:
            if data[0] == f"{names[2]} {names[3]} {names[4]}":
                data.insert(0, names[0])

        if section_name == "Check-up Form":
            fnc.database_con().insert(
                "checkup",
                ("patientID", "patientName", "date", "bloodPressure",
                 "heartRate", "respiratoryRate", "temperature",
                 "oxygenSaturation", "diagnosis", "prescription", "staffID"),
                data
            )
        elif section_name == "Normal Spontaneous Delivery Form":
            fnc.database_con().insert(
                "nsd",
                ("patientID", "patientName", "dateofdelivery",
                 "timeofdelivery", "deliveryNote", "Babyweight",
                 "apgarScore", "staffID"),
                data
            )

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


def main(id):
    root = tk.Tk()
    app = MedicalRecordForm(root, id)
    root.mainloop()


if __name__ == "__main__":
    main()
