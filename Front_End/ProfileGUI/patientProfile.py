import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from PIL import ImageGrab
import sys
import os

# load local module
sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.PagesGUI import patientRegistration


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

        profile_pic = tk.Canvas(header, width=60, height=60, bg="#ecf0f1", highlightthickness=0)
        profile_pic.create_text(30, 30, text="Photo", font=('Arial', 10, 'bold'), fill="#2c3e50")
        profile_pic.pack(side='left', padx=20, pady=10)

        for datainfo in self.registration:
            if self.patient_id == datainfo[0]:
                info = tk.Frame(header, bg="#2c3e50")
                info.pack(side='left', padx=10)
                tk.Label(info, text=f"{datainfo[2]} {datainfo[3]}", font=('Arial', 20, 'bold'), bg="#2c3e50", fg="white").pack(anchor='w')
                tk.Label(info, text=f"DOB: {datainfo[4]}   |   Gender: {datainfo[5]}   |   Patient ID: {datainfo[0]}",
                        font=('Arial', 12), bg="#2c3e50", fg="white").pack(anchor='w')
        
        back_btn = tk.Button(header, text="Back", font=("Arial", 12, "bold"), fg="white",
                            bg="#e74c3c", relief="flat", command= self.back)
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

    def upload_logo(self):
        path = filedialog.askopenfilename(title="Select Logo Image",
                                          filetypes=[('PNG Images', '*.png'), ('GIF Images', '*.gif'), ('All files', '*.*')])
        if path:
            try:
                self.logo_image = PhotoImage(file=path)
                self.footer_logo_label.configure(image=self.logo_image, text="")
                self.footer_logo_label.image = self.logo_image
            except Exception:
                messagebox.showerror("Error", "Could not load selected image.")

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
                    "Contact": f"{datainfo[6]}\n{datainfo[7]}",
                    "Address": f"{datainfo[8]}\n{datainfo[9]}\n{datainfo[10]}\n{datainfo[11]}\n{datainfo[12]}\n{datainfo[13]}",
                    "Emergency Contact": f"{datainfo[14]} ({datainfo[15]})\n{datainfo[16]}/{datainfo[17]}",
                    "Insurance": f"{datainfo[18]}\n{datainfo[19]}"
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
                    "Type": "Check-up",
                    "Date": data[4],
                    "Provider": data[12],
                    "Diagnosis": data[10],
                    "Medications": data[11]
                })

        # Gather all NSD records
        nsd_records = []
        for data in self.nsd:
            if self.patient_id == data[2]:
                nsd_records.append({
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
                tk.Label(card, text=f"{record['Type']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Date']} - {record['Provider']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"Diagnosis: {record['Diagnosis']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Medications: {record['Medications']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)

            for record in nsd_records:
                card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=15, pady=10)
                card.pack(fill="x", padx=20, pady=10)
                tk.Label(card, text=f"{record['Type']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"{record['Date of Delivery']} - {record['Time of Delivery']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
                tk.Label(card, text=f"Delivery Note: {record['Delivery Note']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Baby Weight: {record['Baby Weight']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
                tk.Label(card, text=f"Apgar Score: {record['Apgar Score']}", font=("Arial", 12), bg="white").pack(anchor="w", pady=2)



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
                text="No attachments found.",
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