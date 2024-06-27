import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import subprocess

class CoursesApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Courses Application")
        self.geometry("1200x700")
        self.configure(background='white')

        # Connect to your MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="30127",
            database="futurense"
        )

        # Create a cursor to execute queries
        self.cursor = self.conn.cursor()

        # Create top canvas for logo and dashboard options
        self.header_height = 150  # Adjust header height here
        self.top_canvas = tk.Canvas(self, bg='black', height=self.header_height)
        self.top_canvas.pack(side=tk.TOP, fill=tk.X)

        # Right logo
        logo_path = "background3.jpeg"
        logo = Image.open(logo_path)
        logo = logo.resize((150, 100), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(logo)

        # Left logo
        left_logo_path = "background2.jpeg"
        left_logo = Image.open(left_logo_path)
        left_logo = left_logo.resize((200, 120), Image.LANCZOS)
        self.left_logo_image = ImageTk.PhotoImage(left_logo)

        # Position logos on the header canvas
        left_logo_label = tk.Label(self.top_canvas, image=self.left_logo_image, bg='black')
        left_logo_label.image = self.left_logo_image
        left_logo_label.place(relx=0.07, rely=0.5, anchor='center')

        right_logo_label = tk.Label(self.top_canvas, image=self.logo_image, bg='black')
        right_logo_label.image = self.logo_image
        right_logo_label.place(relx=0.94, rely=0.5, anchor='center')

        # Add the "MY COURSES" label in the middle of the top canvas
        courses_label = tk.Label(self.top_canvas, text="MY COURSES", bg='black', fg='white', font=('Arial', 24, 'bold'))
        courses_label.place(relx=0.5, rely=0.5, anchor='center')

        # Sidebar frame
        self.sidebar_frame = tk.Frame(self, bg='black', width=200)  # Changed bg to black
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        sidebar_buttons = [
            ("Dashboard", lambda: self.open_app('main.py')),
            ("Attendance", lambda:self.open_app('attendance.py')),
            ("Assignment", lambda:self.open_app('Assignment/main1.py')),
            ("Exams", lambda:self.open_app('exam.py')),
            ("Grades", lambda:self.open_app('grade.py'))
        ]
        
        for btn_text, command_func in sidebar_buttons:
            btn = tk.Button(self.sidebar_frame, text=btn_text, bg='black', fg='white', font=('Arial', 12), command=command_func)
            btn.pack(fill=tk.X, pady=20, padx=20)  # Adjusted padding for vertical spacing

        self.sidebar_visible = True

        # Main content frame for courses
        self.courses_frame = tk.Frame(self, bg='white')  # Change bg to white
        self.courses_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
         
        # Fetch courses data from MySQL database
        self.fetch_courses_data()

        # Create course cards
        self.create_course_cards(self.courses_frame, self.courses_data)

        # Bind the window resize event to the on_resize method
        self.bind("<Configure>", self.on_resize)

    def fetch_courses_data(self):
        # Example query to fetch course data from MySQL
        self.cursor.execute("SELECT cid, cname, tid FROM course")
        self.courses_data = self.cursor.fetchall()  # Assuming a list of tuples (cid, cname, tid)

    def open_app(self,x):
        self.destroy()
        subprocess.Popen(['python',x])

    def create_course_cards(self, parent, courses):
        self.course_cards = []

        # Calculate padding and number of columns
        padding_x = 20
        padding_y = 40
        num_columns = 2  # Adjust as needed

        for i, course in enumerate(courses):
            # Create a frame for each course
            card = tk.Frame(parent, bg='goldenrod2', bd=2, relief=tk.RAISED)

            # Create labels and button inside the card
            title_label = tk.Label(card, text=course[1], bg='goldenrod2', font=('Arial', 14, 'bold'))
            title_label.pack(pady=5)

            open_btn = tk.Button(card, text="Get Started", font=('Arial', 12), bg='blue', fg='white', padx=10, pady=5, command=lambda c=course: self.open_course(c))
            open_btn.pack(pady=5)

            # Pack the card frame into the parent with grid layout
            card.grid(row=i//num_columns, column=i%num_columns, padx=padding_x, pady=padding_y, sticky="nsew")

            # Store the card in the list
            self.course_cards.append(card)

        # Configure rows and columns to expand evenly
        for i in range(len(courses)//num_columns + len(courses)%num_columns):
            parent.grid_rowconfigure(i, weight=1)
        for i in range(num_columns):
            parent.grid_columnconfigure(i, weight=1)

    def on_resize(self, event):
        # Calculate number of columns based on width
        width = self.courses_frame.winfo_width()
        if width < 400:
            columns = 1
        elif width < 800:
            columns = 2
        else:
            columns = 3

        # Re-grid the cards based on new number of columns
        for index, card in enumerate(self.course_cards):
            card.grid_forget()
            card.grid(row=index//columns, column=index%columns, padx=20, pady=40, sticky="nsew")

        # Configure rows and columns to expand evenly
        for i in range(len(self.course_cards)//columns + len(self.course_cards)%columns):
            self.courses_frame.grid_rowconfigure(i, weight=1)
        for i in range(columns):
            self.courses_frame.grid_columnconfigure(i, weight=1)

    def open_course(self, course):
        # Fetch additional details about the course
        self.cursor.execute("SELECT tname FROM teacher WHERE tid = %s", (course[2],))
        result = self.cursor.fetchone()

        if result:
            teacher_name = result[0]
            self.cursor.execute("SELECT COUNT(*) FROM student_course WHERE cid = %s", (course[0],))
            enrollment_count = self.cursor.fetchone()[0]

            # Open a new Toplevel window for the course details
            CourseDetailsWindow(self, course[1], teacher_name, enrollment_count)
        else:
            print(f"No teacher found for course {course[1]}")

class CourseDetailsWindow(tk.Toplevel):
    def __init__(self, master, course_name, teacher_name, enrollment_count):
        super().__init__(master)
        self.geometry("1200x700")
        self.title(course_name)

        # Configure the header
        header_frame = tk.Frame(self, height=130, background='black')
        header_frame.pack(fill=tk.X)

        # Left logo
        left_logo_path = "background2.jpeg"
        left_logo = Image.open(left_logo_path)
        left_logo = left_logo.resize((280, 150), Image.LANCZOS)
        self.left_logo_image = ImageTk.PhotoImage(left_logo)

        left_logo_label = tk.Label(header_frame, image=self.left_logo_image, bg='black')
        left_logo_label.image = self.left_logo_image
        left_logo_label.pack(side=tk.LEFT, padx=0, pady=10)

        # Right logo
        right_logo_path = "background3.jpeg"
        right_logo = Image.open(right_logo_path)
        right_logo = right_logo.resize((210, 100), Image.LANCZOS)
        self.right_logo_image = ImageTk.PhotoImage(right_logo)

        right_logo_label = tk.Label(header_frame, image=self.right_logo_image, bg='black')
        right_logo_label.image = self.right_logo_image
        right_logo_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # Display teacher name
        teacher_label = tk.Label(self, text=f"Teacher: {teacher_name}", font=('Georgia', 16,'bold'))
        teacher_label.pack(pady=10)

        # Display number of students enrolled
        enrollment_label = tk.Label(self, text=f"Students Enrolled: {enrollment_count}", font=('Georgia', 14,'bold'))
        enrollment_label.pack(pady=10)
        
if __name__ == "__main__":
    app = CoursesApp()
    app.mainloop()
