from app import db
from sqlalchemy import types


class SqlLiteArray(types.TypeDecorator):

    """ Since sqllite doens't support arrays store it as a space delimited
        string of ints.
    """

    impl = types.String(128)

    def process_bind_param(self, value, dialect):
        """ Before inserting an array, combine it into one string
        """
        return ' '.join([str(val) for val in value])

    def process_result_value(self, value, dialect):
        """ On retrival convert it back to an int
        """
        return [int(val) for val in value.split(' ')]


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    # QUESTION: Why is the region below this lower case for foreign key
    # but upper case for the relationship
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship('Region', backref=db.backref('cities',
                                                          lazy='dynamic'))

    def __init__(self, nickname, region_id):
        self.nickname = nickname
        self.region_id = region_id
        self.region = Region.query.filter_by(id=region_id).first()

    def __repr__(self):
        return 'City[%s] %s' % (self.id, self.nickname)


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    adjacent_regions = db.Column(SqlLiteArray)

    def __init__(self, nickname, adjacent_regions):
        self.nickname = nickname
        self.adjacent_regions = adjacent_regions

    def __repr__(self):
        return 'Region[%s] %s' % (self.id, self.nickname)
