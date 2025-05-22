import tkinter as tk
from tkinter import font, ttk
import sys, os
from datetime import date

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import Dashboard
from Front_End.PagesGUI import patientRegistration
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import medicalRecordForm
from Front_End.FormEditUI import EdittForm
from Front_End.ProfileGUI import medicalProfile

class MedicalRecordManagementApp:
    def __init__(self, root, user_id):
        self.root    = root
        self.user_id = user_id

        self.root.title("Birthing Home — Check Up Management")
        self.root.geometry("1200x700")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)

        self.init_fonts()
        self.create_topbar()
        self.create_content()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def init_fonts(self):
        # Match Inventory GUI styling
        self.title_font  = font.Font(family="Arial", size=22, weight="bold")
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.nav_font    = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12)
        self.table_font  = font.Font(family="Arial", weight="bold", size=12)
        self.small_font  = font.Font(family="Arial", size=11)

    def create_topbar(self):
        topbar = tk.Frame(self.root, bg="#111111", height=70)
        topbar.pack(fill="x")
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=3)
        topbar.grid_columnconfigure(2, weight=1)

        logo = tk.Label(
            topbar,
            text="Birthing Home",
            font=("Helvetica", 16, "bold"),
            bg="#111111",
            fg="white"
        )
        logo.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        nav_frame = tk.Frame(topbar, bg="#111111")
        nav_frame.grid(row=0, column=1)
        nav_items = ["🏠︎Dashboard", "🛌Patients", "🗓️Appointments", "📋Records", "💳Billing", "📦Inventory"]
        for item in nav_items:
            btn = tk.Button(
                nav_frame,
                text=item,
                font=self.nav_font,
                bg="#111111",
                fg="white",
                activebackground="#222222",
                activeforeground="white",
                border=0,
                cursor="hand2",
                command=lambda i=item: self.nav_click(i)
            )
            btn.pack(side="left", padx=16)

        logout_btn = tk.Button(
            topbar,
            text="Log Out",
            font=self.nav_font,
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
        if item == "🏠︎Dashboard":
            Dashboard.main(self.user_id)
        elif item == "🛌Patients":
            patientRegistration.main(self.user_id)
        elif item == "🗓️Appointments":
            Appointment.main(self.user_id)
        elif item == "📋Records":
            main(self.user_id)
        elif item == "💳Billing":
            Billing.main(self.user_id)
        elif item == "📦Inventory":
            Inventory.main(self.user_id)

    def logout(self):
        self.root.destroy()
        Login.LoginUI()

    def create_content(self):
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(self.content_frame)
        self.create_tab_bar(self.content_frame)

        # two sub‑frames: one for Check‑Up, one for NSD
        self.medical_frame = tk.Frame(self.content_frame, bg="white")
        self.nsd_frame     = tk.Frame(self.content_frame, bg="white")

        # Populate Check‑Up tab
        self.create_search(self.medical_frame, "Search check ups…", search_for="checkup")
        self.create_table(
            self.medical_frame,
            title="📋 Check Up Directory",
            sub_title="Manage and view all check ups",
            table_type="checkup"
        )

        # Populate NSD tab
        self.create_search(self.nsd_frame, "Search NSD records…", search_for="nsd")
        self.create_nsd_table(self.nsd_frame)

        # Show default
        self.show_medical_records()

    def create_header(self, parent):
        header = tk.Frame(parent, bg="white")
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="🩺 Medical Records",
            font=self.title_font,
            bg="white"
        ).pack(side=tk.LEFT)
        tk.Button(
            header,
            text="+ Add New Record",
            font=self.button_font,
            bg="#1a1a1a",
            fg="white",
            padx=10,
            pady=6,
            relief=tk.FLAT,
            command=self.add_medical_record
        ).pack(side=tk.RIGHT)

    def add_medical_record(self):
        self.root.destroy()
        medicalRecordForm.main(self.user_id)

    def create_tab_bar(self, parent):
        self.active_tab = tk.StringVar(value="medical")
        tab_frame = tk.Frame(parent, bg="white")
        tab_frame.pack(fill=tk.X, pady=(10, 0))

        self.tab_buttons = {}
        for tab in ("medical", "nsd"):
            label = "Check Up" if tab == "medical" else "NSD Records"
            btn = tk.Button(
                tab_frame,
                text=label,
                font=self.header_font,
                bg="#f0f0f0",
                fg="black",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                command=lambda t=tab: self.switch_tab(t)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.tab_buttons[tab] = btn

    def switch_tab(self, tab):
        self.active_tab.set(tab)
        if tab == "medical":
            self.show_medical_records()
        else:
            self.show_nsd_records()

        for key, btn in self.tab_buttons.items():
            if key == tab:
                btn.config(bg="#111111", fg="white")
            else:
                btn.config(bg="#f0f0f0", fg="black")

    def show_medical_records(self):
        self.nsd_frame.pack_forget()
        self.medical_frame.pack(fill=tk.BOTH, expand=True)

    def show_nsd_records(self):
        self.medical_frame.pack_forget()
        self.nsd_frame.pack(fill=tk.BOTH, expand=True)

    def create_search(self, parent, placeholder, search_for):
        search = tk.Frame(parent, bg="white", pady=20)
        search.pack(fill=tk.X)
        tk.Label(
            search,
            text="🔍 Search:",
            font=self.small_font,
            bg="white"
        ).pack(side=tk.LEFT)

        entry = tk.Entry(
            search,
            font=self.table_font,
            width=50,
            bd=1,
            relief=tk.SOLID
        )
        entry.insert(0, placeholder)
        entry.pack(side=tk.LEFT, padx=10)

        # placeholder logic
        entry.bind(
            "<FocusIn>",
            lambda e, ent=entry, ph=placeholder: ent.delete(0, tk.END)
            if ent.get() == ph else None
        )
        entry.bind(
            "<FocusOut>",
            lambda e, ent=entry, ph=placeholder: ent.insert(0, ph)
            if ent.get().strip() == "" else None
        )

        # key release → refresh
        if search_for == "checkup":
            entry.bind("<KeyRelease>", lambda e: self.refresh_checkup_table())
            self.search_entry = entry
        else:
            entry.bind("<KeyRelease>", lambda e: self.refresh_nsd_table())
            self.nsd_search_entry = entry

    def create_table(self, parent, title, sub_title, table_type):
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text=title, font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(
            frame,
            text=sub_title,
            font=self.small_font,
            fg="#666666",
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 15))

        tbl_wrap = tk.Frame(frame, bg="white")
        tbl_wrap.pack(fill=tk.BOTH, expand=True)

        headers = ["Record ID", "Patient Name", "Condition", "Date", "Doctor", "Actions"]
        widths  = [100, 250, 250, 250, 250, 150]

        hdr = tk.Frame(tbl_wrap, bg="#f5f5f5")
        hdr.pack(fill=tk.X)
        for i, text in enumerate(headers):
            tk.Label(
                hdr,
                text=text,
                font=self.table_font,
                bg="#f5f5f5",
                width=widths[i] // 10,
                anchor="w"
            ).pack(side=tk.LEFT)

        body = tk.Frame(tbl_wrap, bg="white")
        body.pack(fill=tk.BOTH, expand=True)

        canvas    = tk.Canvas(body, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        self.checkup_records_container = tk.Frame(canvas, bg="white")

        canvas.create_window((0, 0), window=self.checkup_records_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.checkup_col_widths = widths

        self.checkup_records_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.populate_table(self.checkup_records_container, widths)

    def populate_table(self, parent, col_w):
        records = fnc.database_con().read("checkup", "*")
        account = fnc.database_con().read("accounts", "*")
        records.sort(reverse=True)
        for r in records:
            for a in account:
                if r[12] == a[0]:
                    name = a[2]
            rec = {
                "ID":           r[0],
                "patient_name": r[3],
                "condition":    r[10],
                "date":         r[1],
                "provider":     f"{name}"
            }
            self._add_checkup_row(parent, rec, col_w)

    def _add_checkup_row(self, parent, rec, col_w):
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=3)

        for i, field in enumerate(
            [rec["ID"], rec["patient_name"], rec["condition"], rec["date"], rec["provider"]]
        ):
            tk.Label(
                row,
                text=field,
                font=self.table_font,
                bg="white",
                width=col_w[i] // 10,
                anchor="w"
            ).pack(side=tk.LEFT)

        actions = tk.Frame(row, bg="white")
        actions.pack(side=tk.LEFT, padx=10)
        tk.Button(
            actions,
            text="View",
            font=self.small_font,
            bg="white",
            fg="black",
            bd=1,
            relief=tk.SOLID,
            command=lambda id=rec["ID"]: self.view_checkup(id)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            actions,
            text="Edit",
            font=self.small_font,
            bg="black",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            command=lambda id=rec["ID"]: self.edit_checkup(id)
        ).pack(side=tk.LEFT)

    def view_checkup(self, record_id):
        self.root.destroy()
        medicalProfile.main(record_id, self.user_id, "checkup")

    def edit_checkup(self, record_id):
        self.root.destroy()
        EdittForm.main(self.user_id, record_id, "checkup", "medicalRecord")

    def create_nsd_table(self, parent):
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="NSD Record Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(
            frame,
            text="Manage and view all NSD records",
            font=self.small_font,
            fg="#666666",
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 15))

        tbl_wrap = tk.Frame(frame, bg="white")
        tbl_wrap.pack(fill=tk.BOTH, expand=True)

        headers = ["NSD ID", "Patient Name", "Delivery Date", "Time of Birth", "Midwife", "Actions"]
        widths  = [100, 250, 250, 250, 250, 150]

        hdr = tk.Frame(tbl_wrap, bg="#f5f5f5")
        hdr.pack(fill=tk.X)
        for i, text in enumerate(headers):
            tk.Label(
                hdr,
                text=text,
                font=self.table_font,
                bg="#f5f5f5",
                width=widths[i] // 10,
                anchor="w"
            ).pack(side=tk.LEFT)

        body = tk.Frame(tbl_wrap, bg="white")
        body.pack(fill=tk.BOTH, expand=True)

        canvas    = tk.Canvas(body, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        self.nsd_records_container = tk.Frame(canvas, bg="white")

        canvas.create_window((0, 0), window=self.nsd_records_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.nsd_records_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.nsd_col_widths = widths
        self.populate_nsd_table(self.nsd_records_container, widths)

    def populate_nsd_table(self, parent, col_w):
        records = fnc.database_con().read("nsd", "*")
        account = fnc.database_con().read("accounts", "*")
        records.sort(reverse=True)
        for r in records:
            for a in account:
                if a[0] == r[9]:
                    name = a[2]
            rec = {
                "ID":            r[0],
                "patient_name":  r[3],
                "delivery_date": r[4],
                "time":          r[5],
                "midwife":       f"{name}"
            }
            self._add_nsd_row(parent, rec, col_w)

    def _add_nsd_row(self, parent, rec, col_w):
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=3)

        for i, field in enumerate(
            [rec["ID"], rec["patient_name"], rec["delivery_date"], rec["time"], rec["midwife"]]
        ):
            tk.Label(
                row,
                text=field,
                font=self.table_font,
                bg="white",
                width=col_w[i] // 10,
                anchor="w"
            ).pack(side=tk.LEFT)

        actions = tk.Frame(row, bg="white")
        actions.pack(side=tk.LEFT, padx=10)
        tk.Button(
            actions,
            text="View",
            font=self.small_font,
            bg="white",
            fg="black",
            bd=1,
            relief=tk.SOLID,
            command=lambda id=rec["ID"]: self.view_nsd(id)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            actions,
            text="Edit",
            font=self.small_font,
            bg="black",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            command=lambda id=rec["ID"]: self.edit_nsd(id)
        ).pack(side=tk.LEFT)

    def view_nsd(self, record_id):
        self.root.destroy()
        medicalProfile.main(record_id, self.user_id, "nsd")

    def edit_nsd(self, record_id):
        self.root.destroy()
        EdittForm.main(self.user_id, record_id, "nsd", "medicalRecord")

    def refresh_checkup_table(self):
        q = self.search_entry.get().lower().strip()
        if q == "search check ups…": 
            q = ""
        for w in self.checkup_records_container.winfo_children():
            w.destroy()
        records = fnc.database_con().read("checkup", "*")
        records.sort(reverse=True)
        for r in records:
            flat = " ".join(str(x).lower() for x in (r[3], r[10], r[1], r[12]))
            if q in flat:
                rec = {
                    "ID":           r[0],
                    "patient_name": r[3],
                    "condition":    r[10],
                    "date":         r[1],
                    "provider":     f"ID: {r[12]}"
                }
                self._add_checkup_row(self.checkup_records_container, rec, self.checkup_col_widths)

    def refresh_nsd_table(self):
        q = self.nsd_search_entry.get().lower().strip()
        if q == "search nsd records…":
            q = ""
        for w in self.nsd_records_container.winfo_children():
            w.destroy()
        records = fnc.database_con().read("nsd", "*")
        records.sort(reverse=True)
        for r in records:
            flat = " ".join(str(x).lower() for x in (r[3], r[4], r[5], r[9]))
            if q in flat:
                rec = {
                    "ID":            r[0],
                    "patient_name":  r[3],
                    "delivery_date": r[4],
                    "time":          r[5],
                    "midwife":       f"ID: {r[9]}"
                }
                self._add_nsd_row(self.nsd_records_container, rec, self.nsd_col_widths)

def main(user_id=8):
    root = tk.Tk()
    app  = MedicalRecordManagementApp(root, user_id)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        Login.main()
