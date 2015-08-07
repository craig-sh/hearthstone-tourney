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

cities = deque()
cities.append(models.City('steepes', 1))
cities.append(models.City('danggg', 1))
cities.append(models.City('planes', 2))
cities.append(models.City('forest', 2))
cities.append(models.City('castle', 3))
cities.append(models.City('toilet', 3))

for city in cities:
    db.session.add(city)

players = deque()
players.append(models.Player('Kai1'))
players.append(models.Player('Kai2'))
players.append(models.Player('Kai3'))

for player in players:
    db.session.add(player)

classes = deque()
classes.append(models.Hsclass('Priest'))
classes.append(models.Hsclass('Warrior'))
classes.append(models.Hsclass('Shaman'))

for hsclass in classes:
    db.session.add(hsclass)

# reg_states = deque()
# reg_states.append(1, 1)
# reg_states.append(2, 1)
# reg_states.append(3, 2)
# reg_states.append(4, 2)
# reg_states.append(5, 2)
# reg_states.append(6, 2)


db.session.commit()
