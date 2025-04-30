import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import base64
from .models import Task
from .queries import get_admin_worker_emails, find_user_by_id

"""
Admin: Gets new email for new job to assign to people or review it
Workers: Gets new email for new job to claim it
Members: Get emails for status updates of their job (could be every status update or just when the job is completed)

Function for each different email with email template that can just input what needs to be changed
"""

def initiate_connection():
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=os.getenv("EMAIL"), password=os.getenv("EMAIL_APP_PWD"))
    return connection

def send_forgot_pwd_email(email: str) -> str:
    with initiate_connection() as connection:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL")
        msg["To"] = email
        msg["Subject"] = "Forgot Password"
        token = base64.urlsafe_b64encode(os.urandom(24)).decode("utf-8")
        body = f"""<a href="{os.getenv("WEBSITE_DOMAIN")}/change_pwd_unauth?utkn={token}">Click here to reset your password</a><p>If link does not work, use this: {os.getenv("WEBSITE_DOMAIN")}/change_pwd_unauth?utkn={token}"""
        msg.attach(MIMEText(body, "html"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL"),
            to_addrs=email,
            msg=msg.as_string()
        )
        print(f"Sent email to {email}")
        connection.quit()
    return token

def send_new_task_email(email: str, task: Task):
    with initiate_connection() as connection:
        for email in get_admin_worker_emails():
            msg = MIMEMultipart()
            msg["From"] = os.getenv("EMAIL")
            msg["To"] = email
            msg["Subject"] = f"New Task Pending - {task.title}"
            body = f"""<h1>{task.title}</h1><p><b>Description:</b> {task.description}</p><p><b>Requested By:</b> {task.requested_by_name}</p><a href="{os.getenv("WEBSITE_DOMAIN")}/"><p>Click here to assign the task</p></a>({os.getenv("WEBSITE_DOMAIN")}/ if link does not work)"""
            msg.attach(MIMEText(body, "html"))
            connection.sendmail(
                from_addr=os.getenv("EMAIL"),
                to_addrs=email,
                msg=msg.as_string()
            )
        connection.quit()

def assigned_to_email(email: str, task: Task):
    with initiate_connection() as connection:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL")
        msg["To"] = email
        msg["Subject"] = f"Task Assigned - {task.title}"
        body = f"""<h1>{task.title}</h1><p><b>Description:</b> {task.description}</p><a href="{os.getenv("WEBSITE_DOMAIN")}/"><p>Click here to view the task</p></a>({os.getenv("WEBSITE_DOMAIN")}/ if link does not work)"""
        msg.attach(MIMEText(body, "html"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL"),
            to_addrs=email,
            msg=msg.as_string()
        )
        connection.quit()

def task_completed_email(task: Task):
    with initiate_connection() as connection:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL")
        msg["To"] = find_user_by_id(task.requested_by).email
        msg["Subject"] = f"Task Completed - {task.title}"
        body = f"""<h1>Task: "{task.title}" has been completed</h1><a href="{os.getenv("WEBSITE_DOMAIN")}/"><p>Click here to delete the task to confirm it has been completed</p></a>({os.getenv("WEBSITE_DOMAIN")}/ if link does not work)"""
        msg.attach(MIMEText(body, "html"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL"),
            to_addrs=find_user_by_id(task.requested_by).email,
            msg=msg.as_string()
        )
        connection.quit()
