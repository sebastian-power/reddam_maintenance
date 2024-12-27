from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.forms import SignupForm, LoginForm, EditProfileForm
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
from .queries import *
import os
import bcrypt
from time import sleep

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home_page():
    return render_template("dashboard.html")


@main_bp.route("/login", methods=("GET", "POST"))
def login():
    """Render's the log in page

    Returns:
        str: The rendered html for the page
    """
    form = LoginForm()
    error = ""
    if session.get('auto_login'):
        print("auto_login")
        session.pop('auto_login')

        email = request.args.get('email')
        password = request.args.get('password')
        user = authenticate_user(email, password)
        if user:
            login_user(user, remember=True)
            return redirect(url_for("main.home_page"))
        else:
            error = "Login failed. Return to login page"

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = authenticate_user(email, password)
        if user:
            login_user(user, remember=True)
            return redirect(url_for("main.home_page"))
        else:
            error = "Invalid email or password. Try again."
        
    return render_template("login.html", form=form, error=error)


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
        session['auto_login'] = True
        return redirect(url_for('main.login', email=email, password=form.password.data))
    return render_template("signup.html", form=form, error="")


@main_bp.route("/profile", methods=("GET", "POST"))
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        if name != current_user.username:
            update_profile(current_user.user_id, name=name)
        if email != current_user.email:
            update_profile(current_user.user_id, email=email)
        return redirect(url_for("main.profile"))
    return render_template("profile.html", form=form)


@main_bp.route("/forgot_password")
def forgot_password():
    # Include form to get email
    return "Link sent to email to change password"
