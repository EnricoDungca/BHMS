import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sys
import os

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import patientRegistration
from Front_End.PagesGUI import medicalRecord
from Front_End.PagesGUI import Billing
from Front_End.PagesGUI import Inventory
from Front_End.PagesGUI import Appointment
from Front_End.PagesGUI import accountManagement

class EditForm:
    def __init__(self, root, staffID, tableName, record_id, tabs):
        self.root = root
        self.record_id = record_id
        self.staffID = staffID
        self.tableName = tableName
        self.tabs = tabs

        self.root.title("Edit Record")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#FFFFFF")

        self.db = fnc.database_con()
        self.columns = [col[0] for col in self.db.column_names(self.tableName)]
        self.entry_vars = []

        self.setup_styles()
        self.build_navbar()
        self.build_form()
        self.load_and_populate()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica Neue", 12), background="#FFFFFF", foreground="#333333")
        style.configure("TEntry", font=("Helvetica Neue", 12))
        style.map("TEntry", foreground=[('focus', '#2980B9')])
        style.configure("Accent.TButton",
                        font=("Helvetica Neue", 12, "bold"),
                        background="#2980B9", foreground="#FFFFFF",
                        borderwidth=0, padding=8)
        style.map("Accent.TButton", background=[('active', '#3498DB')])
        style.configure("Navbar.TFrame", background="#000000")
        style.configure("Nav.TLabel", background="#000000", foreground="#FFFFFF", font=("Helvetica Neue", 14, "bold"))
        style.configure("Nav.TButton", background="#000000", foreground="#FFFFFF", borderwidth=0, font=("Helvetica Neue", 12))

    def back(self):
        self.root.destroy()
        if self.tabs == "accountManagement":
            accountManagement.main()
        elif self.tabs == "patientRegistration":
            patientRegistration.main(self.staffID)
        elif self.tabs == "medicalRecord":
            medicalRecord.main(self.staffID)
        elif self.tabs == "Billing":
            Billing.main(self.staffID)
        elif self.tabs == "Inventory":
            Inventory.main(self.staffID)
        elif self.tabs == "Appointment":
            Appointment.main(self.staffID)

    def build_navbar(self):
        nav = ttk.Frame(self.root, style="Navbar.TFrame", height=50)
        nav.pack(fill="x")

        nav.columnconfigure(0, weight=1)
        nav.columnconfigure(1, weight=1)
        nav.columnconfigure(2, weight=1)

        back_btn = ttk.Button(nav, text="← Back", style="Nav.TButton", command=self.back)
        back_btn.grid(row=0, column=0, sticky="w", padx=15, pady=10)

        title = ttk.Label(nav, text="Edit Record", style="Nav.TLabel", anchor="center")
        title.grid(row=0, column=1)

    def build_form(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(canvas, padding=(40, 20))
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.form_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Center the form dynamically when window resizes
        def resize_canvas(event):
            canvas_width = event.width
            form_width = self.scrollable_frame.winfo_reqwidth()
            x = max((canvas_width - form_width) // 2, 0)
            canvas.coords(self.form_window, x, 0)

        canvas.bind("<Configure>", resize_canvas)

        self.form_frame = self.scrollable_frame

    def _combo(self, parent, var, options):
        combobox = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", width=38)
        return combobox
    

    def load_and_populate(self):
        row = next((r for r in self.db.read(self.tableName, "*") if str(r[0]) == str(self.record_id)), None)
        if not row:
            messagebox.showerror("Error", f"Record with ID {self.record_id} not found.")
            self.root.destroy()
            return

        ttk.Label(self.form_frame, text=f"{self.tableName.capitalize()} Records", font=("Helvetica Neue", 18, "bold"), foreground="#2980B9").grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        
        for idx, value in enumerate(row):
            field = self.columns[idx]

            lbl = ttk.Label(self.form_frame, text=f"{field}:")
            lbl.grid(row=idx + 1, column=0, sticky="e", padx=10, pady=6)

            var = tk.StringVar(value=value)

            if field == "paymentStatus":
                options = ["Paid", "Unpaid", "Pending"]
                ent = self._combo(self.form_frame, var, options)

            elif field == "paymentMethod":
                options = ["Cash", "Insurance"]
                ent = self._combo(self.form_frame, var, options)

            elif field == "apptDate":
                ent = DateEntry(self.form_frame, textvariable=var, width=40, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')

            elif field == "apptType":
                options = ["Check-up", "Follow-up", "Consultation", "Emergency", "Delivery"]
                ent = self._combo(self.form_frame, var, options)

            elif field == "status":
                options = ["Pending", "Confirmed", "Completed", "Cancelled"]
                ent = self._combo(self.form_frame, var, options)

            elif field == "totalPrice":
                ent = tk.Entry(self.form_frame, textvariable=var, width=40, state='readonly')
                try:
                    quantity = float(row[self.columns.index("quantity")])
                    price = float(row[self.columns.index("unitPrice")])
                    total = quantity * price
                    var.set(f"{total:.2f}")
                except (ValueError, IndexError, TypeError) as e:
                    var.set("0.00")
                    
            elif field == "accountstatus":
                options = ["Active", "Disabled"]
                ent = self._combo(self.form_frame, var, options)
            elif field == "otpStatus":
                options = ["Active", "Disabled"]
                ent = self._combo(self.form_frame, var, options)
            else:
                ent = ttk.Entry(self.form_frame, textvariable=var, width=40)
        
            
            ent.grid(row=idx + 1, column=1, padx=10, pady=6, sticky="w")

            if field == "ID" or field == "datesave":
                if isinstance(ent, ttk.Entry):  # Avoid disabling composite widgets like time_frame
                    ent.config(state="disabled")

            if field == "password" and value:
                try:
                    decrypted = fnc.Security().decrypt_str(value)
                    var.set(decrypted)
                except Exception:
                    pass

            self.entry_vars.append((field, var))

        btn = ttk.Button(self.form_frame, text="Save Changes", style="Accent.TButton", command=self.submit)
        btn.grid(row=len(row) + 1, column=0, columnspan=2, pady=(30, 20))
        
        btn = ttk.Button(self.form_frame, text="Delete", style="Accent.TButton", command=self.delete)
        btn.grid(row=len(row) + 2, column=0, columnspan=2, pady=(30, 20))
    
    def delete(self):
        fnc.database_con().Record_delete(self.tableName, "ID", self.record_id)
        self.back()

    def submit(self):
        updates = {field: var.get() for field, var in self.entry_vars}

        # Auto-calculate totalPrice for inventory
        if self.tableName.lower() == "inventory":
            try:
                quantity =  float(updates.get("quantity", 0))
                price = float(updates.get("unitPrice", 0))
                total_price = quantity * price
                updates["totalPrice"] = total_price
            except ValueError:
                messagebox.showerror("Input Error", "Quantity and Price must be valid float values.")
                return

        # inventory logs
        if self.tableName.lower() == "inventory":
            Item = self.db.read("inventory", "*")
            for item in Item:
                if item[0] == self.record_id:
                    old_data = {
                        "ID": item[0],
                        "datesave": item[1].isoformat() if hasattr(item[1], "isoformat") else str(item[1]),
                        "name": item[2],
                        "category": item[3],
                        "quantity": item[4],
                        "price": item[5],
                        "totalprice": item[6],
                    }
            fnc.Sys_log("Inventory", f"Old Data: {old_data} \nNew Data: {updates}").write_log()

        try:
            for col, val in updates.items():
                if col == "password" and val:
                    val = fnc.Security().Encrypt_str(val)
                if col not in ["ID", "datesave"]:  # Don't update these
                    self.db.Record_edit(self.tableName, col, val, "ID", self.record_id)

            messagebox.showinfo("Success", "Record updated successfully!")
            self.back()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update record.\n{e}")


def main(staffID, record_id, table_name, tab):
    root = tk.Tk()
    app = EditForm(root, staffID, table_name, record_id, tab)
    root.mainloop()

if __name__ == "__main__":
    sample_staff_id = 8
    sample_record_id = 6
    sample_table_name = "checkup"
    sample_tab = "billing"
    main(sample_staff_id, sample_record_id, sample_table_name, sample_tab)
