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

## Context Diagram
![RMS-1](https://github.com/user-attachments/assets/b70373f7-5dc8-423b-b863-9c7f7dcb62a5)

## User Stories
- As a school principal, I want everything in the school to be working properly, so that students and teachers can focus on learning and teaching
- As a maintenance admin, I want to:
  - Assign tasks to workers
  - Let others create tasks
  - Change information about my account if needed like my email or password
  - Notify workers of when they recieve a task
  - Be notified when there is a new task or when a task is completed to confirm and delete it
  - So that that I can fulfill the requirement of keeping everything in the school working easily
- As a maintenance worker, I want to:
  - Assign tasks I can do to myself
  - Change information about my account if needed like my email or password
  - Keep a record of the tasks I am working on
  - Be notified when I recieve a task or when a new task is created
  - So that I can manage my workload easier
- As a member of the school, I want to:
  - Create maintenance tasks if something I use or see is not working
  - Be updated on how the job is going
  - Change information about my account if needed like my email or password
  - So that I can keep everything in the school working so I can work unimpeded

## Project Plan
Include images of actual chart
![image](https://github.com/user-attachments/assets/2c8842a3-c2f2-4e54-acb2-5ec06148e7dd)

## Class Diagram of non-imported Classes
![class_diagram drawio](https://github.com/user-attachments/assets/61103f01-6c1a-4768-ab6c-e2543389951c)

## Database Schema Diagram
![drawSQL-image-export-2025-02-05](https://github.com/user-attachments/assets/c4fd649d-d288-41c3-8abc-5a9ca83bc656)
The below images were created by the "describe" command in the MySQL Shell for some extra detail:
![image](https://github.com/user-attachments/assets/b09b8535-ddfd-47ed-b1f0-1c99b7bf21b2)
![image](https://github.com/user-attachments/assets/5b686309-abaf-4b1c-8158-123ef45c8c71)

## Approach to Development
Firstly in the development process, the skeleton of the project was created. Then the development process followed a similar path to the user experience to ensure all functionalities of the previous pages could be used as they had existing functionality to build on top off. For example, the login page was developed before dashboard page so the dashboard page could send the user who requested the task to the server, and the dashboard could adapt to the role of the user. The general order of development went: signup -> login -> profile -> dashboard -> emails.

## Object Oriented Programming
By creating classes for each form, it was easier to render the forms in the jinja templates and to manage the post requests from the frontend in the backend as the structure of the form was already defined. The models.py file creates classes that allow the developer to manage classes like User and Task in the same way throughout the program, which means any time that data relating to users or tasks from the database is interacted with, it is through the User or Task model to make the program easier and more adaptable, allowing the developer to use some of the advantages of an ORM while still having the capability to use raw MySQL queries.

## Data Dictionary
![image](https://github.com/user-attachments/assets/4e14c4a8-1f49-41f4-9c06-48a7398e07ba)
![image](https://github.com/user-attachments/assets/b7453f2b-d9a8-427c-90d7-012ef348e731)
![image](https://github.com/user-attachments/assets/36ffe8b9-d6bc-4b83-a144-cf78a67cb403)

## Designs of Major Algorithms
Encryption algorithm that hides the task_id from the user, ensuring they cannot see the task_id for security reasons
```
return int(
        int("".join([str(alphabet.index(char.lower())) for char in pwd ]))
        / 13087137435673
        )
```
User Authentication. Retrieves User object of user by email inputted by user trying to login, then checks the password inputted against the hash of the password stored in the database. If is the same, user is authenticated
```
user = find_user_by_email(email)
    return user if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")) else None
```
Task Rendering Algorithm (JS)
<ol>
  <li>Retrieve list of tasks in JSON grouped by status from API</li>
  <li>Loop through each status, then through each task in the status group</li>
  <li>Generate HTML for task item and add to list of tasks to be rendered</li>
  <li>Render tasks in specific status group, then clear list for next status group</li>
</ol>

## UI Designs
### Dashboard
![image](https://github.com/user-attachments/assets/e5fecfe9-6f9b-49b1-99e9-c419328ff6f3)
### Profile
![image](https://github.com/user-attachments/assets/5ce225b5-5dd2-491f-92b2-097c848f824f)
### Log In
![image](https://github.com/user-attachments/assets/80e0765b-d437-46a2-b1eb-c834e13dff56)
### Sign Up
![image](https://github.com/user-attachments/assets/cfa268d7-3d02-443c-b9b3-954977c266c1)
### Add Task
![image](https://github.com/user-attachments/assets/64d9f7c5-79d3-4b22-b1de-b50f3d56028b)
### Edit Task
![image](https://github.com/user-attachments/assets/005b349d-414d-4b36-b4b7-92e6cd0dd612)

## Test Plans
### IO Table for renderSortedTasks JS
![image](https://github.com/user-attachments/assets/7c1e4ee8-9ab0-4a58-8bad-85385784ad19)
### IO Table for assignWorker JS
![image](https://github.com/user-attachments/assets/3dee6f78-2db6-4e96-96c3-c5c680187185)
### Tests
The tests located in the test folder test major algorithms in the project that include tests for various API endpoints of the application such as change_status_drag, get_tasks_sorted, delete_task, get_workers, and assign_worker. These methods were prioritised for testing because they are integral for the application's function. These methods also utilise various other modules in the code, so these modules need to work correctly for these functions to pass these tests. TheR provided tests in test_api.py cover various API endpoints of the application, ensuring that they function correctly and handle different scenarios. They use mock objects to simulate database interactions and other dependencies. Additionally, there are tests to verify that unauthorized access to these endpoints is appropriately restricted.
## Major Issues faced
### Prevention of access to real task IDs through encryption
In order to know what task was clicked on, each div needs a unique identifier so the JavaScript file can send a request to the server to retrieve the task data and edit it. This data was encrypted in the div to avoid possible changing of the ID to be able to edit tasks the user isn't supposed to, coupled with backend vertification. The encryption and decryption of this task data added complication throughout many of the backend functions. This complication was solved through a simple function that handled the decryption with each request.
### Render tasks algorithm
The render tasks algorithm involved dynamic generation of HTML with event handles. Each user role needed a different version of this algorithm due to differing permissions, and different HTML for each user dependent on the status and creator of the task and the management of JSON data, resulting in much added complexity and thought about each user's permissions. Many logs to the console to show what point the loop was at helped to overcome this problem and manage the logic, and once the first program was done for admins, it was very easy to adapt the code for different users as admin's can do everything.
### Drag events
Managing drag, drop, and hover events using the jQuery library was rather difficult considering the lack of work I had done with it before and its unique approach to event management, but seeing examples and looking at the documentation helped to overcome this issue. Managing each of these event handlers while they were in an asynchronous function also added a layer of complexity.
### Retrieving task data when task was clicked on in dashboard
The date format was a considerable obstacle in this case due to the varying date formats in JavaScript and its conflict with the default SQL DATETIME format and the datetime element accepted format. This was fixed with relatively simple string manipulation and checking required inputs for the datetime element. The form also had to be dynamically populated, including the encrypted task id hidden input.
