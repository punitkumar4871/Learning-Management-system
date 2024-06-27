create database futurense;
use futurense;
create table student(
sid int primary key auto_increment,
sname varchar(50) not null,
phonenumber int not null,
age int(2) not null,
gender enum("Male","Female","Others"),
email varchar(50) unique,
address varchar(100) not null,
password varchar(100) not null
);

create table teacher(
tid int primary key auto_increment,
tname varchar(50) not null,
phonenumber int not null,
age int(2) not null,
gender enum("Male","Female","Others"),
email varchar(50) unique,
address varchar(100) not null

);
CREATE TABLE course (
    cid INT AUTO_INCREMENT PRIMARY KEY,
    cname VARCHAR(100) NOT NULL,
    tid INT,
    sid INT,
    FOREIGN KEY (tid) REFERENCES teacher(tid),
    FOREIGN KEY (sid) REFERENCES student(sid)
);
CREATE TABLE Grade (
    gid INT AUTO_INCREMENT PRIMARY KEY,
    cid INT,
    eid INT,
    sid INT,
    grades CHAR(1), -- Assuming grades are represented by a single character (A, B, C, etc.)
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (eid) REFERENCES Exams(eid),
    FOREIGN KEY (sid) REFERENCES Student(sid)
);
CREATE TABLE Exams (
    eid INT AUTO_INCREMENT PRIMARY KEY,
    ename VARCHAR(255) NOT NULL,
    sid INT,
    cid INT,
    FOREIGN KEY (sid) REFERENCES Student(sid),
    FOREIGN KEY (cid) REFERENCES Course(cid)
);


CREATE TABLE Assignment (
    aid INT AUTO_INCREMENT PRIMARY KEY,
    assignment_name VARCHAR(100) NOT NULL,
    description TEXT,
    deadline DATE,
    cid INT NOT NULL,
    tid INT NOT NULL,
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (tid) REFERENCES Teacher(tid)
);

CREATE TABLE Attendance (
    atid INT AUTO_INCREMENT PRIMARY KEY,
    sid INT NOT NULL,
    cid INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (sid) REFERENCES student(sid),
    FOREIGN KEY (cid) REFERENCES course(cid)
);

INSERT INTO student (sname, phonenumber, age, gender, email, address, password) VALUES
('Ravi Kumar', '987654321', 21, 'Male', 'ravi@example.com', 'Delhi, India', 'password123'),
('Sita Sharma', '876543210', 22, 'Female', 'sita@example.com', 'Mumbai, India', 'password123'),
('Arjun Singh', '765432109', 23, 'Male', 'arjun@example.com', 'Chennai, India', 'password123'),
('Priya Patel', '654321098', 20, 'Female', 'priya@example.com', 'Kolkata, India', 'password123'),
('Vijay Rao', '543210987', 21, 'Male', 'vijay@example.com', 'Hyderabad, India', 'password123'),
('Anita Das', '432109876', 22, 'Female', 'anita@example.com', 'Pune, India', 'password123'),
('Amit Joshi', '321098765', 23, 'Male', 'amit@example.com', 'Ahmedabad, India', 'password123'),
('Meena Reddy', '210987653', 20, 'Female', 'meena@example.com', 'Bangalore, India', 'password123'),
('Rajesh Mehta', '109876432', 21, 'Male', 'rajesh@example.com', 'Surat, India', 'password123'),
('Neha Gupta', '098765421', 22, 'Female', 'neha@example.com', 'Jaipur, India', 'password123');

INSERT INTO teacher (tname, phonenumber, age, gender, email, address) VALUES
('Dr. Ashok Verma', '988776655', 45, 'Male', 'ashok@example.com', 'Delhi, India'),
('Prof. Sunita Kapoor', '877665544', 40, 'Female', 'sunita@example.com', 'Mumbai, India'),
('Dr. Rajan Iyer', '776654433', 50, 'Male', 'rajan@example.com', 'Chennai, India'),
('Prof. Kavita Sharma', '655443322', 38, 'Female', 'kavita@example.com', 'Kolkata, India'),
('Dr. Mohan Patel', '554432211', 42, 'Male', 'mohan@example.com', 'Hyderabad, India');

INSERT INTO course (cname, tid, sid) VALUES
('Mathematics', 1, 1),
('Physics', 2, 2),
('Chemistry', 3, 3),
('Biology', 4, 4),
('Computer Science', 5, 5),
('Mathematics', 1, 6),
('Physics', 2, 7),
('Chemistry', 3, 8),
('Biology', 4, 9),
('Computer Science', 5, 10);

INSERT INTO Attendance (sid, cid, attendance_date, status) VALUES
(1, 1, '2024-06-01', 'Present'),
(2, 2, '2024-06-01', 'Absent'),
(3, 3, '2024-06-01', 'Present'),
(4, 4, '2024-06-01', 'Present'),
(5, 5, '2024-06-01', 'Absent'),
(6, 1, '2024-06-02', 'Present'),
(7, 2, '2024-06-02', 'Present'),
(8, 3, '2024-06-02', 'Absent'),
(9, 4, '2024-06-02', 'Present'),
(10, 5, '2024-06-02', 'Present');

INSERT INTO Exams (ename, sid, cid) VALUES
('Midterm Mathematics', 1, 1),
('Midterm Physics', 2, 2),
('Midterm Chemistry', 3, 3),
('Midterm Biology', 4, 4),
('Midterm Computer Science', 5, 5);

-- Insert data into Grade
INSERT INTO Grade (cid, eid, sid, grades) VALUES
(1, 1, 1, 'A'),
(2, 2, 2, 'B'),
(3, 3, 3, 'A'),
(4, 4, 4, 'C'),
(5, 5, 5, 'B');

-- Insert data into Assignment
INSERT INTO Assignment (assignment_name, description, deadline, cid, tid) VALUES
('Math Assignment 1', 'Algebra problems', '2024-07-01', 1, 1),
('Physics Assignment 1', 'Mechanics problems', '2024-07-01', 2, 2),
('Chemistry Assignment 1', 'Organic chemistry problems', '2024-07-01', 3, 3),
('Biology Assignment 1', 'Cell biology questions', '2024-07-01', 4, 4),

('CS Assignment 1', 'Programming in Python', '2024-07-01', 5, 5),

('CS Assignment 1', 'Programming in Python', '2024-07-01', 5, 5);

