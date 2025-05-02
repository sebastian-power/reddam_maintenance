from flask import (
    Blueprint,
    request,
    jsonify,
    Response
)
from flask_login import login_required, current_user
from .queries import find_task_by_id, retrieve_tasks, retrieve_workers, update_task_status, delete_task_query, assign_task
from .emails import task_completed_email

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
@login_required
def get_task():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    task = find_task_by_id(decoded_value).__dict__
    return jsonify(task)


@api_bp.route("/get_tasks_sorted", methods=("POST",))
@login_required
def get_tasks_sorted():
    data = request.get_json()
    sort_method = data.get("sort_method")
    tasks = retrieve_tasks(sort_by=sort_method)
    return jsonify({"tasks": tasks})

@api_bp.route("/get_workers", methods=("POST",))
@login_required
def get_workers():
    workers = retrieve_workers()
    return jsonify({"worker_names": workers})

@api_bp.route("/change_status_drag", methods=("POST",))
@login_required
def change_status_drag():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    new_status = data.get("new_status")
    update_task_status(decoded_value, new_status)
    if new_status == "Done":
        task = find_task_by_id(decoded_value)
        task_completed_email(task)
    return "Status updated"

@api_bp.route("/delete_task", methods=("POST",))
@login_required
def delete_task():
    data = request.get_json()
    encoded_value = data.get("encoded_value")
    decoded_value = unencrypt_pwd(encoded_value)
    delete_task_query(decoded_value)
    return "Task deleted"

@api_bp.route("/assign_worker", methods=("POST",))
@login_required
def assign_worker():
    if current_user.role == "Admin" or current_user.role == "Worker":
        data = request.get_json()
        encoded_value = data.get("encoded_value")
        decoded_value = unencrypt_pwd(encoded_value)
        assign_task(decoded_value, current_user.user_id)
        return "Worker assigned"
    else:
        return Response(status=403)

@api_bp.route("/current_user", methods=("GET",))
@login_required
def current_user_api():
    return jsonify({"user_id": current_user.user_id})
