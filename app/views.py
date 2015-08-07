from app import app
from flask import render_template
from .models import Region, City


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           cities=Region.query.first().cities)
