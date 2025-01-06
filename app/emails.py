import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import base64

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

def send_forgot_pwd_email(email: str):
    with initiate_connection() as connection:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL")
        msg["To"] = email
        msg["Subject"] = "Forgot Password"
        token = base64.urlsafe_b64encode(os.urandom(24)).decode("utf-8")
        body = f"""<a href="127.0.0.1:5000/change_pwd_unauth?utkn={token}">Click here to reset your password</a>"""
        msg.attach(MIMEText(body, "html"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL"),
            to_addrs=email,
            msg=msg.as_string()
        )
        connection.quit()
    return token
