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
from Front_End.PagesGUI import Billing
from Front_End.FormGUI import inventoryForm

class InventoryManagementApp:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Birthing Home - Inventory Management")
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
            Billing.main(self.id)
        elif item == "Inventory":
            main(self.id)

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

        tk.Label(header_frame, text="Inventory Management", font=self.title_font, bg="white").pack(side=tk.LEFT)

        tk.Button(header_frame, text="+ Add New Inventory Item", font=self.button_font,
                  bg="#1a1a1a", fg="white", padx=10, pady=5, relief=tk.FLAT,
                  command=self.add_inventory_item).pack(side=tk.RIGHT)

    def add_inventory_item(self):
        self.root.destroy()
        inventoryForm.main()

    def create_search(self, parent):
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=self.table_font, width=50, relief=tk.SOLID, bd=1)
        self.search_entry.insert(0, "Search inventory items...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search inventory items...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search inventory items...")

    def update_search(self, event=None):
        search_term = self.search_entry.get().strip().lower()
        if search_term == "search inventory items...":
            search_term = ""
        self.refresh_table(search_term)

    def create_table(self, parent):
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(dir_frame, text="Inventory Item Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text="Manage and view all inventory items", font=self.small_font,
                 fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))

        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Item ID", "Item Name", "Category", "Quantity", "Price", "Date Added", "Actions"]
        col_widths = [150, 350, 350, 350, 350, 350, 350]

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

        self.scrollable_frame = scrollable_frame
        self.col_widths = col_widths

        self.populate_table(self.scrollable_frame, self.col_widths)

    def refresh_table(self, search_term=""):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.populate_table(self.scrollable_frame, self.col_widths, search_term)

    def populate_table(self, parent, col_widths, search_term=""):
        items = fnc.database_con().read("inventory", "*")
        items.sort(reverse=True)

        filtered_items = [
            row for row in items
            if search_term in str(row[0]).lower()
            or search_term in str(row[1]).lower()
            or search_term in str(row[2]).lower()
        ]

        for row in filtered_items:
            item = {
                "ID": row[0],
                "name": row[1],
                "category": row[2],
                "quantity": row[3],
                "price": row[4],
                "date_added": row[5],
            }
            self.create_inventory_row(parent, item, col_widths)

    def create_inventory_row(self, parent, item, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)

        values = [item["ID"], item["name"], item["category"], item["quantity"],
                  item["price"], item["date_added"]]
        for i, val in enumerate(values):
            tk.Label(row_frame, text=val, font=self.table_font, bg="white",
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(actions_frame, text="View", font=self.small_font, bg="white", fg="black",
                  bd=1, relief=tk.SOLID, padx=10,
                  command=lambda: print(f"View inventory item {item['ID']}"))\
.pack(side=tk.LEFT, padx=5)

        tk.Button(actions_frame, text="Edit", font=self.small_font, bg="black", fg="white",
                  bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit inventory item {item['ID']}"))\
.pack(side=tk.LEFT)

def main(id):
    root = tk.Tk()
    app = InventoryManagementApp(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
