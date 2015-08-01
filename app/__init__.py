from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
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
reg = models.Region('terra', [1, 2, 3])
db.session.add(reg)
db.session.commit()
