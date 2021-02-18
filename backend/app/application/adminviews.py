from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import session, redirect, url_for, request, flash
from .models import Mentor
from flask_login import current_user
from wtforms.validators import DataRequired, Email
import os
import hashlib 

class AdminView(ModelView):

    create_modal = True
    edit_modal = True

    def is_accessible(self):
        try:
            mentor = Mentor.query.get(current_user.mentor_id)
            return  mentor.is_admin == 1
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth_bp.login', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        try:
            mentor = Mentor.query.get(current_user.mentor_id)
            return  mentor.is_admin == 1
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth_bp.login', next=request.url))

class MentorView(AdminView):
    can_create = True
    def __init__(self, *args, **kwargs):
        super(MentorView, self).__init__(*args, **kwargs)

    def on_model_change(self, form, model, is_created): 
        """Salt/Hash and save the user's new password."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            model.password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        model.password = key
        model.salt = salt
    
    form_args = dict(
        mentor_fname=dict(label='Firstname', validators=[DataRequired()]),
        mentor_lname=dict(label='Lastname', validators=[DataRequired()]),
        mentor_email=dict(label='Email', validators=[DataRequired(), Email()]),
        password=dict(label='Password', validators=[DataRequired()]),
    )

    column_list = ('mentor_id', 'mentor_fname', 'mentor_lname', 'mentor_email', 'is_admin')
    column_searchable_list = ('mentor_fname', 'mentor_lname', 'mentor_email')
    column_filters = ('mentor_email',)
    form_excluded_columns = ['salt', 'certification']
    # form_columns = ("mentor_email", "password", )

class CourseView(AdminView):

    def __init__(self, *args, **kwargs):
        super(CourseView, self).__init__(*args, **kwargs)

    column_list = ('course_id', 'course_name', 'course_details',)
    column_searchable_list = ('course_id', 'course_name', 'course_details',)
    column_filters = ('course_name',)
    form_excluded_columns = ['course']

    form_args = dict(
        course_name=dict(label='Course Name', validators=[DataRequired()]),
        course_details=dict(label='Course Description', validators=[DataRequired()]),   
    )

class StudentView(AdminView):

    def __init__(self, *args, **kwargs):
        super(StudentView, self).__init__(*args, **kwargs)

    column_list = ('student_id', 'student_fname', 'student_lname', 'student_email',)
    column_searchable_list = ('student_id', 'student_fname', 'student_lname', 'student_email',)
    column_filters = ('student_lname', 'student_email')

class CertificationView(AdminView):
    can_create = False
    can_edit = False
    can_export = True
    def __init__(self, *args, **kwargs):
        super(CertificationView, self).__init__(*args, **kwargs)

    column_list = ('certification_id', 'student', 'mentor', 'course', 'certification_code', 'certification_date')
    column_searchable_list = ('certification_id', 'student_id', 'mentor_id', 'course_id', 'certification_code', )
    column_filters = ('certification_id', 'student_id', 'mentor_id', 'course_id', 'certification_code', 'certification_date',)
    form_excluded_columns = ['student']
    form_args = dict(
        student_fname=dict(label='Firstname', validators=[DataRequired()]),
        student_lname=dict(label='Lastname', validators=[DataRequired()]),   
        student_email=dict(label='Email', validators=[DataRequired(), Email()]),   
    )
    def date_format(self, view, value):
        return value.strftime('%B-%m-%Y')