import mysql.connector
from .models import *
import os

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
