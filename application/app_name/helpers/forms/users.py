from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from application.app_name.helpers.forms.default import DefaultForm
from application.app_name.crypt import decrypt
from application.app_name.models.role import RolesModel


class UsersForm(DefaultForm, FlaskForm):

    def get_choice_list(self):
        item_list = []
        query = RolesModel.query.with_entities(RolesModel.id, RolesModel.name)
        items = query.all()
        for item in items:
            item_list.append([item.id, decrypt(item.name)])
        return item_list

    def __init__(self):
        self.roles.kwargs['choices'] = self.get_choice_list()

        super().__init__()

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'NoobMaster69'}
    )
    phone = StringField(
        'Phone Number',
        validators=[Length(min=10)],
        render_kw={'placeholder': '+55XX9xxxxxxxx'}
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), EqualTo('confirm_password', message='Passwords need to match')],
        render_kw={'placeholder': '***********'}
    )
    confirm_password = PasswordField(
        'Confirm your password',
        render_kw={'placeholder': '***********'},
    )

    roles = SelectMultipleField('Roles selected')

    submit = SubmitField("Save")
