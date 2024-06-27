from tkinter import *
import mysql.connector
from datetime import datetime, date
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess

username = "root"
password = "30127"

# MySQL connection code
my_db = mysql.connector.connect(
    host="localhost",
    user=username,
    passwd=password,
    database="futurense"
)
cursor = my_db.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

window = ThemedTk(theme='aqua')
window.geometry("1766x768")
window.title("Futurense")

# Load the background image
bg_image = Image.open("main_page/background.jpg")
bg_image= bg_image.resize((1766,768),Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)


# Create a label to display the background image
bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to create a card button in the left column frame
def create_card_button(window, text, image_path, command, x, y,raise_distance=5):
    icon_image = Image.open(image_path)
    icon_image = icon_image.resize((260, 160), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Create shadow button to create a raised effect
    shadow = Button(window, image=icon_photo, compound='top', borderwidth=0, width=260, height=190)
    shadow.image = icon_photo  # keep a reference to avoid garbage collection
    shadow.place(x=x + raise_distance, y=y + raise_distance)

    # Create main button with text and image
    button = Button(window, text=text, image=icon_photo, compound='top', command=command, borderwidth=0, width=263, height=193, font=('Times', 16, 'bold'))
    button.image = icon_photo  # keep a reference to avoid garbage collection

    # Place button slightly above the shadow to create a raised effect
    button.place(x=x, y=y)

    return button

# Function definitions for button commands
def button_command(x):
    window.destroy()
    subprocess.Popen(['python',x])
create_card_button(window,"Show Courses", "main_page/course.jpg", lambda:button_command('course_page.py'), 210, 190)
create_card_button(window,"Show Assignments", "main_page/assignment.jpg",lambda:button_command('Assignment/main1.py'), 210, 490)
# Toggle function to show/hide the left column

left_column_width = 0.25 * 1366  # 25% of the window width
left_column_frame = Frame(window, width=left_column_width, bg='gray16')
pic=Image.open('main_page/graduated.png')
pic=pic.resize((100,100),Image.LANCZOS)
profile_pic=ImageTk.PhotoImage(pic)
left_pic_label=Label(left_column_frame,image=profile_pic,bg='gray16')
left_column_label = Label(left_column_frame, text="PROFILE", bg='gray16',fg='white', font=('Times', 30,'bold'))
left_name_label = Label(left_column_frame, text="Name:", bg='gray16',fg='white', font=('Times', 14,'bold'))
left_phone_label = Label(left_column_frame, text="Phone no.:", bg='gray16',fg='white', font=('Times', 14,'bold'))
left_age_label = Label(left_column_frame, text="Age:", bg='gray16',fg='white', font=('Times', 14,'bold'))
left_gender_label = Label(left_column_frame, text="Gender:", bg='gray16',fg='white', font=('Times', 14,'bold'))
left_address_label = Label(left_column_frame, text="Address:", bg='gray16',fg='white', font=('Times', 14,'bold'))
left_column_frame.place_forget()
left_column_visible = False

def toggle_left_column():
    global left_column_visible
    if left_column_visible:
        left_column_frame.place_forget()
        left_column_visible = False
    else:
        left_column_frame.place(x=0, y=100, relheight=1, anchor='nw')
        left_column_visible = True

        # Place the labels inside the left column frame
        left_column_label.place(x=70, y=50, anchor='nw')
        left_pic_label.place(x=100, y=120)
        left_name_label.place(x=50, y=250, anchor='nw')
        left_phone_label.place(x=50, y=300, anchor='nw')
        left_address_label.place(x=50, y=350, anchor='nw')
        left_age_label.place(x=50, y=400, anchor='nw')
        left_gender_label.place(x=50, y=450, anchor='nw')

        # Read the user_entry from the text file
        with open("log.txt", "r") as file:
            user = file.read()

        # Fetch the student's information from the database
        query = "SELECT * FROM student WHERE email = %s"
        cursor.execute(query, (user,))
        result = cursor.fetchone()

        if result:
            # Display the student's information in the left column
            left_name_label.config(text=f"Name: {result[1]}")
            left_phone_label.config(text=f"Phone no.: {result[2]}")
            left_address_label.config(text=f"Age: {result[3]}")
            left_age_label.config(text=f"Gender: {result[4]}")
            left_gender_label.config(text=f"Email: {result[5]}")
        else:
            messagebox.showerror("Error", "Student not found")
# Load the account icon
icon_image = Image.open("main_page/account.png")
icon_image = icon_image.resize((50, 50), Image.LANCZOS)  # Resize the image to 50x50
icon_photo = ImageTk.PhotoImage(icon_image)

# Create a button with the icon for toggling left column visibility
toggle_button = Button(window, image=icon_photo, command=toggle_left_column, borderwidth=0, bg="goldenrod2")
toggle_button.place(x=1450, y=150)  # Place the button in the middle below the header

# Create card buttons directly on the window
create_card_button(window,"Show Attendance", "main_page/attendance.jpg", lambda:button_command('attendance.py'), 655, 320)
create_card_button(window,"Show Grades", "main_page/grades.jpg", lambda:button_command('grade.py'), 1110, 490)
create_card_button(window,"Show Exams", "main_page/exams.jpg", lambda:button_command('exam.py'), 1110, 190)
header_frame = Frame(window, height=120, bg='black')
header_frame.place(x=0, y=0, relwidth=1)

# Create a Canvas within the header frame
header_canvas = Canvas(header_frame, height=120, bg='black')
header_canvas.pack(fill='both', expand=True)

# Load the image
image = Image.open('background2.jpeg')
image = image.resize((230, 150), Image.LANCZOS)  # Adjust size as necessary
photo = ImageTk.PhotoImage(image)

# Add image to the Canvas
header_canvas.create_image(100, 60, image=photo, anchor='center')  # Adjust position as necessary

# Add text to the Canvas
header_canvas.create_text(775, 60, text="Learning Management System", fill='white', font=('Times', 30, 'bold'), anchor='center')  # Adjust position as necessary
yellow_line_frame = Frame(window, height=2, bg='goldenrod2')
yellow_line_frame.place(x=0, y=120, height=10,relwidth=1)
def logout():
    window.destroy()
    subprocess.Popen(['python', 'project.py'])
logout_button = Button(header_frame, text="Logout", command=logout, bg='firebrick1', fg='white', font=('Times', 16, 'bold'), borderwidth=0)
logout_button.place(relx=1.0, x=-120, y=25, anchor='nw')
window.mainloop()
# mainloop ended
