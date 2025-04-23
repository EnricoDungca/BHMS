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
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import medicalRecordForm

class MedicalRecordManagementApp:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Birthing Home - Check Up")
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
        self.title_font  = font.Font(family="Arial", size=18, weight="bold")
        self.header_font = font.Font(family="Arial", size=12, weight="bold")
        self.nav_font    = font.Font(family="Arial", size=11)
        self.button_font = font.Font(family="Arial", size=10)
        self.table_font  = font.Font(family="Arial", size=10)
        self.small_font  = font.Font(family="Arial", size=9)

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
            btn = tk.Button(nav_frame, text=item, font=("Helvetica", 10),
                            bg="#111111", fg="white", activebackground="#222222",
                            activeforeground="white", border=0, cursor="hand2",
                            command=lambda i=item: self.nav_click(i))
            btn.pack(side="left", padx=12)

        logout_btn = tk.Button(topbar, text="Log Out", font=("Helvetica", 10),
                               bg="#111111", fg="white", activebackground="#222222",
                               activeforeground="white", border=0, cursor="hand2",
                               command=self.logout)
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
            main(self.id)
        elif item == "Billing":
            Billing.main(self.id)
        elif item == "Inventory":
            Inventory.main(self.id)

    def logout(self):
        self.root.destroy()
        Login.LoginUI()

    def create_content(self):
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(self.content_frame)
        self.create_tab_bar(self.content_frame)

        # Create separate frames for each tab.
        self.medical_frame = tk.Frame(self.content_frame, bg="white")
        self.nsd_frame     = tk.Frame(self.content_frame, bg="white")

        # Build Check Up (formerly Medical Records) tab.
        self.create_search(self.medical_frame, "Search check ups...", search_for="checkup")
        self.create_table(self.medical_frame, title="Check Up Directory",
                          sub_title="Manage and view all check ups", table_type="checkup")

        # Build NSD Records tab.
        self.create_search(self.nsd_frame, "Search NSD records...", search_for="nsd")
        self.create_nsd_table(self.nsd_frame)

        # Show default tab.
        self.show_medical_records()

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Check Up Management", font=self.title_font, bg="white").pack(side=tk.LEFT)
        tk.Button(header_frame, text="+ Add New Record", font=self.button_font,
                  bg="#1a1a1a", fg="white", padx=10, pady=5, relief=tk.FLAT,
                  command=self.add_medical_record).pack(side=tk.RIGHT)

    def add_medical_record(self):
        self.root.destroy()
        medicalRecordForm.main(self.id)

    def create_tab_bar(self, parent):
        self.active_tab = tk.StringVar(value="medical")
        tab_frame = tk.Frame(parent, bg="white")
        tab_frame.pack(fill=tk.X, pady=(10, 0))
        self.tab_buttons = {}
        for tab in ["medical", "nsd"]:
            text = "Check Up" if tab == "medical" else "NSD Records"
            btn = tk.Button(tab_frame, text=text, font=self.header_font,
                            bg="#f0f0f0", fg="black", relief=tk.FLAT, padx=10, pady=5,
                            command=lambda t=tab: self.switch_tab(t))
            btn.pack(side=tk.LEFT, padx=5)
            self.tab_buttons[tab] = btn

    def switch_tab(self, tab):
        self.active_tab.set(tab)
        if tab == "medical":
            self.show_medical_records()
        else:
            self.show_nsd_records()
        for t, btn in self.tab_buttons.items():
            btn.config(bg="#1a1a1a" if t==tab else "#f0f0f0", fg="white" if t==tab else "black")

    def show_medical_records(self):
        self.nsd_frame.pack_forget()
        self.medical_frame.pack(fill=tk.BOTH, expand=True)

    def show_nsd_records(self):
        self.medical_frame.pack_forget()
        self.nsd_frame.pack(fill=tk.BOTH, expand=True)

    def create_search(self, parent, placeholder_text, search_for):
        # Generic search bar creation for both tabs.
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, font=self.table_font, width=50,
                                relief=tk.SOLID, bd=1)
        search_entry.insert(0, placeholder_text)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<FocusIn>", lambda e, entry=search_entry, text=placeholder_text: self.clear_placeholder(e, entry, text))
        search_entry.bind("<FocusOut>", lambda e, entry=search_entry, text=placeholder_text: self.restore_placeholder(e, entry, text))
        # Bind key-release to refresh the table based on search.
        if search_for == "checkup":
            search_entry.bind("<KeyRelease>", lambda e: self.refresh_checkup_table())
            self.search_entry = search_entry  # for check ups
        elif search_for == "nsd":
            search_entry.bind("<KeyRelease>", lambda e: self.refresh_nsd_table())
            self.nsd_search_entry = search_entry  # for NSD

    def clear_placeholder(self, event, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)

    def restore_placeholder(self, event, entry, placeholder_text):
        if entry.get() == "":
            entry.insert(0, placeholder_text)

    def create_table(self, parent, title, sub_title, table_type):
        # Generic table creation for Check Up records.
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(dir_frame, text=title, font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text=sub_title, font=self.small_font, fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))
        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Record ID", "Patient Name", "Condition", "Date", "Doctor", "Actions"]
        col_widths = [150, 350, 350, 350, 350, 150]

        header_row = tk.Frame(table_frame, bg="#f5f5f5")
        header_row.pack(fill=tk.X)
        for i, header in enumerate(headers):
            tk.Label(header_row, text=header, font=self.table_font,
                     bg="#f5f5f5", width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        # Create scrollable container.
        body_frame = tk.Frame(table_frame, bg="white")
        body_frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(body_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Save the container and col_widths for search refresh.
        if table_type == "checkup":
            self.checkup_records_container = scrollable_frame
            self.checkup_col_widths = col_widths
            self.populate_table(scrollable_frame, col_widths)
        # (The NSD table uses its own creation method below.)

    def populate_table(self, parent, col_widths):
        # Retrieve check up records from "medical_records".
        records = fnc.database_con().read("checkup", "*")
        records.sort(reverse=True)
        for row in records:
            record = {
                "ID": row[0],
                "patient_name": row[1],
                "condition": row[2],
                "date": row[3],
                "doctor": row[4],
            }
            self.create_record_row(parent, record, col_widths)

    def create_record_row(self, parent, record, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)
        values = [record["ID"], record["patient_name"], record["condition"], record["date"], record["doctor"]]
        for i, val in enumerate(values):
            tk.Label(row_frame, text=val, font=self.table_font, bg="white",
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)
        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)
        tk.Button(actions_frame, text="View", font=self.small_font,
                  bg="white", fg="black", bd=1, relief=tk.SOLID, padx=10,
                  command=lambda: print(f"View record {record['ID']}")).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="Edit", font=self.small_font,
                  bg="black", fg="white", bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit record {record['ID']}")).pack(side=tk.LEFT)

    def create_nsd_table(self, parent):
        # Build NSD Records table with similar UI to Check Up.
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(dir_frame, text="NSD Record Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text="Manage and view all NSD records", font=self.small_font,
                 fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))
        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        headers = ["NSD ID", "Patient Name", "Delivery Date", "Doctor", "Midwife", "Actions"]
        col_widths = [150, 350, 350, 350, 350, 150]
        header_row = tk.Frame(table_frame, bg="#f5f5f5")
        header_row.pack(fill=tk.X)
        for i, header in enumerate(headers):
            tk.Label(header_row, text=header, font=self.table_font,
                     bg="#f5f5f5", width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)
        body_frame = tk.Frame(table_frame, bg="white")
        body_frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(body_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.nsd_records_container = scrollable_frame
        self.nsd_col_widths = col_widths
        self.populate_nsd_table(scrollable_frame, col_widths)

    def populate_nsd_table(self, parent, col_widths):
        records = fnc.database_con().read("nsd", "*")
        records.sort(reverse=True)
        for row in records:
            record = {
                "ID": row[0],
                "patient_name": row[1],
                "delivery_date": row[2],
                "doctor": row[3],
                "midwife": row[4]
            }
            self.create_nsd_record_row(parent, record, col_widths)

    def create_nsd_record_row(self, parent, record, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)
        values = [record["ID"], record["patient_name"], record["delivery_date"], record["doctor"], record["midwife"]]
        for i, val in enumerate(values):
            tk.Label(row_frame, text=val, font=self.table_font, bg="white",
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)
        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)
        tk.Button(actions_frame, text="View", font=self.small_font,
                  bg="white", fg="black", bd=1, relief=tk.SOLID, padx=10,
                  command=lambda: print(f"View NSD record {record['ID']}")).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="Edit", font=self.small_font,
                  bg="black", fg="white", bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit NSD record {record['ID']}")).pack(side=tk.LEFT)

    def refresh_checkup_table(self):
        # Retrieve the search query, clear the container, and repopulate with filtered Check Up records.
        query = self.search_entry.get().lower().strip()
        for widget in self.checkup_records_container.winfo_children():
            widget.destroy()
        records = fnc.database_con().read("checkup", "*")
        records.sort(reverse=True)
        for row in records:
            record = {
                "ID": row[0],
                "patient_name": row[1],
                "condition": row[2],
                "date": row[3],
                "doctor": row[4],
            }
            # Check if the query exists in any record field.
            record_text = " ".join(str(val).lower() for val in record.values())
            if query in record_text or query in ["", "search check ups..."]:
                self.create_record_row(self.checkup_records_container, record, self.checkup_col_widths)

    def refresh_nsd_table(self):
        # Retrieve the search query, clear the container, and repopulate with filtered NSD records.
        query = self.nsd_search_entry.get().lower().strip()
        for widget in self.nsd_records_container.winfo_children():
            widget.destroy()
        records = fnc.database_con().read("nsd", "*")
        records.sort(reverse=True)
        for row in records:
            record = {
                "ID": row[0],
                "patient_name": row[1],
                "delivery_date": row[2],
                "doctor": row[3],
                "midwife": row[4]
            }
            record_text = " ".join(str(val).lower() for val in record.values())
            if query in record_text or query in ["", "search nsd records..."]:
                self.create_nsd_record_row(self.nsd_records_container, record, self.nsd_col_widths)

def main(id):
    root = tk.Tk()
    app = MedicalRecordManagementApp(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
