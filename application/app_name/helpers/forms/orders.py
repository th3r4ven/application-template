from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from crowd_supporter.app.helpers.forms.default import DefaultForm
from crowd_supporter.app.models import FanModel
from crowd_supporter.app.crypt import decrypt


class OrdersForm(DefaultForm, FlaskForm):

    def get_choice_list(self):
        item_list = []
        query = FanModel.query.with_entities(FanModel.id, FanModel.username)
        items = query.all()
        for item in items:
            item_list.append([item.id, decrypt(item.name)])
        return item_list

    def __init__(self):
        self.fan_id.kwargs['choices'] = self.get_choice_list()

        super().__init__()

    type = SelectField(
        'Tipo de Transação',
        validators=[DataRequired()],
        choices=[['donation', 'Doação'], ['supporter', 'Socio Torcedor']]
    )
    value = IntegerField(
        'Valor',
        validators=[NumberRange(min=1)],
        render_kw={'placeholder': 'NoobMaster69@dezorganizada.com'}
    )
    fan_id = SelectField(
        'Torcedor',
        validators=[DataRequired()]
    )
    paid_at = DateField(
        'Pago em'
    )
    paid = BooleanField(
        'Pago'
    )

    submit = SubmitField("Salvar")
