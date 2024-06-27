from tkinter import *
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess
# MySQL connection details
username = "root"
password = "30127"
database = "futurense"

# Function to connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user=username,
        passwd=password,
        database=database
    )

def fetch_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT cid, cname FROM course")
    courses = cursor.fetchall()
    conn.close()
    return courses

# Function to fetch exam details for the logged-in student
def fetch_exam_details(student_email):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    SELECT 
        e.ename, 
        s.sname AS student_name, 
        e.date, 
        c.cname AS course_name, 
        t.tname AS teacher_name,
        g.grades AS grade
    FROM exams e
    JOIN student s ON e.sid = s.sid
    JOIN course c ON e.cid = c.cid
    JOIN teacher t ON c.tid = t.tid
    LEFT JOIN Grade g ON e.eid = g.eid
    WHERE s.email = %s
    """
    cursor.execute(query, (student_email,))
    exam_details = cursor.fetchall()
    conn.close()
    return exam_details

# Function to read logged-in student's email from log.txt
def read_logged_in_email():
    with open("log.txt", "r") as f:
        logged_in_email = f.readline().strip()  # Read the first line (assuming only one email stored)
    return logged_in_email

# Initialize main window
window = tk.Tk()
window.geometry("1366x768")
window.title("Futurense")

# Configure main window background to be transparent
window.configure(bg='white')

logo_path = "login_page/lms-2.ico"
window.iconbitmap(logo_path)

# Create frame1 with white background
frame1 = tk.Frame(window, bg="white")
frame1.place(relx=0.57, rely=0.553, anchor=tk.CENTER, width=1100, height=500)

# Background image for frame1
'''frame1_bg_image = Image.open("white4.png")
frame1_bg_image = frame1_bg_image.resize((1400, 620))
frame1_bg_photo = ImageTk.PhotoImage(frame1_bg_image)

# Create a label inside frame1 to display the background image
frame1_label = tk.Label(frame1, image=frame1_bg_photo)
frame1_label.place(x=0, y=0, relwidth=1, relheight=1)'''

# Fetch courses from the database
courses = fetch_courses()

# Calculate uniform size for all frames
frame_width = 332
frame_height = 150

# Calculate gaps between columns and rows
column_gap = 120
row_gap = (576 - 2 * frame_height) / 3  # Gap between rows based on available height

# Left column menu
left_column_width = 0.15 * 1366
left_column_frame = Frame(window, width=left_column_width, bg='gray16')
left_column_frame.place(x=0, y=0, relheight=1, anchor='nw')
def open_app(x):
    window.destroy()
    subprocess.Popen(['python', x])

dash_button = Button(left_column_frame, text="DASHBOARD", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('main.py'))
dash_button.place(x=20, y=150)
assin_button = Button(left_column_frame, text="ASSIGNMENT", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('main.py'))
assin_button.place(x=20, y=250)
attendance_button = Button(left_column_frame, text="ATTENDANCE", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('attendance.py'))
attendance_button.place(x=20, y=350)
dash_button = Button(left_column_frame, text="COURSES", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('course_page.py'))
dash_button.place(x=20, y=450)
dash_button = Button(left_column_frame, text="GRADES", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('grade.py'))
dash_button.place(x=20, y=550)
# Function to toggle left column visibility
left_column_visible = True
def toggle_left_column():
    global left_column_visible
    if left_column_visible:
        left_column_frame.place_forget()
        left_column_visible = False
    else:
        left_column_frame.place(x=0, y=0, relheight=1, anchor='nw')
        left_column_visible = True

toggle_button = tk.Button(window, text="☰", command=toggle_left_column, borderwidth=0, bg="black", fg="white")
toggle_button.place(x=1500, y=150)

# Header frame
header_frame = Frame(window, height=120, bg='black')
header_frame.place(x=0, y=0, relwidth=1)
header_canvas = tk.Canvas(header_frame, height=120, bg='black')
header_canvas.pack(fill='both', expand=True)
image = Image.open('background2.jpeg')
image = image.resize((230, 150))
photo = ImageTk.PhotoImage(image)
header_canvas.create_image(100, 60, image=photo, anchor='center')
header_canvas.create_text(750, 60, text="EXAMS LMS FUTURENSE", fill='white', font=('Times', 30, 'bold'), anchor='center')

x = Image.open('background3.jpeg')
x = x.resize((180, 120))
y = ImageTk.PhotoImage(x)
header_canvas.create_image(1400, 60, image=y, anchor='center')

# Function to display exam details in frame1 for the logged-in student
def display_exam_details():
    logged_in_email = read_logged_in_email()
    exams = fetch_exam_details(logged_in_email)

    # Create a frame to hold the table
    table_frame = Frame(frame1, bg="white")
    table_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Define column headers
    headers = ["EXAM NAME", "STUDENT NAME", "DATE", "Course Name", "Teacher Name", "Grade", "Status"]
    for col, header in enumerate(headers):
        label = Label(table_frame, text=header, bg="purple4", fg="white",font=("Helvetica", 13, "bold"), borderwidth=2, relief="groove",pady=12)
        label.grid(row=0, column=col, sticky="nsew")

    # Prepare data with "Completed" status
    modified_exams = []
    for exam in exams:
        modified_exam = list(exam)  # Convert tuple to list
        modified_exam.append("Completed")  # Add "Completed" status
        modified_exams.append(modified_exam)

    # Display data
    for row, exam in enumerate(modified_exams, start=1):
        for col, value in enumerate(exam):
            label = Label(table_frame, text=value, bg="goldenrod2", fg="black",font=("Helvetica", 13), borderwidth=2, relief="groove",pady=12)
            label.grid(row=row, column=col, sticky="nsew")

# Call the function to display exam details for the logged-in student
display_exam_details()

window.mainloop()

