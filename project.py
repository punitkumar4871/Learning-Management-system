from tkinter import *
import mysql.connector
from datetime import datetime
from datetime import date
import ttkbootstrap as tb
from tkinter import Frame
from tkinter import ttk
from tkinter import messagebox
import random

username = "root"
password = "30127"

# MySQL connection code
my_db = mysql.connector.connect(
    host="localhost",
    user=username,
    passwd=password,
    database="futurense"
)
cursor= my_db.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
from PIL import Image, ImageTk
# to see all table avaiable

'''for course in tables:
  print(f"Table: {course[0]}")  # Assuming table name is in the first column

  # Execute a query to fetch all data (replace with specific query if needed)
  cursor.execute(f"SELECT * FROM {course[0]}")
  data = cursor.fetchall()

  # Print data (handle potential formatting for large datasets)
  for row in data:
    print(row)  # This might print large data in a single line, adjust for readability

  print("\n")  # Add a newline between tables'''
window = tb.Window()
window.geometry("1366x768")
window.title("Futurense")
logo_path = "login_page/lms-2.png"      
window.iconbitmap(logo_path)
window.style.configure('my.Treeview', rowheight=25)
def generate_otp():
    return str(random.randint(1000, 9999))
def reset_password():
    entered_otp = otp_entry.get()
    if entered_otp == generated_otp:
        reset_window = tb.Toplevel(forgot_window)
        reset_window.title("Password Reset")
        
        reset_window.iconbitmap(logo_path)
        reset_window.geometry("1366x768")
        background_image1 = Image.open("login_page/password1.png")
        background_image1 = background_image1.resize((1900, 1100)) 
        background_photo1 = ImageTk.PhotoImage(background_image1)
        background_label = tb.Label(reset_window, image=background_photo1)
        background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    
        background_label1 = tb.Label(forgot_window, image=background_photo1)
        background_label1.place(relx=0, rely=0, relwidth=1, relheight=1)
        new_centered_frame = ttk.Frame(reset_window, style='mystyle.TFrame')
        new_centered_frame.place(relx=0.5, rely=0.5, anchor="center")

        
        reset_label1=tb.Label(new_centered_frame,text="Enter new password:-",font=("Times", 20), foreground='sky blue').grid(row=0,column=0)
        new_label_entry = ttk.Entry(new_centered_frame, font=("Times", 14), width=30)
        new_label_entry.grid(row=1, column=0, padx=20, pady=10)

        
        confirm_label = tb.Label(new_centered_frame, text="confirmation:", font=("Times", 20), foreground='sky blue').grid(row=2, column=0)
        confirm_var = StringVar(value="No")
        confirm_yes = ttk.Radiobutton(new_centered_frame, text="Yes", variable=confirm_var, value="Yes")
        confirm_no = ttk.Radiobutton(new_centered_frame, text="No", variable=confirm_var, value="No")
        confirm_yes.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        confirm_no.grid(row=3, column=0, padx=20, pady=10, sticky="e")

        def confirm_reset():
            if confirm_var.get() == "Yes":
                new_password = new_label_entry.get()
                if new_password:
                    try:
                        # Update the password in the database
                        email = forgot_username_entry.get()
                        query = "UPDATE student SET password = %s WHERE email = %s"
                        cursor.execute(query, (new_password, email))
                        my_db.commit()
                        messagebox.showinfo("Success", "Password has been reset successfully!")
                        reset_window.destroy()
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"Failed to update password: {err}")
                else:
                    messagebox.showerror("Error", "Please enter a new password")
            else:
                messagebox.showerror("Error", "Please confirm password reset")

        reset_password_button = ttk.Button(new_centered_frame, text="Reset Password", command=confirm_reset)
        reset_password_button.grid(row=4, column=0, padx=20, pady=20, ipadx=20, ipady=10)
        icon_path = "login_page/lms3.png"
        icon_image1 = Image.open(icon_path)
        icon_image1 = icon_image.resize((200, 100))  
        photo_icon2 = ImageTk.PhotoImage(icon_image1)
    
        icon_title_frame1 = tb.Frame(reset_window)  
        icon_title_frame1.pack(anchor='nw', padx=10, pady=10)
        icon_label2 = tb.Label(icon_title_frame1, image=photo_icon2)
        icon_label2.image = photo_icon2
        icon_label2.pack(side="left")
        background_label1.lower()

        reset_window.mainloop()
        
        
    else:
        messagebox.showerror("Error", "Invalid OTP")
