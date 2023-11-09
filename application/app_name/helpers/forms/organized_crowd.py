from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from crowd_supporter.app.helpers.forms.default import DefaultForm


class OrganizedCrowdForm(DefaultForm, FlaskForm):

    name = StringField(
        'Nome',
        validators=[DataRequired(), Length(min=3)],
        render_kw={'placeholder': 'DeZorganizada'}
    )

    submit = SubmitField("Salvar")
