# reddam_maintenance
# Development Setup Instructions
## Files
`git clone https://github.com/sebastian-power/reddam_maintenance.git`
## Python Reqs
`pip install -r requirements.txt`
## MySQL Server
[Install MySQL Server](https://www.geeksforgeeks.org/how-to-install-mysql-on-linux/) if you haven't already
`mysql -u root -p`
`CREATE DATABASE dbnamehere`
## .env
Create a file named `.env` in the root project directory with contents
```
DB_PWD="root password here"
DB_NAME="database to be used for project here"
```