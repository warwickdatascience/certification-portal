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
    # post to http://127.0.0.1:50000/token/auth
    url = "http://127.0.0.1:50000/token/auth"
    data = {'username': 'admin', 'password': os.environ['ADMIN_PASSWORD']}
    x = requests.post(url, json=data)
    
    return x.json()['access_token']

# MENTORS


def add_mentor_api(access_token, fname, lname):
    url = "http://127.0.0.1:50000/api/crud/mentor"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}

    data = {'mentor_fname': fname, 'mentor_lname': lname}
    request = requests.post(url, json=data, headers=headers)        
    
# STUDENTS
def add_student_api(access_token, fname, lname, email):
    url = "http://127.0.0.1:50000/api/crud/student"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}

    data = {'student_fname': fname, 'student_lname': lname, 'student_email': email}
    response = requests.post(url, json=data, headers=headers)        
    
    return response.json()['id']

# COURSES
def add_course_api(access_token, course_name, course_details):
    url = "http://127.0.0.1:50000/api/crud/course"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}

    data = {'course_name': course_name, 'course_details': course_details}
    request = requests.post(url, json=data, headers=headers)        

def add_certificate(student_id, mentor_id, course_id, access_token):
    url = "http://127.0.0.1:50000/api/generate"
    headers = {"Authorization": f'JWT {access_token}',
               "Cookie": f'access_token_cookie={access_token}'}
    data = {
        "student_id": student_id,
        "mentor_id": mentor_id,
        "course_id": course_id}
    x = requests.post(url, json=data, headers=headers)

    return x.json()['cert_id']


def pre_load_mentors():
    add_mentor_api(jwt, "Tim", "Hargreaves")
    add_mentor_api(jwt, "Brandusa", "Draghici")
    add_mentor_api(jwt, "Ciarán", "Evans")
    add_mentor_api(jwt, "Farhan", "Tariq")
    add_mentor_api(jwt, "Gabriel", "Musker")
    add_mentor_api(jwt, "Horia", "Druliac")
    add_mentor_api(jwt, "Janique", "Krasnowska")
    add_mentor_api(jwt, "Lucy", "McArthur")
    add_mentor_api(jwt, "Martin", "Smit")
    add_mentor_api(jwt, "Raul-Octavian", "Rus")
    add_mentor_api(jwt, "Yasser", "Qureshi")


def pre_load_courses():
    add_course_api(jwt, "Introduction to Python", "16-hour Asssesed Course")
    add_course_api(jwt, 
        "Introduction to Python",
        "16-hour Asssesed Course w/ Additional Pythonic Programming Foundations")
    add_course_api(jwt, "Into the Tidyverse", "15-hour Asssesed Course")


def create_certificate(jwt):
    fname = input("STUDENT FNAME: ")
    lname = input("STUDENT LNAME: ")
    mycursor.execute(
        f"SELECT * FROM student WHERE student_fname='{fname}' AND student_lname='{lname}'")
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        print("**new student identified**")
        email = input("STUDENT EMAIL: ")
        add_student(fname, lname, email)
        student_id = mycursor.lastrowid
    else:
        print("Student(s) with the same name detected")
        for x in myresult:
            print(x)
        x = input("Add new student? [y/n]")
        if x == "y":
            email = input("STUDENT EMAIL: ")
            add_student(fname, lname, email)
            student_id = mycursor.lastrowid
        else:
            student_id = int(input("STUDENT ID: "))
    print(f'student id: {student_id}')

    mycursor.execute("SELECT * FROM mentor")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    mentor_id = int(input("MENTOR ID: "))

    mycursor.execute("SELECT * FROM course")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    course_id = int(input("COURSE ID: "))
    print(add_certificate(student_id, mentor_id, course_id, jwt))

def existing_students(access_token, fname, lname):
    url = "http://127.0.0.1:50000/api/crud/student"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}
    request = requests.get(url, headers=headers)        
    existing_students = []
    for student in request.json():
        if student['student_fname'].upper() == fname.upper() and student['student_lname'].upper() == lname.upper():
            existing_students.append(student)
    return existing_students



def print_all_mentor(access_token):
    url = "http://127.0.0.1:50000/api/crud/mentor"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}
    request = requests.get(url, headers=headers)        
    for mentor in request.json():
        print(f"{mentor['mentor_id']} {mentor['mentor_fname']} {mentor['mentor_lname']}")

def print_all_course(access_token):
    url = "http://127.0.0.1:50000/api/crud/course"
    headers = {"Authorization": f'JWT {access_token}',
            "Cookie": f'access_token_cookie={access_token}'}
    request = requests.get(url, headers=headers)        
    for course in request.json():
        print(f"{course['course_id']} {course['course_name']} {course['course_details']}")


def create_certificate_api(jwt):
    fname = input("STUDENT FNAME: ")
    lname = input("STUDENT LNAME: ")
    same_name = existing_students(jwt, fname, lname)
    if len(same_name) == 0:
        print("**new student identified**")
        email = input("STUDENT EMAIL: ")
        student_id = add_student_api(jwt, fname, lname, email)    
    else:
        print("Student(s) with the same name detected")
        for x in same_name:
            print(f"{x['student_id']} {x['student_fname']} {x['student_lname']}")
        
        x = input("Add new student? [y/n]")
        if x == "y":
            email = input("STUDENT EMAIL: ")
            student_id = add_student_api(jwt, fname, lname, email)
        else:
            student_id = int(input("STUDENT ID: "))
    print(f'student id: {student_id}')
    
    print_all_mentor(jwt)    
    mentor_id = int(input("MENTOR ID: "))

    print_all_course(jwt)
    course_id = int(input("COURSE ID: "))
    print(f"cert id: {add_certificate(student_id, mentor_id, course_id, jwt)}")


jwt = get_jwt_token()


print("CERTIFICATE GENERATOR")
x = input("preload? [y/n]")
if x == "y":
    pre_load_mentors()
    pre_load_courses()
while(input("add cert [y/n]: ") == "y"):
    create_certificate_api(jwt)
