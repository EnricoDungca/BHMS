import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
from tkinter.font import Font
from datetime import datetime
import os
from PIL import ImageGrab, Image, ImageTk
import sys

# load local module
sys.path.insert(0, os.path.join(os.getcwd(), 'BHMS'))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Billing     # ← change this to the page you want to go back to

class BillingViewer:
    def __init__(self, root, staff_id, billing_data=None):
        self.root = root
        self.root.title("Patient Billing Statement")
        self.root.attributes('-fullscreen', True)

        # sample data if none provided ----------------------------------------
        self.billing_data = billing_data or {
            "Patient Information": {
                "Full Name": "Juan Dela Cruz"
            },
            "Billing Details": {
                "Invoice #":      "INV-0001",
                "Billing Date":   "2025-04-24",
                "description":    "General consultation and delivery services.",
                "Total Charges":  "₱ 5 000.00",
                "Total Payments": "₱ 2 000.00",
                "Balance":        "₱ 3 000.00",
                "Status":         "PARTIALLY PAID",
                "Notes":          "Follow-up payment due next visit."
            }
        }
        # ---------------------------------------------------------------------

        self.staff_id = staff_id
        self.profile_image = Image.open("Front_End/Pic/logo.png")  # logo / placeholder

        # color palette
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "section_bg": "#f9f9f9",
            "success": "#2ecc71",
            "danger": "#e74c3c"
        }
        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["section_bg"])
        style.configure("TSeparator", background=self.colors["accent"])

    def create_widgets(self):
        # header
        header = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header.pack(fill="x")
        title_font = Font(family="Arial", size=18, weight="bold")
        tk.Label(header,
                 text="Patient Billing Statement",
                 font=title_font,
                 bg=self.colors["accent"],
                 fg="white").pack(pady=15)

        # main container
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(fill="both", expand=True, padx=40, pady=30)

        # create & center card
        self.card_frame = self.create_billing_card(main)

        # footer buttons
        footer = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        footer.pack(side="bottom", fill="x")

        tk.Button(footer,
                  text="Save as PNG",
                  font=("Arial", 12),
                  command=self.save_as_png,
                  bg=self.colors["accent"],
                  fg="white",
                  padx=20, pady=8, bd=0,
                  activebackground="#333333",
                  activeforeground="white"
                  ).pack(side="right", padx=20)

        tk.Button(footer,
                  text="Exit",
                  font=("Arial", 12),
                  command=self.back,
                  bg=self.colors["danger"],
                  fg="white",
                  padx=20, pady=8, bd=0,
                  activebackground="#c0392b",
                  activeforeground="white"
                  ).pack(side="right")

    def back(self):
        self.root.destroy()
        Billing.main(self.staff_id)

    def create_billing_card(self, parent):
        card_w = 800

        container = tk.Frame(parent, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, style="Card.TFrame", width=card_w)

        # — center exactly like appointmentProfile.py —
        screen_width = parent.winfo_screenwidth()
        card.pack(
            pady=20,
            fill="both",
            expand=True,
            padx=(screen_width - card_w) // 2
        )

        # HEADER (name + status)
        hdr = tk.Frame(card, bg=self.colors["section_bg"])
        hdr.pack(fill="x", padx=30, pady=(30, 20))

        name_font = Font(family="Arial", size=24, weight="bold")
        full_name = self.billing_data["Patient Information"]["Full Name"]
        tk.Label(hdr,
                 text=full_name,
                 font=name_font,
                 bg=self.colors["section_bg"],
                 fg=self.colors["accent"]
                 ).pack(anchor="w")

        status_val = self.billing_data["Billing Details"]["Status"]
        status_color = (
            self.colors["success"]
            if status_val.upper() == "PAID"
            else self.colors["danger"]
        )
        tk.Label(hdr,
                 text=f"Status: {status_val}",
                 font=Font(family="Arial", size=14),
                 bg=self.colors["section_bg"],
                 fg=status_color
                 ).pack(anchor="w", pady=(5, 0))

        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=30, pady=10)

        # DETAILS
        details = tk.Frame(card, bg=self.colors["section_bg"])
        details.pack(fill="both", expand=True, padx=30, pady=20)

        left = tk.Frame(details, bg=self.colors["section_bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0,10))
        right = tk.Frame(details, bg=self.colors["section_bg"])
        right.pack(side="right", fill="both", expand=True, padx=(10,0))

        self.add_item(left, "Invoice #", self.billing_data["Billing Details"]["Invoice #"])
        self.add_item(left, "Billing Date",
                      self.format_date(self.billing_data["Billing Details"]["Billing Date"]))
        self.add_item(left, "Description",
                      self.billing_data["Billing Details"]["description"])
        self.add_item(left, "Total Charges", self.billing_data["Billing Details"]["Total Charges"])

        self.add_item(right, "Total Payments", self.billing_data["Billing Details"]["Total Payments"])
        self.add_item(right, "Balance", self.billing_data["Billing Details"]["Balance"])
        self.add_item(right, "Notes", self.billing_data["Billing Details"]["Notes"])

        # IMAGE + INSTRUCTIONS
        img_block = tk.Frame(card, bg=self.colors["section_bg"], height=150)
        img_block.pack(fill="x", padx=30, pady=(20, 30))

        holder = tk.Frame(img_block, bg=self.colors["section_bg"], width=150, height=150)
        holder.pack(side="left")
        holder.pack_propagate(False)

        img = ImageTk.PhotoImage(self.profile_image.resize((150,150), Image.LANCZOS))
        tk.Label(holder, image=img, bg=self.colors["section_bg"]).pack(fill="both", expand=True)
        holder.image = img

        instr = tk.Frame(img_block, bg=self.colors["section_bg"])
        instr.pack(side="left", fill="both", expand=True, padx=20)
        tk.Label(instr,
                 text=(
                     "\n\nFor questions or to settle your balance,\n"
                     "please visit the VMUF Birthing Home or contact 0907 762 1867.\n"
                     "Thank you for choosing VMUF Birthing Home."
                 ),
                 font=("Arial", 11),
                 bg=self.colors["section_bg"],
                 fg=self.colors["text"],
                 justify="left",
                 wraplength=400
                 ).pack(anchor="w")

        return card

    def add_item(self, parent, label_txt, value_txt):
        row = tk.Frame(parent, bg=self.colors["section_bg"], pady=10)
        row.pack(fill="x")
        tk.Label(row,
                 text=label_txt,
                 font=("Arial", 12, "bold"),
                 bg=self.colors["section_bg"],
                 fg=self.colors["text"]
                 ).pack(anchor="w")
        tk.Label(row,
                 text=value_txt,
                 font=("Arial", 14),
                 bg=self.colors["section_bg"],
                 fg=self.colors["accent"]
                 ).pack(anchor="w", pady=(5,0))

    def format_date(self, date_str):
        try:
            y, m, d = map(int, date_str.split("-"))
            return datetime(y, m, d).strftime("%B %d, %Y")
        except:
            return str(date_str)

    def save_as_png(self):
        try:
            self.root.update_idletasks()
            self.root.update()

            # ensure Billing Date is string
            raw_date = self.billing_data["Billing Details"]["Billing Date"]
            if isinstance(raw_date, datetime):
                date_text = raw_date.strftime("%Y-%m-%d")
            else:
                date_text = str(raw_date)
            date_str = date_text.replace("-", "")

            full_name = self.billing_data["Patient Information"]["Full Name"]
            default_name = f"{full_name.replace(' ', '_')}_{date_str}.png"

            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=default_name,
                title="Save Billing Statement As"
            )
            if not file_path:
                return

            x = self.card_frame.winfo_rootx()
            y = self.card_frame.winfo_rooty()
            w = self.card_frame.winfo_width()
            h = self.card_frame.winfo_height()

            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            img.save(file_path)

            messagebox.showinfo("Saved", f"Billing exported!\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image:\n{e}")

# ---------------------------------------------------------------------------
def main(invoice_id, staff_id):
    rec = fnc.database_con().read("billing", "*")
    billing_data = None
    for record in rec:
        if record[0] == invoice_id:
            billing_data = {
                "Patient Information": {"Full Name": record[3]},
                "Billing Details": {
                    "Invoice #":      record[0],
                    "Billing Date":   record[1],
                    "description":    record[4],
                    "Total Charges":  record[6],
                    "Total Payments": record[5],
                    "Balance":        record[7],
                    "Status":         record[9],
                    "Notes":          record[10]
                }
            }
            break

    if billing_data is None:
        messagebox.showerror("Not found", "Invoice not found.")
        return

    root = tk.Tk()
    BillingViewer(root, staff_id, billing_data)
    root.mainloop()

if __name__ == "__main__":
    main(1, 8)
