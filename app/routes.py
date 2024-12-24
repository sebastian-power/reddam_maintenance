from flask import Blueprint, render_template, redirect
from .forms import LoginForm, SignupForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home_page():
    """Page looks different for everyone, redirects user to login/signup if cookies don't exist or are validated
    """
    return redirect("/login")

@main_bp.route("/login")
def login():
    """Render's the log in page

    Returns:
        str: The rendered html for the page
    """
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        print(name, password)
    return render_template("login.html", form=form)

@main_bp.route("/signup")
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name
        email = form.email
        role = form.role
        role_pwd = form.role_pwd
        password = form.password
    return render_template("signup.html", form=form)
        
    