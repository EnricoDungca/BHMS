import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter.font import Font

# ─── project imports ──────────────────────────────────────────
PROJECT_ROOT = Path(r"\BHMS").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Back_End import systemfnc as fnc  # type: ignore
from Front_End.PagesGUI import Billing  # type: ignore

__all__ = ["BillingForm", "main"]


class BillingForm:
    """Full‑screen window that captures a billing record."""

    # ──────────────────────── init ────────────────────────
    def __init__(self, root: tk.Tk, staff_id: int) -> None:
        self.root = root
        self.staff_id = staff_id

        self._init_window()
        self._load_db()

        self.item_rows: list[tuple[str, int, float, float]] = []
        self.form_vars: dict[str, tk.StringVar] = {}
        self.combos: dict[str, ttk.Combobox] = {}

        self._build_header()
        self._build_body()
        self._build_footer()

    # ───────────────── helpers ─────────────────
    def _init_window(self) -> None:
        self.root.title("Billing Form")
        self.root.attributes("-fullscreen", True)
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9",
        }
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Section.TFrame", background=self.colors["section_bg"])
        style.configure(
            "TScrollbar",
            background=self.colors["bg"],
            troughcolor=self.colors["light_bg"],
            arrowcolor=self.colors["text"],
        )

    def _load_db(self) -> None:
        self.patients = fnc.database_con().read("registration", "*") or []
        self.inventory = fnc.database_con().read("inventory", "*") or []

    # ───────────────── GUI build ─────────────────
    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Billing Form",
            font=Font(family="Arial", size=18, weight="bold"),
            bg=self.colors["accent"],
            fg="white",
        ).pack(pady=15)

    def _build_body(self) -> None:
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        body = ttk.Frame(canvas)

        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        cid = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cid, width=e.width))
        canvas.configure(yscrollcommand=vscroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.scrollable_frame = body
        self._build_billing_section()

    def _build_footer(self) -> None:
        bar = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        bar.pack(side="bottom", fill="x")

        tk.Button(
            bar,
            text="Submit Billing",
            font=("Arial", 12),
            command=self._submit,
            bg=self.colors["accent"],
            fg="white",
            padx=20,
            pady=8,
            bd=0,
        ).pack(side="right", padx=20)

        tk.Button(
            bar,
            text="Exit",
            font=("Arial", 12),
            command=self._back_to_menu,
            bg=self.colors["danger"],
            fg="white",
            padx=20,
            pady=8,
            bd=0,
        ).pack(side="right")

    # ───────────────── billing form ─────────────────
    def _build_billing_section(self) -> None:
        section = tk.LabelFrame(
            self.scrollable_frame,
            text="Billing Information",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Arial", 14, "bold"),
            bd=2,
            relief="groove",
            padx=10,
            pady=10,
        )
        section.pack(fill="x", padx=30, pady=15)

        for field in (
            "Patient Name",
            "Total Payment",      # editable
            "Total Charges",      # auto
            "Balance",            # auto
            "Payment Method",
            "Payment Status",
            "Notes",
        ):
            self._build_field(section, field)

        self._build_items_table(section)

    def _build_field(self, parent: tk.Widget, field: str) -> None:
        row = tk.Frame(parent, bg=self.colors["bg"])
        row.pack(fill="x", pady=6)

        tk.Label(
            row, text=f"{field}:", font=("Arial", 12),
            bg=self.colors["bg"], fg=self.colors["text"], anchor="w"
        ).pack(fill="x")

        var = tk.StringVar()
        self.form_vars[field] = var

        if field == "Patient Name":
            names = [f"{p[2]} {p[3]}" for p in self.patients] or ["— no patients —"]
            self._combo(row, var, ["– select patient –", *names])
        elif field == "Payment Method":
            self._combo(row, var, ["– select method –", "Cash", "Insurance"])
        elif field == "Payment Status":
            self._combo(row, var, ["– select status –", "Paid", "Unpaid", "Pending"])
        elif field in ("Total Charges", "Balance"):
            tk.Entry(row, textvariable=var, font=("Arial", 12), state="readonly")\
                .pack(fill="x", pady=5)
            var.set("0.00")
        elif field == "Total Payment":
            tk.Entry(row, textvariable=var, font=("Arial", 12)).pack(fill="x", pady=5)
            # update balance whenever cashier types
            var.trace_add("write", self._update_balance)
        else:  # Notes
            tk.Entry(row, textvariable=var, font=("Arial", 12)).pack(fill="x", pady=5)

    # ---------- items table ----------
    def _build_items_table(self, parent: tk.Widget) -> None:
        box = tk.LabelFrame(
            parent,
            text="Items Used",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=6,
        )
        box.pack(fill="both", expand=True, pady=10)

        cols = ("Item", "Qty", "Unit Price", "Line Total")
        self.tree = ttk.Treeview(box, columns=cols, show="headings", height=6)
        for col in cols:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=150 if col == "Item" else 90)
        self.tree.pack(fill="both", expand=True, side="left", padx=(0, 5))

        ttk.Scrollbar(box, orient="vertical", command=self.tree.yview).pack(
            fill="y", side="right"
        )

        btns = tk.Frame(parent, bg=self.colors["bg"])
        btns.pack(anchor="e", pady=(5, 0))

        tk.Button(
            btns,
            text="➕  Add Item",
            command=self._open_item_dialog,
            font=("Arial", 11),
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            padx=12,
            pady=4,
        ).pack(side="left", padx=4)

        tk.Button(
            btns,
            text="🗑  Remove Selected",
            command=self._remove_selected,
            font=("Arial", 11),
            bg=self.colors["danger"],
            fg="white",
            bd=0,
            padx=12,
            pady=4,
        ).pack(side="left", padx=4)

    # ---------- small helpers ----------
    def _combo(self, parent: tk.Widget, sv: tk.StringVar, values: list[str]) -> None:
        cb = ttk.Combobox(parent, values=values, state="readonly", font=("Arial", 12))
        cb.current(0)
        sv.set("")
        cb.pack(fill="x", pady=5)
        cb.bind("<<ComboboxSelected>>", lambda _e, var=sv, box=cb: var.set(box.get()))

    # ───────────────── item dialog ─────────────────
    def _open_item_dialog(self) -> None:
        dlg = tk.Toplevel(self.root)
        dlg.title("Select Item")
        dlg.grab_set()
        dlg.resizable(False, False)

        tk.Label(dlg, text="Item:", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=8)
        tk.Label(dlg, text="Quantity:", font=("Arial", 12)).grid(row=1, column=0, padx=8, pady=8)

        item_var, qty_var = tk.StringVar(), tk.StringVar(value="1")
        items = [row[2] for row in self.inventory]  # col 1 = item
        ttk.Combobox(dlg, textvariable=item_var, values=items, state="readonly")\
            .grid(row=0, column=1, padx=8, pady=8)
        if items:
            item_var.set(items[0])

        tk.Entry(dlg, textvariable=qty_var, width=8).grid(row=1, column=1, padx=8, pady=8)

        def _add() -> None:
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid", "Quantity must be a positive integer.", parent=dlg)
                return

            name = item_var.get()
            rec = next((r for r in self.inventory if r[2] == name), None)
            if rec is None:
                messagebox.showerror("Error", "Item not found.", parent=dlg)
                return

            unit_price = float(rec[5])      # col 3 = unit price
            line_total = unit_price * qty
            self.item_rows.append((name, qty, unit_price, line_total))
            self.tree.insert("", "end", values=(name, qty, f"{unit_price:.2f}", f"{line_total:.2f}"))
            self._update_total()
            dlg.destroy()

        tk.Button(dlg, text="Add", command=_add, width=12)\
            .grid(row=2, column=0, columnspan=2, pady=10)

    def _remove_selected(self) -> None:
        for iid in self.tree.selection():
            val = self.tree.item(iid, "values")
            self.item_rows = [
                row for row in self.item_rows if not (row[0] == val[0] and str(row[1]) == val[1])
            ]
            self.tree.delete(iid)
        self._update_total()

    # ---------- totals & balance ----------
    def _update_total(self) -> None:
        self.form_vars["Total Charges"].set(f"{sum(r[3] for r in self.item_rows):.2f}")
        self._update_balance()

    def _update_balance(self, *_: object) -> None:
        """Balance = Total Payment − Total Charges (positive ⇒ change)."""
        try:
            payment = float(self.form_vars["Total Payment"].get())
        except ValueError:
            payment = 0.0
        try:
            charges = float(self.form_vars["Total Charges"].get())
        except ValueError:
            charges = 0.0
        self.form_vars["Balance"].set(f"{charges - payment:.2f}")

    # ───────────────── submit ─────────────────
    def _submit(self) -> None:
        header = {fld: var.get().strip() for fld, var in self.form_vars.items()}
        missing = [f for f, v in header.items() if not v and f not in ("Total Charges", "Balance")]
        if missing:
            messagebox.showwarning("Missing", "Please fill / choose:\n• " + "\n• ".join(missing))
            return
        if not self.item_rows:
            messagebox.showwarning("Missing", "Add at least one inventory item.")
            return

        patient_name = header["Patient Name"]
        patient_id = next((p[0] for p in self.patients if f"{p[2]} {p[3]}" == patient_name), None)
        if patient_id is None:
            messagebox.showerror("Error", "Selected patient not found.")
            return

        item_details = "\n".join(f"{name}  x{qty}  @ {unit:.2f} = {total:.2f}" for name, qty, unit, total in self.item_rows)

        # Update inventory per item
        for name, qty, unit, total in self.item_rows:
            # Find the inventory entry
            for row in self.inventory:
                item_id = row[0]
                item_name = row[2]
                item_qty = row[4]
                item_price = row[5]
                if name == item_name:
                    try:
                        new_qty = int(item_qty) - int(qty)
                        new_total_price = float(item_price) * new_qty
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid quantity or price data for item '{name}'")
                        return

                    fnc.database_con().Record_edit(
                        "inventory",
                        "quantity",
                        new_qty,
                        "id",
                        item_id
                    )
                    fnc.database_con().Record_edit(
                        "inventory",
                        "totalPrice",
                        new_total_price,
                        "id",
                        item_id
                    )
                    break
            else:
                messagebox.showerror("Error", f"Item '{name}' not found in inventory.")
                return

        # Insert billing record
        fnc.database_con().insert(
            "billing",
            (
                'patientID',
                'patientName',
                'itemused',
                'totalpayment',
                'totalcharges',
                'balance',
                'paymentMethod',
                'paymentStatus',
                'notes',
                'staffID'
            ),
            [
                patient_id,
                patient_name,
                item_details,
                header["Total Payment"],
                header["Total Charges"],
                header["Balance"],
                header["Payment Method"],
                header["Payment Status"],
                header["Notes"],
                self.staff_id,
            ],
        )

        self._clear_form()


    # ───────────────── misc ─────────────────
    def _clear_form(self) -> None:
        for fld, var in self.form_vars.items():
            var.set("0.00" if fld in ("Total Charges", "Balance") else "")
            if fld in self.combos:
                self.combos[fld].current(0)
        self.tree.delete(*self.tree.get_children())
        self.item_rows.clear()

    def _back_to_menu(self) -> None:
        self.root.destroy()
        Billing.main(self.staff_id)


# ───────────────── manual test ─────────────────
def main(staff_id: int = 8) -> None:  # pragma: no cover
    root = tk.Tk()
    BillingForm(root, staff_id)
    root.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main()
