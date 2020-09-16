import mysql.connector 

 mydb = mysql.connector.connect(
  host="127.00.00.1",
  user="root",
  password="root"
)

mycursor = mydb.cursor()


mycursor.execute("SHOW DATABASES")

if 'certificate_portal' not in mycursor:
    mycursor.execute("CREATE DATABASE certificate_portal")
    mycursor.execute("USE certificate_portal")
    mycursor.execute("CREATE TABLE mentor(mentor_id INT PRIMARY KEY AUTO_INCREMENT, mentor_fname VARCHAR(30), mentor_lname VARCHAR(30))")
    mycursor.execute("CREATE TABLE mentor(mentor_id INT PRIMARY KEY AUTO_INCREMENT, mentor_fname VARCHAR(30), mentor_lname VARCHAR(30))")
    mycursor.execute("CREATE TABLE student(student_id INT PRIMARY KEY AUTO_INCREMENT, student_fname VARCHAR(30), student_lname VARCHAR(30))") 
    mycursor.execute("CREATE TABLE course(course_id INT PRIMARY KEY AUTO_INCREMENT, course_name VARCHAR(30), course_details VARCHAR(200))") 
    mycursor.execute("CREATE TABLE certification(certification_id INT PRIMARY KEY AUTO_INCREMENT, student_id INT, mentor_id INT, course_id INT, certification_code VARCHAR(100), certification_date DATETIME, FOREIGN KEY(student_id) REFERENCES student(student_id), FOREIGN KEY(mentor_id) REFERENCES mentor(mentor_id), FOREIGN KEY(course_id) REFERENCES course(course_id))") 
    mycursor.execute("CREATE TABLE users(user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(30), password VARCHAR(30))") 

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x) 


# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)

# mydb.commit()