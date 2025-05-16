import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import Dashboard

# 1. Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DATA_FILE = "beds_data.json"

class Bed:
    def __init__(self, bed_id, occupant=None):
        self.bed_id = bed_id
        self.occupant = occupant

    @property
    def status(self):
        return f"Occupied by {self.occupant}" if self.occupant else "Available"

    def to_dict(self):
        return {"bed_id": self.bed_id, "occupant": self.occupant}

    @classmethod
    def from_dict(cls, d):
        return cls(d["bed_id"], d.get("occupant"))

class BedTrackingApp(ctk.CTk):
    def __init__(self, id):
        super().__init__()
        self.title("Bed Tracking System")
        self.attributes('-fullscreen', True)

        self.beds = self._load_data()
        self.id = id
        
        self._build_navbar()
        self._build_content()
        self._update_tree()

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                return [Bed.from_dict(d) for d in data]
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load data: {e}")
        return [Bed(f"Bed {i+1}") for i in range(10)]

    def _save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([bed.to_dict() for bed in self.beds], f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {e}")

    def _build_navbar(self):
        nav = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="black")
        nav.pack(fill="x")

        ctk.CTkLabel(
            nav,
            text="VMUF Birthing Home Bed Tracker",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=30)

        ctk.CTkButton(
            nav, text="↺ Refresh",
            command=self._update_tree,
            fg_color="transparent", text_color="white",
            hover_color="#333",
            font=ctk.CTkFont(size=18)
        ).pack(side="right", padx=20)

        ctk.CTkButton(
            nav, text="Back ->",
            command=self.back,
            fg_color="transparent", text_color="white",
            hover_color="#333",
            font=ctk.CTkFont(size=18)
        ).pack(side="right", padx=10)

    def back(self):
        self.destroy()
        Dashboard.main(self.id)

    def _build_content(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white",
                        rowheight=35,
                        font=("Arial", 14))
        style.configure("Treeview.Heading",
                        font=("Arial", 16, "bold"))
        style.map("Treeview",
                  background=[("selected", "#1f6aa5")],
                  foreground=[("selected", "white")])

        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="white")
        frame.pack(padx=40, pady=30, fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=("ID", "Status"), show="headings")
        self.tree.heading("ID", text="Bed ID")
        self.tree.heading("Status", text="Status")
        self.tree.column("ID", width=180, anchor="center")
        self.tree.column("Status", width=400, anchor="center")
        self.tree.pack(pady=25, padx=25, fill="both", expand=True)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Mark as Occupied",
            width=200, height=50, corner_radius=25,
            command=self._mark_occupied,
            font=ctk.CTkFont(size=16)
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            btn_frame, text="Mark as Available",
            width=200, height=50, corner_radius=25,
            command=self._mark_available,
            font=ctk.CTkFont(size=16)
        ).grid(row=0, column=1, padx=20)

    def _update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for bed in self.beds:
            self.tree.insert("", "end", values=(bed.bed_id, bed.status))

    def _get_selected_bed(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a bed.")
            return None
        bed_id = self.tree.item(sel[0])['values'][0]
        return next((b for b in self.beds if b.bed_id == bed_id), None)

    def _mark_occupied(self):
        bed = self._get_selected_bed()
        if not bed:
            return
        name = simpledialog.askstring(
            "Occupant Name",
            f"Enter patient name for {bed.bed_id}:",
            parent=self
        )
        if name:
            bed.occupant = name
            self._save_data()
            self._update_tree()

    def _mark_available(self):
        bed = self._get_selected_bed()
        if bed:
            bed.occupant = None
            self._save_data()
            self._update_tree()

def main(id):
    app = BedTrackingApp(id)
    app.mainloop()

if __name__ == "__main__":
    main()
