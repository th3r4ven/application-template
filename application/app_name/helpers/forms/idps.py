from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, URLField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from crowd_supporter.app.helpers.forms.default import DefaultForm


class IDPsForm(DefaultForm, FlaskForm):
    name = StringField(
        'Nome',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'Google APP PRD'}
    )
    scopes = StringField(
        'Escopos',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'openid profile'}
    )
    client_id = StringField(
        'Client ID',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': ''}
    )
    authorization_url = URLField(
        'URL de Autorização',
        validators=[DataRequired()],
        render_kw={'placeholder': 'https://example.com/oauth2/authorize'}
    )
    token_url = URLField(
        'URL de Token',
        validators=[DataRequired()],
        render_kw={'placeholder': 'https://example.com/oauth2/token'}
    )
    userinfo_url = URLField(
        'URL de informações do usuário',
        validators=[DataRequired()],
        render_kw={'placeholder': 'https://example.com/oauth2/userinfo'}
    )
    client_secret = PasswordField(
        'Client Secret',
        validators=[DataRequired()],
        render_kw={'placeholder': '***********'}
    )
    idp_type = SelectField(
        'Tipo de integração', choices=['google', 'facebook', 'twitter', 'github',
                                       'discord', 'instagram', 'apple', 'other'],
        validators=[DataRequired()]
    )

    submit = SubmitField("Salvar")
