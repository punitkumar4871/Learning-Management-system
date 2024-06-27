import subprocess
from tkinter import *
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox

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

# Function to fetch courses from the database
def fetch_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT cid, cname FROM course")
    courses = cursor.fetchall()
    conn.close()
    return courses

# Function to fetch grades for a specific course
def fetch_grades(course_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    SELECT student.sname, grade.grades
    FROM grade
    JOIN student ON grade.sid = student.sid
    WHERE grade.cid = %s
    """
    cursor.execute(query, (course_id,))
    grades = cursor.fetchall()
    conn.close()
    return grades

# Function to open course page and display details
def open_course_page(course_id):
    # Read email from log file
    with open("log.txt", "r") as file:
        user_email = file.read().strip()  # Read and strip to remove any leading/trailing whitespace

    # Fetch student information based on email
    conn = connect_db()
    cursor = conn.cursor()
    query_student = """
    SELECT student.sid, student.sname, grade.grades, course.cname, teacher.tname,teacher.tid
    FROM student
    JOIN grade ON student.sid = grade.sid
    JOIN course ON grade.cid = course.cid
    JOIN teacher ON course.tid = teacher.tid
    WHERE student.email = %s AND grade.cid = %s
    """
    cursor.execute(query_student, (user_email, course_id))
    student_info = cursor.fetchone()
    conn.close()

    if student_info:
        student_sid = student_info[0]
        student_name = student_info[1]
        student_grade = student_info[2]
        course_name = student_info[3]
        teacher_name = student_info[4]
        t_id=student_info[5]

        # New window for course details
        marks_window = tk.Toplevel()
        marks_window.title("Course Details")
        marks_window.configure(bg="goldenrod2")
        marks_window.geometry("1024x768")

        # HEADER1
        header_frame1 = Frame(marks_window, height=50, bg='black')
        header_frame1.place(x=0, y=462, relwidth=1)
        header_canvas1 = Canvas(header_frame1, height=50, bg='black')
        header_canvas1.pack(fill='both', expand=True)

        # HEADER2
        header_frame2 = Frame(marks_window, height=75, bg='black')
        header_frame2.place(x=0, y=0, relwidth=1)
        header_canvas2 = Canvas(header_frame2, height=75, bg='black')
        header_canvas2.pack(fill='both', expand=True)

        # Set text
        header_canvas1.create_text(760, 30, text=f"MY GRADE", fill='white', font=('Times', 30, 'bold'), anchor='center')
        header_canvas2.create_text(750, 50, text="LEADERBOARD", fill='white', font=('Times', 30, 'bold'), anchor='center')

        # Display student information and grades for the selected course
        results_frame = tk.Frame(marks_window, bg="white")
        results_frame.place(relx=0.05, rely=0.095, relwidth=0.9, relheight=0.489)

        left_frame = Frame(results_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame = Frame(results_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Blank frame at the bottom (20% coverage)
        blank_frame = tk.Frame(marks_window, bg="white")
        blank_frame.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.38)

        # Labels for student information
        info_label1 = Label(blank_frame, text=f"SID: {student_sid}", bg='gray16', fg='white', font=('Times', 18, 'bold'))
        info_label2 = Label(blank_frame, text=f"Name: {student_name}", bg='white', fg='black', font=('Times', 18, 'bold'))
        info_label3 = Label(blank_frame, text=f"Grade: {student_grade}", bg='white', fg='black', font=('Times', 18, 'bold'))
        info_label4 = Label(blank_frame, text=f"Course: {course_name}", bg='white', fg='black', font=('Times', 18, 'bold'))
        info_label5 = Label(blank_frame, text=f"Teacher: {teacher_name}", bg='white', fg='black', font=('Times', 18, 'bold'))
        info_label6 = Label(blank_frame, text=f"Tid: {t_id}", bg='white', fg='black', font=('Times', 18, 'bold'))

        # Place labels for student information
        info_label1.place(x=143, y=220)
        info_label2.place(x=350, y=20)
        info_label3.place(x=350, y=190)
        info_label5.place(x=800, y=20)
        info_label6.place(x=800, y=100)
        info_label4.place(x=350, y=100)



        # Profile photo
        # Load image for profile (assuming you want it in the blank frame)
        profile_image = Image.open("grade_page/profile.png")  # Replace with your image file
        profile_image = profile_image.resize((200, 200))  # Resize image as needed
        profile_photo = ImageTk.PhotoImage(profile_image)

        # Create a label to display the profile image
        profile_label = tk.Label(blank_frame, image=profile_photo, bg="white")
        profile_label.image = profile_photo  # Keep a reference
        profile_label.pack(pady=10, anchor="nw", padx=70)

        # Headers for columns
        name_label = Label(left_frame, text="Name", bg="white", font=('Helvetica', 12, 'bold'), anchor="w", width=30)
        name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        grade_label = Label(right_frame, text="Grade", bg="white", font=('Helvetica', 12, 'bold'), anchor="e", width=10)
        grade_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        # Fetch and display grades for the selected course
        grades = fetch_grades(course_id)
        for idx, (student_name, grade) in enumerate(grades, start=1):
            student_label = Label(left_frame, text=student_name, bg="white", font=('Helvetica', 12), anchor="w", width=30)
            student_label.grid(row=idx, column=0, sticky="w", padx=5, pady=5)
            grade_label = Label(right_frame, text=grade, bg="white", font=('Helvetica', 12), anchor="e", width=10)
            grade_label.grid(row=idx, column=0, sticky="e", padx=5, pady=5)

    else:
        messagebox.showerror("Error", "Student not found for this course.")
# Initialize main window
window = tk.Tk()
window.geometry("1366x768")
window.title("Futurense")

# Background image for the main window
bg_image = Image.open("grade_page/white4.png")
bg_image = bg_image.resize((1550, 768))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(window, width=1366, height=768)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Configure main window background to be transparent
window.configure(bg='black')

logo_path = "login_page/lms-2.ico"
window.iconbitmap(logo_path)

# Create frame1 with white background
frame1 = tk.Frame(window, bg="white")
frame1.place(relx=0.62, rely=0.70, anchor=tk.CENTER, width=1400, height=620)

# Background image for frame1
frame1_bg_image = Image.open("grade_page/white4.png")
frame1_bg_image = frame1_bg_image.resize((1400, 620))
frame1_bg_photo = ImageTk.PhotoImage(frame1_bg_image)

# Create a label inside frame1 to display the background image
frame1_label = tk.Label(frame1, image=frame1_bg_photo)
frame1_label.place(x=0, y=0, relwidth=1, relheight=1)

# Fetch courses from the database
courses = fetch_courses()

# Calculate uniform size for all frames
frame_width = 332
frame_height = 150

# Calculate gaps between columns and rows
column_gap = 120
row_gap = (576 - 2 * frame_height) / 3  # Gap between rows based on available height

# Create course frames and buttons dynamically
for idx, (course_id, course_name) in enumerate(courses):
    row = idx // 3
    col = idx % 3
    
    x_position = col * (frame_width + column_gap)
    y_position = row * (frame_height + row_gap)
    
    course_frame = tk.Frame(frame1, bg="goldenrod2", width=frame_width, height=frame_height)
    course_frame.place(x=x_position, y=y_position, width=frame_width, height=frame_height)
    
    course_label = tk.Label(course_frame, text=course_name, bg="goldenrod2", fg="black", font=('times', 15, 'bold'))
    course_label.pack(pady=25, padx=10)
    
    course_button = tk.Button(course_frame, text="Show Result", command=lambda cid=course_id: open_course_page(cid), height=2, width=10, font=('helvetica', 10), bg="purple4", fg="white")
    course_button.pack(pady=20)

# Left column menu
left_column_width = 0.15 * 1366
left_column_frame = Frame(window, width=left_column_width, bg='gray16')
left_column_frame.place(x=0, y=0, relheight=1, anchor='nw')
def open_app(x):
        window.destroy()
        subprocess.Popen(['python',x])
dash_button = Button(left_column_frame, text="DASHBOARD", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('main.py'))
dash_button.place(x=20, y=150)
assin_button = Button(left_column_frame, text="ASSIGNMENT", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('Assignment/main1.py'))
assin_button.place(x=20, y=250)
attendance_button = Button(left_column_frame, text="ATTENDANCE", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('attendance.py'))
attendance_button.place(x=20, y=350)
assin_button = Button(left_column_frame, text="EXAMS", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('exam.py'))
assin_button.place(x=20, y=450)
attendance_button = Button(left_column_frame, text="COURSES", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('grade.py'))
attendance_button.place(x=20, y=550)

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

toggle_button = tk.Button(window, text="☰", command=toggle_left_column, borderwidth=0, bg="white", fg="black")
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
header_canvas.create_text(750, 60, text="COURSES RESULT FUTURENSE LMS", fill='white', font=('Times', 30, 'bold'), anchor='center')

x = Image.open('background3.jpeg')
x = x.resize((180, 120))
y = ImageTk.PhotoImage(x)
header_canvas.create_image(1400, 60, image=y, anchor='center')

window.mainloop()
