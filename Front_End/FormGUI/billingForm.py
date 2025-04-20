import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
import sys

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Billing

class BillingForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Form")
        self.root.attributes('-fullscreen', True)

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
            "Patient Name", "Billing Date", "Service Description",
            "Amount", "Payment Status"
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

            if field == "Payment Status":
                var.set("Select Status")
                dropdown = ttk.Combobox(frame, textvariable=var,
                                        values=["Unpaid", "Paid", "Partially Paid"],
                                        font=("Arial", 11), state="readonly")
                dropdown.pack(fill="x", ipady=4)
            elif field == "Discount":
                var.set("0.00")
                entry = tk.Entry(frame, textvariable=var, font=("Arial", 11),
                                 bd=0, highlightthickness=1,
                                 highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
                entry.pack(fill="x", ipady=8)
            elif field == "Insurance Payment":
                var.set("0.00")
                entry = tk.Entry(frame, textvariable=var, font=("Arial", 11),
                                 bd=0, highlightthickness=1,
                                 highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
                entry.pack(fill="x", ipady=8)
            else:
                entry = tk.Entry(frame, textvariable=var, font=("Arial", 11),
                                 bd=0, highlightthickness=1,
                                 highlightbackground="#e0e0e0", highlightcolor=self.colors["accent"])
                entry.pack(fill="x", ipady=8)

    def submit_data(self):
        data = {field: var.get() for field, var in self.form_vars.items()}
        empty_fields = [field for field, value in data.items() if not value or value.startswith("Select")]

        if empty_fields:
            messagebox.showwarning("Missing Information", "Please fill in the following fields:\n• " + "\n• ".join(empty_fields))
            return

        summary = "\n".join(f"{k}: {v}" for k, v in data.items())
        messagebox.showinfo("Billing Submitted", "Billing information submitted successfully!\n\nSummary:\n" + summary)
        self.clear_form()

    def clear_form(self):
        for var in self.form_vars.values():
            var.set("")

    def back(self):
        self.root.destroy()
        Billing.main()
    
def main():
    root = tk.Tk()
    app = BillingForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
