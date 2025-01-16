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