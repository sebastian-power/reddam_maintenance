from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id=None, username=None, email=None, password=None, role=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
    def get_id(self):
        return self.user_id
    
        
    

class Task:
    def __init__(self, task_id: int = None, title: str =None, description: str =None, requested_by: int =None, status: str = None, assigned_to: int = None, created_at: str = None, due_by: str = None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.requested_by = requested_by
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.due_by = due_by