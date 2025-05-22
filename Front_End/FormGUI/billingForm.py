import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
import re
import os
from tkcalendar import DateEntry  # if needed for date fields

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc  # type: ignore
from Front_End.PagesGUI import Billing  # type: ignore


class AutocompleteCombobox(ttk.Combobox):
    """
    A ttk.Combobox with live filtering as the user types.
    """
    def __init__(self, master=None, completevalues=None, **kwargs):
        self.all_values = completevalues or []
        super().__init__(master, **kwargs)
        # allow user typing
        self.configure(state='normal')
        self.bind('<KeyRelease>', self._on_keyrelease)

    def _on_keyrelease(self, event):
        text = self.get()
        # filter
        matches = [item for item in self.all_values if text.lower() in item.lower()]
        # update dropdown
        self['values'] = matches
        if matches:
            self.event_generate('<Down>')


class BillingForm:
    """
    Full-screen billing form with autocomplete patient lookup.
    """
    def __init__(self, root: tk.Tk, staff_id: int):
        self.root = root
        self.staff_id = staff_id
        self._init_window()
        self._load_db()

        self.item_rows = []  # list of (name, qty, unit, total)
        self.form_vars = {}
        self.combos = {}

        self._build_header()
        self._build_body()
        self._build_footer()

    def _init_window(self):
        self.root.title("Billing Form")
        # load icon
        icon_path = Path(BASE_DIR) / 'resources' / 'app.ico'
        if icon_path.exists():
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        # fullscreen & styling
        self.root.attributes('-fullscreen', True)
        self.colors = {
            'bg': '#ECF0F1',
            'accent': '#34495E',
            'danger': '#C0392B',
            'success': '#27AE60',
            'text': '#2C3E50',
            'optional': '#7F8C8D',
            'required': '#E74C3C'
        }
        self.root.configure(bg=self.colors['bg'])
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Treeview', background='white', fieldbackground='white')

    def _load_db(self):
        # preload registration and inventory
        self.patients = fnc.database_con().read('registration', '*') or []
        self.patient_names = [f"{p[2]} {p[3]} {p[4]}" for p in self.patients]
        self.inventory = fnc.database_con().read('inventory', '*') or []

    def _build_header(self):
        header = tk.Frame(self.root, bg="black", height=70)
        header.pack(fill='x')
        tk.Label(
            header, text='Billing Form', font=('Helvetica', 20, 'bold'),
            bg='black', fg='white'
        ).pack(pady=15)
        legend = tk.Frame(self.root, bg=self.colors['bg'])
        legend.pack(fill='x')
        tk.Label(
            legend, text='* Required fields', font=('Arial',10),
            fg=self.colors['required'], bg=self.colors['bg']
        ).pack(side='left', padx=10)
        tk.Label(
            legend, text='(optional)', font=('Arial',10,'italic'),
            fg=self.colors['optional'], bg=self.colors['bg']
        ).pack(side='left')

    def _build_body(self):
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill='both', expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        win = canvas.create_window((0,0), window=self.scroll_frame, anchor='nw')
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # billing section
        self._build_billing_section()

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=self.colors['bg'], pady=10)
        footer.pack(fill='x', side='bottom')
        tk.Button(
            footer, text='🔙 Exit', bg=self.colors['danger'], fg='white',
            font=('Arial',12,'bold'), bd=0, padx=20, pady=8,
            command=self._back_to_menu
        ).pack(side='right', padx=10)
        tk.Button(
            footer, text='💾 Submit Billing', bg=self.colors['success'], fg='white',
            font=('Arial',12,'bold'), bd=0, padx=20, pady=8,
            command=self._submit
        ).pack(side='right')

    def _build_billing_section(self):
        lf = tk.LabelFrame(
            self.scroll_frame, text='Billing Information',
            font=('Arial',14,'bold'), padx=10, pady=10,
            bg=self.colors['bg'], fg=self.colors['text']
        )
        lf.pack(fill='x', pady=10)
        fields = [
            ('Patient Name', True),
            ('Total Payment', True),
            ('Total Charges', False),
            ('Balance', False),
            ('Payment Method', True),
            ('Payment Status', True),
            ('Notes', False)
        ]
        for name, req in fields:
            self._build_field(lf, name, req)
        self._build_items_table(lf)

    def _build_field(self, parent, field, required):
        frm = tk.Frame(parent, bg=self.colors['bg'])
        frm.pack(fill='x', pady=5)
        lbl = f"{'* ' if required else ''}{field}{'' if required else ' (optional)'}:"
        fg = self.colors['required'] if required else self.colors['optional']
        tk.Label(frm, text=lbl, font=('Arial',12), fg=fg, bg=self.colors['bg']).pack(anchor='w')

        var = tk.StringVar()
        self.form_vars[field] = var

        if field == 'Patient Name':
            # autocomplete combobox
            acb = AutocompleteCombobox(
                frm, textvariable=var,
                completevalues=self.patient_names,
                values=self.patient_names,
                font=('Arial',12)
            )
            acb.pack(fill='x', pady=2)
            self.combos[field] = acb
        elif field in ('Total Charges','Balance'):
            ent = tk.Entry(frm, textvariable=var, font=('Arial',12), state='readonly')
            ent.pack(fill='x', pady=2)
            var.set('0.00')
        elif field == 'Total Payment':
            ent = tk.Entry(frm, textvariable=var, font=('Arial',12))
            ent.pack(fill='x', pady=2)
            ent.bind('<FocusOut>', lambda e, v=var, f=field: self._validate_numeric(v,f))
            var.trace_add('write', self._update_balance)
        elif field == 'Payment Method':
            cb = self._make_combo(frm, var, ['– select –', 'Cash', 'Insurance'])
            self.combos[field] = cb
        elif field == 'Payment Status':
            cb = self._make_combo(frm, var, ['– select –', 'Paid', 'Unpaid', 'Pending'])
            self.combos[field] = cb
        else:
            # Notes
            tk.Entry(frm, textvariable=var, font=('Arial',12)).pack(fill='x', pady=2)

    def _make_combo(self, parent, var, values):
        cb = ttk.Combobox(parent, values=values, state='readonly', font=('Arial',12))
        cb.current(0)
        var.set('')
        cb.pack(fill='x', pady=2)
        cb.bind('<<ComboboxSelected>>', lambda e: var.set(cb.get()))
        return cb

    def _build_items_table(self, parent):
        frm = tk.LabelFrame(
            parent, text='Items Used', font=('Arial',12,'bold'),
            padx=10, pady=10, bg=self.colors['bg'], fg=self.colors['text']
        )
        frm.pack(fill='both', expand=True, pady=10)
        cols = ('Item','Qty','Unit Price','Line Total')
        self.tree = ttk.Treeview(frm, columns=cols, show='headings', height=6)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120 if c=='Item' else 80)
        self.tree.pack(side='left', fill='both', expand=True)
        ttk.Scrollbar(frm, orient='vertical', command=self.tree.yview).pack(side='right', fill='y')

        btnf = tk.Frame(parent, bg=self.colors['bg'])
        btnf.pack(fill='x', pady=5)
        tk.Button(btnf, text='➕ Add Item', bg=self.colors['accent'], fg='white', bd=0,
                  padx=10, pady=5, command=self._open_item_dialog).pack(side='left', padx=5)
        tk.Button(btnf, text='🗑 Remove Selected', bg=self.colors['danger'], fg='white', bd=0,
                  padx=10, pady=5, command=self._remove_selected).pack(side='left')

    def _validate_numeric(self, var, field):
        val = var.get().strip()
        if not re.match(r'^\d+(?:\.\d{1,2})?$', val):
            messagebox.showerror('Invalid', f"{field} must be a number.", parent=self.root)
            var.set('')
            return False
        return True

    def _open_item_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title('Select Item')
        dlg.grab_set()
        dlg.resizable(False, False)
        tk.Label(dlg, text='Item:', font=('Arial',12)).grid(row=0, column=0, padx=8, pady=8)
        tk.Label(dlg, text='Quantity:', font=('Arial',12)).grid(row=1, column=0, padx=8, pady=8)
        item_var = tk.StringVar()
        qty_var = tk.StringVar(value='1')
        items = [r[2] for r in self.inventory]
        cb = ttk.Combobox(dlg, textvariable=item_var, values=items, state='readonly')
        cb.grid(row=0, column=1, padx=8, pady=8)
        if items:
            cb.current(0); item_var.set(items[0])
        tk.Entry(dlg, textvariable=qty_var, width=6).grid(row=1, column=1, padx=8, pady=8)

        def add_and_close():
            try:
                q = int(qty_var.get())
                if q < 1: raise ValueError
            except:
                messagebox.showerror('Invalid','Quantity must be positive integer.', parent=dlg)
                return
            name = item_var.get()
            rec = next((r for r in self.inventory if r[2]==name), None)
            if not rec:
                messagebox.showerror('Error','Item not found.', parent=dlg)
                return
            unit = float(rec[5]); total = unit * q
            self.item_rows.append((name, q, unit, total))
            self.tree.insert('', 'end', values=(name, q, f"{unit:.2f}", f"{total:.2f}"))
            self._update_total()
            dlg.destroy()

        tk.Button(dlg, text='Add', width=12, command=add_and_close).grid(row=2, column=0, columnspan=2, pady=10)

    def _remove_selected(self):
        for iid in self.tree.selection():
            vals = self.tree.item(iid,'values')
            self.item_rows = [r for r in self.item_rows if not (r[0]==vals[0] and str(r[1])==vals[1])]
            self.tree.delete(iid)
        self._update_total()

    def _update_total(self):
        total = sum(r[3] for r in self.item_rows)
        self.form_vars['Total Charges'].set(f"{total:.2f}")
        self._update_balance()

    def _update_balance(self, *args):
        try:
            pay = float(self.form_vars['Total Payment'].get())
        except:
            pay = 0.0
        try:
            charges = float(self.form_vars['Total Charges'].get())
        except:
            charges = 0.0
        bal = charges - pay
        self.form_vars['Balance'].set(f"{bal:.2f}")
        # auto status
        cb = self.combos.get('Payment Status')
        if cb:
            vals = list(cb['values'])
            target = 'Paid' if abs(bal) < 0.005 else 'Unpaid'
            if target in vals:
                cb.current(vals.index(target))
                self.form_vars['Payment Status'].set(target)

    def _submit(self):
        data = {k: v.get().strip() for k, v in self.form_vars.items()}

        # Validate required fields
        missing = [f for f in ('Patient Name', 'Total Payment', 'Payment Method', 'Payment Status')
                if not data.get(f)]
        if missing:
            messagebox.showwarning('Missing', f"Complete required: {', '.join(missing)}", parent=self.root)
            return

        if not self.item_rows:
            messagebox.showwarning('Missing', 'Add at least one item.', parent=self.root)
            return

        # Get patient ID
        pid = next((p[0] for p in self.patients if f"{p[2]} {p[3]} {p[4]}" == data['Patient Name']), None)
        if pid is None:
            messagebox.showerror('Error', 'Patient not found.', parent=self.root)
            return

        # Log details before submit to database
        logs = []
        for name, qty, unit_price, total_price in self.item_rows:
            rec = next((r for r in self.inventory if r[2] == name), None)
            if rec:
                old_qty = rec[4]
                old_total = rec[5]
                logs.append(
                    f"\n[Item Detail] Item Name: {rec[2]} | Old Quantity: {old_qty} | Total Price: {old_total:.2f}"
                )
                logs.append(
                    f"[Item Used] Item Name: {name} | Used Quantity: {qty} | Unit Price: {unit_price:.2f} | Total: {total_price:.2f}"
                )
                logs.append(
                    f"[New Inventory Quantity] Item Name: {rec[2]} | New Quantity: {old_qty - qty}"
                )

        log_message = "\n".join(logs)
        

        # Update inventory
        for name, qty, _, _ in self.item_rows:
            rec = next((r for r in self.inventory if r[2] == name), None)
            if rec:
                new_qty = int(rec[4]) - qty
                new_total_price = float(rec[5]) * new_qty
                fnc.database_con().Record_edit('inventory', 'quantity', new_qty, 'id', rec[0])
                fnc.database_con().Record_edit('inventory', 'totalPrice', new_total_price, 'id', rec[0])

        # Build item used details
        details = '\n'.join(f"{n} x{q} @ {u:.2f} = {t:.2f}" for n, q, u, t in self.item_rows)

        # Insert billing record into database
        fnc.database_con().insert(
            'billing',
            ('patientID', 'patientName', 'itemused', 'totalpayment', 'totalcharges',
            'balance', 'paymentMethod', 'paymentStatus', 'notes', 'staffID'),
            [pid, data['Patient Name'], details,
            data['Total Payment'], data['Total Charges'], data['Balance'],
            data['Payment Method'], data['Payment Status'], data.get('Notes', ''), self.staff_id]
        )

        fnc.Sys_log("Billing_Log", f"Patient Name: {data['Patient Name']} \n{log_message}").write_log()
        
        self._clear_form()


    def _clear_form(self):
        for f,var in self.form_vars.items():
            if f in ('Total Charges','Balance'):
                var.set('0.00')
            else:
                var.set('')
            if f in self.combos:
                self.combos[f].current(0)
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        self.item_rows.clear()

    def _back_to_menu(self):
        self.root.destroy()
        Billing.main(self.staff_id)
        
    
def main(staff_id: int):
    root = tk.Tk()
    BillingForm(root, staff_id)
    root.mainloop()
