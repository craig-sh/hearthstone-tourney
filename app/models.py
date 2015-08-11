from app import db
from sqlalchemy import types
from datetime import datetime

MAX_EVENTS_PER_DAY = 20


class SqlLiteArray(types.TypeDecorator):

    """ Since sqllite doens't support arrays store it as a space delimited
        string of ints.
    """

    impl = types.String(128)

    def process_bind_param(self, value, dialect):
        """ Before inserting an array, combine it into one string
        """
        if value:
            return ' '.join([str(val) for val in value])
        return ''

    def process_result_value(self, value, dialect):
        """ On retrival convert it back to an int
        """
        if not value:
            return []
        return [int(val) for val in value.split(' ')]


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    # QUESTION: Why is the region below this lower case for foreign key
    # but upper case for the relationship
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship('Region', backref=db.backref('cities'))

    def __init__(self, name, region_id):
        self.name = name
        self.region_id = region_id

    def __repr__(self):
        return 'City[%s] %s' % (self.id, self.name)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    adjacent_regions = db.Column(SqlLiteArray)

    def __init__(self, name, adjacent_regions):
        self.name = name
        self.adjacent_regions = adjacent_regions

    def __repr__(self):
        return 'Region[%s] %s' % (self.id, self.name)


class CityState(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City', backref=db.backref('state', uselist=False))

    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    owner = db.relationship('Player', foreign_keys=owner_id)

    health = db.Column(db.Integer, default=30)

    def __init__(self, city_id, owner_id, health=None):
        self.city_id = city_id
        self.owner_id = owner_id
        if health is not None:
            self.health = health


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    # http://www.w3schools.com/html/html_colornames.asp
    color = db.Column(db.String(64), unique=True)

    def __init__(self, name, color):
        self.name = name
        self.color = color


class Hsclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, name):
        self.name = name


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attacker_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    attacker = db.relationship('Player', foreign_keys=attacker_id)

    defender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    defender = db.relationship('Player', foreign_keys=defender_id)

    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    winner = db.relationship('Player', foreign_keys=winner_id)

    attacker_class_id = db.Column(db.Integer, db.ForeignKey('hsclass.id'))
    attacker_class = db.relationship('Hsclass', foreign_keys=attacker_class_id)

    defender_class_id = db.Column(db.Integer, db.ForeignKey('hsclass.id'))
    defender_class = db.relationship('Hsclass', foreign_keys=defender_class_id)

    attacker_city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    attacker_city = db.relationship('City', foreign_keys=attacker_city_id)

    defender_city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    defender_city = db.relationship('City', foreign_keys=defender_city_id)

    event_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, attacker, defender,
                 winner,
                 attacker_class, defender_class,
                 attacker_city, defender_city,
                 event_date=None):
        self.attacker_id = attacker
        self.defender_id = defender
        self.winner_id = winner
        self.attacker_class_id = attacker_class
        self.defender_class_id = defender_class
        self.attacker_city_id = attacker_city
        self.defender_city_id = defender_city

        if event_date is not None:
            self.event_date = event_date

    def process_event(self):
        db.session.add(self)
        db.session.flush()

        today = datetime.today().date()
        if Event.query.filter(Event.event_date > today).count() > MAX_EVENTS_PER_DAY:
            raise Exception('Too many events today')

        if self.winner_id == self.attacker_id:
            self.defender_city.state.owner_id = self.attacker_id
            self.defender_city.state.health -= 2
            self.attacker_city.state.health -= 2
        else:
            self.defender_city.state.health -= 2
            self.attacker_city.state.health -= 4

        db.session.commit()


class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn = db.Column(db.Integer, index=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), index=True)
    player = db.relationship('Player', foreign_keys=player_id)

    def __init__(self, turn, player_id):
        self.turn = turn
        self.player_id = player_id
