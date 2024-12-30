from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, StringField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError

def validate_role_pwd(form, field):
        if form.role.data == "Admin" and not field.data:
            raise ValidationError("Role password is required for Admin role")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your email"})
    password = PasswordField("Password", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Continue")

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="This field is required"), Length(max=100)], render_kw={"placeholder": "Enter your name"})
    email = EmailField("Email", validators=[DataRequired(message="This field is required"), Email(message="Please enter a valid email"), Length(max=100)], render_kw={"placeholder": "Enter your email"})
    role = SelectField("Role", validators=[DataRequired(message="This field is required")], choices=[("Member", "Member"), ("Worker", "Worker"), ("Admin", "Admin")])
    role_pwd = PasswordField("Role Password", validators=[validate_role_pwd], render_kw={"placeholder": "Enter the role password"})
    password = PasswordField("Password", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Create an account")

class EditProfileForm(FlaskForm):
     name = StringField("Name", validators=[DataRequired(message="This field is required"), Length(max=100)])
     email = EmailField("Email", validators=[DataRequired(message="This field is required"), Email(message="Please enter a valid email"), Length(max=100)])
     submit = SubmitField("Save")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your new password"})
    submit = SubmitField("Confirm")

class ForgotPasswordForm(FlaskForm):
     email = EmailField("Email", validators=[Email(message="Please enter a valid email")], render_kw={"placeholder": "Enter your email"})
     submit = SubmitField("Send Password Reset Link")

class AddTaskForm(FlaskForm):
     title = StringField("Title", validators=[DataRequired(message="This field is required"), Length(max=255, message="Title cannot be longer than 255 characters")], render_kw={"placeholder": "Enter task title"})
     due_by = DateField("To be completed by", validators=[Length(max=255, message="Title cannot be longer than 255 characters")])
     description = TextAreaField("Task Details", validators=[Length(max=255, message="Title cannot be longer than 255 characters")], render_kw={"placeholder": "Enter task description"})
     submit = SubmitField("Create Task")
