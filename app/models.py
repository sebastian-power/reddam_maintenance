class User:
    def __init__(self, user_id=None, username=None, email=None, password=None, role=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

class Task:
    def __init__(self, task_id=None, title=None, description=None, requested_by=None, status=None, assigned_to=None, created_at=None, due_by=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.requested_by = requested_by
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.due_by = due_by