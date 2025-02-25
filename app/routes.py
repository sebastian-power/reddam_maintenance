from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
)
from app.forms import (
    SignupForm,
    LoginForm,
    EditProfileForm,
    ChangePasswordForm,
    ForgotPasswordForm,
    AddTaskForm,
    EditTaskForm,
    AssignWorkerForm
)
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
from .queries import *
from .emails import *
import os
import bcrypt
from datetime import datetime

alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
]
def unencrypt_pwd(pwd):
    return int(
        int("".join([str(alphabet.index(char.lower())) for char in pwd ]))
        / 13087137435673
        )

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=("GET", "POST"))
@login_required
def home_page():
    edit_task_form = EditTaskForm()
    add_task_form = AddTaskForm()
    assign_worker_form = AssignWorkerForm()
    if add_task_form.validate_on_submit():
        title = add_task_form.title.data
        description = add_task_form.description.data
        requested_by = current_user.user_id
        status = "Pending"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_by = add_task_form.due_by.data.strftime("%Y-%m-%d %H:%M:%S") if add_task_form.due_by.data else None
        new_task = Task(
            title=title,
            description=description,
            requested_by=requested_by,
            status=status,
            created_at=created_at,
            due_by=due_by,
        )
        add_task(new_task)
        send_new_task_email(current_user.email, new_task)
        return redirect(url_for("main.home_page"))
    if edit_task_form.validate_on_submit():
        title = edit_task_form.title_edit.data
        description = edit_task_form.description_edit.data
        task_id_encrypted = request.form.get("task_id_encrypted")
        decoded_value = unencrypt_pwd(task_id_encrypted)
        due_by = edit_task_form.due_by_edit.data.strftime("%Y-%m-%d %H:%M:%S") if edit_task_form.due_by_edit.data else None
        new_task = Task(
            task_id=decoded_value,
            title=title,
            description=description,
            due_by=due_by,
        )
        update_task(new_task)
        return redirect(url_for("main.home_page"))
    if assign_worker_form.validate_on_submit():
        worker = assign_worker_form.worker.data
        task_id_encrypted = request.form.get("task_id_encrypted")
        decoded_value = unencrypt_pwd(task_id_encrypted)
        assign_task(decoded_value, find_user_by_name(worker).user_id)
        assigned_to_email(find_user_by_name(worker).email, find_task_by_id(decoded_value))
    if current_user.role == "Admin":
        return render_template("admin.html", add_task_form=add_task_form, edit_form=edit_task_form, assign_worker_form=assign_worker_form)
    elif current_user.role == "Worker":
        return render_template("worker.html", add_task_form=add_task_form, edit_form=edit_task_form)
    elif current_user.role == "Member":
        return render_template("member.html", add_task_form=add_task_form, edit_form=edit_task_form)
    


@main_bp.route("/login", methods=("GET", "POST"))
def login():
    """Render's the log in page

    Returns:
        str: The rendered html for the page
    """
    form = LoginForm()
    error = ""
    if session.get("auto_login"):
        print("auto_login")
        session.pop("auto_login")

        email = request.args.get("email")
        password = request.args.get("password")
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
        hashed_password = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        if role == "Admin" and role_pwd != os.getenv("ROLE_PWD"):
            return render_template(
                "signup.html", form=form, error="Role password is incorrect"
            )
        elif role == "Worker" and role_pwd != os.getenv("WRKR_PWD"):
            return render_template(
                "signup.html", form=form, error="Role password is incorrect"
            )
        add_user(User(username=name, email=email, role=role, password=hashed_password))
        session["auto_login"] = True
        return redirect(url_for("main.login", email=email, password=form.password.data))
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


@main_bp.route("/forgot_password", methods=("GET", "POST"))
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        if find_user_by_email(email):
            token = send_forgot_pwd_email(email)
            add_token_to_db(email, token)
            return "Email with reset link sent"
        else:
            return "Account with email does not exist"

    return render_template("forgot_pwd.html", form=form)


@main_bp.route("/change_pwd_unauth", methods=("GET", "POST"))
def change_pwd_unauth():
    form = ChangePasswordForm()
    token = request.args.get("utkn")
    session["token"] = token
    email_for_token = find_token_in_db(token)
    if form.validate_on_submit():
        newpwd = form.password.data
        session["token"] = token
        email_for_token = find_token_in_db(token)
        if email_for_token:
            update_profile(find_user_by_email(email_for_token).user_id, password=newpwd)
        return redirect(url_for("main.login"))
    if email_for_token:
        return render_template("change_password.html", form=form)
    else:
        return "Invalid token"


@main_bp.route("/change_pwd_auth", methods=("GET", "POST"))
@login_required
def change_pwd_auth():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        update_profile(current_user.user_id, password=password)
        return redirect(url_for("main.profile"))
    return render_template("change_password.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))