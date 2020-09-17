import mysql.connector 
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host="127.00.00.1",
  port="32000",
  user="root",
  password=os.environ["SQL_ROOT_PASSWORD"]
)

mycursor = mydb.cursor()



# MENTORS
def add_mentor(fname, lname):
    sql = "INSERT INTO mentor (mentor_fname, mentor_lname) VALUES (%s, %s)"
    val = (fname, lname)
    mycursor.execute(sql, val)
    mydb.commit()

# STUDENTS
def add_student(fname, lname):
    sql = "INSERT INTO student (student_fname, student_lname) VALUES (%s, %s)"
    val = (fname, lname)
    mycursor.execute(sql, val)
    mydb.commit()

# COURSES
def add_course(course_name, course_details):
    sql = "INSERT INTO course (course_name, course_details) VALUES (%s, %s)"
    val = (course_name, course_details)
    mycursor.execute(sql, val)
    mydb.commit()

mycursor.execute("SELECT * FROM student")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
