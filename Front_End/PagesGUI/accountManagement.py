import tkinter as tk
from tkinter import font, ttk
import sys
from datetime import date

# load local modules
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login
from Front_End.FormGUI import registerNewAccount

class AccountManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Birthing Home - Account Management")
        self.root.geometry("1200x700")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)

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

        # Removed all nav items

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

    def logout(self):
        self.root.destroy()
        Login.LoginUI()

    def create_content(self):
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(content_frame)
        self.create_search(content_frame)
        self.create_table(content_frame)

    def register_account(self):
        self.root.destroy()
        registerNewAccount.main()


    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white")
        header_frame.pack(fill=tk.X)

        # Use grid for proper alignment between left and right sides
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        title_label = tk.Label(header_frame, text="Account Management", font=self.title_font, bg="white")
        title_label.grid(row=0, column=0, sticky="w")

        register_btn = tk.Button(
            header_frame,
            text="+ Register New Account",
            font=self.button_font,
            bg="#111111",
            fg="white",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.register_account  # Placeholder for your logic
        )
        register_btn.grid(row=0, column=1, sticky="e")

    def create_search(self, parent):
        search_frame = tk.Frame(parent, bg="white", pady=20)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search: ", bg="white").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, font=self.table_font, width=50, relief=tk.SOLID, bd=1)
        self.search_entry.insert(0, "Search accounts...")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.perform_search)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search accounts...":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search accounts...")

    def create_table(self, parent):
        dir_frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, padx=20, pady=20)
        dir_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(dir_frame, text="Account Directory", font=self.header_font, bg="white").pack(anchor=tk.W)
        tk.Label(dir_frame, text="Manage and view all registered accounts", font=self.small_font,
                 fg="#666666", bg="white").pack(anchor=tk.W, pady=(0, 15))

        table_frame = tk.Frame(dir_frame, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)

        headers = ["Account ID", "Email", "Role", "Status", "Actions"]
        col_widths = [150, 300, 300, 200, 200]

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
        accounts = fnc.database_con().read("accounts", "*")
        accounts.sort(reverse=True)

        for row in accounts:
            account = {
                "ID": row[0],
                "name": row[2],
                "role": row[3],
                "status": row[6],
            }
            self.create_account_row(parent, account, col_widths)

    def create_account_row(self, parent, account, col_widths):
        row_frame = tk.Frame(parent, bg="white")
        row_frame.pack(fill=tk.X, pady=3)

        status_color = {
            "Active": "#4CAF50",
            "Inactive": "#F44336"
        }.get(account["status"], "#9C27B0")

        values = [account["ID"], account["name"], account["role"], account["status"]]
        for i, val in enumerate(values):
            fg = status_color if i == 3 else "black"
            tk.Label(row_frame, text=val, font="Arial 10", bg="white", fg=fg,
                     width=col_widths[i] // 10, anchor="w").pack(side=tk.LEFT)

        actions_frame = tk.Frame(row_frame, bg="white")
        actions_frame.pack(side=tk.LEFT, padx=10)

        tk.Button(actions_frame, text="Edit", font=self.small_font, bg="black", fg="white",
                  bd=0, relief=tk.FLAT, width=4,
                  command=lambda: print(f"Edit account {account['ID']}"))\
.pack(side=tk.LEFT)

    def perform_search(self, event=None):
        query = self.search_entry.get().lower().strip()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        accounts = fnc.database_con().read("accounts", "*")
        accounts.sort(reverse=True)

        for row in accounts:
            account = {
                "ID": row[0],
                "name": row[2],
                "role": row[3],
                "status": row[6],
            }

            if query in str(account["ID"]).lower() or query in account["name"].lower() or query in account["role"].lower():
                self.create_account_row(self.scrollable_frame, account, [150, 300, 300, 200, 200])


def main():
    root = tk.Tk()
    app = AccountManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        Login.main()
