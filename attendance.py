import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
import subprocess
from itertools import cycle

username = "root"
password = "30127"

my_db = mysql.connector.connect(
    host="localhost",
    user=username,
    passwd=password,
    database="futurense"
)

# variables to store attendance
one = 0
two = 0
three = 0
four = 0
five = 0
with open("log.txt", "r") as file:
    user = file.read()
# 1st subject
cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 36;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    one = int(i[0])

# 2nd subject
cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 37;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    two = int(i[0])

# 3rd subject
cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 38;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    three = int(i[0])

# 4th subject
cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 39;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    four = int(i[0])

# 5th subject
cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 40;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    five = int(i[0])

cursor = my_db.cursor()
query="SELECT (COUNT(CASE WHEN status = 'Present' THEN 1 END) / COUNT(status)) * 100 from Attendance where sid = (select sid from student where email=%s) and cid = 41;"
cursor.execute(query,(user,))
tables = cursor.fetchall()

for i in tables:
    six = int(i[0])

# total
total_percent = (one + two + three + four + five+six)/6


def grade():
    root.destroy()
    subprocess.run(["python", "grade.py"])
def course():
    subprocess.run(["python", "course_page.py"])
    root.destroy()
def close_loading_window():
    loading_window.destroy()  # Destroy the loading window
def home(x):
    global loading_window
    root.destroy
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
    loading_window.after(2300, home)
    # Open the main application window
    root.destroy()
    subprocess.Popen(['python',x])

def assignment():
    root.destroy()
    subprocess.run(["python", "Assignment/main1.py"])

def exams():
    root.destroy()
    subprocess.run(["python", "exam.py"])
root = tk.Tk()
root.title("Attendance")
root.geometry("1766x768")  # Set the geometry of the window
bg_image = Image.open("background_image.jpg")  # Replace with your image file path
# Resize the image to fit the window sizeW
bg_image = bg_image.resize((1378, 700), Image.LANCZOS)
# Convert Image object to Tkinter PhotoImage object
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# Sidebar Frane
sidebar = tk.Frame(root, width=250, bg="gray16")
sidebar.place(x=0, y=105, height=800, width=205)  

# Create a frame for the header with black background
header = tk.Frame(root, bg="black", width=1550, height=120)
header.pack()

# Create a label inside the header frame
header_label = tk.Label(header, text="Attendance", fg="white", bg="black", font=("Georgia", 24, "bold"))
header_label.place(relx=0.5, rely=0.5, anchor="center")


# Image label
pil_image = Image.open("background2.jpeg")
pil_image = pil_image.resize((100, 100))
lpu_image = Image.open("background3.jpeg")
lpu_image = lpu_image.resize((200, 100))

tk_image = ImageTk.PhotoImage(pil_image)
lpu_image = ImageTk.PhotoImage(lpu_image)

image_label = tk.Label(header, image=tk_image, bg="black")
image_label.image = tk_image
image_label.place(x=0, y=0)

lpu_label = tk.Label(header, image=lpu_image, bg="black")
lpu_label.image = tk_image
lpu_label.place(x = 1325, y = 0)


def open_app(x):
    root.destroy()
    subprocess.Popen(['python',x])

# Attendance heading




# Create subject frame
maths = tk.Frame(root, width=900, height=80, bg="goldenrod2")
maths.place(x=400, y=150)
physics = tk.Frame(root, width=900, height=80, bg="goldenrod2")
physics.place(x=400, y=250)
chem = tk.Frame(root, width=900, height=80, bg="goldenrod2")
chem.place(x=400, y=350)
bio = tk.Frame(root, width=900, height=80, bg="goldenrod2")
bio.place(x=400, y=450)
cs = tk.Frame(root, width=900, height=80, bg="goldenrod2")
cs.place(x=400, y=550)
se=tk.Frame(root,width=900,height=80, bg='goldenrod2')
se.place(x=400, y=650)


# Subject name
maths_label = tk.Label(maths, text="Mathematics", font=("Times", 16), bg="goldenrod2")
maths_label.place(x=50, y=10)
physics_label = tk.Label(physics, text="DSA", font=("Times", 16), bg="goldenrod2")
physics_label.place(x=50, y=10)
chem_label = tk.Label(chem, text="DBMS", font=("Times", 16), bg="goldenrod2")
chem_label.place(x=50, y=10)
bio_label = tk.Label(bio, text="Data Networking and Communication", font=("Times", 16), bg="goldenrod2")
bio_label.place(x=50, y=10)
cs_label = tk.Label(cs, text="Python", font=("Times", 16), bg="goldenrod2")
cs_label.place(x=50, y=10)
se_label = tk.Label(se, text="Software Engineering", font=("Times", 16), bg="goldenrod2", fg='black')
se_label.place(x=50, y=10)

