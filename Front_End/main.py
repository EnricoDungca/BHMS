import sys 
from tkinter import messagebox

sys.path.insert(0, '\\BHMS')
from Front_End.LoginGUI import Login

def main():
    try:
        Login.main()
    except Exception as e:
        messagebox.showerror("Error", e)

if __name__ == "__main__":
    main()
    