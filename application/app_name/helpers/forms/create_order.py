from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange

from crowd_supporter.app.helpers.forms.default import DefaultForm


class CreateOrderForm(DefaultForm, FlaskForm):

    type = SelectField(
        'Tipo de Transação',
        validators=[DataRequired()],
        choices=[['donation', 'Doação'], ['supporter', 'Socio Torcedor']]
    )

    value = IntegerField(
        'Valor',
        validators=[NumberRange(min=1)],
        default=25,
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )

    fan_id = StringField(
        'Torcedor',
        validators=[DataRequired()]
    )

    submit = SubmitField("Criar")
