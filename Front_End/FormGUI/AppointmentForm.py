import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from datetime import datetime
from tkcalendar import DateEntry
import sys, os
import re

BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
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
            "accent": "#0d6efd",
            "text": "#222222",
            "light_bg": "#f2f2f2",
            "danger": "#dc3545",
            "section_bg": "#fafafa",
        }

        self.configure_styles()
        self.form_vars = {}
        self.create_widgets()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Section.TFrame", background=self.colors["section_bg"])
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

    def create_widgets(self):
        header = tk.Frame(self.root, bg="black", height=70)
        header.pack(fill="x")
        title = tk.Label(header, text="📅 Appointment Scheduling", font=("Arial", 20, "bold"),
                         bg="black", fg="white")
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

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.bind_scroll()

        self.create_section("👤 Patient Information", {
            "First Name *": "",
            "Last Name *": "",
            "Phone Number *": "",
            "Email": ""  # optional
        })

        self.create_section("🩺 Appointment Details", {
            "Appointment Date *": "",
            "Appointment Time *": "",
            "Appointment Type *": ["Check-up", "Follow-up", "Consultation", "Emergency", "Delivery"],
            "Preferred Provider *": "",
            "Appointment Status *": ["Pending", "Confirmed", "Completed", "Cancelled"],
            "Notes": ""  # optional
        })

        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=20, padx=20)

        submit = tk.Button(btn_frame, text="✅ Schedule Appointment", command=self.submit_data,
                           bg=self.colors["accent"], fg="white", font=("Arial", 13), padx=30, pady=10)
        submit.pack(side="right", padx=10)

        cancel = tk.Button(btn_frame, text="❌ Exit", command=self.back,
                           bg=self.colors["danger"], fg="white", font=("Arial", 13), padx=20, pady=10)
        cancel.pack(side="right", padx=10)

    def bind_scroll(self):
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def create_section(self, title, fields):
        section = tk.LabelFrame(self.scrollable_frame, text=title,
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                font=("Arial", 14, "bold"), bd=1, relief="groove", padx=15, pady=15)
        section.pack(fill="x", pady=15, padx=30)

        for field, options in fields.items():
            frame = tk.Frame(section, bg=self.colors["section_bg"])
            frame.pack(fill="x", pady=8)

            # Label color red if required field
            label_color = "#d60000" if "*" in field else self.colors["text"]

            label = tk.Label(frame, text=field, font=("Arial", 13), fg=label_color,
                            bg=self.colors["section_bg"], anchor="w")
            label.pack(fill="x")

            var = tk.StringVar()
            if "Date" in field:
                entry = DateEntry(frame, textvariable=var, font=("Arial", 12),
                                date_pattern='yyyy-mm-dd')
                entry.pack(fill="x", ipady=6)
            elif "Time" in field:
                time_frame = tk.Frame(frame, bg=self.colors["section_bg"])
                time_frame.pack(fill="x")

                hour_var = tk.StringVar(value="HH")
                minute_var = tk.StringVar(value="MM")
                hours = [f"{h:02}" for h in range(24)]
                minutes = [f"{m:02}" for m in range(0, 60, 5)]

                hour_menu = ttk.Combobox(time_frame, textvariable=hour_var, values=hours,
                                        width=5, state="readonly", font=("Arial", 12))
                minute_menu = ttk.Combobox(time_frame, textvariable=minute_var, values=minutes,
                                        width=5, state="readonly", font=("Arial", 12))

                hour_menu.pack(side="left", padx=(0, 10))
                minute_menu.pack(side="left")

                self.form_vars[field] = (hour_var, minute_var)
            elif isinstance(options, list):  # dropdown
                combo = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", font=("Arial", 12))
                combo.set("Select")
                combo.pack(fill="x", ipady=6)
                self.form_vars[field] = var
            else:
                entry = tk.Entry(frame, textvariable=var, font=("Arial", 12),
                                bd=1, relief="solid", highlightthickness=0)
                entry.pack(fill="x", ipady=6)
                self.form_vars[field] = var


    import re  # Add this at the top if not already present

    def submit_data(self):
        data = []
        for key, var in self.form_vars.items():
            if isinstance(var, tuple):  # time
                hour = var[0].get()
                minute = var[1].get()
                if hour == "HH" or minute == "MM":
                    messagebox.showwarning("Missing Time", f"Please select a valid time for {key}.")
                    return
                data.append(f"{hour}:{minute}")
            else:
                value = var.get().strip()

                # Required field check
                if "*" in key and not value:
                    messagebox.showwarning("Missing Field", f"{key} is required.")
                    return

                # Regex validations
                if key == "Phone Number *":
                    if not re.fullmatch(r"^\d{11}$", value):
                        messagebox.showerror("Invalid Input", "Phone number must be exactly 11 digits.")
                        return

                elif key == "Email" and value:  # Optional but validate if present
                    if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
                        messagebox.showerror("Invalid Input", "Please enter a valid email address.")
                        return

                elif key in ["First Name *", "Last Name *"]:
                    if not re.fullmatch(r"^[A-Za-z\s]+$", value):
                        messagebox.showerror("Invalid Input", f"{key} should only contain letters and spaces.")
                        return

                data.append(value)

        data.append(self.id)
        print("Data submitted:", data)
        fnc.database_con().insert("appointment", ("Fname", "Lname", "phonenum", "email",
                                                "apptDate", "apptTime", "apptType", "provider",
                                                "status", "notes", "staffID"), data)
        self.clear_form()
        messagebox.showinfo("Success", "Appointment scheduled successfully!")


    def clear_form(self):
        for key, var in self.form_vars.items():
            if isinstance(var, tuple):
                var[0].set("HH")
                var[1].set("MM")
            elif isinstance(var, tk.StringVar):
                if "Type" in key:
                    var.set("Select")
                else:
                    var.set("")

    def back(self):
        self.root.destroy()
        Appointment.main(self.id)

def main(id=8):
    root = tk.Tk()
    app = AppointmentForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
