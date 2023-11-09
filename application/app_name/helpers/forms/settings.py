from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from application.app_name.helpers.forms.default import DefaultForm


class SettingsForm(DefaultForm, FlaskForm):
    log_level = SelectField(
        'Select log level', choices=['info', 'debug', 'warn', 'error', 'critical'],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")
