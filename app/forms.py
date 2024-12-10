from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your email"})
    password = PasswordField("Password", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Continue")
