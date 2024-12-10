from flask import Blueprint, render_template, redirect
from .forms import LoginForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home_page():
    """Page looks different for everyone, redirects user to login/signup if cookies don't exist or are validated
    """
    return redirect("/login")

@main_bp.route('/login')
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
