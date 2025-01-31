# reddam_maintenance
# Development Setup Instructions
## Files
`git clone https://github.com/sebastian-power/reddam_maintenance.git`
## Python Reqs
Navigate to the project folder that was downloaded then run
```
python -m venv venv
source venv/bin/activate (Linux & MacOS)
.\venv\Scripts\activate (Windows)
pip install -r requirements.txt
```
## MySQL Server
[Install MySQL Server](https://www.geeksforgeeks.org/how-to-install-mysql-on-linux/) if you haven't already
`mysql -u root -p`
`CREATE DATABASE dbnamehere`
## .env
Create a file named `.env` in the root project directory with contents
```
DB_PWD="root password here"
DB_NAME="database name created earlier for project here"
SECRET_KEY="generate some random letters and numbers here for csrf prevention"
ROLE_PWD="password for admins to create an account"
WRKR_PWD="password for workers to create an account"
EMAIL="email to use to send notifications to users"
EMAIL_APP_PWD="google app password"
```
To create a google app password, navigate to [App Passwords - Google Account](https://myaccount.google.com/apppasswords) and create a new app password with whatever name you want. Paste the generated password into the env file at EMAIL_APP_PWD

# Documentation
## Project Overview
The Reddam Maintenance System is a web-based task management system that allows users to create, assign, and manage tasks, with features for user authentication and email notifications.
>### Roles
  Users may sign up as a Member, Worker, or Admin (workers and admins require passwords) to the system. Members can create, edit, and delete their own tasks, while being able to view all tasks. Workers can self-assign tasks, create, edit, and delete their own tasks, and view all tasks, and change the status of tasks assigned to them. Admins may create, edit, and delete tasks, update the status of tasks, and assign tasks to any worker.
  >### Task Properties
  All tasks have a title, description, status, and due by date that may be changed at any time. They also store various pieces of metadata visible in the database schema later on.
  >### User Authentication and Accounts
  In order to sign up, a username, email, and password are required (and role password to verify that user is allowed to sign up as an admin or worker). 
  >### Emails
  Emails are sent out by the server if: a task is created (admin, worker), for forgot password links, a task is assigned to a worker (relevant worker), a task is completed (admin, user who created task).
## Technologies
The Reddam Maintenance System utilises various frontend and backend technologies, the most significant of which are:
- MySQL Server & MySQL Python connector
- Flask & Jinja2
- Flask-Login
- Flask-WTF
- smtplib
- jQuery
The four programming languages used were:
- Python (Backend)
- HTML5
- CSS3
- JS ES7+

![image](https://github.com/user-attachments/assets/2c8842a3-c2f2-4e54-acb2-5ec06148e7dd)
