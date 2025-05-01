import sys 
from tkinter import messagebox

sys.path.insert(0, '\\BHMS')
from Back_End import systemfnc as fnc
from Front_End.LoginGUI import Login

def main():
    try:
        if fnc.database_con().check_connection():
            Login.main()
    except Exception as e:
        messagebox.showerror("Error", e)

if __name__ == "__main__":
    main()
    