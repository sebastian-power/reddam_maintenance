import mysql.connector
from .models import User, Task
import os
import bcrypt


def connect_db():
    dbtemp = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.getenv("DB_PWD"),
                database=os.getenv("DB_NAME")
            )
    return dbtemp, dbtemp.cursor()

def add_user(user: User):
    db, cursor = connect_db()
    cursor.execute("""
    INSERT INTO users(username, email, password, role)
    VALUES(%s, %s, %s, %s)
    """, (user.username, user.email, user.password, user.role))
    db.commit()
    cursor.close()
    db.close()

def find_user_by_email(search_string: str) -> User:
    """Returns User object of user with same email

    Args:
        search_string (str): The email to search for

    Returns:
        User: The user object with the same email
    """
    db, cursor = connect_db()
    cursor.execute("""
    SELECT * FROM users WHERE email = %s
    """, (search_string,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return User(user[0], user[1], user[2], user[3], user[4]) if user else None

def find_user_by_name(search_string: str) -> User:
    """Returns User object of user with same username

    Args:
        search_string (str): The username to search for

    Returns:
        User: The user object with the same username
    """
    db, cursor = connect_db()
    cursor.execute("""
    SELECT * FROM users WHERE username = %s
    """, (search_string,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return User(user[0], user[1], user[2], user[3], user[4]) if user else None

def find_user_by_id(search_string: str) -> User:
    """Returns User object of user with same user id

    Args:
        search_string (str): The id to search for

    Returns:
        User: The user object with the same id
    """
    db, cursor = connect_db()
    cursor.execute("""
    SELECT * FROM users WHERE user_id = %s
    """, (int(search_string),))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return User(user[0], user[1], user[2], user[3], user[4]) if user else None

def authenticate_user(email: str, password: str) -> User:
    """Checks if the user is authenticated

    Args:
        email (str): The email of the user
        password (str): The password of the user

    Returns:
        User: True if the user is authenticated, False otherwise
    """
    user = find_user_by_email(email)
    return user if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")) else None

def update_profile(user_id: str, email: str = None, name: str = None, password: str = None):
    """Updates name and email of user (for form in profile)

    Args:
        email (str): New email
        name (str): New name
    """
    db, cursor = connect_db()
    if email:
        cursor.execute("""
        UPDATE users SET email = %s WHERE user_id = %s
        """, (email, int(user_id)))
    if name:
        cursor.execute("""
        UPDATE users SET username = %s WHERE user_id = %s
        """, (name, int(user_id)))
    if password:
        password_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("""
        UPDATE users SET password = %s WHERE user_id = %s
        """, (password_hashed, int(user_id)))
    db.commit()
    cursor.close()
    db.close()

def add_task(task: Task):
    db, cursor = connect_db()
    if task.due_by:
        cursor.execute("""
        INSERT INTO tasks(title, description, requested_by, status, created_at, due_by)
        VALUES(%s, %s, %s, %s, %s, %s)
        """, (task.title, task.description, task.requested_by, task.status, task.created_at, task.due_by))
    else:
        cursor.execute("""
        INSERT INTO tasks(title, description, requested_by, status, created_at)
        VALUES(%s, %s, %s, %s, %s)
        """, (task.title, task.description, task.requested_by, task.status, task.created_at))
    db.commit()
    cursor.close()
    db.close()

def retrieve_tasks(sort_by: str = "due_by") -> dict:
    db, cursor = connect_db()
    tasks = {"Pending": [], "Not Started": [], "In Progress": [], "Done": []}
    for status in tasks.keys():
        cursor.execute(f"""
        SELECT task_id, title, description, requested_by, status, assigned_to, due_by FROM tasks WHERE status = %s ORDER BY %s{" DESC" if sort_by in ["created_at"] else ""}
        """, (status,sort_by))
        task_list_list = cursor.fetchall()
        if task_list_list:
            tasks[status] = [Task(task_id=task_list[0], title=task_list[1], description=task_list[2], requested_by=task_list[3], requested_by_name=find_user_by_id(str(task_list[3])).username, status=task_list[4], assigned_to=task_list[5], assigned_to_name=find_user_by_id(str(task_list[5])).username if task_list[5] else None, due_by=task_list[6]).__dict__ for task_list in task_list_list]
    cursor.close()
    db.close()
    return tasks if tasks != {} else None

def find_task_by_id(task_id: int) -> Task:
    db, cursor = connect_db()
    cursor.execute("""
    SELECT * FROM tasks WHERE task_id = %s
    """, (task_id,))
    task = cursor.fetchone()
    cursor.close()
    db.close()
    return Task(task_id=task[0], title=task[1], description=task[2], requested_by=task[3], requested_by_name=find_user_by_id(str(task[3])).username, status=task[4], assigned_to_name=find_user_by_id(str(task[5])).username if task[5] else None, created_at=task[6], due_by=task[7]) if task else None

def update_task_status(task_id: int, status: str):
    db, cursor = connect_db()
    cursor.execute("""
    UPDATE tasks SET status = %s WHERE task_id = %s
    """, (status, task_id))
    db.commit()
    cursor.close()
    db.close()

def add_token_to_db(email: str, token: str):
    db, cursor = connect_db()
    cursor.execute("""
    INSERT INTO tokens(token, email)
    VALUES(%s, %s)
    """, (token, email))
    db.commit()
    cursor.close()
    db.close()

def find_token_in_db(token: str) -> str:
    db, cursor = connect_db()
    cursor.execute("""
    SELECT email FROM tokens WHERE token = %s
    """, (token,))
    email = cursor.fetchone()
    cursor.close()
    db.close()
    return email[0] if email else None

def update_task(new_task: Task):
    db, cursor = connect_db()
    
    query = "UPDATE tasks SET "
    params = []
    
    if new_task.title is not None:
        query += "title = %s, "
        params.append(new_task.title)
    if new_task.description is not None:
        query += "description = %s, "
        params.append(new_task.description)
    if new_task.assigned_to is not None:
        query += "assigned_to = %s, "
        params.append(new_task.assigned_to)
    if new_task.due_by is not None:
        query += "due_by = %s, "
        params.append(new_task.due_by)
    
    query = query.rstrip(", ")
    
    query += " WHERE task_id = %s"
    params.append(new_task.task_id)
    
    cursor.execute(query, tuple(params))
    db.commit()
    cursor.close()
    db.close()

def retrieve_workers() -> list[str]:
    db, cursor = connect_db()
    cursor.execute("""
    SELECT username FROM users WHERE role = "Worker"
    """)
    workers = cursor.fetchall()
    cursor.close()
    db.close()
    return [worker[0] for worker in workers]

def assign_task(task_id: int, worker_id: int):
    db, cursor = connect_db()
    cursor.execute("""
    UPDATE tasks SET assigned_to = %s WHERE task_id = %s;
    """, (worker_id, task_id))
    db.commit()
    cursor.execute("""
    UPDATE tasks SET status = 'Not Started' WHERE task_id = %s;
    """, (task_id,))
    db.commit()
    cursor.close()
    db.close()

def delete_task_query(task_id: int):
    db, cursor = connect_db()
    cursor.execute("""
    DELETE FROM tasks WHERE task_id = %s
    """, (task_id,))
    db.commit()
    cursor.close()
    db.close()

def get_admin_worker_emails() -> list[str]:
    db, cursor = connect_db()
    cursor.execute("""
    SELECT email FROM users WHERE role = "Admin" OR role = "Worker"
    """)
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return [user[0] for user in users]
