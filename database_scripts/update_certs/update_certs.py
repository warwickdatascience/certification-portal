import mysql.connector
import os
from dotenv import load_dotenv
import jinja2
import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader

load_dotenv()

db = mysql.connector.connect(
        host="127.00.00.1",
        port="32000",
        user="root",
        password=os.environ["SQL_ROOT_PASSWORD"]
)

cursor = db.cursor()

def get_certificates():
    global cursor
    cursor.execute("USE certificate_portal")
    cursor.execute("SELECT student_fname, student_lname, mentor_fname, mentor_lname, course_name, course_details, certification_code, certification_date FROM certification NATURAL JOIN student NATURAL JOIN mentor NATURAL JOIN course")
    return cursor.fetchall()

def generate_pdf(name, mentor, course, details, cert_id, cert_date):
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "/templates/htmltemplate.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    outputText = template.render(
        id=cert_id,
        name=name,
        course_name=course,
        additional_course_details=details,
        date=cert_date.date(),
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
            os.path.dirname(__file__) + f"/newcerts/wdss_cert_{cert_id}.pdf"
        )
        pdfkit.from_file(file_path, dest, options=options)

        infile = PdfFileReader(dest, "rb")
        output = PdfFileWriter()
        p = infile.getPage(0)
        output.addPage(p)
    except Exception as e:
        return str(e)

certs = get_certificates()

for cert in certs:
    name = cert[0] + " " + cert[1]
    mentor = cert[2] + " " + cert[3]
    course = cert[4]
    details = cert[5]
    cert_id = cert[6]
    cert_date = cert[7]
    generate_pdf(name, mentor, course, details, cert_id, cert_date)
