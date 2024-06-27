import tkinter as tk
from tkinter import filedialog

def upload_file():
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the selected file path
        label.config(text=f"Selected file: {file_path}")
        messagebox.showinfo("Upload File", "File uploaded successfully")

# Create the main window
'''root = tk.Tk()
root.title("File Upload Example")

# Create and pack the label widget
label = tk.Label(root, text="No file selected")
label.pack(pady=20)

# Create and pack the upload button widget
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

# Run the application
root.mainloop()
'''