from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from application.app_name.helpers.forms.default import DefaultForm


class ProfileForm(DefaultForm, FlaskForm):
    hide_list = ['_prefix', 'meta', '_fields', '_csrf', 'submit', 'csrf_token', 'form_errors']

    username = StringField(
        'Name',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'NoobMaster69'}
    )
    phone = StringField(
        'Phone number',
        render_kw={'placeholder': '+55XX9xxxxxxxx'}
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )

    submit = SubmitField("Save")
