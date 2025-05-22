# MedicalRecordViewer_fixed.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from datetime import datetime
import os
from PIL import ImageGrab, Image, ImageTk
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import medicalRecord  # ensure this matches your module name


class MedicalRecordViewer:
    def __init__(self, root, staff_id, record_data=None):
        self.root = root
        self.root.title("Patient Medical Record")
        self.root.attributes('-fullscreen', True)

        # default sample data
        self.record_data = record_data or {
            "Patient Information": {"Full Name": "Maria Clara", "Patient ID": "P-0001"},
            "Medical Details": {"Record ID": "MR-0001", "Date": "2025-04-24", "Diagnosis": "Example", "Notes": "N/A"}
        }

        self.staff_id = staff_id
        self.profile_image = Image.open(resource_path(os.path.join("Front_End", "Pic", "logo.png")))


        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "section_bg": "#f9f9f9",
        }
        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["section_bg"])
        style.configure("TSeparator", background=self.colors["accent"])

    def _create_widgets(self):
        # header
        header = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Patient Medical Record",
            font=Font(family="Arial", size=18, weight="bold"),
            bg=self.colors["accent"], fg="white"
        ).pack(pady=15)

        # main container
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(fill="both", expand=True, padx=40, pady=30)

        self.card_frame = self._create_record_card(main)

        # footer
        footer = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        footer.pack(side="bottom", fill="x")
        tk.Button(
            footer, text="Save as PNG", font=("Arial", 12),
            command=self.save_as_png, bg=self.colors["accent"], fg="white",
            padx=20, pady=8, bd=0,
            activebackground="#333333", activeforeground="white"
        ).pack(side="right", padx=20)
        tk.Button(
            footer, text="Exit", font=("Arial", 12), command=self.back,
            bg="#e74c3c", fg="white", padx=20, pady=8, bd=0,
            activebackground="#c0392b", activeforeground="white"
        ).pack(side="right")

    def back(self):
        self.root.destroy()
        medicalRecord.main(self.staff_id)  # ensure this navigates correctly

    def _create_record_card(self, parent):
        # slightly smaller width for card
        card_w = 1000
        container = tk.Frame(parent, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, style="Card.TFrame", width=card_w)
        screen_w = parent.winfo_screenwidth()
        card.pack(
            pady=20, fill="both", expand=True,
            padx=(screen_w - card_w)//2
        )

        # header info
        hdr = tk.Frame(card, bg=self.colors["section_bg"])
        hdr.pack(fill="x", padx=30, pady=(30, 20))
        Font_header = Font(family="Arial", size=24, weight="bold")
        pi = self.record_data.get("Patient Information", {})
        name = pi.get("Full Name", "Unknown")
        tk.Label(hdr, text=name, font=Font_header,
                 bg=self.colors["section_bg"], fg=self.colors["accent"]).pack(anchor="w")
        pid = pi.get("Patient ID")
        if pid:
            tk.Label(
                hdr, text=f"Patient ID: {pid}", font=("Arial", 14),
                bg=self.colors["section_bg"], fg=self.colors["text"]
            ).pack(anchor="w", pady=(5,0))

        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=30, pady=10)

        # dynamic details
        details = tk.Frame(card, bg=self.colors["section_bg"])
        details.pack(fill="both", expand=True, padx=30, pady=20)
        left = tk.Frame(details, bg=self.colors["section_bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0,10))
        right = tk.Frame(details, bg=self.colors["section_bg"])
        right.pack(side="right", fill="both", expand=True, padx=(10,0))

        items = list(self.record_data.get("Medical Details", {}).items())
        half = (len(items)+1)//2
        for idx, (lbl, val) in enumerate(items):
            target = left if idx < half else right
            self.add_item(target, lbl, val)

        # logo + instructions
        img_block = tk.Frame(card, bg=self.colors["section_bg"], height=150)
        img_block.pack(fill="x", padx=30, pady=(20,30))
        holder = tk.Frame(img_block, bg=self.colors["section_bg"], width=150, height=150)
        holder.pack(side="left")
        holder.pack_propagate(False)
        img = ImageTk.PhotoImage(self.profile_image.resize((150,150), Image.LANCZOS))
        tk.Label(holder, image=img, bg=self.colors["section_bg"]).pack(fill="both", expand=True)
        holder.image = img

        instr = tk.Frame(img_block, bg=self.colors["section_bg"])
        instr.pack(side="left", fill="both", expand=True, padx=20)
        tk.Label(
            instr,
            text=("\n\nFor follow-up checkups or medical inquiries,\n"
                  "please visit the VMUF Birthing Home or contact 0907 762 1867.\n"
                  "Thank you for choosing VMUF Birthing Home."),
            font=("Arial", 11), bg=self.colors["section_bg"],
            fg=self.colors["text"], justify="left", wraplength=400
        ).pack(anchor="w")

        return card

    def add_item(self, parent, label_txt, value_txt):
        row = tk.Frame(parent, bg=self.colors["section_bg"], pady=10)
        row.pack(fill="x")
        tk.Label(
            row, text=label_txt, font=("Arial",12,"bold"),
            bg=self.colors["section_bg"], fg=self.colors["text"]
        ).pack(anchor="w")
        tk.Label(
            row, text=value_txt, font=("Arial",14),
            bg=self.colors["section_bg"], fg=self.colors["accent"]
        ).pack(anchor="w", pady=(5,0))

    def format_date(self, date_str):
        try:
            y, m, d = map(int, date_str.split("-"))
            return datetime(y,m,d).strftime("%B %d, %Y")
        except:
            return str(date_str)

    def save_as_png(self):
        try:
            self.root.update_idletasks(); self.root.update()
            raw_date = self.record_data["Medical Details"].get("Date", "")
            date_str = str(raw_date).replace("-", "")
            name = self.record_data.get("Patient Information",{}).get("Full Name","").replace(" ","_")
            default = f"{name}_{date_str}.png"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png", filetypes=[("PNG files","*.png")],
                initialfile=default, title="Save Medical Record As"
            )
            if not file_path: return
            x,y = self.card_frame.winfo_rootx(), self.card_frame.winfo_rooty()
            w,h = self.card_frame.winfo_width(), self.card_frame.winfo_height()
            img = ImageGrab.grab(bbox=(x,y,x+w,y+h)); img.save(file_path)
            messagebox.showinfo("Saved", f"Exported!\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image:\n{e}")


# -----------------------------------------------------------------------------
def main(record_id, staff_id, rec_type):
    # fetch data based on type
    table = "checkup" if rec_type =="checkup" else "nsd"
    recs = fnc.database_con().read(table, "*")
    record_data = None
    for rec in recs:
        if rec[0] == record_id:
            pid = rec[2]; name = rec[3]
            if rec_type == "checkup":
                md = {
                    "Record ID": rec[0], "Date": rec[4],
                    "Blood Pressure": rec[5], "Heart Rate": rec[6],
                    "Resp Rate": rec[7], "Temperature": rec[8],
                    "Oxygen Sat": rec[9], "Diagnosis": rec[10],
                    "Prescription": rec[11], "Provider #": rec[12]
                }
            else:
                md = {
                    "Record ID": rec[0], "Date of Delivery": rec[4],
                    "Time of Delivery": rec[5], "Delivery Notes": rec[6],
                    "Baby Weight": rec[7], "Apgar Score": rec[8],
                    "Provider #": rec[9]
                }
            record_data = {
                "Patient Information": {"Full Name": name, "Patient ID": pid},
                "Medical Details": md
            }
            break
    if not record_data:
        messagebox.showerror("Not found", "Medical record not found.")
        return

    root = tk.Tk()
    MedicalRecordViewer(root, staff_id, record_data)
    root.mainloop()


if __name__ == "__main__":
    # example: use "checkup" or "nsd"
    main(7, 8, rec_type="checkup")
