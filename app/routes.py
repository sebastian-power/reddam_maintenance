from flask import Blueprint, render_template, redirect, url_for
from app.forms import SignupForm, LoginForm
from app.models import User
from .queries import *
import os
import bcrypt

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home_page():
    """Page looks different for everyone, redirects user to login/signup if cookies don't exist or are validated"""
    return render_template("dashboard.html")
    # return redirect("/login")


@main_bp.route("/login", methods=("GET", "POST"))
def login():
    """Render's the log in page

    Returns:
        str: The rendered html for the page
    """
    form = LoginForm()
    if form.validate_on_submit():
        name = form.email.data
        password = form.password.data
    return render_template("login.html", form=form)


@main_bp.route("/signup", methods=("GET", "POST"))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        role = form.role.data
        role_pwd = form.role_pwd.data
        hashed_password = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        print(hashed_password)
        if role == "Admin" and role_pwd != os.getenv("ROLE_PWD"):
            return render_template(
                "signup.html", form=form, error="Role password is incorrect"
            )
        add_user(User(username=name, email=email, role=role, password=hashed_password))
        # Make login request next
    return render_template("signup.html", form=form, error="")


@main_bp.route("/profile")
def profile():
    # For now just retrieve user data from db to prove that login worked correctly
    return render_template("profile.html")


@main_bp.route("/forgot_password")
def forgot_password():
    return "That's on you bud"
