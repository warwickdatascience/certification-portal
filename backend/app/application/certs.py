import time
import os
import random
import traceback
from flask import Flask, render_template, request, jsonify, url_for, Blueprint

from flask_jwt_extended import jwt_required


from flask_login import current_user, login_required
import jinja2
import pdfkit
import datetime

from PyPDF2 import PdfFileWriter, PdfFileReader


from . import db
from .models import User, Mentor, Course, Certification, Student

certs_bp = Blueprint("certs_bp", __name__)


def generate_pdf(name, mentor, course, details, cert_id):
    """
    create pdf
    @param name: student name
    @param mentor: mentor name
    @param course: course name
    @param details: course description
    @param cert_id: certificate id

    @return bool
    """
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "/templates/htmltemplate.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    outputText = template.render(
        id=cert_id,
        name=name,
        course_name=course,
        additional_course_details=details,
        date=datetime.date.today(),
        mentor=mentor,
    )

    file_path = os.path.dirname(__file__) + "/templates/certificate.html"
    html_file = open(file_path, "w")
    html_file.write(outputText)
    html_file.close()

    options = {
        "enable-local-file-access": None,
        "orientation": "Landscape",
        "background": None,
        "margin-top": "0",
        "margin-right": "0",
        "margin-bottom": "0",
        "margin-left": "0",
    }
    try:
        dest = (
            os.path.dirname(__file__) + f"/static/certificates/wdss_cert_{cert_id}.pdf"
        )
        pdfkit.from_file(file_path, dest, options=options)

        infile = PdfFileReader(dest, "rb")
        output = PdfFileWriter()
        p = infile.getPage(0)
        output.addPage(p)

        with open(dest, "wb") as f:
            output.write(f)
    except Exception as e:
        return str(e)
    return True


@certs_bp.route("/api/certificate/update", methods=["GET", "POST"])
@jwt_required
def update():
    if request.method == "POST":
        cert_id = request.json["certificate_code"]
        cert_curr = Certification.query.filter_by(
            certification_code=cert_id
        ).first_or_404()

        if "student_id" in request.json:
            student_id = request.json["student_id"]
        else:
            student_id = cert_curr.student_id

        if "mentor_id" in request.json:
            mentor_id = request.json["mentor_id"]
        else:
            mentor_id = cert_curr.mentor_id

        if "course_id" in request.json:
            course_id = request.json["course_id"]
        else:
            course_id = cert_curr.course_id

        params = {
            "name": f"{Student.query.get_or_404(student_id).student_fname} {Student.query.get_or_404(student_id).student_lname}",
            "mentor": f"{Mentor.query.get_or_404(mentor_id).mentor_fname} {Mentor.query.get_or_404(mentor_id).mentor_lname}",
            "course": Course.query.get_or_404(course_id).course_name,
            "desc": Course.query.get_or_404(course_id).course_details,
        }

        try:
            cert = Certification.query.filter_by(certification_code=cert_id).update(
                dict(student_id=student_id, course_id=course_id, mentor_id=mentor_id)
            )
            db.session.commit()

            x = generate_pdf(
                params["name"],
                params["mentor"],
                params["course"],
                params["desc"],
                cert_id,
            )

            resp = jsonify(cert_id=cert_id, success=True, msg=x)
            return resp
        except BaseException:
            return f"There was an issue updating your certificate {params} {cert_id}"
    mentors = Mentor.query.all()
    courses = Course.query.all()
    students = Student.query.all()
    return render_template(
        "generate.html", mentors=mentors, courses=courses, students=students
    )


@certs_bp.route("/api/certificate/generate", methods=["GET", "POST"])
@jwt_required
def generate_api():
    if request.method == "POST":

        student_id = request.json["student_id"]
        mentor_id = request.json["mentor_id"]
        course_id = request.json["course_id"]

        params = {
            "name": f"{Student.query.get_or_404(student_id).student_fname} {Student.query.get_or_404(student_id).student_lname}",
            "mentor": f"{Mentor.query.get_or_404(mentor_id).mentor_fname} {Mentor.query.get_or_404(mentor_id).mentor_lname}",
            "course": Course.query.get_or_404(course_id).course_name,
            "desc": Course.query.get_or_404(course_id).course_details,
        }

        cert_id = str(random.randint(00000000, 99999999)).zfill(8)
        entry = Certification(
            student_id=student_id,
            course_id=course_id,
            mentor_id=mentor_id,
            certification_code=cert_id,
            certification_date=datetime.date.today(),
        )

        try:
            db.session.add(entry)
            db.session.commit()

            x = generate_pdf(
                params["name"],
                params["mentor"],
                params["course"],
                params["desc"],
                cert_id,
            )

            resp = jsonify(cert_id=cert_id, success=True, msg=x)
            return resp
        except BaseException as e:

            return f"There was an issue creating your certificate {params} {cert_id}"

    courses = Course.query.all()
    students = Student.query.all()
    return render_template(
        "generate.html", mentor=current_user, courses=courses, students=students
    )


