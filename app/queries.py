import mysql.connector
from .models import *
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
    print("Connected")
    if email:
        cursor.execute("""
        UPDATE users SET email = %s WHERE user_id = %s
        """, (email, int(user_id)))
    if name:
        cursor.execute("""
        UPDATE users SET username = %s WHERE user_id = %s
        """, (name, int(user_id)))
    if password:
        cursor.execute("""
        UPDATE users SET password = %s WHERE user_id = %s
        """, (password, int(user_id)))
    db.commit()
    cursor.close()
    db.close()