def get_otp():
    email = forgot_username_entry.get()
    phonenumber = forgot_mobile_entry.get()
    
    if not email or not phonenumber:
        messagebox.showerror("Error", "Please enter both username and mobile number")
        return
    
    query = "SELECT * FROM student WHERE email = %s AND phonenumber = %s"
    cursor.execute(query, (email,phonenumber))
    result = cursor.fetchone()
    
    if result:
        global generated_otp
        generated_otp = generate_otp()
        print(f"Generated OTP: {generated_otp}")  # For debugging purposes, remove this in production
        messagebox.showinfo("Success", "OTP sent to your mobile number")
    else:
        messagebox.showerror("Error", "Invalid username or mobile number")
import subprocess  # Import subprocess to open the main.py script

def login():
    global user
    user = user_entry.get()
    password = password_entry.get()

    if not user or not password:
        messagebox.showerror("Error", "Please enter valid username or password")
        return

    query = "SELECT * FROM student WHERE email = %s AND password = %s"
    cursor.execute(query, (user, password))
    result = cursor.fetchone()

    if result:
        with open("log.txt", "w") as file:
            file.write(user)

        messagebox.showinfo("Success", "Login successful!")
        window.destroy()  # Close the login window
        open_main_app()  # Open the main application window

    else:
        messagebox.showerror("Error", "Invalid username or password")
        
def open_main_app():
    subprocess.Popen(['python', 'main.py'])
def forgot_password():
    global forgot_window, forgot_username_entry, forgot_mobile_entry, otp_entry
    forgot_window = tb.Toplevel(window)
    forgot_window.title("Forgot Password")
    forgot_window.geometry("1366x768")  
    forgot_window.iconbitmap(logo_path)
    
    # Background image
    background_image = Image.open("login_page/password reset.png")
    background_image = background_image.resize((2000, 1200)) 
    background_photo = ImageTk.PhotoImage(background_image)
    
    background_label = tb.Label(forgot_window, image=background_photo)
    background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    centered_frame = ttk.Frame(forgot_window, style='mystyle.TFrame')
    centered_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Label for username entry
    forgot_label = tb.Label(centered_frame, text="Enter your username to reset password:", font=("Times", 12), background='white', foreground='blue')
    forgot_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    # Username entry field (styled)
    forgot_username_entry = ttk.Entry(centered_frame, font=("Times", 14), width=30)
    forgot_username_entry.grid(row=1, column=0, padx=20, pady=10)

    # Label for mobile number entry
    forgot_label = tb.Label(centered_frame, text="Enter your mobile number to reset password:", font=("Times", 12), background='white', foreground='blue')
    forgot_label.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
    
    # Mobile number entry field (styled)
    forgot_mobile_entry = ttk.Entry(centered_frame, font=("Times", 14), width=30)
    forgot_mobile_entry.grid(row=3, column=0, padx=20, pady=10)

    # Generate OTP button
    forgot_button = ttk.Button(centered_frame, text="Get OTP", style="CustomButton.TButton", command=get_otp)
    forgot_button.grid(row=4, column=0, padx=20, pady=20, ipadx=20, ipady=10, sticky="nsew")

    # OTP section
    otp_label = tb.Label(centered_frame, text="Enter the OTP:", font=("Times", 12), background='white', foreground='blue')
    otp_label.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
    
    otp_entry = ttk.Entry(centered_frame, font=("Times", 14), width=30)
    otp_entry.grid(row=6, column=0, padx=20, pady=10)
    
    # Reset password button
    reset_button = ttk.Button(centered_frame, text="Reset Password", style="CustomButton.TButton", command=reset_password)
    reset_button.grid(row=7, column=0, padx=20, pady=20, ipadx=20, ipady=10, sticky="nsew")
    
    # Icon image
    icon_path = "login_page/lms3.png"
    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((200, 100))  
    photo_icon1 = ImageTk.PhotoImage(icon_image)
    
    icon_title_frame = tb.Frame(forgot_window)  
    icon_title_frame.pack(anchor='nw', padx=10, pady=10)
    icon_label = tb.Label(icon_title_frame, image=photo_icon1)
    icon_label.image = photo_icon1  # Keep a reference to the image
    icon_label.pack(side="left")
    
    # Ensure the background image is behind other widgets
    background_label.lower()

    forgot_window.mainloop()


