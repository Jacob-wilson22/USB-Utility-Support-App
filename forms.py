from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

class DeviceLogForm(FlaskForm):
    fault_type = SelectField('Fault Type', choices=[], coerce=str)
    fault_severity = StringField('Fault Severity', validators=[InputRequired()])
    fault_description = TextAreaField('Fault Description', validators=[InputRequired()])
    submit = SubmitField('Submit')