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

app = Flask(__name__)

# name of the database
db_name = "certificate_portal.db"

# add config variables for SQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# the variable to be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)

class CourseMentor(db.Model):
    __tablename__ = "coursementors"
    id = db.Column(db.Integer, primary_key=True)
    mentorID = db.Column(db.Integer, db.ForeignKey("people.id"))
    courseID = db.Column(db.Integer, db.ForeignKey("courses.id"))

class Certificate(db.Model):
    __tablename__ = "certificates"
    id = db.Column(db.Integer, primary_key=True)
    hashValue = db.Column(db.String)
    studentID = db.Column(db.Integer, db.ForeignKey("people.id"))
    mentorID = db.Column(db.Integer, db.ForeignKey("people.id"))
    courseID = db.Column(db.Integer, db.ForeignKey("courses.id"))

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

    studentID = request.json["studentID"]
    mentorID = request.json["mentorID"]
    courseID = request.json["courseID"]

    params = {
        "name": Person.query.get_or_404(studentID).name,
        "mentor": Person.query.get_or_404(mentorID).name,
        "course": Course.query.get_or_404(courseID).name,
        "desc": Course.query.get_or_404(courseID).desc
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
    entry = Certificate(hashValue=cert_id, studentID=studentID, mentorID=mentorID, courseID=courseID)

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

    certInfo = Certificate.query.filter_by(hashValue=iden).first()

    courseName = Course.query.get_or_404(certInfo.courseID).name
    studentName = Person.query.get_or_404(certInfo.studentID).name

    return render_template("cert.html", iden=url_for('static', filename=f"certificates/{iden}.pdf"), courseName=courseName, studentName=studentName)
    # return send_file('static/certificates/certificate-docker2.pdf', attachment_filename=f'{iden}.pdf')
    # with open('/code/certificate-docker.pdf', 'rb') as static_file:
        # return send_file(static_file, attachment_filename='eew324432io328dh.pdf')
# 


@app.route("/tables")
def tables():
    try:
        people = Person.query.all()
        text = ""
        for person in people:
            text += person.name
        return text
    except Exception as e:
        return str(e)

