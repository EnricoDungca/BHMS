import tkinter as tk
from tkinter import font, ttk
import sys
from datetime import date

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import Dashboard
from Front_End.PagesGUI import patientRegistration
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import billingForm

class BillingManagementApp:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Birthing Home - Billing Management")
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
            patientRegistration.main(self.id)
        elif item == "Appointments":
            Appointment.main(self.id)
        elif item == "Records":
            medicalRecord.main(self.id)
        elif item == "Billing":
            main(self.id)
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

        tk.Label(header_frame, text="Billing Management", font=self.title_font, bg="white").pack(side=tk.LEFT)

        tk.Button(header_frame, text="+ Add New Billing", font=self.button_font,
                  bg="#1a1a1a", fg="white", padx=10, pady=5, relief=tk.FLAT,
                  command=self.add_billing).pack(side=tk.RIGHT)

    def add_billing(self):
        self.root.destroy()
        billingForm.main()

    def create_search(self, parent):
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=self.table_font, width=50, relief=tk.SOLID, bd=1)
        self.search_entry.insert(0, "Search billing records...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search billing records...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search billing records...")

    def create_table(self, parent):
        self.dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        self.dir_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.dir_frame, text="Billing Record Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(self.dir_frame, text="Manage and view all billing records", font=self.small_font,
                fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))

        self.table_frame = tk.Frame(self.dir_frame, bg="white")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.headers = ["Billing ID", "Patient Name", "Total Amount", "Status", "Balance", "Date", "Actions"]
        self.col_widths = [150, 350, 350, 350, 350, 350, 350]

        self.draw_table()

    def draw_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        header_row = tk.Frame(self.table_frame, bg="#f5f5f5")
        header_row.pack(fill=tk.X)
        for i, header in enumerate(self.headers):
            tk.Label(header_row, text=header, font=self.table_font,
                     bg="#f5f5f5", width=self.col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        self.body_frame = tk.Frame(self.table_frame, bg="white")
        self.body_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.body_frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.body_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.update_search()

    def update_search(self, event=None):
        query = self.search_entry.get().lower()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        records = fnc.database_con().read("billing", "*")
        records.sort(reverse=True)

        for row in records:
            record = {
                "ID": row[0],
                "patient_name": row[1],
                "total_amount": row[2],
                "amount_paid": row[3],
                "balance": row[4],
                "date": row[5],
            }
            if query in str(record["ID"]).lower() or query in record["patient_name"].lower():
                self.create_billing_row(self.scrollable_frame, record, self.col_widths)

    def create_billing_row(self, parent, record, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)

        values = [record["ID"], record["patient_name"], record["total_amount"],
                record["amount_paid"], record["balance"], record["date"]]
        for i, val in enumerate(values):
            tk.Label(row_frame, text=val, font=self.table_font, bg="white",
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(actions_frame, text="View", font=self.small_font, bg="white", fg="black",
                bd=1, relief=tk.SOLID, padx=10,
                command=lambda: print(f"View billing {record['ID']}"))\
.pack(side=tk.LEFT, padx=5)

        tk.Button(actions_frame, text="Edit", font=self.small_font, bg="black", fg="white",
                bd=0, relief=tk.FLAT, width=4,
                command=lambda: print(f"Edit billing {record['ID']}"))\
.pack(side=tk.LEFT)

def main(id):
    root = tk.Tk()
    app = BillingManagementApp(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()