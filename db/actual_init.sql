CREATE DATABASE certificates;
use certificates;

CREATE TABLE mentor (
  mentor_id INT NOT NULL AUTO_INCREMENT,
  mentor_fname VARCHAR(30),
  mentor_lname VARCHAR(30),
  PRIMARY KEY (mentor_id)
);

CREATE TABLE student (
  student_id INT NOT NULL AUTO_INCREMENT,
  student_fname VARCHAR(30),
  student_lname VARCHAR(30),
  PRIMARY KEY (student_id)
);

CREATE TABLE course (
  course_id INT NOT NULL AUTO_INCREMENT,
  course_name VARCHAR(30),
  course_details VARCHAR(30),
  PRIMARY KEY (course_id)
);

CREATE TABLE certification (
  certification_id INT NOT NULL AUTO_INCREMENT,
  student_id INT,
  course_id INT,
  mentor_id INT,
  certification_code VARCHAR(60),
  certification_date DATETIME,
  PRIMARY KEY (certification_id),
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (course_id) REFERENCES course(course_id),
  FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id)
);

INSERT INTO mentor
  (mentor_fname, mentor_lname)
VALUES
  ("John", "Smith");
