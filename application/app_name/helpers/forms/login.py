from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from application.app_name.helpers.forms.default import DefaultForm


class LoginForm(DefaultForm, FlaskForm):
    hide_list = ['_prefix', 'meta', '_fields', '_csrf', 'submit', 'csrf_token', 'confirm_password', 'form_errors']

    email = StringField(
        'Username or Email',
        validators=[DataRequired()],
        render_kw={'placeholder': 'NoobMaster69 or NoobMaster69@example.com'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={'placeholder': '***********'}
    )

    submit = SubmitField("Login")
