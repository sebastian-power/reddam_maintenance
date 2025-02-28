from flask_login import UserMixin
from datetime import datetime
from random import choice

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
    def __init__(self, task_id: int = None, title: str =None, description: str =None, requested_by: int =None, requested_by_name: str = None, status: str = None, assigned_to: int = None, assigned_to_name: str = None, created_at: str = None, due_by: str = None):
        self.task_id = task_id
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        if self.task_id:
            self.task_id_encoded = ''.join([choice([alphabet[int(char)], alphabet[int(char)].capitalize()]) for char in str(self.task_id*13087137435673)])
        self.title = title
        self.description = description
        self.requested_by = requested_by
        self.requested_by_name = requested_by_name
        self.status = status
        self.assigned_to = assigned_to
        self.assigned_to_name = assigned_to_name
        self.created_at = created_at
        if self.created_at:
            self.created_at_str = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S").strftime("%B %-d, %Y")
        self.due_by = due_by
        if self.due_by:
            self.due_by_str = datetime.strptime(str(self.due_by), "%Y-%m-%d %H:%M:%S").strftime("%B %-d, %Y")