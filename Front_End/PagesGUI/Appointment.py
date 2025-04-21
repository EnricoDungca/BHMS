import tkinter as tk
from tkinter import font, ttk
import sys
from datetime import date

# load local modules
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import Dashboard
from Front_End.PagesGUI import patientRegistration
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import AppointmentForm
from Front_End.ProfileGUI import appointmentProfile

class AppointmentManagementApp:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Birthing Home - Appointments")
        self.root.geometry("1200x700")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.id = id
        
        self.init_fonts()
        self.create_topbar()
        self.create_content()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def init_fonts(self):
        self.title_font = font.Font(family="Arial", size=18, weight="bold")
        self.header_font = font.Font(family="Arial", size=12, weight="bold")
        self.nav_font = font.Font(family="Arial", size=11)
        self.button_font = font.Font(family="Arial", size=10)
        self.table_font = font.Font(family="Arial", weight="bold", size=10)
        self.small_font = font.Font(family="Arial", size=9)

    def create_topbar(self):
        topbar = tk.Frame(self.root, bg="#111111", height=60)
        topbar.pack(fill="x")

        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=3)
        topbar.grid_columnconfigure(2, weight=1)

        logo = tk.Label(topbar, text="Birthing Home", font=("Helvetica", 14, "bold"),
                        bg="#111111", fg="white")
        logo.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        nav_frame = tk.Frame(topbar, bg="#111111")
        nav_frame.grid(row=0, column=1)

        nav_items = ["Dashboard", "Patients", "Appointments", "Records", "Billing", "Inventory"]
        for item in nav_items:
            btn = tk.Button(
                nav_frame,
                text=item,
                font=("Helvetica", 10),
                bg="#111111",
                fg="white",
                activebackground="#222222",
                activeforeground="white",
                border=0,
                cursor="hand2",
                command=lambda i=item: self.nav_click(i)
            )
            btn.pack(side="left", padx=12)

        logout_btn = tk.Button(
            topbar,
            text="Log Out",
            font=("Helvetica", 10),
            bg="#111111",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            border=0,
            cursor="hand2",
            command=self.logout
        )
        logout_btn.grid(row=0, column=2, sticky="e", padx=20)

    def nav_click(self, item):
        self.root.destroy()
        if item == "Dashboard":
            Dashboard.main(self.id)
        elif item == "Patients":
            patientRegistration.main(self.id)
        elif item == "Appointments":
            main(self.id)
        elif item == "Records":
            medicalRecord.main(self.id)
        elif item == "Billing":
            Billing.main(self.id)
        elif item == "Inventory":
            Inventory.main(self.id)

    def logout(self):
        self.root.destroy()
        Login.LoginUI()

    def create_content(self):
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(content_frame)
        self.create_search(content_frame)
        self.create_table(content_frame)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="Appointment Management", font=self.title_font, bg="white").pack(side=tk.LEFT)

        tk.Button(header_frame, text="+ Schedule New Appointment", font=self.button_font,
                  bg="#1a1a1a", fg="white", padx=10, pady=5, relief=tk.FLAT,
                  command=self.schedule_appointment).pack(side=tk.RIGHT)

    def schedule_appointment(self):
        self.root.destroy()
        AppointmentForm.main(self.id)

    def create_search(self, parent):
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=self.table_font, width=50, relief=tk.SOLID, bd=1)
        self.search_entry.insert(0, "Search appointments...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.perform_search)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search appointments...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search appointments...")

    def create_table(self, parent):
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(dir_frame, text="Appointment Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text="Manage and view all scheduled appointments", font=self.small_font,
                 fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))

        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Appointment ID", "Patient Name", "Date/Time", "Provider", "Status", "Actions"]
        col_widths = [150, 300, 300, 300, 300, 300, 300]

        header_row = tk.Frame(table_frame, bg="#f5f5f5")
        header_row.pack(fill=tk.X)
        for i, header in enumerate(headers):
            tk.Label(header_row, text=header, font=self.table_font,
                     bg="#f5f5f5", width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        body_frame = tk.Frame(table_frame, bg="white")
        body_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(body_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.populate_table(self.scrollable_frame, col_widths)

    def populate_table(self, parent, col_widths):
        appointments = fnc.database_con().read("appointment", "*")
        appointments.sort(reverse=True)

        for row in appointments:
            appointment = {
                "ID": row[0],
                "patient_name": row[2],
                "datetime": f"{row[6]} - {row[7]}",
                "provider": row[9],
                "status": row[10],
            }
            self.create_appointment_row(parent, appointment, col_widths)

    def create_appointment_row(self, parent, appointment, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)

        status_color = {
            "Scheduled": "#4CAF50",
            "Completed": "#2196F3",
            "Cancelled": "#F44336"
        }.get(appointment["status"], "#9C27B0")

        values = [appointment["ID"], appointment["patient_name"],
                  appointment["datetime"], appointment["provider"], 
                  appointment["status"]]
        for i, val in enumerate(values):
            fg = status_color if i == 5 else "black"
            tk.Label(row_frame, text=val, font="Arial 10", bg="white", fg=fg,
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(actions_frame, text="View", font=self.small_font, bg="white", fg="black",
                  bd=1, relief=tk.SOLID, padx=10,
                  command=lambda: self.viewProfile(appointment["ID"])).pack(side=tk.LEFT, padx=5)

        tk.Button(actions_frame, text="Edit", font=self.small_font, bg="black", fg="white",
                  bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit appointment {appointment['ID']}"))\
.pack(side=tk.LEFT)

    def perform_search(self, event=None):
        query = self.search_entry.get().lower().strip()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        appointments = fnc.database_con().read("appointment", "*")
        appointments.sort(reverse=True)

        for row in appointments:
            appointment = {
                "ID": row[0],
                "patient_name": row[2],
                "datetime": f"{row[6]} - {row[7]}",
                "provider": row[9],
                "status": row[10],
            }

            if query in str(appointment["ID"]).lower() or query in appointment["patient_name"].lower():
                self.create_appointment_row(self.scrollable_frame, appointment, [150, 300, 300, 300, 300, 300])

    def viewProfile(self, ID):
        self.root.destroy()
        appointmentProfile.show_profile(ID)

def main(id):
    root = tk.Tk()
    app = AppointmentManagementApp(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()