@certs_bp.route("/certificate/generate", methods=["GET", "POST"])
@login_required
def generate():
    if request.method == "POST":
        if not request.json:

            if "student" in request.form:
                student_id = request.form["student"]

            else:
                student_fname = request.form["student_fname"]
                student_lname = request.form["student_lname"]
                student_email = request.form["student_email"]
                students = Student.query.all()
                for student in students:
                    if student.student_email == student_email:
                        courses = Course.query.all()
                        students = Student.query.all()
                        return render_template(
                            "generate.html",
                            mentor=current_user,
                            courses=courses,
                            students=students,
                            error="Student already exists",
                        )
                entry = Student(
                    student_fname=request.form["student_fname"],
                    student_lname=request.form["student_lname"],
                    student_email=request.form["student_email"],
                )

                db.session.add(entry)
                db.session.commit()
                student_id = entry.student_id

            mentor_id = request.form["mentor"]
            course_id = request.form["course"]
        else:
            student_id = request.json["student_id"]
            mentor_id = request.json["mentor_id"]
            course_id = request.json["course_id"]

        params = {
            "name": f"{Student.query.get_or_404(student_id).student_fname} {Student.query.get_or_404(student_id).student_lname}",
            "mentor": f"{Mentor.query.get_or_404(mentor_id).mentor_fname} {Mentor.query.get_or_404(mentor_id).mentor_lname}",
            "course": Course.query.get_or_404(course_id).course_name,
            "desc": Course.query.get_or_404(course_id).course_details,
        }

        cert_id = str(random.randint(00000000, 99999999)).zfill(8)
        entry = Certification(
            student_id=student_id,
            course_id=course_id,
            mentor_id=mentor_id,
            certification_code=cert_id,
            certification_date=datetime.date.today(),
        )

        try:
            db.session.add(entry)
            db.session.commit()

            x = generate_pdf(
                params["name"],
                params["mentor"],
                params["course"],
                params["desc"],
                cert_id,
            )
            if not request.json:

                courses = Course.query.all()
                students = Student.query.all()
                return render_template(
                    "generate.html",
                    mentor=current_user,
                    courses=courses,
                    students=students,
                    cert_id=cert_id,
                )

            resp = jsonify(cert_id=cert_id, success=True, msg=x)
            return resp
        except BaseException as e:
            return traceback.format_exc()
            return f"There was an issue creating your certificate {params} {cert_id}"

    courses = Course.query.all()
    students = Student.query.all()
    return render_template(
        "generate.html", mentor=current_user, courses=courses, students=students
    )


@certs_bp.route("/api/htmltemplate")
# @jwt_required
def htmltemplate():
    return render_template("htmltemplate.html")


@certs_bp.route("/api/preview")
@jwt_required
def preview():
    return render_template("certificate.html")


@certs_bp.route("/certificate/all")
@login_required
def all_certificates():
    """
    get all certificates
    """
    certs = Certification.query.all()
    res = []
    for cert in certs:
        mentor = f"{Mentor.query.get_or_404(cert.mentor_id).mentor_fname} {Mentor.query.get_or_404(cert.mentor_id).mentor_lname}"
        course = f"{Course.query.get_or_404(cert.course_id).course_name} {Course.query.get_or_404(cert.course_id).course_details}"
        student = f"{Student.query.get_or_404(cert.student_id).student_fname} {Student.query.get_or_404(cert.student_id).student_lname}"
        student_email = f"{Student.query.get_or_404(cert.student_id).student_email}"

        res.append(
            [
                cert.certification_code,
                student,
                student_email,
                course,
                mentor,
                cert.certification_date,
            ]
        )
    return render_template("allcerts.html", certificates=res)


@certs_bp.route("/certificate/<iden>")
def certificate(iden):

    if iden == "00000000":
        return render_template(
            "cert.html",
            iden=url_for("static", filename=f"certificates/wdss_cert_{iden}.pdf"),
            courseName="Introduction to Python",
            studentName="Ann Example",
            cert_id=iden,
        )

    certInfo = Certification.query.filter_by(certification_code=iden).first()
    if certInfo is None:
        return "<p> Certificate does not exist or was not found. If you believe that this is a mistake, please email hello@warwickdatascience.com </p>"
    courseName = Course.query.get_or_404(certInfo.course_id).course_name
    studentName = f"{Student.query.get_or_404(certInfo.student_id).student_fname} {Student.query.get_or_404(certInfo.student_id).student_lname}"

    return render_template(
        "cert.html",
        iden=url_for("static", filename=f"certificates/wdss_cert_{iden}.pdf"),
        courseName=courseName,
        studentName=studentName,
        cert_id=iden,
    )
