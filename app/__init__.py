from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from collections import deque
import os


def init_db():
    regions = dict(
        edmenheim=models.Region('Edmenheim', []),
        yarg=models.Region('Yarg Forest', []),
        lou=models.Region('Lou Highlands', []),
        markee=models.Region('Markee Planes', []),
        terra=models.Region("Terra D'Creg", []),
        dang=models.Region('Dang Hazerath Steppes', []))

    for region in regions.values():
        db.session.add(region)
    db.session.flush()

    cities = dict(
        triplets=models.City('Triplets', regions['edmenheim'].id),
        vorrros=models.City('Vorros Port', regions['edmenheim'].id),

        circle=models.City('The Circle', regions['yarg'].id),
        cannibal=models.City('Cannibal Village', regions['yarg'].id),
        big=models.City('Bigdee Place', regions['yarg'].id),

        hug=models.City('Hugfarts', regions['lou'].id),
        ash=models.City('Plato of Ashes', regions['lou'].id),
        bat=models.City('Bat Caves', regions['lou'].id),

        sands=models.City('Sands', regions['markee'].id),
        ryangard=models.City('Ryangard', regions['markee'].id),
        ryborg=models.City('Ryborg', regions['markee'].id),

        citadel=models.City('Citadel', regions['terra'].id),
        spikes=models.City('Spikes', regions['terra'].id),
        temple=models.City('Temple of Kai', regions['terra'].id),

        taro=models.City('Taro Rocks', regions['dang'].id),
        dry=models.City('Dry Creek', regions['dang'].id),
        east=models.City('East Zerath', regions['dang'].id),
        high=models.City('High Borough', regions['dang'].id))

    for city in cities.values():
        db.session.add(city)
    db.session.flush()

    players = dict(
        edmond=models.Player('Edmond', 'Orange'),
        dang=models.Player('Dang', 'LightCoral'),
        mark=models.Player('Mark', 'MediumPurple'),
        craig=models.Player('Craig', 'LightSkyBlue'),
        david=models.Player('David', 'LightGreen'),
        ryan=models.Player('Ryan', 'Cyan'))

    for player in players.values():
        db.session.add(player)
    db.session.flush()

    classes = deque()
    classes.append(models.Hsclass('Priest'))
    classes.append(models.Hsclass('Warrior'))
    classes.append(models.Hsclass('Shaman'))
    classes.append(models.Hsclass('Warlock'))
    classes.append(models.Hsclass('Druid'))
    classes.append(models.Hsclass('Mage'))
    classes.append(models.Hsclass('Hunter'))
    classes.append(models.Hsclass('Rogue'))
    classes.append(models.Hsclass('Paladin'))

    for hsclass in classes:
        db.session.add(hsclass)
    db.session.flush()

    city_states = dict(
        triplets=models.CityState(cities['triplets'].id, players['mark'].id),
        vorrros=models.CityState(cities['vorrros'].id, players['mark'].id, 26),

        circle=models.CityState(cities['circle'].id, players['ryan'].id, 28),
        cannibal=models.CityState(cities['cannibal'].id, players['ryan'].id, 28),
        big=models.CityState(cities['big'].id, players['ryan'].id, 28),

        hug=models.CityState(cities['hug'].id, players['ryan'].id, 28),
        ash=models.CityState(cities['ash'].id, players['ryan'].id, 28),
        bat=models.CityState(cities['bat'].id, players['craig'].id, 26),

        sands=models.CityState(cities['sands'].id, players['david'].id, 26),
        ryangard=models.CityState(cities['ryangard'].id, players['ryan'].id),
        ryborg=models.CityState(cities['ryborg'].id, players['ryan'].id, 24),

        citadel=models.CityState(cities['citadel'].id, players['ryan'].id, 28),
        spikes=models.CityState(cities['spikes'].id, players['dang'].id, 26),
        temple=models.CityState(cities['temple'].id, players['craig'].id),

        taro=models.CityState(cities['taro'].id, players['edmond'].id, 26),
        dry=models.CityState(cities['dry'].id, players['dang'].id),
        east=models.CityState(cities['east'].id, players['edmond'].id),
        high=models.CityState(cities['high'].id, players['dang'].id))

    for state in city_states.values():
        db.session.add(state)
    db.session.flush()

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
# the app in the import statement below is not the same
# as the app variable above it. It does however import
# the app variable which is why it is placed after instatiating
# and assigning the Flask instance to app
from app import views, models

db_exists = os.path.exists(app.config['DB_FILE_PATH'])
db.create_all()

if not db_exists:
    init_db()

db.session.commit()
