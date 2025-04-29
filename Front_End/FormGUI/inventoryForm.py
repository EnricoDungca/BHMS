import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Inventory


class InventoryForm:
    def __init__(self, root, staff_id):
        self.root = root
        self.root.title("Inventory Form")
        self.root.attributes('-fullscreen', True)

        self.staff_id = staff_id

        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }

        self.configure_styles()
        self.form_vars: dict[str, tk.StringVar] = {}
        self.qty_var = self.price_var = self.total_var = None    # will hold StringVars
        self.total_entry = None                                   # will hold the Entry widget
        self.create_widgets()

    # ──────────────────────────  STYLES ──────────────────────────
    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Section.TFrame", background=self.colors["section_bg"])
        style.configure("TScrollbar",
                        background=self.colors["bg"],
                        troughcolor=self.colors["light_bg"],
                        arrowcolor=self.colors["text"])

    # ──────────────────────────  WIDGETS ──────────────────────────
    def create_widgets(self):
        # header
        header = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header.pack(fill="x")
        tk.Label(header, text="Inventory Form",
                 font=Font(family="Arial", size=18, weight="bold"),
                 bg=self.colors["accent"], fg="white").pack(pady=15)

        # scrollable body
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        cid = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cid, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.scrollable_frame = scrollable
        self.create_inventory_section()

        # footer buttons
        button_bar = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_bar.pack(side="bottom", fill="x")

        tk.Button(button_bar, text="Add Item", font=("Arial", 12),
                  command=self.submit_data, bg=self.colors["accent"],
                  fg="white", padx=20, pady=8, bd=0).pack(side="right", padx=20)

        tk.Button(button_bar, text="Exit", font=("Arial", 12),
                  command=self.back, bg=self.colors["danger"],
                  fg="white", padx=20, pady=8, bd=0).pack(side="right")

    # ──────────────────  INVENTORY FORM SECTION ──────────────────
    def create_inventory_section(self):
        fields = ["Item Name", "Category", "Quantity", "Unit Price", "Total Price"]

        section = tk.LabelFrame(self.scrollable_frame, text="Inventory Information",
                                bg=self.colors["bg"], fg=self.colors["text"],
                                font=("Arial", 14, "bold"), bd=2, relief="groove",
                                padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        for field in fields:
            row = tk.Frame(section, bg=self.colors["bg"])
            row.pack(fill="x", pady=8)

            tk.Label(row, text=f"{field}:", font=("Arial", 12),
                     bg=self.colors["bg"], fg=self.colors["text"], anchor="w"
                     ).pack(fill="x")

            var = tk.StringVar()
            self.form_vars[field] = var

            entry_state = "normal"
            if field == "Total Price":
                entry_state = "disabled"    # user can’t type here

            e = tk.Entry(row, textvariable=var, font=("Arial", 11),
                         bd=0, highlightthickness=1,
                         highlightbackground="#e0e0e0",
                         highlightcolor=self.colors["accent"],
                         state=entry_state)
            e.pack(fill="x", ipady=8)

            # keep references for live calculation
            if field == "Quantity":
                self.qty_var = var
            elif field == "Unit Price":
                self.price_var = var
            elif field == "Total Price":
                self.total_var = var
                self.total_entry = e

        # call self.update_total whenever Quantity or Unit Price changes
        self.qty_var.trace_add("write", self.update_total)
        self.price_var.trace_add("write", self.update_total)

    # ────────────────────  LIVE TOTAL UPDATE ────────────────────
    def update_total(self, *args):
        """Compute quantity × unit price and display in Total Price."""
        def safe_float(txt):
            try:
                return float(txt)
            except ValueError:
                return 0.0

        qty = safe_float(self.qty_var.get())
        price = safe_float(self.price_var.get())
        total = qty * price

        # temporarily enable, write, then disable again
        self.total_entry.config(state="normal")
        self.total_var.set(total)
        self.total_entry.config(state="disabled")

    # ─────────────────────  BUTTON HANDLERS ─────────────────────
    def submit_data(self):
        data = {f: v.get() for f, v in self.form_vars.items()}
        empty = [f for f, v in data.items() if not v]

        if empty:
            messagebox.showwarning("Missing Information",
                                   "Please fill in the following fields:\n• "
                                   + "\n• ".join(empty))
            return

        fnc.database_con().insert(
            "inventory",
            ("item", "category", "quantity", "unitPrice", "totalPrice", "staffID"),
            [*data.values(), self.staff_id]
        )
        self.clear_form()

    def clear_form(self):
        for var in self.form_vars.values():
            var.set("")
        # ensure total resets to 0.00
        self.update_total()

    def back(self):
        self.root.destroy()
        Inventory.main(self.staff_id)


# ────────────────────────────  MAIN ────────────────────────────
def main(id):
    root = tk.Tk()
    InventoryForm(root, id)
    root.mainloop()


if __name__ == "__main__":
    main()
