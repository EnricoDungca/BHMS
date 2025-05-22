import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from PIL import ImageGrab, Image, ImageTk
import sys, os, io

# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import patientRegistration
from Front_End.ProfileGUI import medicalProfile
from Front_End.ProfileGUI import billingProfile


class PatientProfileApp:
    def __init__(self, root, patient_id, staff_id):
        self.root = root
        self.root.title("Patient Profile")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="white")

        self.logo_image = None
        self.logo_text = "VM"
        self.patient_id = patient_id
        self.id = staff_id

        # database
        self.registration = fnc.database_con().read("registration", "*")
        self.nsd = fnc.database_con().read("nsd", "*")
        self.checkup = fnc.database_con().read("checkup", "*")
        self.billing = fnc.database_con().read("billing", "*")

        default_logo_path = "Z:/BHMS/Front_End/Pic/logo.png"
        try:
            self.logo_image = PhotoImage(file=default_logo_path)
        except Exception:
            print("Logo image not found, using text fallback.")

        self.create_header()
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(fill="both", expand=True)

        self.setup_ui()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(side='top', fill='x')

        # Default image
        profile_image = self.logo_image

        # Load from DB
        try:
            for pid, _, _, filename, blob in fnc.database_con().read("attachment", "*"):
                if pid == self.patient_id and "profilepic" in filename.lower() and any(ext in filename.lower() for ext in (".jpg", ".jpeg", ".png")):
                    if blob:
                        # Debug save
                        with open("debug_profilepic", "wb") as f:
                            f.write(blob)
                        img = Image.open(io.BytesIO(blob))
                        img = img.resize((60, 60), Image.LANCZOS)
                        profile_image = ImageTk.PhotoImage(img)
                    break
        except Exception as e:
            print(f"[ERROR] Loading profile pic: {e}")

        # Display image
        pic_frame = tk.Frame(header, width=60, height=60, bg="#ecf0f1")
        pic_frame.pack_propagate(False)
        pic_frame.pack(side='left', padx=20, pady=10)

        profile_label = tk.Label(pic_frame, image=profile_image, bg="#ecf0f1")
        profile_label.image = profile_image
        self.current_profile_image = profile_image
        profile_label.pack(expand=True)

        # Patient info
        info_frame = tk.Frame(header, bg="#2c3e50")
        info_frame.pack(side='left', padx=10)
        found = False
        for r in self.registration:
            if r[0] == self.patient_id:
                tk.Label(info_frame, text=f"{r[2]} {r[3]} {r[4]}", font=('Arial',20,'bold'), bg="#2c3e50", fg="white").pack(anchor='w')
                tk.Label(info_frame, text=f"DOB: {r[5]} | Gender: {r[6]} | ID: {r[0]}", font=('Arial',12), bg="#2c3e50", fg="white").pack(anchor='w')
                found = True
                break
        if not found:
            tk.Label(info_frame, text="Patient Not Found", font=('Arial',20,'bold'), bg="#2c3e50", fg="white").pack(anchor='w')
            tk.Label(info_frame, text=f"ID: {self.patient_id}", font=('Arial',12), bg="#2c3e50", fg="white").pack(anchor='w')

        back_btn = tk.Button(header, text="Back", font=("Arial",12,"bold"), fg="white", bg="#e74c3c", relief="flat", command=self.back)
        back_btn.pack(side="right", padx=20)
        
    
    def back(self):
        self.root.destroy()
        patientRegistration.main(self.id)
    
    def setup_ui(self):
        sidebar = tk.Frame(self.main_container, bg="#f0f0f0", width=280)
        sidebar.pack(side="left", fill="y")
        self.quick_info(sidebar)

        content_area = tk.Frame(self.main_container, bg="white")
        content_area.pack(side="right", fill="both", expand=True)

        notebook = ttk.Notebook(content_area)
        notebook.pack(fill="both", expand=True)

        self.medical_tab(notebook)
        self.billing_tab(notebook)
        self.attachment_tab(notebook)

    def create_footer(self):
        footer = tk.Frame(self.root, bg="#2c3e50", height=50)
        footer.pack(side="bottom", fill="x")

        container = tk.Frame(footer, bg="#2c3e50")
        container.pack(anchor='center', pady=5)

        if self.logo_image:
            small_logo = self.logo_image.subsample(3, 3)
            self.footer_logo_label = tk.Label(container, image=small_logo, bg="#2c3e50")
            self.footer_logo_label.image = small_logo
            self.footer_logo_label.pack(side='left', padx=5)
        else:
            self.footer_logo_label = tk.Label(container, text=self.logo_text, bg="white",
                                              font=('Arial', 12, 'bold'), width=4, height=2)
            self.footer_logo_label.pack(side='left', padx=5)

        title = tk.Label(container, text="VMUF Birthing Home", bg="#2c3e50",
                         fg="white", font=('Arial', 14, 'bold'))
        title.pack(side='left', padx=5)


    def save_profile_as_image(self):
        self.root.update()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = x + self.root.winfo_width()
        h = y + self.root.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
                                                title="Save Profile Screenshot")
        if filepath:
            img.save(filepath)
            messagebox.showinfo("Success", f"Profile saved as PNG at:\n{filepath}")

    def quick_info(self, parent):
        tk.Label(parent, text="Full Info", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=15)
        info = None
        for datainfo in self.registration:
            if self.patient_id == datainfo[0]:
                info = {
                    "Contact": f"{datainfo[7]}\n{datainfo[8]}",
                    "Address": f"{datainfo[9]}\n{datainfo[10]}\n{datainfo[11]}\n{datainfo[12]}\n{datainfo[13]}\n{datainfo[14]}",
                    "Emergency Contact": f"{datainfo[15]} ({datainfo[16]})\n{datainfo[17]}/{datainfo[18]}",
                    "Insurance": f"{datainfo[19]}\n{datainfo[20]}"
                }
                break

        if info:
            for title, text in info.items():
                tk.Label(parent, text=title, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
                tk.Label(parent, text=text, bg="#f0f0f0", justify="left", wraplength=250, font=("Arial", 11)).pack(anchor="w", padx=15)

        btn = tk.Button(parent, text="Save Profile as PNG", command=self.save_profile_as_image,
                        bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                        relief="flat", padx=12, pady=6, cursor="hand2")
        btn.pack(pady=20)
        
        btn = tk.Button(parent, text="Upload Attachment", command=self.upload_attachment,
                        bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                        relief="flat", padx=12, pady=6, cursor="hand2")
        btn.pack(pady=20)
        
    def upload_attachment(self):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
        )

        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                filename = file_path.split('/')[-1]

            # Insert into the database: (upload_date, patient_id, filename, file_data)
            fnc.database_con().insert(
                "attachment",
                ("patientID", "filename", "attachment"),
                (self.patient_id, filename, file_data)
        )

    def medical_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Medical Records")

        canvas = tk.Canvas(tab, bg="white")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 🖱️ Mousewheel binding for Windows/macOS
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # 🖱️ Mousewheel binding for Linux
        def _on_mousewheel_linux(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)         # Windows/macOS
        canvas.bind_all("<Button-4>", _on_mousewheel_linux)     # Linux scroll up
        canvas.bind_all("<Button-5>", _on_mousewheel_linux)     # Linux scroll down

        # Gather all checkup records
        checkup_records = []
        for data in self.checkup:
            if self.patient_id == data[2]:
                checkup_records.append({
                    "ID": data[0],
                    "Type": "Check-up",
                    "Date": data[1],
                    "Diagnosis": data[10],
                    "Medications": data[11]
                })

        # Gather all NSD records
        nsd_records = []
        for data in self.nsd:
            if self.patient_id == data[2]:
                nsd_records.append({
                    "ID": data[0],
                    "Type": "NSD",
                    "Date of Delivery": data[4],
                    "Time of Delivery": data[5],
                    "Delivery Note": data[6],
                    "Baby Weight": data[7],
                    "Apgar Score": data[5]
                })
        
        if not checkup_records and not nsd_records:
            no_record_label = tk.Label(scroll_frame, text="No medical record found.", font=("Arial", 14), bg="white", fg="gray")
            no_record_label.pack(pady=20)
        else:
            for record in checkup_records:
                card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
                card.pack(fill="x", padx=20, pady=10)
                tk.Label(card, text=f"Record ID: {record['ID']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Type']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Date']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"Diagnosis: {record['Diagnosis']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Medications: {record['Medications']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                
                view_btn = tk.Button(card, text="View", command=lambda rid=record['ID']: self.view(self.id, rid, "checkup"), font=("Arial", 12), bg="#3498db", fg="white", relief="flat", padx=12, pady=6, cursor="hand2")
                view_btn.pack(pady=20)

            for record in nsd_records:
                card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
                card.pack(fill="x", padx=20, pady=10)
                tk.Label(card, text=f"Record ID: {record['ID']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Type']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Date of Delivery']} - {record['Time of Delivery']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"Delivery Note: {record['Delivery Note']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Baby Weight: {record['Baby Weight']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Apgar Score: {record['Apgar Score']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                
                view_btn = tk.Button(card, text="View", command=lambda: self.view(self.id, record["ID"], "NSD"), font=("Arial", 12), bg="#3498db", fg="white", relief="flat", padx=12, pady=6, cursor="hand2")
                view_btn.pack(pady=20)

        
    def view(self, staff_id, patient_id, record_type):
        self.root.destroy()
        print (patient_id, staff_id, record_type)
        medicalProfile.main(patient_id, staff_id, record_type)
        


    def billing_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Billing")

        canvas = tk.Canvas(tab, bg="white")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Mouse wheel binding for Windows and Mac
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # For Linux systems (if needed):
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        billing_records = []
        for data in self.billing:
            if self.patient_id == data[2]:
                billing_records.append({
                    "Date": data[1],
                    "Service": data[4],
                    "Amount": data[6],
                    "Paid": data[5],
                    "Payment Date": data[1]
                })

        if not billing_records:
            no_billing_label = tk.Label(scroll_frame, text="No billing record found.", font=("Arial", 14), bg="white", fg="gray")
            no_billing_label.pack(pady=20)
        else:
            for record in billing_records:
                card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=20, pady=15)
                card.pack(fill="x", padx=20, pady=10)

                tk.Label(card, text=f"Date: {record['Date']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"Service/Item Used: {record['Service']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=5)

                billing_info = [
                    ("Amount", record['Amount']),
                    ("Paid", record['Paid']),
                    ("Payment Date", record['Payment Date'])
                ]

                for key, value in billing_info:
                    row = tk.Frame(card, bg="white")
                    row.pack(anchor="w", pady=3)
                    tk.Label(row, text=f"{key}:", font=("Arial", 12, "bold"), width=15, anchor="w", bg="white").pack(side="left")
                    tk.Label(row, text=value, font=("Arial", 12), bg="white").pack(side="left")

                tk.Frame(card, bg="#bdc3c7", height=1).pack(fill="x", pady=10)


    def attachment_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Attachments")

        canvas = tk.Canvas(tab, bg="white")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # Retrieve attachments for the current patient
        attachment_data = fnc.database_con().read("attachment", "*")
        files = [a for a in attachment_data if a[2] == self.patient_id]

        if not files:
            tk.Label(
                scroll_frame,
                text="No attachments found.\nTo upload a Profile Picture the file name must be (example: profilepic.(jpg or png)).",
                font=("Arial", 14),
                bg="white",
                fg="gray"
            ).pack(pady=20)
        else:
            for record in files:
                attachment_id = record[0]
                uploaded_date = record[1]
                filename      = record[3]
                file_blob     = record[4]  # make sure your DB read returns the binary here

                card = tk.Frame(
                    scroll_frame,
                    bg="white",
                    bd=1,
                    relief="solid",
                    padx=20,
                    pady=10
                )
                card.pack(fill="x", padx=20, pady=10)

                tk.Label(
                    card,
                    text=f"File: {filename}",
                    font=("Arial", 12, "bold"),
                    bg="white"
                ).pack(anchor="w")
                tk.Label(
                    card,
                    text=f"Date Uploaded: {uploaded_date}",
                    font=("Arial", 11),
                    bg="white",
                    fg="gray"
                ).pack(anchor="w")

                def download(name=filename, data=file_blob):
                    if not data:
                        messagebox.showerror("Error", "No file data available.")
                        return
                    # pick extension from the original filename
                    ext = os.path.splitext(name)[1] or ".bin"
                    dest_path = filedialog.asksaveasfilename(
                        defaultextension=ext,
                        initialfile=name,
                        filetypes=[("All Files", "*.*")]
                    )
                    if dest_path:
                        try:
                            with open(dest_path, "wb") as f:
                                f.write(data)
                            messagebox.showinfo("Success", "File downloaded successfully.")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save file: {e}")
                
                def delete_attachment():
                    fnc.database_con().Record_delete("attachment", "ID", attachment_id)
                
                tk.Button(
                    card,
                    text="Download",
                    font=("Arial", 11, "bold"),
                    bg="#27ae60",
                    fg="white",
                    relief="flat",
                    command=download
                ).pack(anchor="e", pady=5)
                
                tk.Button(
                    card,
                    text="Delete",
                    font=("Arial", 11, "bold"),
                    bg="#c0392b",
                    fg="white",
                    relief="flat",
                    command=delete_attachment
                ).pack(anchor="e", pady=5)
                
                tk.Frame(card, bg="#bdc3c7", height=1).pack(fill="x", pady=10)
    
    
        




def main(pID, sID):
    print(pID, sID)
    root = tk.Tk()
    app = PatientProfileApp(root, pID, sID)
    root.mainloop()

if __name__ == "__main__":
    # Example patient ID for testing
    main('P123')  # <-- replace 'P123' with an actual patient ID when testing