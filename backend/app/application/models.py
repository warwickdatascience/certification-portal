from flask_login import UserMixin
from . import db
import json

class Mentor(UserMixin, db.Model):
    __tablename__ = "mentor"
    __table_args__ = {'extend_existing': True} 
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
    __table_args__ = {'extend_existing': True} 
    student_id = db.Column(db.Integer, primary_key=True)
    student_fname = db.Column(db.String)
    student_lname = db.Column(db.String)
    student_email = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"
    __table_args__ = {'extend_existing': True} 
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    course_details = db.Column(db.String)


class Certification(db.Model):
    __tablename__ = "certification"
    __table_args__ = {'extend_existing': True} 
    certification_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.mentor_id"))
    certification_code = db.Column(db.String)
    certification_date = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.BLOB)
    salt = db.Column(db.BLOB)

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)