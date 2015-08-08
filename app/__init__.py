from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from collections import deque
import os


app = Flask(__name__)
app.config.from_object('config')
try:
    os.remove(app.config['DB_FILE_PATH'])
except FileNotFoundError:
    pass

db = SQLAlchemy(app)
# the app in the import statement below is not the same
# as the app variable above it. It does however import
# the app variable which is why it is placed after instatiating
# and assigning the Flask instance to app
from app import views, models

db.create_all()

regions = deque()
regions.append(models.Region('terra', [2]))  # 1
regions.append(models.Region('markee', [1]))  # 2
regions.append(models.Region('heim', [1, 2]))  # 3

for region in regions:
    db.session.add(region)
db.session.flush()

cities = deque()
cities.append(models.City('steepes', 1))
cities.append(models.City('danggg', 1))
cities.append(models.City('planes', 2))
cities.append(models.City('forest', 2))
cities.append(models.City('castle', 3))
cities.append(models.City('toilet', 3))

for city in cities:
    db.session.add(city)
db.session.flush()


players = deque()
players.append(models.Player('Kai1'))
players.append(models.Player('Kai2'))
players.append(models.Player('Kai3'))

for player in players:
    db.session.add(player)
db.session.flush()

classes = deque()
classes.append(models.Hsclass('Priest'))
classes.append(models.Hsclass('Warrior'))
classes.append(models.Hsclass('Shaman'))

for hsclass in classes:
    db.session.add(hsclass)
db.session.flush()

city_states = deque()
city_states.append(models.CityState(1, 1))
city_states.append(models.CityState(2, 1))
city_states.append(models.CityState(3, 2))
city_states.append(models.CityState(4, 3))
city_states.append(models.CityState(5, 2))
city_states.append(models.CityState(6, 3))

for state in city_states:
    db.session.add(state)
db.session.flush()

db.session.commit()
