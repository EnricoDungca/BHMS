import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Billing

class BillingForm:
    def __init__(self, root, id):
        self.root = root
        self.root.title("Billing Form")
        self.root.attributes('-fullscreen', True)

        self.id = id
        
        self.data = fnc.database_con().read("registration", "*")
        
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9"
        }

        self.configure_styles()
        self.form_vars = {}
        self.create_widgets()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Section.TFrame", background=self.colors["section_bg"])
        style.configure("TScrollbar", background=self.colors["bg"],
                        troughcolor=self.colors["light_bg"],
                        arrowcolor=self.colors["text"])

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header_frame.pack(fill="x")
        title_font = Font(family="Arial", size=18, weight="bold")
        title = tk.Label(header_frame, text="Billing Form",
                         font=title_font, bg=self.colors["accent"], fg="white")
        title.pack(pady=15)

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(window_id, width=canvas_width)

        canvas.bind("<Configure>", resize_canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = scrollable_frame
        self.create_billing_section()

        button_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_frame.pack(side="bottom", fill="x")

        submit_btn = tk.Button(button_frame, text="Submit Billing", font=("Arial", 12),
                               command=self.submit_data, bg=self.colors["accent"],
                               fg="white", padx=20, pady=8, bd=0,
                               activebackground="#333333", activeforeground="white")
        submit_btn.pack(side="right", padx=20)

        exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 12),
                             command=self.back, bg=self.colors["danger"],
                             fg="white", padx=20, pady=8, bd=0,
                             activebackground="#c0392b", activeforeground="white")
        exit_btn.pack(side="right")

    def create_billing_section(self):
        fields = [
            "Patient Name", "Service Description",
            "Amount", "Payment Method", "Payment Status"
        ]

        section = tk.LabelFrame(self.scrollable_frame, text="Billing Information",
                                bg=self.colors["bg"], fg=self.colors["text"],
                                font=("Arial", 14, "bold"), bd=2, relief="groove", padx=10, pady=10)
        section.pack(fill="x", padx=30, pady=15)

        for field in fields:
            frame = tk.Frame(section, bg=self.colors["bg"])
            frame.pack(fill="x", pady=8)

            label = tk.Label(frame, text=field + ":", font=("Arial", 12),
                            bg=self.colors["bg"], fg=self.colors["text"], anchor="w")
            label.pack(fill="x")

            var = tk.StringVar()
            self.form_vars[field] = var

            if field == "Patient Name":
                name_options = [f"{names[2]} {names[3]}" for names in self.data]
                combobox = ttk.Combobox(frame, textvariable=var, values=name_options, state="readonly", font=("Arial", 12))
                combobox.current(0)
                combobox.pack(fill="x", pady=5)
            elif field == "Payment Method":
                method_options = ["Select Method", "Cash", "Insurance"]
                combobox = ttk.Combobox(frame, textvariable=var, values=method_options, state="readonly", font=("Arial", 12))
                combobox.current(0)
                combobox.pack(fill="x", pady=5)
            elif field == "Payment Status":
                status_options = ["Select Status", "Paid", "Unpaid", "Pending"]
                combobox = ttk.Combobox(frame, textvariable=var, values=status_options, state="readonly", font=("Arial", 12))
                combobox.current(0)
                combobox.pack(fill="x", pady=5)

            else:
                entry = tk.Entry(frame, textvariable=var, font=("Arial", 12))
                entry.pack(fill="x", pady=5)


    def submit_data(self):
        data = {field: var.get() for field, var in self.form_vars.items()}
        empty_fields = [field for field, value in data.items() if not value or value.startswith("Select")]

        if empty_fields:
            messagebox.showwarning("Missing Information", "Please fill in the following fields:\n• " + "\n• ".join(empty_fields))
            return

        values = [val for val in data.values()]
        for v in self.data:
            if values[0] == f"{v[2]} {v[3]}":
                values.insert(0, v[0])
        values.append(self.id)
        print(values)
            
        fnc.database_con().insert("billing", ("patientID", "patientName", "service", "amount", "paymentMethod", "paymentStatus", "staffID"), values)
        
        self.clear_form()

    def clear_form(self):
        for var in self.form_vars.values():
            var.set("")

    def back(self):
        self.root.destroy()
        Billing.main(self.id)
    
def main(id):
    root = tk.Tk()
    app = BillingForm(root, id)
    root.mainloop()

if __name__ == "__main__":
    main()
