from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, URLField, BooleanField
from wtforms.validators import DataRequired, Length

from crowd_supporter.app.helpers.forms.default import DefaultForm


class BadgeForm(DefaultForm, FlaskForm):

    name = StringField(
        'Nome',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'Furia Top 1 HLTV!!'}
    )
    points = IntegerField(
        "Pontos"
    )
    logo = URLField(
        "Url da logo"
    )
    available = BooleanField(
        "Ativa",
        default=True
    )

    submit = SubmitField("Salvar")
