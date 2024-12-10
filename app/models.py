from app import db

class User:
    def __init__(self, user_id, username, email, password, role):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

class Task:
    def __init__(self, task_id, title, description, requested_by, status, assigned_to, created_at, due_by):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.requested_by = requested_by
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.due_by = due_by
 