# Subject Timings
maths_timing = tk.Label(maths, text="9:00 - 10:00 AM",font=("Times", 16), bg="goldenrod2")
maths_timing.place(x=1200, y=10)
physics_timing = tk.Label(physics, text="9:00 - 10:00 AM",font=("Times", 16), bg="goldenrod2")
physics_timing.place(x=1200, y=10)
chem_timing = tk.Label(chem, text="9:00 - 10:00 AM", font=("Times", 16), bg="goldenrod2")
chem_timing.place(x=1200, y=10)
bio_timing = tk.Label(bio, text="9:00 - 10:00 AM", font=("Times", 16), bg="goldenrod2")
bio_timing.place(x=1200, y=10)
cs_timing = tk.Label(cs, text="9:00 - 10:00 AM", font=("Times", 16), bg="goldenrod2")
cs_timing.place(x=1200, y=10)
se_timing = tk.Label(se, text="9:00 - 10:00 AM", font=("Times", 16), bg="goldenrod2")
se_timing.place(x=1200, y=10)

# Attendance
maths_att = tk.Label(maths, text="Attendance", font=("Times", 16), bg="goldenrod2")
maths_att.place(x=600, y=10)
physics_att = tk.Label(physics, text="Attendance", font=("Times", 16), bg="goldenrod2")
physics_att.place(x=600, y=10)
chem_att = tk.Label(chem, text="Attendance", font=("Times", 16), bg="goldenrod2")
chem_att.place(x=600, y=10)
bio_att = tk.Label(bio, text="Attendance", font=("Times", 16), bg="goldenrod2")
bio_att.place(x=600, y=10)
cs_att = tk.Label(cs, text="Attendance",font=("Times", 16),  bg="goldenrod2")
cs_att.place(x=600, y=10)
se_att = tk.Label(se, text="Attendance",font=("Times", 16),  bg="goldenrod2")
se_att.place(x=600,y=10)

# Attendance percentage
maths_att = tk.Label(maths, text=str(one), font=("Times", 16), bg="goldenrod2")
maths_att.place(x=625, y=55)
physics_att = tk.Label(physics, text=str(two), font=("Times", 16), bg="goldenrod2")
physics_att.place(x=625, y=55)
chem_att = tk.Label(chem, text=str(three), font=("Times", 16), bg="goldenrod2")
chem_att.place(x=625, y=55)
bio_att = tk.Label(bio, text=str(four), font=("Times", 16), bg="goldenrod2")
bio_att.place(x=625, y=55)
cs_att = tk.Label(cs, text=str(five),font=("Times", 16),  bg="goldenrod2")
cs_att.place(x=625, y=55)
total_att = tk.Label(se, text=str(six), font=("Times", 16), bg="goldenrod2")
total_att.place(x = 625, y = 55)



# Buttons
button1 = tk.Button(sidebar, text="DASHBOARD", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:home('main.py'))
button1.place(x=20, y=70)
button2 = tk.Button(sidebar, text="ASSIGNMENT", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('Assignment/main1.py'))
button2.place(x=20, y=170)
button3 = tk.Button(sidebar, text="ATTENDANCE", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('attendance.py'))
button3.place(x=20, y=270)
button4 = tk.Button(sidebar, text="EXAMS", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('exam.py'))
button4.place(x=20, y=370)
button5 = tk.Button(sidebar, text="COURSES", bg='gray16', fg='white', font=('helvetica', 12, 'bold'), width=15,command=lambda:open_app('grade.py'))
button5.place(x=20, y=470)

# Function to toggle left column visibility
left_column_visible = True
def toggle_left_column():
    global left_column_visible
    if left_column_visible:
        sidebar.place_forget()
        left_column_visible = False
    else:
        sidebar.place(x=0, y=0, relheight=1, anchor='nw')
        left_column_visible = True

toggle_button = tk.Button(root, text="☰", command=toggle_left_column, borderwidth=0, bg="white", fg="black")
toggle_button.place(x=1500, y=150)


root.mainloop()
