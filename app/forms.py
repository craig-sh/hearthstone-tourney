from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, AnyOf
from . import models
from itertools import chain


class ActionForm(Form):

    attacker = StringField('Atacker', validators=[DataRequired()])
    defender = StringField('Defender', validators=[DataRequired()])

    winner = StringField('Winner', validators=[DataRequired()])

    attacking_class = StringField('Attacking Class', validators=[DataRequired()])
    defending_class = StringField('Defending Class', validators=[DataRequired()])

    attacking_city = StringField('Attacking City', validators=[DataRequired()])
    defending_city = StringField('Defending City', validators=[DataRequired()])

    def validate(self):
        _player_names = [m.name for m in models.Player.query.all()]
        dynamic_player_validators = [self.attacker, self.defender, self.winner]
        for field in dynamic_player_validators:
            field.validators.append(AnyOf(values=_player_names,
                                          message='Must be one of %(values)s'))

        _city_names = [m.nickname for m in models.City.query.all()]
        dynamic_city_validators = [self.attacking_city, self.defending_city]
        for field in dynamic_city_validators:
            field.validators.append(AnyOf(values=_city_names,
                                          message='Must be one of %(values)s'))

        _class_names = [m.name for m in models.Hsclass.query.all()]
        dynamic_class_validators = [self.attacking_class, self.defending_class]
        for field in dynamic_class_validators:
            field.validators.append(AnyOf(values=_class_names,
                                          message='Must be one of %(values)s'))

        res = Form.validate(self)

        for field in chain(dynamic_player_validators,
                           dynamic_city_validators,
                           dynamic_class_validators):
            field.validators.pop(-1)

        return res
