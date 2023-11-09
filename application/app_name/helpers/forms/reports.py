from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask import session

from crowd_supporter.app.helpers.forms.default import DefaultForm
from crowd_supporter.app.crypt import decrypt
from crowd_supporter.app.models import OrganizedCrowdModel


class ReportForm(DefaultForm, FlaskForm):

    def get_choice_list(self):
        item_list = []
        query = OrganizedCrowdModel.query.with_entities(OrganizedCrowdModel.id, OrganizedCrowdModel.name)
        if session.get('organized_crowd_id'):
            query = query.filter(OrganizedCrowdModel.id == session['organized_crowd_id'])
        else:
            item_list.append(["all", "Todas"])

        items = query.all()

        for item in items:
            item_list.append([item.id, decrypt(item.name)])

        return item_list

    def __init__(self):
        self.organized_crowd_id.kwargs['choices'] = self.get_choice_list()
        super().__init__()

    option = SelectField(
        'Gerar relatorio de',
        choices=[['crowd_fans', 'Torcedores'], ['payments', 'Financeiro']],
        validators=[DataRequired()]
    )
    organized_crowd_id = SelectField(
        'Torcida Organizada',
        validators=[DataRequired()]
    )
    old_date = DateField(
        'De',
        default=datetime.now() - timedelta(days=15),
        render_kw={'placeholder': '***********'}
    )
    newest_date = DateField(
        'Até',
        default=datetime.now()
    )
    submit = SubmitField("Solicitar relatório")
