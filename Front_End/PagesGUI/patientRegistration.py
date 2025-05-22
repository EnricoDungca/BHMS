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
from Front_End.PagesGUI import patientRegistration as PatientPage
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import registerForm
from Front_End.ProfileGUI import patientProfile
from Front_End.FormEditUI import EdittForm

class PatientManagementApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Birthing Home - Patient Management")
        self.root.geometry("1200x700")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)

        self.init_fonts()
        self.create_topbar()
        self.create_content()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def init_fonts(self):
        self.title_font = font.Font(family="Arial", size=22, weight="bold")
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.nav_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12)
        self.table_font = font.Font(family="Arial", weight="bold", size=12)
        self.small_font = font.Font(family="Arial", size=11)

    def create_topbar(self):
        topbar = tk.Frame(self.root, bg="#111111", height=70)
        topbar.pack(fill="x")
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=3)
        topbar.grid_columnconfigure(2, weight=1)

        logo = tk.Label(topbar, text="Birthing Home", font=("Helvetica", 16, "bold"), bg="#111111", fg="white")
        logo.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        nav_frame = tk.Frame(topbar, bg="#111111")
        nav_frame.grid(row=0, column=1)
        nav_items = ["🏠︎Dashboard", "🛌Patients", "🗓️Appointments", "📋Records", "💳Billing", "📦Inventory"]
        for item in nav_items:
            tk.Button(nav_frame, text=item, font=self.nav_font, bg="#111111", fg="white",
                      activebackground="#222222", activeforeground="white", border=0, cursor="hand2",
                      command=lambda i=item: self.nav_click(i)).pack(side="left", padx=16)

        logout_btn = tk.Button(topbar, text="Log Out", font=self.nav_font, bg="#111111", fg="white",
                               activebackground="#222222", activeforeground="white", border=0, cursor="hand2",
                               command=self.logout)
        logout_btn.grid(row=0, column=2, sticky="e", padx=20)

    def nav_click(self, item):
        self.root.destroy()
        if item == "🏠︎Dashboard": Dashboard.main(self.user_id)
        elif item == "🛌Patients": main(self.user_id)
        elif item == "🗓️Appointments": Appointment.main(self.user_id)
        elif item == "📋Records": medicalRecord.main(self.user_id)
        elif item == "💳Billing": Billing.main(self.user_id)
        elif item == "📦Inventory": Inventory.main(self.user_id)

    def logout(self):
        self.root.destroy()
        Login.LoginUI()

    def create_content(self):
        content = tk.Frame(self.root, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.create_header(content)
        self.create_search(content)
        self.create_table(content)

    def create_header(self, parent):
        header = tk.Frame(parent, bg="white")
        header.pack(fill=tk.X)
        tk.Label(header, text="👥 Patient Management", font=self.title_font, bg="white").pack(side=tk.LEFT)
        tk.Button(header, text="+ Register New Patient", font=self.button_font, bg="#1a1a1a", fg="white",
                  padx=10, pady=6, relief=tk.FLAT, command=self.register_patient).pack(side=tk.RIGHT)

    def register_patient(self):
        self.root.destroy()
        registerForm.main(self.user_id)

    def create_search(self, parent):
        search = tk.Frame(parent, bg="white", pady=20)
        search.pack(fill=tk.X)
        tk.Label(search, text="🔍 Search: ", font=self.small_font, bg="white").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search, font=self.table_font, width=50, bd=1, relief=tk.SOLID)
        self.search_entry.insert(0, "Search patients...")
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.perform_search)

    def clear_placeholder(self, e):
        if self.search_entry.get() == "Search patients...": self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, e):
        if self.search_entry.get() == "": self.search_entry.insert(0, "Search patients...")

    def create_table(self, parent):
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="📋 Patient Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(frame, text="Manage and view all registered patients", font=self.small_font,
                 fg="#666", bg="white").pack(anchor=tk.W, pady=(0,15))
        table = tk.Frame(frame, bg="white")
        table.pack(fill=tk.BOTH, expand=True)
        headers = ["Patient ID", "Name", "Phone", "Email", "Last Visit", "Actions"]
        col_w = [100,250,250,250,250,200]
        hdr = tk.Frame(table, bg="#f5f5f5")
        hdr.pack(fill=tk.X)
        for i, h in enumerate(headers):
            tk.Label(hdr, text=h, font=self.table_font, bg="#f5f5f5",
                     width=col_w[i]//10, anchor="w").pack(side=tk.LEFT)
        body = tk.Frame(table, bg="white")
        body.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(body, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0,0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.populate_table(self.list_frame, col_w)

    def populate_table(self, parent, col_w):
        data = fnc.database_con().read("registration", "*")
        data.sort(reverse=True)
        for r in data:
            patient = {
                "ID": r[0],
                "name": f"{r[2]} {r[3]} {r[4]}",
                "phone": r[7],
                "email": r[8],
                "visit": r[1]
            }
            self.add_row(parent, patient, col_w)

    def add_row(self, parent, p, col_w):
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=4)
        vals = [p["ID"], p["name"], p["phone"], p["email"], p["visit"]]
        for i, v in enumerate(vals):
            tk.Label(row, text=v, font=self.table_font, bg="white",
                     width=col_w[i]//10, anchor="w").pack(side=tk.LEFT)
        act = tk.Frame(row, bg="white"); act.pack(side=tk.LEFT, padx=10)
        tk.Button(act, text="View", font=self.small_font, bg="white", bd=1, relief=tk.SOLID,
                  command=lambda id=p["ID"]: self.view(id)).pack(side=tk.LEFT, padx=5)
        tk.Button(act, text="Edit", font=self.small_font, bg="black", fg="white",
                  bd=0, relief=tk.FLAT, width=5,
                  command=lambda id=p["ID"]: self.edit(id)).pack(side=tk.LEFT)

    def perform_search(self, e=None):
        q = self.search_entry.get().lower().strip()
        for w in self.list_frame.winfo_children(): w.destroy()
        data = fnc.database_con().read("registration", "*")
        data.sort(reverse=True)
        for r in data:
            name = f"{r[2]} {r[3]} {r[4]}".lower()
            if q in name or q in str(r[0]):
                patient = {"ID":r[0],"name":name.title(),"phone":r[7],"email":r[8],"visit":r[1]}
                self.add_row(self.list_frame, patient, [100,200,150,200,150,200])

    def view(self, pid):
        self.root.destroy()
        patientProfile.main(pid, self.user_id)

    def edit(self, pid):
        self.root.destroy()
        EdittForm.main(self.user_id, pid, "registration", "patientRegistration")


def main(user_id):
    root = tk.Tk()
    app = PatientManagementApp(root, user_id)
    root.mainloop()

if __name__ == "__main__":
    try:
        main(None)
    except Exception as e:
        print(e)
        Login.main()
