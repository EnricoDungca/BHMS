import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from datetime import datetime
from tkcalendar import DateEntry  # 🔹 Import Date Picker
import sys

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Appointment

class AppointmentForm:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Appointment Scheduling")
        self.root.attributes('-fullscreen', True)

        self.id = id
        
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
            "Patient Information": {},
            "Appointment Details": {}
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
        title = tk.Label(header_frame, text="Appointment Scheduling",
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

        window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def resize_canvas(event):
            canvas_width = event.width
            self.canvas.itemconfig(window_id, width=canvas_width)

        self.canvas.bind("<Configure>", resize_canvas)

        self.bind_scroll_wheel()

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.form_frame = tk.Frame(self.scrollable_frame, bg=self.colors["bg"])
        self.form_frame.pack(fill="both", expand=True)

        self.create_section("Patient Information", ["First Name", "Last Name", "Phone Number", "Email"])
        self.create_section("Appointment Details", [
            "Appointment Date", "Appointment Time", "Appointment Type",
            "Preferred Provider", "Appointment Status", "Notes"
        ])

        button_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_frame.pack(side="bottom", fill="x")

        submit_btn = tk.Button(button_frame, text="Schedule Appointment", font=("Arial", 12),
                               command=self.submit_data, bg=self.colors["accent"],
                               fg="white", padx=20, pady=8, bd=0,
                               activebackground="#333333", activeforeground="white")
        submit_btn.pack(side="right", padx=20)

        exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 12),
                             command= self.back, bg=self.colors["danger"],
                             fg="white", padx=20, pady=8, bd=0,
                             activebackground="#c0392b", activeforeground="white")
        exit_btn.pack(side="right")

    def bind_scroll_wheel(self):
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

    def create_section(self, section_name, fields):
        section = tk.LabelFrame(self.form_frame, text=section_name,
                                bg=self.colors["bg"], fg=self.colors["text"],
                                font=("Arial", 14, "bold"), bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        self.form_vars[section_name] = {}

        for field in fields:
            field_frame = tk.Frame(section, bg=self.colors["bg"])
            field_frame.pack(fill="x", pady=8)

            label = tk.Label(field_frame, text=field + ":", font=("Arial", 12),
                             bg=self.colors["bg"], fg=self.colors["text"], anchor="w")
            label.pack(fill="x")

            var = tk.StringVar()

            if field == "Appointment Type":
                var.set("Select Type")
                options = ["Check-up", "Follow-up", "Consultation", "Emergency", "Delivery"]
                dropdown = ttk.Combobox(field_frame, textvariable=var, values=options,
                                        font=("Arial", 11), state="readonly")
                dropdown.pack(fill="x", ipady=4)

            elif field == "Appointment Status":
                var.set("Select Status")
                statuses = ["Pending", "Confirmed", "Completed", "Cancelled"]
                dropdown = ttk.Combobox(field_frame, textvariable=var, values=statuses,
                                        font=("Arial", 11), state="readonly")
                dropdown.pack(fill="x", ipady=4)

            elif field == "Appointment Date":
                date_entry = DateEntry(field_frame, textvariable=var, font=("Arial", 11),
                                       background="darkblue", foreground="white", borderwidth=2,
                                       date_pattern='yyyy-mm-dd')
                date_entry.pack(fill="x", ipady=4)

            elif field == "Appointment Time":
                time_frame = tk.Frame(field_frame, bg=self.colors["bg"])
                time_frame.pack(fill="x")

                hour_var = tk.StringVar()
                minute_var = tk.StringVar()

                hours = [f"{i:02d}" for i in range(0, 24)]
                minutes = [f"{i:02d}" for i in range(0, 60, 5)]

                hour_menu = ttk.Combobox(time_frame, textvariable=hour_var, values=hours, width=5, state="readonly", font=("Arial", 11))
                hour_menu.set("HH")
                hour_menu.pack(side="left", padx=(0, 5))

                minute_menu = ttk.Combobox(time_frame, textvariable=minute_var, values=minutes, width=5, state="readonly", font=("Arial", 11))
                minute_menu.set("MM")
                minute_menu.pack(side="left")

                self.form_vars[section_name][field] = (hour_var, minute_var)

            else:
                entry = tk.Entry(field_frame, textvariable=var, font=("Arial", 11),
                                 bd=0, highlightthickness=1,
                                 highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
                entry.pack(fill="x", ipady=8)

                self.form_vars[section_name][field] = var

            if field not in ["Appointment Time"]:
                self.form_vars[section_name][field] = var

    def submit_data(self):
        all_data = {}
        empty_fields = []

        for section, fields in self.form_vars.items():
            all_data[section] = {}
            for field, var in fields.items():
                if isinstance(var, tuple):  # For Appointment Time (hour, minute)
                    hour = var[0].get()
                    minute = var[1].get()
                    if hour == "HH" or minute == "MM":
                        empty_fields.append(f"{section} - {field}")
                        all_data[section][field] = ""
                    else:
                        all_data[section][field] = f"{hour}:{minute}"
                else:
                    value = var.get()
                    all_data[section][field] = value
                    if not value or value.startswith("Select"):
                        empty_fields.append(f"{section} - {field}")

        if empty_fields:
            messagebox.showwarning("Missing Information", "Please fill in the following fields:\n• " + "\n• ".join(empty_fields))
            return
        
        values = [value for values in all_data.values() for value in values.values()]
        
        fnc.database_con().insert("appointment", ("Fname", "Lname", "phonenum", "email", "apptDate", "apptTime", "apptType", "provider", "status", "notes"), values)
        
        summary = "\n\n".join(f"{section}:\n" + "\n".join(f"  {k}: {v}" for k, v in fields.items()) for section, fields in all_data.items())
        messagebox.showinfo("Appointment Scheduled", "Your appointment has been scheduled successfully!\n\nSummary:\n" + summary)
        self.clear_form()

    def clear_form(self):
        for section, fields in self.form_vars.items():
            for field, var in fields.items():
                if isinstance(var, tuple):
                    var[0].set("HH")
                    var[1].set("MM")
                elif field in ["Appointment Type", "Appointment Status"]:
                    var.set(f"Select {'Type' if 'Type' in field else 'Status'}")
                else:
                    var.set("")
                    
    def back(self):
        self.root.destroy()
        Appointment.main(self.id)

def main(id):
    root = tk.Tk()
    app = AppointmentForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
