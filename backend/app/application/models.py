from flask_login import UserMixin
from . import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import os
import hashlib


class Mentor(UserMixin, db.Model):
    __tablename__ = "mentor"
    mentor_id = db.Column(db.Integer, primary_key=True)
    mentor_fname = db.Column(db.String)
    mentor_lname = db.Column(db.String)
    mentor_email = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)

    def get_id(self):
        return self.mentor_id

    def __unicode__(self):
        return self.mentor_email
    
    def __repr__(self):
        return self.mentor_email


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    student_fname = db.Column(db.String)
    student_lname = db.Column(db.String)
    student_email = db.Column(db.String)

    def __unicode__(self):
        return f"{self.student_fname} {self.student_lname} {self.student_email}"
    
    def __repr__(self):
        return f"{self.student_fname} {self.student_lname} {self.student_email}"


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    course_details = db.Column(db.String)

    def __unicode__(self):
        return f"{self.course_name} {self.course_details}"

    def __repr__(self):
        return f"{self.course_name} {self.course_details}"

class Certification(db.Model):
    __tablename__ = "certification"
    certification_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.mentor_id"))
    certification_code = db.Column(db.String)
    certification_date = db.Column(db.DateTime)
    mentor = db.relationship("Mentor", backref="certification")
    student = db.relationship("Student", backref="student")
    course = db.relationship("Course", backref="course")
    # mentor_name = db.relationship("Mentor", foreign_keys=[mentor_id])


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)
