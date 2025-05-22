import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
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
from Front_End.PagesGUI import Appointment

class ProfileViewer:
    def __init__(self, root, id , patient_data=None):
        self.root = root
        self.root.title("Patient Appointment Profile")
        self.root.attributes('-fullscreen', True)
        
        # Sample data if none provided
        self.patient_data = patient_data or {
            "Patient Information": {
                "First Name": "Juan",
                "Last Name": "Dela Cruz"
            },
            "Appointment Details": {
                "Appointment Date": "2025-04-20",
                "Appointment Time": "10:30 AM",
                "Appointment Type": "Regular Check-up",
                "Preferred Doctor": "Dr. Santos - General Medicine",
                "Department": "General Medicine",
                "Notes": "Please fast for 8 hours prior."
            }
        }
        
        self.id = id
        # Profile image (can be passed in or use default)
        self.profile_image = Image.open(resource_path(os.path.join("Front_End", "Pic", "logo.png")))

        
        # Modern color scheme with black accent
        self.colors = {
            "bg": "#ffffff",
            "accent": "#000000",
            "text": "#333333",
            "light_bg": "#f5f5f5",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "section_bg": "#f9f9f9",
            "highlight": "#f2f2f2"
        }
        
        # Configure styles
        self.configure_styles()
        
        # Create widgets
        self.create_widgets()

    def configure_styles(self):
        # Configure the root window
        self.root.configure(bg=self.colors["bg"])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame style
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["section_bg"])
        
        # Separator style
        style.configure("TSeparator", background=self.colors["accent"])

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors["accent"], height=70)
        header_frame.pack(fill="x")
        
        title_font = Font(family="Arial", size=18, weight="bold")
        title = tk.Label(header_frame, text="Patient Appointment Profile", 
                         font=title_font, bg=self.colors["accent"], fg="white")
        title.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Profile card
        self.card_frame = self.create_profile_card(main_frame)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        button_frame.pack(side="bottom", fill="x")
        
        # Save as PNG Button
        save_btn = tk.Button(button_frame, text="Save as PNG", font=("Arial", 12), 
                             command=self.save_as_png, bg=self.colors["accent"], 
                             fg="white", padx=20, pady=8, bd=0,
                             activebackground="#333333", activeforeground="white")
        save_btn.pack(side="right", padx=20)
        
        # Exit Button
        exit_btn = tk.Button(button_frame, text="Exit", font=("Arial", 12), 
                             command=self.back, bg=self.colors["danger"], 
                             fg="white", padx=20, pady=8, bd=0,
                             activebackground="#c0392b", activeforeground="white")
        exit_btn.pack(side="right")

    def back(self):
        self.root.destroy()
        Appointment.main(self.id)

    def create_profile_card(self, parent):
        # Create a centered card
        card_width = 800
        
        # Container to center the card
        container = tk.Frame(parent, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)
        
        # Profile card
        card = ttk.Frame(container, style="Card.TFrame", width=card_width)
        card.pack(
            pady=20, fill="both", expand=True,
            padx=(parent.winfo_screenwidth() - card_width) // 2
        )
        
        # Patient name and appointment status
        header_frame = tk.Frame(card, bg=self.colors["section_bg"])
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Get patient name
        first_name = self.patient_data["Patient Information"]["First Name"]
        middle_name = self.patient_data["Patient Information"]["Middle Name"]
        last_name = self.patient_data["Patient Information"]["Last Name"]
        full_name = f"{first_name} {middle_name} {last_name}"
        
        # Patient name
        name_font = Font(family="Arial", size=24, weight="bold")
        name_label = tk.Label(header_frame, text=full_name, font=name_font, 
                              bg=self.colors["section_bg"], fg=self.colors["accent"])
        name_label.pack(anchor="w")
        
        # Appointment status (if you have a status field)
        status = self.patient_data["Appointment Details"].get("status", "Scheduled")
        status_font = Font(family="Arial", size=14)
        status_label = tk.Label(header_frame, text=f"Status: {status}", 
                                font=status_font, bg=self.colors["section_bg"], 
                                fg=self.colors["success"])
        status_label.pack(anchor="w", pady=(5, 0))
        
        # Separator
        separator = ttk.Separator(card, orient="horizontal")
        separator.pack(fill="x", padx=30, pady=10)
        
        # Appointment details
        details_frame = tk.Frame(card, bg=self.colors["section_bg"])
        details_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Create two columns
        left_col = tk.Frame(details_frame, bg=self.colors["section_bg"])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_col = tk.Frame(details_frame, bg=self.colors["section_bg"])
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Appointment date & time
        appt_date = self.patient_data["Appointment Details"]["Appointment Date"]
        appt_time = self.patient_data["Appointment Details"]["Appointment Time"]
        self.create_detail_item(
            left_col, 
            "Appointment Date & Time", 
            f"{self.format_date(appt_date)} at {appt_time}"
        )
        
        # Appointment type
        self.create_detail_item(
            left_col, 
            "Appointment Type", 
            self.patient_data["Appointment Details"]["Appointment Type"]
        )
        
        # Provider
        self.create_detail_item(
            right_col, 
            "Provider", 
            self.patient_data["Appointment Details"]["Preferred Doctor"]
        )
        
        # Department
        self.create_detail_item(
            right_col,
            "Location",
            "SITIO AGTAS, SAN JUAN,\n San Carlos City, \nPhilippines, 2420. \nVMUF Birthing Home"
        )
        
        # Notes
        notes = self.patient_data["Appointment Details"].get("Notes","")
        self.create_detail_item(
            left_col,
            "Notes",
            notes
        )
        
        # Image and instructions section
        image_frame = tk.Frame(card, bg=self.colors["section_bg"], height=150)
        image_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        # Patient image (or initials)
        image_container = tk.Frame(image_frame, bg=self.colors["section_bg"], width=150, height=150)
        image_container.pack(side="left")
        image_container.pack_propagate(False)
        
        if self.profile_image:
            img = ImageTk.PhotoImage(self.profile_image.resize((150, 150), Image.LANCZOS))
            img_label = tk.Label(image_container, image=img, bg=self.colors["section_bg"])
            img_label.image = img
            img_label.pack(fill="both", expand=True)
        else:
            initials = f"{first_name[0]}{last_name[0]}"
            initials_label = tk.Label(
                image_container, text=initials,
                font=("Arial", 48, "bold"),
                bg=self.colors["accent"], fg="white"
            )
            initials_label.pack(fill="both", expand=True)
        
        instructions_frame = tk.Frame(image_frame, bg=self.colors["section_bg"])
        instructions_frame.pack(side="left", fill="both", expand=True, padx=20)
        instructions_text = (
            "\nPlease arrive 10 minutes early.\n"
            "Bring a valid ID for verification.\n"
            "Contact 0907 762 1867 or email 1x7r4@example.com if you need to reschedule.\n"
            "Thank you for choosing VMUF Birthing Home!"
        )
        instructions = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 11),
            bg=self.colors["section_bg"],
            fg=self.colors["text"],
            justify="left", wraplength=400
        )
        instructions.pack(anchor="w")
        
        return card

    def create_detail_item(self, parent, label_text, value_text):
        container = tk.Frame(parent, bg=self.colors["section_bg"], pady=10)
        container.pack(fill="x")
        
        tk.Label(
            container, text=label_text,
            font=("Arial", 12, "bold"),
            bg=self.colors["section_bg"],
            fg=self.colors["text"]
        ).pack(anchor="w")
        
        tk.Label(
            container, text=value_text,
            font=("Arial", 14),
            bg=self.colors["section_bg"],
            fg=self.colors["accent"]
        ).pack(anchor="w", pady=(5, 0))

    def format_date(self, date_str):
        try:
            y, m, d = map(int, date_str.split("-"))
            return datetime(y, m, d).strftime("%B %d, %Y")
        except:
            return str(date_str)

    def save_as_png(self):
        try:
            # Make sure all geometry is up to date
            self.root.update_idletasks()
            self.root.update()

            # Build a sane default filename
            raw_date = self.patient_data["Appointment Details"]["Appointment Date"]
            if isinstance(raw_date, datetime):
                date_text = raw_date.strftime("%Y-%m-%d")
            else:
                date_text = str(raw_date)
            date_str = date_text.replace("-", "")

            first = self.patient_data["Patient Information"]["First Name"]
            last  = self.patient_data["Patient Information"]["Last Name"]
            default_name = f"{last}_{first}_{date_str}.png"

            # Ask the user where to save
            file_path = filedialog.asksaveasfilename(
                title="Save Appointment as PNG",
                defaultextension=".png",
                filetypes=[("PNG Image","*.png")],
                initialfile=default_name
            )
            if not file_path:
                return  # user cancelled

            # Capture just the card area
            x = self.card_frame.winfo_rootx()
            y = self.card_frame.winfo_rooty()
            w = self.card_frame.winfo_width()
            h = self.card_frame.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            img.save(file_path)

            messagebox.showinfo("Saved", f"Appointment saved!\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image:\n{e}")


def show_profile(ID, staffID):
    data = fnc.database_con().read("appointment", "*")
    patient_data = None
    for row in data:
        if row[0] == ID:
            patient_data = {
                "Patient Information": {
                    "First Name": row[2],
                    "Middle Name": row[3],
                    "Last Name": row[4]
                },
                "Appointment Details": {
                    "status": row[11],
                    "Appointment Date": row[7],
                    "Appointment Time": row[8],
                    "Appointment Type": row[9],
                    "Preferred Doctor": row[10],
                    "Notes": row[12] if len(row) > 12 else ""
                }
            }
            break

    if not patient_data:
        messagebox.showerror("Error", "Appointment not found.")
        return

    root = tk.Tk()
    ProfileViewer(root, staffID, patient_data)
    root.mainloop()

# For testing
if __name__ == "__main__":
    show_profile(1, 8)
