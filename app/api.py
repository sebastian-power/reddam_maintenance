from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
    jsonify,
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
import base64
from datetime import datetime
import json

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

api_bp = Blueprint("api", __name__)

@api_bp.route("/get_task", methods=("POST",))
def get_task():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    task = find_task_by_id(decoded_value).__dict__
    return jsonify(task)


@api_bp.route("/get_tasks_sorted", methods=("POST",))
def get_tasks_sorted():
    data = request.get_json()
    sort_method = data.get("sort_method")
    tasks = retrieve_tasks(sort_by=sort_method)
    return jsonify({"tasks": tasks})

@api_bp.route("/get_workers", methods=("POST",))
def get_workers():
    workers = retrieve_workers()
    return jsonify({"worker_names": workers})

@api_bp.route("/change_status_drag", methods=("POST",))
def change_status_drag():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    new_status = data.get("new_status")
    update_task_status(decoded_value, new_status)
    return "Status updated"

@api_bp.route("/delete_task", methods=("POST",))
def delete_task():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    delete_task_query(decoded_value)
    return "Task deleted"

@api_bp.route("/assign_worker", methods=("POST",))
def assign_worker():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    assign_task(decoded_value, current_user.user_id)
    return "Worker assigned"

@api_bp.route("/current_user", methods=("GET",))
def current_user_api():
    return jsonify({"user_id": current_user.user_id})