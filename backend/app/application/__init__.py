import time
import os
import random

from flask import (
    Flask,
    render_template,
    request,
    abort,
    jsonify,
    redirect,
    url_for)
from flask import send_file

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import safe_str_cmp
import requests
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
from dotenv import load_dotenv
import pymysql
import jsonpickle




db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=False)
    app.debug = True
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    # Set the cookie paths, so that you are only sending your access token
    # cookie to the access endpoints, and only sending your refresh token
    # to the refresh endpoint. Technically this is optional, but it is in
    # your best interest to not send additional cookies in the request if
    # they aren't needed.
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

    # Disable CSRF protection for this example. In almost every case,
    # this is a bad idea. See examples/csrf_protection_with_cookies.py
    # for how safely store JWTs in cookies
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # Set the secret key to sign the JWTs with
    app.config['JWT_SECRET_KEY'] = 'Jiowaj213eddDw'  # Change this!

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{os.environ['SQL_ROOT_PASSWORD']}@db:3306/certificate_portal"        # the variable to be used for all SQLAlchemy commands
    login_manager = LoginManager()

    
    
    login_manager.init_app(app)

    # initilise plugins
    db.init_app(app)
    jwt.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Mentor

    @login_manager.user_loader
    def load_user(user_id):
        return Mentor.query.get(int(user_id))

    @app.route('/')
    def home():
        return redirect("https://www.wdss.io/")


    with app.app_context():
        # import parts of our application
        # from . import auth, crud, certs
        from . import auth, crud, certs
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(crud.crud_bp)
        app.register_blueprint(certs.certs_bp)

        return app







