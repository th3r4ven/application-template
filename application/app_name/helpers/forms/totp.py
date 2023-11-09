from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

from crowd_supporter.app.helpers.forms.default import DefaultForm


class TOTPForm(DefaultForm, FlaskForm):

    otp = IntegerField(
        'Codigo OTP',
        validators=[DataRequired()]
    )

    submit = SubmitField("Validar")