# Load the image
icon_path="login_page/lms3.png"
image = Image.open("login_page/lms1.png")
image = image.resize((1900// 2, 1300))  # Resize image to half width
photo = ImageTk.PhotoImage(image)

# Create a label for the image
image_label = tb.Label(window, image=photo)
image_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)  # Position image on left half

####### Create login form on the right side
login_frame = ttk.Frame(window)
login_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
style = ttk.Style(window)
style.configure('mystyle.TFrame', background='white')

# Apply the style to the login frame
login_frame.configure(style='mystyle.TFrame')

# Title label

icon_image = Image.open(icon_path)
icon_size = (300, 100)  # Adjust size as needed
icon_image = icon_image.resize(icon_size)  # Resize icon image
photo_icon = ImageTk.PhotoImage(icon_image)
icon_title_frame = tb.Frame(login_frame)  # Adjust background color if needed
icon_title_frame.pack(anchor='nw',padx=10, pady=70)
icon_label = tb.Label(icon_title_frame, image=photo_icon)
icon_label.pack(side="left")  # Pack the icon on the left side

title_label = tb.Label(login_frame, text="WELCOME BACK", font=("Times", 50,"bold") ,background='white', foreground='black')
title_label.pack(anchor='nw',padx=10,pady=0)  # Add padding for spacing

title_label5 = tb.Label(login_frame, text="Nice to see you!\nPlease log in with your account.", font=("Times", 24),background='white', foreground='black')
title_label5.pack(padx=0,pady=20)  # Add padding for spacing


# Username label and entry
user_label = Label(login_frame, text="Username", font=("Times", 12,'bold'),bg='white',fg='black')
user_label.pack(pady=10)
user_entry = ttk.Entry(login_frame, font=("Helvetica", 14), width=50)
user_entry.pack(pady=5)

password_label = Label(login_frame, text="Password", font=("Times", 12,'bold'),bg='white',fg='black')
password_label.pack(pady=10)
password_entry = ttk.Entry(login_frame, font=("Helvetica", 14), show="*", width=50)
password_entry.pack(pady=5)


'''# Additional entry fields (replace with your labels as needed)
email_label = tb.Label(login_frame, text="Email:")
email_label.pack(pady=10, padx=20)
email_entry = tb.Entry(login_frame)
email_entry.pack(pady=5, padx=20)

phone_label = tb.Label(login_frame, text="Phone:")
phone_label.pack(pady=10, padx=20)
phone_entry = tb.Entry(login_frame)
phone_entry.pack(pady=5, padx=20)'''

# Forgot password button (aligned left)
forgot_password_button = tb.Button(login_frame, text="Forgot Password?", command=forgot_password)
forgot_password_button.pack(pady=10, padx=10, anchor="e")  # Pack with left alignment

'''
login_button = tb.Button(login_frame, text="Login", command=login)
login_button.pack(pady=15, padx=20, ipadx=30, ipady=10)  # Add padding and interior padding

'''
# Create a style
button_style = ttk.Style()
button_style.configure("CustomButton.TButton", font=("Times", 14),)  # Add background color if desired
login_button = ttk.Button(login_frame, text="Login", style="CustomButton", command=login).pack(pady=15, padx=20, ipadx=30, ipady=10)

# Create the login button with the custom style
login_button = ttk.Button(login_frame, text="Login", style="CustomButton", command=login)
# Focus on username entry for initial interaction

user_entry.focus_set()


# Run the main loop
window.mainloop()
