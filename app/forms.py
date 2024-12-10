from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your email"})
    password = StringField("Password", validators=[DataRequired(message="This field is required")], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Continue")
