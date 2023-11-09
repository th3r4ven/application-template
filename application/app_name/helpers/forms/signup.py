from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from crowd_supporter.app.helpers.forms.default import DefaultForm


class SignupForm(DefaultForm, FlaskForm):
    username = StringField(
        'Nome',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'NoobMaster69'}
    )
    phone = StringField(
        'Numero de telefone',
        render_kw={'placeholder': '+55XX9xxxxxxxx'}
    )
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )
    password = PasswordField(
        'Senha',
        validators=[EqualTo('confirm_password', message='As senhas precisam ser iguais')],
        render_kw={'placeholder': '***********'}
    )
    confirm_password = PasswordField(
        'Confirme sua senha',
        render_kw={'placeholder': '***********'},
    )

    submit = SubmitField("Criar conta")
