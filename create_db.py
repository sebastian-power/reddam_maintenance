import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PWD")
)
db.database = os.getenv("DB_NAME")

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Worker', 'Member') NOT NULL
);
""")
cursor.close()
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    task_id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    title TINYTEXT NOT NULL,
    description TINYTEXT,
    requested_by SMALLINT,
    status ENUM('Pending','Not Started','In Progress','Done') NOT NULL,
    assigned_to SMALLINT,
    created_at DATETIME NOT NULL,
    due_by DATETIME,
    FOREIGN KEY (requested_by) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE
);
""")
cursor.close()
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tokens(
    token VARCHAR(70) PRIMARY KEY,
    email VARCHAR(100)
);
""")
db.commit()