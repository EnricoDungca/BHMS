import tkinter as tk
from tkinter import filedialog

def choose_file():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file picker dialog
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
    )

    if file_path:
        return file_path
    else:
        print("No file selected.")

# Example usage
choose_file()
