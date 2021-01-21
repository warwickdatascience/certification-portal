import time
import os
import random

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    Blueprint,
)

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_login import (
    current_user,
    login_user,
    login_required,
    logout_user,
)

import hashlib

from . import db

from .models import Mentor, User

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/token/auth", methods=["GET", "POST"])
def auth():
    error = None

    if request.method == "POST":
        # hash user password\
        if not request.json:
            entered_username = request.form["username"]
            entered_pass = request.form["password"]
        else:
            entered_username = request.json["username"]
            entered_pass = request.json["password"]

        # get username and password from database
        user = User.query.filter_by(username=entered_username).first()
        username = user.username
        password = user.password
        salt = user.salt

        key = hashlib.pbkdf2_hmac(
            "sha256",  # The hash digest algorithm for HMAC
            entered_pass.encode("utf-8"),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        )

        # compare the values
        if entered_username != username or key != password:
            error = f"Invalid Credentials. Please try again."
        else:
            dictToSend = {"username": entered_username, "password": entered_pass}
            access_token = create_access_token(identity=dictToSend["username"])
            refresh_token = create_refresh_token(identity=dictToSend["username"])
            # Set the JWT cookies in the response
            resp = jsonify(
                {
                    "login": True,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return resp, 200
    return "ok", 200
    # return render_template('login.html', error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/api/password/temp/", methods=["POST"])
# @jwt_required
def temp_pass():
    password = os.environ["TEMP_MENTOR_PASSWORD"]
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        "sha256",  # The hash digest algorithm for HMAC
        password.encode("utf-8"),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    mentor = Mentor.query.filter_by(mentor_id=str(request.json["mentor_id"])).update(
        dict(password=key, salt=salt)
    )
    db.session.commit()
    return str(request.json["mentor_id"])


@auth_bp.route("/changepassword", methods=["GET", "POST"])
@login_required
def change_password():
    error = None
    success = None
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        user = Mentor.query.get_or_404(current_user.mentor_id)
        salt = user.salt
        new_salt = os.urandom(32)

        key = hashlib.pbkdf2_hmac(
            "sha256",  # The hash digest algorithm for HMAC
            old_password.encode("utf-8"),  # Convert the password to bytes
            salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        )

        new_key = hashlib.pbkdf2_hmac(
            "sha256",  # The hash digest algorithm for HMAC
            new_password.encode("utf-8"),  # Convert the password to bytes
            new_salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        confirm_key = hashlib.pbkdf2_hmac(
            "sha256",  # The hash digest algorithm for HMAC
            confirm_password.encode("utf-8"),  # Convert the password to bytes
            new_salt,  # Provide the salt
            100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        # compare the values
        if user.password != key:
            error = f"Invalid Password. Please try again."
        elif new_key != confirm_key:
            error = f"Passwords do not match. Please try again."
        else:
            user.password = new_key
            user.salt = new_salt
            mentor = Mentor.query.filter_by(mentor_id=user.mentor_id).update(
                dict(password=new_key, salt=new_salt)
            )
            db.session.commit()
            success = "Password updated"

    return render_template("changepass.html", error=error, success=success)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # get username and password from database
        post_email = request.form["email"].lower()
        mentor = Mentor.query.filter_by(mentor_email=post_email).first()
        if mentor is None:
            error = f"Invalid Credentials. Please try again."
        else:
            email = mentor.mentor_email
            password = mentor.password
            salt = mentor.salt
            # hash user password
            entered_pass = request.form["password"]
            key = hashlib.pbkdf2_hmac(
                "sha256",  # The hash digest algorithm for HMAC
                entered_pass.encode("utf-8"),  # Convert the password to bytes
                salt,  # Provide the salt
                100000,  # It is recommended to use at least 100,000 iterations of SHA-256
            )

            # compare the values
            if post_email != email or key != password:
                error = f"Invalid Credentials. Please try again."
            else:
                login_user(mentor, remember=True)
                return redirect(url_for("certs_bp.generate"))
    return render_template("login.html", error=error)
