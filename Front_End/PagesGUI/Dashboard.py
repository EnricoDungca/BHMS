import tkinter as tk
from tkinter import font, ttk, messagebox
import sys, os
from datetime import date

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.PagesGUI import patientRegistration
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.FormGUI import emailSender
from Front_End.FormEditUI import EdittForm
from Front_End.PagesGUI import bedTracking

class DashboardApp(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        # Window
        self.title("Birthing Home — Dashboard")
        self.geometry("1200x700")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.exit_fullscreen)
        
        Inventory.InventoryManagementApp.low_stock_alert(self)

        # Fonts
        self.init_fonts()

        # Build UI
        self.create_topbar()
        self.create_main_content()

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        self.geometry("1200x700")

    def init_fonts(self):
        self.title_font  = font.Font(family="Arial", size=22, weight="bold")
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.nav_font    = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12)
        self.small_font  = font.Font(family="Arial", size=11)

    def nav_click(self, item):
        self.destroy()
        if item == "🏠︎Dashboard":
            DashboardApp(self.user_id).mainloop()
        elif item == "🛌Patients":
            patientRegistration.main(self.user_id)
        elif item == "🗓️Appointments":
            Appointment.main(self.user_id)
        elif item == "📋Records":
            medicalRecord.main(self.user_id)
        elif item == "💳Billing":
            Billing.main(self.user_id)
        elif item == "📦Inventory":
            Inventory.main(self.user_id)

    def logout(self):
        self.destroy()
        Login.LoginUI()

    def create_topbar(self):
        topbar = tk.Frame(self, bg="#111111", height=70)
        topbar.pack(fill="x")
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=3)
        topbar.grid_columnconfigure(2, weight=1)

        # Logo
        logo = tk.Label(
            topbar,
            text="Birthing Home",
            font=("Helvetica", 16, "bold"),
            bg="#111111",
            fg="white"
        )
        logo.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Nav buttons
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

        # Log Out
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

    def create_main_content(self):
        content = tk.Frame(self, bg="#f4f5f7")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = tk.Frame(content, bg="#f4f5f7")
        header.pack(fill="x")
        tk.Label(header, text="📊 Dashboard", font=self.title_font, bg="#f4f5f7").pack(side="left")
        
        # Action buttons
        btn_frame = tk.Frame(header, bg="#f4f5f7")
        btn_frame.pack(side="right")
        for label, cmd in [("Bed Tracking", self.open_beds), ("Send Email", self.send_email)]:
            tk.Button(btn_frame, text=label, font=self.button_font,
                      bg="#f4f5f7", fg="#666666", relief="flat",
                      cursor="hand2", command=cmd).pack(side="left", padx=8)

        # Date
        tk.Label(header, text=date.today().strftime("%B %d, %Y"),
                 font=self.small_font, bg="#f4f5f7").pack(side="right", padx=12)

        # Summary cards
        self.create_summary_cards(content)

        # Today's appointments
        self.create_appointments_section(content)

    def create_summary_cards(self, parent):
        frame = tk.Frame(parent, bg="#f4f5f7")
        frame.pack(pady=30)
        total_pats = len(fnc.database_con().read("registration", "*"))
        total_rec  = (len(fnc.database_con().read("checkup", "*"))
                      + len(fnc.database_con().read("nsd", "*")))
        for idx, (title, value) in enumerate([("Total Registered Patients", total_pats), ("Medical Records", total_rec)]):
            card = tk.Frame(frame, bg="white", bd=1, relief="flat", width=300, height=100)
            card.grid(row=0, column=idx, padx=30)
            card.grid_propagate(False)
            tk.Label(card, text=title, font=("Arial",11), fg="#666666", bg="white").pack(anchor="w", pady=(12,4), padx=12)
            tk.Label(card, text=str(value), font=("Arial",20,"bold"), bg="white").pack(expand=True, fill="both", padx=12)

    def create_appointments_section(self, parent):
        container = tk.Frame(parent, bg="#f4f5f7")
        container.pack(fill="both", expand=True, pady=10)
        canvas = tk.Canvas(container, bg="#f4f5f7", highlightthickness=0)
        scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=scroll.set)

        inner = tk.Frame(canvas, bg="#f4f5f7")
        win_id = canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        container.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        tk.Label(inner,
                 text=f"Today's Appointments — {date.today().strftime('%B %d, %Y')}",
                 font=self.header_font, bg="#f4f5f7").pack(anchor="w", pady=(0,12))

        for appt in fnc.database_con().read("appointment", "*"):
            if str(appt[6]) == str(date.today().strftime("%Y-%m-%d")):
                data = {
                    "ID": appt[0],
                    "name": f"{appt[2]} {appt[3]}",
                    "dt": f"{appt[6]} · {appt[7]}",
                    "type": appt[8],
                    "status": appt[10]
                }
                self._add_appointment_card(inner, data)

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def _add_appointment_card(self, parent, appt):
        card = tk.Frame(parent, bg="white", bd=1, relief="flat")
        card.pack(fill="x", padx=10, pady=6)

        body = tk.Frame(card, bg="white")
        body.pack(fill="x", padx=10, pady=6)

        left = tk.Frame(body, bg="white")
        left.pack(side="left", fill="both", expand=True)
        tk.Label(left, text=appt["name"], font=("Arial",11,"bold"), bg="white").pack(anchor="w")
        tk.Label(left,
                 text=f"{appt['dt']} · {appt['type']} · {appt['status']}" ,
                 font=("Arial",9), fg="#666666", bg="white").pack(anchor="w", pady=(2,0))

        right = tk.Frame(body, bg="white")
        right.pack(side="right")
        tk.Button(right, text="Reschedule",
                  command=lambda i=appt["ID"]: self.reschedule(i),
                  bg="Black", fg="white", bd=0, cursor="hand2").pack(side="left", padx=4)
        tk.Button(right, text="Check In",
                  command=lambda i=appt["ID"]: self.check_in(i),
                  bg="Black", fg="white", bd=0, cursor="hand2").pack(side="left")

    def reschedule(self, appt_id):
        self.destroy()
        EdittForm.main(self.user_id, appt_id, "appointment", "Appointment")

    def check_in(self, appt_id):
        try:
            recs = fnc.database_con().read("appointment", "*")
            for r in recs:
                if r[0] == appt_id and r[10] == "Completed":
                    messagebox.showerror("Error", "Already checked in!")
                    return
            fnc.database_con().Record_edit("appointment", "status", "Completed", "ID", appt_id)
            messagebox.showinfo("Success", "Checked in successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_email(self):
        self.destroy()
        emailSender.main(self.user_id)

    def open_beds(self):
        self.destroy()
        bedTracking.main(self.user_id)


def main(user_id):
    app = DashboardApp(user_id)
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        Login.main()
