import tkinter as tk
from tkinter import font, ttk
import sys
from datetime import date

# load local modules
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import Dashboard
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import registerForm


class PatientManagementApp:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Birthing Home - Patient Management")
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
        self.table_font = font.Font(family="Arial", size=10)
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
            main(self.id)
        elif item == "Appointments":
            Appointment.main(self.id)
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

        tk.Label(header_frame, text="Patient Management", font=self.title_font, bg="white").pack(side=tk.LEFT)

        tk.Button(header_frame, text="+ Register New Patient", font=self.button_font,
                  bg="#1a1a1a", fg="white", padx=10, pady=5, relief=tk.FLAT,
                  command=self.register_patient).pack(side=tk.RIGHT)

    def register_patient(self):
        self.root.destroy()
        registerForm.main(self.id)

    def create_search(self, parent):
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=self.table_font, width=50, relief=tk.SOLID, bd=1)
        self.search_entry.insert(0, "Search patients...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.filter_patients)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search patients...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search patients...")

    def create_table(self, parent):
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(dir_frame, text="Patient Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text="Manage and view all registered patients", font=self.small_font,
                 fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))

        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Patient Name", "Phone Number", "Email", "Last Visit", "Actions"]
        self.col_widths = [200, 200, 200, 200, 200]

        header_row = tk.Frame(table_frame, bg="#f5f5f5")
        header_row.pack(fill=tk.X)
        for i, header in enumerate(headers):
            tk.Label(header_row, text=header, font="arial 10 bold",
                     bg="#f5f5f5", width=self.col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        self.canvas = tk.Canvas(table_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.canvas.yview)
        self.table_body_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=self.table_body_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_body_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.populate_table(self.table_body_frame, self.col_widths)

    def filter_patients(self, event=None):
        search_query = self.search_entry.get().lower()
        if search_query == "search patients...":
            search_query = ""

        self.table_body_frame.destroy()
        self.table_body_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.table_body_frame, anchor="nw")
        self.populate_table(self.table_body_frame, self.col_widths, search_query)

    def populate_table(self, parent, col_widths, search_query=""):
        patients = fnc.database_con().read("registration", "*")
        patients.sort(reverse=True)

        for row in patients:
            name = f"{row[2]} {row[3]}"
            if search_query in name.lower():
                patient = {
                    "ID": row[0],
                    "name": name,
                    "phone": row[6],
                    "email": row[7],
                    "last_visit": row[1],
                }
                self.create_patient_row(parent, patient, col_widths)

    def create_patient_row(self, parent, patient, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)

        values = [patient["name"], patient["phone"], patient["email"], patient["last_visit"]]
        for i, val in enumerate(values):
            fg = "black"
            tk.Label(row_frame, text=val, font=self.table_font, bg="white", fg=fg,
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(actions_frame, text="View", font=self.small_font, bg="white", fg="black",
                  bd=1, relief=tk.SOLID, padx=10,
                  command=lambda: print(f"View patient {patient['ID']}"))\
.pack(side=tk.LEFT, padx=5)

        tk.Button(actions_frame, text="Edit", font=self.small_font, bg="black", fg="white",
                  bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit patient {patient['ID']}"))\
.pack(side=tk.LEFT)

def main(id):
    root = tk.Tk()
    app = PatientManagementApp(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
