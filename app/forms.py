from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, StringField, SelectField
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
