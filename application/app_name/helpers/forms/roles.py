from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField
from wtforms.validators import DataRequired

from application.app_name.helpers.forms.default import DefaultForm
from application.app_name.models.user import UsersModel
from application.app_name.crypt import decrypt


class RoleForm(DefaultForm, FlaskForm):

    def get_choice_list(self):
        item_list = []
        query = UsersModel.query.with_entities(UsersModel.id, UsersModel.username)
        items = query.all()
        for item in items:
            item_list.append([item.id, decrypt(item.username)])
        return item_list

    def __init__(self):
        self.users.kwargs['choices'] = self.get_choice_list()

        super().__init__()

    name = StringField("Name", validators=[DataRequired()])

    users = SelectMultipleField('Users selected')

    submit = SubmitField("Save")
