from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from application.app_name.helpers.forms.default import DefaultForm


class ProfilePasswordForm(DefaultForm, FlaskForm):
    hide_list = ['_prefix', 'meta', '_fields', '_csrf', 'submit', 'csrf_token', 'confirm_password', 'form_errors']

    old_password = PasswordField(
        'Old password',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'New Password',
        validators=[DataRequired(), EqualTo('confirm_password', message='Passwords need to match')],
        render_kw={'placeholder': '***********'}
    )
    confirm_password = PasswordField(
        'Confirm your password',
        render_kw={'placeholder': '***********'},
    )

    submit = SubmitField("Salve")
