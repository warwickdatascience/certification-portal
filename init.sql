CREATE DATABASE certificate_portal;
USE certificate_portal;
CREATE TABLE mentor(mentor_id INT PRIMARY KEY AUTO_INCREMENT, mentor_fname VARCHAR(30), mentor_lname VARCHAR(30));
CREATE TABLE student(student_id INT PRIMARY KEY AUTO_INCREMENT, student_fname VARCHAR(30), student_lname VARCHAR(30));
CREATE TABLE course(course_id INT PRIMARY KEY AUTO_INCREMENT, course_name VARCHAR(30), course_details VARCHAR(200));
CREATE TABLE certification(certification_id INT PRIMARY KEY AUTO_INCREMENT, student_id INT, mentor_id INT, course_id INT, certification_code VARCHAR(100), certification_date DATETIME, FOREIGN KEY(student_id) REFERENCES student(student_id), FOREIGN KEY(mentor_id) REFERENCES mentor(mentor_id), FOREIGN KEY(course_id) REFERENCES course(course_id));
