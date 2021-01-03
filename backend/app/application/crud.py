import time
import os
import random

from flask import Flask, request, jsonify, redirect, Blueprint

from flask_jwt_extended import jwt_required
 

from PyPDF2 import PdfFileWriter, PdfFileReader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import jsonpickle
from . import db
from .models import Student, Course, Certification, Mentor

crud_bp = Blueprint("crud_bp", __name__)


# test the database connection through this route (for debugging)
@crud_bp.route("/api/dbtest")
@jwt_required
def testdb():
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return "<h1>It works.</h1>"
    except Exception as e:
        # e holds descirption of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text


@crud_bp.route("/api/crud/<table>", methods=["POST", "GET"])
@jwt_required
def crudTable(table):
    # create a new entry
    if request.method == "POST":
        # no checking - just throw an exception if SQL fails
        # if table == "mentor":
        #     entry = Mentor(
        #         mentor_fname=request.json["mentor_fname"],
        #         mentor_lname=request.json["mentor_lname"])
        if table == "student":
            entry = Student(
                student_fname=request.json["student_fname"],
                student_lname=request.json["student_lname"],
                student_email=request.json["student_email"],
            )
        elif table == "course":
            entry = Course(
                course_name=request.json["course_name"],
                course_details=request.json["course_details"],
            )
        elif table == "certification":
            # don't know when this would be used
            entry = Certification(
                student_id=request.json["student_id"],
                course_id=request.json["course_id"],
                mentor_id=request.json["mentor_id"],
                certification_code=request.json["certification_code"],
                certification_date=request.json["certification_date"],
            )
        else:
            return f"Table {table} does not exist!"
        try:
            db.session.add(entry)
            db.session.commit()
            if table == "mentor":
                entry_id = entry.mentor_id
            elif table == "student":
                entry_id = entry.student_id
            elif table == "course":
                entry_id = entry.course_id
            elif table == "certification":
                entry_id = entry.certification_id
            resp = jsonify(success=True, id=entry_id)
            return resp
        except Exception as e:
            return str(e)

    # get all entries
    if table == "mentor":
        returnArray = Mentor.query.all()
    elif table == "student":
        returnArray = Student.query.all()
    elif table == "course":
        returnArray = Course.query.all()
    elif table == "certification":
        returnArray = Certification.query.all()
    else:
        return f"Table {table} does not exist!"

    return jsonpickle.encode(returnArray)


@crud_bp.route("/api/crud/<table>/<iden>", methods=["GET", "PUT", "DELETE"])
@jwt_required
def crudTableId(table, iden):
    if table == "mentor":
        field = Mentor.query.get_or_404(iden)
    elif table == "student":
        field = Student.query.get_or_404(iden)
    elif table == "course":
        field = Course.query.get_or_404(iden)
    elif table == "certification":
        field = Certification.query.get_or_404(iden)
    else:
        return f"Table {table} does not exist!"

    if request.method == "PUT":
        if table == "mentor":
            if "mentor_fname" in request.json:
                field.mentor_fname = request.json["mentor_fname"]
            if "mentor_lname" in request.json:
                field.mentor_lname = request.json["mentor_lname"]

        elif table == "student":
            if "student_fname" in request.json:
                field.student_fname = request.json["student_fname"]
            if "student_lname" in request.json:
                field.student_lname = request.json["student_lname"]

        elif table == "course":
            if "course_name" in request.json:
                field.course_name = request.json["course_name"]
            if "course_details" in request.json:
                field.course_details = request.json["course_details"]

        elif table == "certification":
            # don't know when this would be used
            if "student_id" in request.json:
                field.student_id = request.json["student_id"]
            if "course_id" in request.json:
                field.course_id = request.json["course_id"]
            if "mentor_id" in request.json:
                field.mentor_id = request.json["mentor_id"]
            if "certification_code" in request.json:
                field.certification_code = request.json["certification_code"]
            if "certification_date" in request.json:
                field.certification_date = request.json["certification_date"]

        else:
            return f"Table {table} does not exist!"
        try:
            db.session.commit()
            return redirect(request.url)
        except Exception as e:
            return str(e)

    if request.method == "DELETE":
        try:
            db.session.delete(field)
            db.session.commit()
            return f"Successfully deleted field with id {iden}"
        except Exception as e:
            return str(e)

    return jsonpickle.encode(field)
