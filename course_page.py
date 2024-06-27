import subprocess
from tkinter import *
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox
from itertools import cycle

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

# Function to fetch grades and teacher name for a specific course
# Function to fetch grades and teacher name for a specific course
# Function to fetch grades and teacher name for a specific course
def fetch_grades(course_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT teacher.tname, COUNT(student.sid) as enrollment_count
    FROM grade
    JOIN student ON grade.sid = student.sid
    JOIN course ON grade.cid = course.cid
    JOIN teacher ON course.tid = teacher.tid
    WHERE grade.cid = %s
    GROUP BY teacher.tname
    """
    cursor.execute(query, (course_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        teacher_name, enrollment_count = result
        return teacher_name, enrollment_count
    else:
        return None, None


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
    
    course_button = tk.Button(course_frame, text="Get Started", command=lambda c=course_id: open_course_details(c), height=2, width=10, font=('helvetica', 10), bg="purple4", fg="white")
    course_button.pack(pady=20)

def open_course_details(course_id):
    teacher_name, enrollment_count = fetch_grades(course_id)
    
    if teacher_name is not None and enrollment_count is not None:
        # Open a new Toplevel window for the course details
        course_details_window = tk.Toplevel()
        course_details_window.geometry("600x400")
        course_details_window.title("Course Details")

        # Display teacher name
        teacher_label = tk.Label(course_details_window, text=f"Teacher: {teacher_name}", font=('Arial', 16, 'bold'))
        teacher_label.pack(pady=10)

        # Display number of students enrolled
        enrollment_label = tk.Label(course_details_window, text=f"Students Enrolled: {enrollment_count}", font=('Arial', 14))
        enrollment_label.pack(pady=10)

    else:
        messagebox.showerror("Error", "Failed to fetch course details.")
left_column_width = 0.15 * 1366
left_column_frame = Frame(window, width=left_column_width, bg='gray16')
left_column_frame.place(x=0, y=0, relheight=1, anchor='nw')
def close_loading_window():
    loading_window.destroy()  # Destroy the loading window


def open_app2(x):
    global loading_window
    window.destroy
    loading_window = tk.Tk()
    loading_window.title("Loading")
    loading_window.geometry("3200x1200")
    loading_window.configure(bg='white')

    # Display loading animation
    loading_frame = tk.Frame(loading_window, bg='white')
    loading_frame.place(relx=0.5, rely=0.5, anchor='center')
    loading_label = tk.Label(loading_frame, text="Logging in...", font=("Helvetica", 16), bg='white')
    loading_label.pack(pady=20)
    # Infinity symbol animation
    spinner = cycle(['|', '/', '-', '\\'])
    spinner_label = tk.Label(loading_frame, text="", font=("Helvetica", 24), bg='white')
    spinner_label.pack()
    def animate():
        spinner_label.config(text=next(spinner))
        loading_window.after(50, animate)

    animate()
    # Warning message
    warning_label = tk.Label(loading_frame, text="Please do not close the window until we redirect to your new window", font=("Helvetica", 12), fg='grey', bg='white')
    warning_label.pack(pady=20)
    # Show the loading page for 3 seconds before transitioning to the dashboard
    loading_window.after(2300, close_loading_window)
    loading_window.after(2300, open_app2)
    # Open the main application window
    window.destroy()
    subprocess.Popen(['python',x])

def open_app(x):
        window.destroy()
        subprocess.Popen(['python',x])
dash_button = Button(left_column_frame, text="DASHBOARD", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app2('main.py'))
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
header_canvas.create_text(750, 60, text="MY COUSRES", fill='white', font=('Times', 30, 'bold'), anchor='center')

x = Image.open('background3.jpeg')
x = x.resize((180, 120))
y = ImageTk.PhotoImage(x)
header_canvas.create_image(1400, 60, image=y, anchor='center')

window.mainloop()
