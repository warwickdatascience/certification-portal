import mysql.connector 
import os
import hashlib
import random
from dotenv import load_dotenv
import requests

load_dotenv()

mydb = mysql.connector.connect(
  host="127.00.00.1",
  port="32000",
  user="root",
  password=os.environ["SQL_ROOT_PASSWORD"]
)

mycursor = mydb.cursor()
mycursor.execute("USE certificate_portal")
def get_jwt_token():
    # post to https://cert.wdss.io/token/auth
    url = "https://cert.wdss.io/token/auth"
    data = {'username': 'admin', 'password': os.environ['ADMIN_PASSWORD']}
    
    x = requests.post(url, data=data)
    return x.json()['access_token']

# MENTORS
def add_mentor(fname, lname):
    # check if mentor exists
    # if not exist
    sql = "INSERT INTO mentor (mentor_fname, mentor_lname) VALUES (%s, %s)"
    val = (fname, lname)
    mycursor.execute(sql, val)
    mydb.commit()
        # return mycursor.lastrowid
    # else get id 
        # return id


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

def add_certificate(student_id, mentor_id, course_id, access_token):
    #cert_id = random.randint(0000000, 99999999)i
    #sql = "INSERT INTO certificate (student_id, mentor_id, course_id, cert_id) VALUES (%s %s %s %s)"
    #val = (student_id, mentor_id, course_id, cert_id)
    #mycursor.execute(sql, val)
    url = "https://cert.wdss.io/api/generate"
    headers = {"Authorization": access_token}
    data = {"student_id": student_id, "mentor_id": mentor_id, "course_id": course_id}
    x = requests.post(url, json=data, headers=headers)    
    print(x.text)
    return x.json()['cert_id']

def create_certificate():
    fname = input("STUDENT FNAME: ")
    lname = input("STUDENT LNAME: ")
    add_student(fname, lname)
    student_id = mycursor.lastrowid
    print(student_id)
    access_token = f'JWT get_jwt_token()'
    add_certificate(1, 1, 1, access_token)
create_certificate()
