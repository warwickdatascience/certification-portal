import time


from flask import (Flask, render_template, request, abort, jsonify, redirect, url_for)
from flask import send_file

import jinja2
import pdfkit
import datetime
import hashlib
import uuid
from os import listdir
from os.path import isfile, join
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import pymysql

app = Flask(__name__)
'''
FOR LOCAL TESTING ONLY

# name of the database
db_name = "certificate_portal.db"

# add config variables for SQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
'''

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://cert_app:PASSWORD@localhost/certificate_database"

# the variable to be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class Mentor(db.Model):
    __tablename__ = "mentor"
    mentor_id = db.Column(db.Integer, primary_key=True)
    mentor_fname = db.Column(db.String)
    mentor_lname = db.Column(db.String)

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    student_fname = db.Column(db.String)
    student_lname = db.Column(db.String)

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

# test the database connection through this route (for debugging)
@app.route("/dbtest")
def testdb():
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return "<h1>It works.</h1>"
    except Exception as e:
        # e holds descirption of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text

def generate_pdf(name, mentor, course, details, cert_id):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "templates/htmltemplate.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(
        id=cert_id,
        name=name,
        course_name=course,
        additional_course_details=details,
        date=datetime.date.today(),
        mentor=mentor)

    html_file = open('templates/certificate.html', 'w')
    html_file.write(outputText)
    html_file.close()

    options = {
        "enable-local-file-access": None,
        "orientation": "Landscape",
        "background": None,
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
    }

    pdfkit.from_file('templates/certificate.html',
                     f'static/certificates/{cert_id}.pdf', options=options)
    infile = PdfFileReader(f'static/certificates/{cert_id}.pdf', 'rb')
    output = PdfFileWriter()
    p = infile.getPage(0)
    output.addPage(p)

    with open(f'static/certificates/{cert_id}.pdf', 'wb') as f:
        output.write(f)


@app.route('/generate', methods=['POST'])
def generate():
    if not request.json:
        abort(400)

    student_id = request.json["student_id"]
    mentor_id = request.json["mentor_id"]
    course_id = request.json["course_id"]

    params = {
        "name": f"{Student.query.get_or_404(student_id).student_fname} {Student.query.get_or_404(student_id).student_lname}",
        "mentor": f"{Mentor.query.get_or_404(mentor_id).mentor_fname} {Mentor.query.get_or_404(mentor_id).mentor_lname}",
        "course": Course.query.get_or_404(course_id).course_name,
        "desc": Course.query.get_or_404(course_id).course_details
    }

    '''
    params = {
        'name': request.json['name'],
        'mentor': request.json['mentor'],
        'course': request.json['course'],
        'desc': request.json['desc']
    }
    '''
    cert_id = str(uuid.uuid1())
    entry = Certification(student_id=student_id, course_id=course_id, mentor_id=mentor_id, certification_code=cert_id, certification_date=datetime.date.today())

    try:
        db.session.add(entry)
        db.session.commit()

        generate_pdf(params['name'], params['mentor'],
                 params['course'], params['desc'], cert_id)
        resp = jsonify(success=True)
        return resp
    except:
        return "There was an issue creating your certificate"


@app.route('/htmltemplate')
def htmltemplate():
    return render_template("htmltemplate.html")


@app.route('/preview')
def preview():
    return render_template("certificate.html")


@app.route('/certificate/<iden>')
def certificate(iden):
    if False: # TODO abort if file does not exist
        abort(400)

    certInfo = Certification.query.filter_by(certification_code=iden).first()

    courseName = Course.query.get_or_404(certInfo.course_id).course_name
    studentName = f"{Student.query.get_or_404(certInfo.student_id).student_fname} {Student.query.get_or_404(certInfo.student_id).student_lname}"

    return render_template("cert.html", iden=url_for('static', filename=f"certificates/{iden}.pdf"), courseName=courseName, studentName=studentName)
    # return send_file('static/certificates/certificate-docker2.pdf', attachment_filename=f'{iden}.pdf')
    # with open('/code/certificate-docker.pdf', 'rb') as static_file:
        # return send_file(static_file, attachment_filename='eew324432io328dh.pdf')
# 
