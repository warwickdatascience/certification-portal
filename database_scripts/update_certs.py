import requests

def get_certifications():
    url = "https://cert.wdss.io/api/crud/table/certification"
    return requests.get(url).text

def add_certificate(student_id, mentor_id, course_id, certificate_code):
    url = "https://cert.wdss.io/api/certificate/update"

    data = {
    "student_id": student_id,
    "mentor_id": mentor_id,
    "course_id": course_id,
    "certificate_code": certificate_code}
    x = requests.post(url, json=data)

print(get_certifications())