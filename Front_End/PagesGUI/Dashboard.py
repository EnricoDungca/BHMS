import tkinter as tk
from tkinter import ttk
from datetime import date
import sys
from tkinter import messagebox

sys.path.insert(0, '\\BHMS')
# load local module
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
    def __init__(self, id):
        super().__init__()
        self.title("BirthCare Dashboard")
        self.geometry("1000x750")
        self.configure(bg="#f4f5f7")
        # fullscreen
        self.attributes('-fullscreen', True)
        # exit fullscreen and fullscreen
        self.bind('<Escape>', self.exit_fullscreen)
        self.bind('<F11>', self.fullscreen)
        
        self.id = id
        
        print(self.id)
 
        self.setup_styles()
        self.create_topbar()
        self.create_main_content()

    def fullscreen(self, event=None):
        self.attributes('-fullscreen', True)
    
    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        self.geometry("1000x750")
    
    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('default')

        style.configure("Card.TFrame", background="white", borderwidth=0, relief="flat")
        style.configure("CardTitle.TLabel", font=("Helvetica", 11), foreground="#666", background="white")
        style.configure("CardValue.TLabel", font=("Helvetica", 20, "bold"), background="white")

        style.map("Nav.TButton",
                  background=[('active', '#222')],
                  foreground=[('active', 'white')])

    def nav_click(self, item):
        self.destroy()
        if item == "Dashboard":
            main(self.id)
        elif item == "Patients":
            patientRegistration.main(self.id)
        elif item == "Appointments":
            Appointment.main(self.id)
        elif item == "Records":
            medicalRecord.main(self.id)
        elif item == "Billing":
            Billing.main(self.id)
        elif item == "Inventory":
            Inventory.main(self.id)
    
    def logout(self):
        self.destroy()
        Login.LoginUI(mode="user")
    
    def create_topbar(self):
        topbar = tk.Frame(self, bg="#111111", height=60)
        topbar.pack(fill="x")

        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=3)
        topbar.grid_columnconfigure(2, weight=1)

        # Logo
        logo = tk.Label(topbar, text="Birthing Home", font=("Helvetica", 14, "bold"),
                        bg="#111111", fg="white")
        logo.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # Navigation
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

        # Log Out Button
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

    def create_main_content(self):
        content_frame = tk.Frame(self, bg="#f4f5f7")
        content_frame.pack(fill="both", expand=True)
        
        # Header Bar
        header_frame = tk.Frame(content_frame, bg="#f4f5f7")
        header_frame.pack(fill="x", padx=40, pady=20)

        dashboard_label = tk.Label(header_frame, text="Dashboard", font=("Helvetica", 20, "bold"), bg="#f4f5f7")
        dashboard_label.pack(side="left")

        # send email button
        send_email_btn = tk.Button(header_frame, command= self.send_email,text="Send Email", font=("Helvetica", 10), bg="#f4f5f7", fg="#666", cursor="hand2")
        send_email_btn.pack(side="right", padx=5)
        
        # Bed tracking
        send_email_btn = tk.Button(header_frame, command= self.beds,text="Bed Tracking", font=("Helvetica", 10), bg="#f4f5f7", fg="#666", cursor="hand2")
        send_email_btn.pack(side="right", padx=5)
        
        date_label = tk.Label(header_frame, text=date.today().strftime("%B %d, %Y"),
                              font=("Helvetica", 10), bg="#f4f5f7")
        date_label.pack(side="right")

        # Create summary cards
        self.create_summary_cards(content_frame)
        # Create appointments section
        self.create_appointments_section(content_frame)

    def create_summary_cards(self, parent):
        cards_frame = tk.Frame(parent, bg="#f4f5f7")
        cards_frame.pack(pady=30)

        self.create_card(cards_frame, "Total Patients", len(fnc.database_con().read("registration", "*")), 0)
        self.create_card(cards_frame, "Medical Records", len(fnc.database_con().read("nsd", "*"))+len(fnc.database_con().read("checkup", "*")), 1)

    def create_card(self, parent, title, value, column):
        card = ttk.Frame(parent, style="Card.TFrame", width=300, height=100)
        card.grid(row=0, column=column, padx=30)
        card.grid_propagate(False)

        title_label = ttk.Label(card, text=title, style="CardTitle.TLabel")
        title_label.pack(anchor="w", padx=15, pady=(16, 4))

        # Center the number by expanding it over the available space.
        value_label = ttk.Label(card, text=str(value), style="CardValue.TLabel")
        value_label.pack(expand=True, fill="both", padx=15)

    def create_appointments_section(self, parent):
        """
        Creates a scrollable area for appointments with design improvements.
        """
        # Container frame to hold canvas and scrollbar
        container = tk.Frame(parent, bg="#f4f5f7")
        container.pack(pady=10, fill="both", expand=True, padx=40)
        
        # Create Canvas widget
        canvas = tk.Canvas(container, bg="#f4f5f7", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add a vertical scrollbar linked to the canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas that will contain the appointment cards
        scrollable_frame = tk.Frame(canvas, bg="#f4f5f7")
        # Store the window ID so we can adjust its width during a resize
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Update the canvas scrollregion whenever the contents change
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_configure)
        
        # Update the width of the inner frame to match the canvas
        def resize_canvas(event):
            canvas.itemconfig(window_id, width=event.width)
        container.bind("<Configure>", resize_canvas)
        
        # Title for the appointment section
        title = tk.Label(
            scrollable_frame,
            text=f"Today's Appointments - {date.today().strftime('%B %d, %Y')}",
            font=("Helvetica", 14, "bold"),
            bg="#f4f5f7"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        # Loop to create the appointment cards
        for appt in fnc.database_con().read("appointment", "*"):
            # Only display appointments for today or scheduled appointments from another day
            if str(appt[6]) == str(date.today().strftime("%Y-%m-%d")):
                data = {"ID": appt[0], "name": f"{appt[2]} {appt[3]}", "datetime": f"{appt[6]} - {appt[7]}", "type": appt[8], "status": appt[10]}
                self.create_appointment_card(scrollable_frame, data)
        
        # Enable mouse wheel scrolling on Windows and MacOS
        def on_mousewheel(event):
            # For Windows, event.delta is a multiple of 120; for MacOS, it might differ.
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def create_appointment_card(self, parent, appointment):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill="x", padx=10, pady=6, ipady=5)

        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="x", padx=10, pady=5)

        left = tk.Frame(content_frame, bg="white")
        left.pack(side="left", fill="x", expand=True)

        name_label = tk.Label(left, text=appointment["name"], font=("Helvetica", 11, "bold"), bg="white")
        name_label.pack(anchor="w")

        type_label = tk.Label(
            left,
            text=f"{appointment['datetime']} - {appointment['type']} - {appointment['status']}",
            font=("Helvetica", 9),
            bg="white",
            fg="#666"
        )
        type_label.pack(anchor="w")

        right = tk.Frame(content_frame, bg="white")
        right.pack(side="right")

        ttk.Button(right, text="Reschedule", command= lambda: self.reschedule(appointment["ID"])).pack(side="left", padx=5)
        ttk.Button(right, text="Check In", command= lambda: self.check_in(appointment["ID"])).pack(side="left")
    
    def reschedule(self, id):
        self.destroy()
        EdittForm.main(self.id, id, "appointment", "Appointment")
        
    def check_in(self, id):
        try:
            
            for data in fnc.database_con().read("appointment", "*"):
                if data[0] == id:
                    if data[10] == "Completed":
                        messagebox.showerror("Error", "Appointment already checked in!")
                        return
            
            fnc.database_con().Record_edit("appointment", "status", "Completed", "ID", id)
            messagebox.showinfo("Success", "Appointment checked in successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update record.\n{e}")
            return

    def send_email(self):
        self.destroy()
        emailSender.main(self.id)
    
    def beds(self):
        self.destroy()
        bedTracking.main(self.id)
    
def main(id=8):
    app = DashboardApp(id)
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        Login.main()
