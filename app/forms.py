from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class ActionForm(Form):
    attacker = StringField('Attacker', validators=[DataRequired()])
    defender = StringField('Defender', validators=[DataRequired()])
