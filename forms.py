from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError



def character_check(form,field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


# Register form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=15, message='Password must be between 8 and 15 characters in length.')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Both password fields must be equal!')])
    #role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[InputRequired()])
    submit = SubmitField('Register')


# Login form
class LoginForm(FlaskForm):
        username = StringField(validators=[InputRequired(), Email()])
        password = PasswordField(validators=[InputRequired()])
        submit = SubmitField('Login')


class DeviceLogForm(FlaskForm):
    fault_type = SelectField('Fault Type', choices=[], coerce=str)
    fault_severity = StringField('Fault Severity', validators=[InputRequired()])
    fault_description = TextAreaField('Fault Description', validators=[InputRequired()])
    submit = SubmitField('Submit')