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

app = Flask(__name__)


def generate_pdf(name, mentor, course, details):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "templates/htmltemplate.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    cert_id = uuid.uuid1()
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
                     f'static/certificates/{cert_id}-temp.pdf', options=options)
    infile = PdfFileReader(f'static/certificates/{cert_id}-temp.pdf', 'rb')
    output = PdfFileWriter()
    p = infile.getPage(0)
    output.addPage(p)

    with open(f'static/certificates/{cert_id}.pdf', 'wb') as f:
        output.write(f)


@app.route('/generate', methods=['POST'])
def generate():
    if not request.json:
        abort(400)
    params = {
        'name': request.json['name'],
        'mentor': request.json['mentor'],
        'course': request.json['course'],
        'desc': request.json['desc']
    }
    generate_pdf(params['name'], params['mentor'],
                 params['course'], params['desc'])
    resp = jsonify(success=True)
    return resp


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

    return render_template("cert.html", iden=url_for('static', filename="certificates/"+iden+".pdf"))
    # return send_file('static/certificates/certificate-docker2.pdf', attachment_filename=f'{iden}.pdf')
    # with open('/code/certificate-docker.pdf', 'rb') as static_file:
        # return send_file(static_file, attachment_filename='eew324432io328dh.pdf')
# 
