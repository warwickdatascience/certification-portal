from flask_login import UserMixin
from . import db


class Mentor(UserMixin, db.Model):
    __tablename__ = "mentor"
    mentor_id = db.Column(db.Integer, primary_key=True)
    mentor_fname = db.Column(db.String)
    mentor_lname = db.Column(db.String)
    mentor_email = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)

    def get_id(self):
        return self.mentor_id


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    student_fname = db.Column(db.String)
    student_lname = db.Column(db.String)
    student_email = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    course_details = db.Column(db.String)


class Certification(db.Model):
    __tablename__ = "certification"
    certification_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.mentor_id"))
    certification_code = db.Column(db.String)
    certification_date = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)
