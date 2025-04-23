import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter.font import Font
from datetime import datetime
import os
from PIL import ImageGrab, Image, ImageTk
import sys

# load local module
sys.path.insert(0, '\\BHMS')
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
                "Appointment Date": "2025-4-20",
                "Appointment Time": "10:30 AM",
                "Appointment Type": "Regular Check-up",
                "Preferred Doctor": "Dr. Santos - General Medicine",
                "Department": "General Medicine"
            }
        }
        
        self.id = id
        # Profile image (can be passed in or use default)
        self.profile_image = Image.open("Front_End\Pic\logo.png")
        
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
        card.pack(pady=20, fill="both", expand=True, padx=(parent.winfo_screenwidth() - card_width) // 2)
        
        # Patient name and appointment status
        header_frame = tk.Frame(card, bg=self.colors["section_bg"])
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Get patient name
        first_name = self.patient_data["Patient Information"]["First Name"]
        last_name = self.patient_data["Patient Information"]["Last Name"]
        full_name = f"{first_name} {last_name}"
        
        # Patient name
        name_font = Font(family="Arial", size=24, weight="bold")
        name_label = tk.Label(header_frame, text=full_name, font=name_font, 
                             bg=self.colors["section_bg"], fg=self.colors["accent"])
        name_label.pack(anchor="w")
        
        # Appointment status
        status_font = Font(family="Arial", size=14)
        status_label = tk.Label(header_frame, text=f"Appointment {self.patient_data['Appointment Details']['status']}", font=status_font, 
                               bg=self.colors["section_bg"], fg=self.colors["success"])
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
        
        # Appointment date and time
        self.create_detail_item(
            left_col, 
            "Appointment Date & Time", 
            f"{self.format_date(self.patient_data['Appointment Details']['Appointment Date'])} at {self.patient_data['Appointment Details']['Appointment Time']}"
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
            self.patient_data["Appointment Details"]["Provider"]
        )
        
        # Department
        self.create_detail_item(
            right_col,
            "Location",
            "VMUF Birhting Home"
        )
        
        # Notes
        self.create_detail_item(
            left_col,
            "Notes",
            self.patient_data["Appointment Details"]["Notes"]
        )
        
        # Image and instructions section
        image_frame = tk.Frame(card, bg=self.colors["section_bg"], height=150)
        image_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        # Patient image (either provided or default)
        image_container = tk.Frame(image_frame, bg=self.colors["section_bg"], width=150, height=150)
        image_container.pack(side="left")
        image_container.pack_propagate(False)  # Prevent the frame from shrinking
        
        if self.profile_image:
            # If an image was provided, use it
            img = ImageTk.PhotoImage(self.profile_image.resize((150, 150), Image.LANCZOS))
            img_label = tk.Label(image_container, image=img, bg=self.colors["section_bg"])
            img_label.image = img  # Keep a reference to prevent garbage collection
            img_label.pack(fill="both", expand=True)
        else:
            # Create a default placeholder with patient initials
            initials = f"{first_name[0]}{last_name[0]}"
            initials_label = tk.Label(image_container, text=initials, font=("Arial", 48, "bold"),
                                     bg=self.colors["accent"], fg="white")
            initials_label.pack(fill="both", expand=True)
        
        # Instructions
        instructions_frame = tk.Frame(image_frame, bg=self.colors["section_bg"])
        instructions_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        instructions_text = (
            "\nPlease arrive 10 minutes before your appointment.\n"
            "Bring a valid ID for verification.\n"
            "Contact 0912345678 or email BHMS@example.com if you need to reschedule.\n"
            "Thank you for choosing VMUF Birhting Home for your medical needs."
        )
        
        instructions = tk.Label(instructions_frame, text=instructions_text, font=("Arial", 11), 
                              bg=self.colors["section_bg"], fg=self.colors["text"],
                              justify="left", wraplength=400)
        instructions.pack(anchor="w")
        
        return card

    def create_detail_item(self, parent, label_text, value_text):
        # Container
        container = tk.Frame(parent, bg=self.colors["section_bg"], pady=10)
        container.pack(fill="x")
        
        # Label
        label = tk.Label(container, text=label_text, font=("Arial", 12, "bold"), 
                        bg=self.colors["section_bg"], fg=self.colors["text"])
        label.pack(anchor="w")
        
        # Value
        value = tk.Label(container, text=value_text, font=("Arial", 14), 
                        bg=self.colors["section_bg"], fg=self.colors["accent"])
        value.pack(anchor="w", pady=(5, 0))

    def format_date(self, date_str):
        # Convert YYYY-MM-DD to a more readable format
        try:
            year, month, day = date_str.split("-")
            date_obj = datetime(int(year), int(month), int(day))
            return date_obj.strftime("%B %d, %Y")
        except:
            return date_str

    def save_as_png(self):
        try:
            # Create a directory for saved appointments if it doesn't exist
            save_dir = "saved_appointments"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Generate filename based on patient name and date
            first_name = self.patient_data["Patient Information"]["First Name"]
            last_name = self.patient_data["Patient Information"]["Last Name"]
            date_str = self.patient_data["Appointment Details"]["Appointment Date"].replace("-", "")
            
            filename = f"{save_dir}/{last_name}_{first_name}_{date_str}.png"
            
            # Hide buttons temporarily for clean screenshot
            self.root.update()
            
            # Get the position of the card on screen
            x = self.card_frame.winfo_rootx()
            y = self.card_frame.winfo_rooty()
            width = self.card_frame.winfo_width()
            height = self.card_frame.winfo_height()
            
            # Take screenshot of the card area
            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            
            # Save the image
            screenshot.save(filename)
            
            # Show success message
            messagebox.showinfo(
                "Success", 
                f"Appointment saved as PNG!\nLocation: {os.path.abspath(filename)}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {str(e)}")

def show_profile(ID, staffID):
    data = fnc.database_con().read("appointment", "*")
    print(staffID)
    for row in data:
        if row[0] == ID:
            patient_data = {
                "Patient Information": {
                    "First Name": row[2],
                    "Last Name": row[3]
                },
                "Appointment Details": {
                    "status": row[10],
                    "Appointment Date": row[6],
                    "Appointment Time": row[7],
                    "Appointment Type": row[8],
                    "Provider": row[9],
                    "Notes": row[11]
                }
            }
            break
    
    root = tk.Tk()
    app = ProfileViewer(root, staffID, patient_data)
    root.mainloop()

# For testing purposes
if __name__ == "__main__":
    show_profile()
    
    # # Sample data
    # sample_data = {
    #     "Patient Information": {
    #         "First Name": "Juan",
    #         "Last Name": "Dela Cruz"
    #     },
    #     "Appointment Details": {
    #         "Appointment Date": "2025-4-20",
    #         "Appointment Time": "10:30 AM",
    #         "Appointment Type": "Regular Check-up",
    #         "Preferred Doctor": "Dr. Santos - General Medicine",
    #         "Department": "General Medicine"
    #     }
    # }
    
    
    # # Or without an image (will use initials):
    # show_profile(sample_data)