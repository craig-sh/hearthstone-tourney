from app import app
from flask import render_template
from .models import City
from .forms import ActionForm


@app.route('/')
@app.route('/index')
def index():
    cities = City.query.all()
    return render_template('index.html',
                           cities=cities)


@app.route('/action', methods=['GET', 'POST'])
def login():
    form = ActionForm()
    return render_template('action.html',
                           form=form)
