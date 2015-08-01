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


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    adjacent_regions = db.Column(SqlLiteArray)

    def __init__(self, nickname, adjacent_regions):
        print(nickname, adjacent_regions)
        self.nickname = nickname
        self.adjacent_regions = adjacent_regions

    def __repr__(self):
        return 'Region[%s] %s' % (self.id, self.nickname)
