import mysql.connector 
import os
import hashlib
mydb = mysql.connector.connect(
  host="127.00.00.1",
  port="32000",
  user="root",
  password="root"
)

mycursor = mydb.cursor()


mycursor.execute("SHOW DATABASES")
flag = False
for x in mycursor:
    if 'certificate_portal' in x:
        flag = True

if not flag:
    mycursor.execute("CREATE DATABASE certificate_portal")

mycursor.execute("USE certificate_portal")
mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
mycursor.execute("DROP TABLE IF EXISTS mentor") 
mycursor.execute("DROP TABLE IF EXISTS student") 
mycursor.execute("DROP TABLE IF EXISTS course") 
mycursor.execute("DROP TABLE IF EXISTS certification") 
mycursor.execute("DROP TABLE IF EXISTS user")
mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
mycursor.execute("CREATE TABLE mentor(mentor_id INT PRIMARY KEY AUTO_INCREMENT, mentor_fname VARCHAR(30), mentor_lname VARCHAR(30))")
mycursor.execute("CREATE TABLE student(student_id INT PRIMARY KEY AUTO_INCREMENT, student_fname VARCHAR(30), student_lname VARCHAR(30))") 
mycursor.execute("CREATE TABLE course(course_id INT PRIMARY KEY AUTO_INCREMENT, course_name VARCHAR(30), course_details VARCHAR(200))") 
mycursor.execute("CREATE TABLE certification(certification_id INT PRIMARY KEY AUTO_INCREMENT, student_id INT, mentor_id INT, course_id INT, certification_code VARCHAR(100), certification_date DATETIME, FOREIGN KEY(student_id) REFERENCES student(student_id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY(mentor_id) REFERENCES mentor(mentor_id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY(course_id) REFERENCES course(course_id) ON UPDATE CASCADE ON DELETE CASCADE)") 
mycursor.execute("CREATE TABLE user(user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(30), password BLOB, salt BLOB)") 
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x) 

# MENTORS
sql = "INSERT INTO mentor (mentor_fname, mentor_lname) VALUES (%s, %s)"
val = ("Sheldon", "Bazinga")
mycursor.execute(sql, val)
val = ("Mark", "Corrigan")
mycursor.execute(sql, val)
mydb.commit()

# STUDENTS
sql = "INSERT INTO student (student_fname, student_lname) VALUES (%s, %s)"
val = ("Jeff", "Bezos")
mycursor.execute(sql, val)
val = ("Mark", "Zuckerberg")
mycursor.execute(sql, val)
mydb.commit()

# COURSES
sql = "INSERT INTO course (course_name, course_details) VALUES (%s, %s)"
val = ("Intro to Python", "Intro to python for data science")
mycursor.execute(sql, val)
mydb.commit()

# USERS
sql = "INSERT INTO user (username, password, salt) VALUES (%s, %s, %s)"
password = "admin"
salt = os.urandom(32)
print(salt)
key = hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000 # It is recommended to use at least 100,000 iterations of SHA-256 
)
# print(key.decode('utf-8'))
val = ("admin", key, salt)
mycursor.execute(sql, val)
mydb.commit()
mycursor.execute("SELECT * FROM student")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
