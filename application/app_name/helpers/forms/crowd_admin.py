from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from crowd_supporter.app.helpers.forms.default import DefaultForm
from crowd_supporter.app.models import OrganizedCrowdModel
from crowd_supporter.app.crypt import decrypt


class CrowdAdminForm(DefaultForm, FlaskForm):

    def get_choice_list(self):
        item_list = []
        query = OrganizedCrowdModel.query.with_entities(OrganizedCrowdModel.id, OrganizedCrowdModel.name)
        items = query.all()
        for item in items:
            item_list.append([item.id, decrypt(item.name)])
        return item_list

    def __init__(self):
        self.organized_crowd_id.kwargs['choices'] = self.get_choice_list()

        super().__init__()

    hide_list = ['_prefix', 'meta', '_fields', '_csrf', 'submit', 'csrf_token', 'confirm_password', 'form_errors']

    username = StringField(
        'Nome de Usuário',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'NoobMaster69'}
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )
    organized_crowd_id = SelectField(
        'Torcida Organizada',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Senha',
        validators=[DataRequired(), EqualTo('confirm_password', message='As senhas precisam ser iguais')],
        render_kw={'placeholder': '***********'}
    )
    confirm_password = PasswordField(
        'Confirme sua senha',
        render_kw={'placeholder': '***********'},
    )

    submit = SubmitField("Salvar")
