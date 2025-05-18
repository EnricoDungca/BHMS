import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys, os
import re  # Regex module

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Inventory

class InventoryForm:
    def __init__(self, root, staff_id):
        self.root = root
        self.root.title("Inventory Form")
        self.root.attributes('-fullscreen', True)

        self.staff_id = staff_id

        self.colors = {
            "bg": "#f0f2f5",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#ffffff",
            "danger": "#e74c3c",
            "section_bg": "#ffffff",
            "required": "#e74c3c"
        }

        self.required_fields = ["Item or Service Name", "Category", "Quantity", "Unit Price"]
        self.optional_fields = ["Total Price"]

        self.configure_styles()
        self.form_vars = {}
        self.qty_var = self.price_var = self.total_var = None
        self.total_entry = None
        self.create_widgets()

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

    def create_widgets(self):
        header = tk.Frame(self.root, bg=self.colors["accent"], height=90)
        header.pack(fill="x")
        tk.Label(header, text="Inventory Form",
                 font=Font(family="Arial", size=22, weight="bold"),
                 bg=self.colors["accent"], fg="white").pack(pady=25)

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

        button_bar = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_bar.pack(side="bottom", fill="x")

        tk.Button(button_bar, text="➕ Add Item", font=("Arial", 14),
                  command=self.submit_data, bg=self.colors["accent"],
                  fg="white", padx=20, pady=10, bd=0).pack(side="right", padx=20)

        tk.Button(button_bar, text="❌ Exit", font=("Arial", 14),
                  command=self.back, bg=self.colors["danger"],
                  fg="white", padx=20, pady=10, bd=0).pack(side="right")

    def create_inventory_section(self):
        fields = self.required_fields + self.optional_fields

        section = tk.LabelFrame(self.scrollable_frame, text="Inventory Information",
                                bg=self.colors["section_bg"], fg=self.colors["text"],
                                font=("Arial", 16, "bold"), bd=2, relief="groove",
                                padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        for field in fields:
            row = tk.Frame(section, bg=self.colors["section_bg"])
            row.pack(fill="x", pady=10)

            label_fg = self.colors["required"] if field in self.required_fields else self.colors["text"]
            suffix = " *" if field in self.required_fields else ""

            tk.Label(row, text=f"{field}:{suffix}", font=("Arial", 14),
                     bg=self.colors["section_bg"], fg=label_fg, anchor="w"
                     ).pack(fill="x")

            var = tk.StringVar()
            self.form_vars[field] = var

            entry_state = "normal"
            if field == "Total Price":
                entry_state = "disabled"

            e = tk.Entry(row, textvariable=var, font=("Arial", 13),
                         bd=0, highlightthickness=1,
                         highlightbackground="#e0e0e0",
                         highlightcolor=self.colors["accent"],
                         state=entry_state)
            e.pack(fill="x", ipady=10)

            if field == "Quantity":
                self.qty_var = var
            elif field == "Unit Price":
                self.price_var = var
            elif field == "Total Price":
                self.total_var = var
                self.total_entry = e

        self.qty_var.trace_add("write", self.update_total)
        self.price_var.trace_add("write", self.update_total)

    def update_total(self, *args):
        def safe_float(txt):
            try:
                return float(txt)
            except ValueError:
                return 0.0

        qty = safe_float(self.qty_var.get())
        price = safe_float(self.price_var.get())
        total = qty * price

        self.total_entry.config(state="normal")
        self.total_var.set(total)
        self.total_entry.config(state="disabled")

    def validate_inputs(self, data):
        errors = []

        if not re.fullmatch(r"[A-Za-z0-9\s\-]+", data["Item or Service Name"]):
            errors.append("Item Name should only contain letters, numbers, spaces, or hyphens.")

        if not re.fullmatch(r"[A-Za-z0-9\s\-]+", data["Category"]):
            errors.append("Category should only contain letters, numbers, spaces, or hyphens.")

        if not re.fullmatch(r"\d+", data["Quantity"]):
            errors.append("Quantity should be a whole number.")

        if not re.fullmatch(r"\d+(\.\d{1,2})?", data["Unit Price"]):
            errors.append("Unit Price should be a valid number (e.g., 10 or 10.50).")

        return errors

    def submit_data(self):
        data = {f: v.get() for f, v in self.form_vars.items()}
        empty = [f for f in self.required_fields if not data[f]]

        if empty:
            messagebox.showwarning("Missing Information",
                                   "Please fill in the following required fields:\n• " +
                                   "\n• ".join(empty))
            return

        errors = self.validate_inputs(data)
        if errors:
            messagebox.showerror("Invalid Input", "\n".join(errors))
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
        self.update_total()

    def back(self):
        self.root.destroy()
        Inventory.main(self.staff_id)

def main(id):
    root = tk.Tk()
    InventoryForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main(1)
