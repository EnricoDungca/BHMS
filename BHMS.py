import os, sys, datetime
from tkinter import messagebox


# Ensure relative import paths work after PyInstaller bundling
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "BHMS"))

from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login

date_now = datetime.date.today()

def main(): 
    try:
        if fnc.database_con().check_connection():
            if date_now.day == 1:
                fnc.database_con().database_backup()
            Login.main()
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
