from app import app
from flask import render_template, redirect, url_for, flash, request
from . import models
from .forms import ActionForm


@app.route('/')
@app.route('/index')
def index():
    regions = models.Region.query.order_by(models.Region.name.asc())
    # flash('Testing flash')
    return render_template('index.html',
                           regions=regions)


@app.route('/action', methods=['GET', 'POST'])
def action():
    form = ActionForm()
    if form.is_submitted():
        if request.form['btn'] == 'heal':
            for state in models.CityState.query.all():
                state.add_health(2)
            return redirect(url_for('index'))
        elif form.validate():
            # session['name'] = form.name.data
            a_id = models.Player.query.filter_by(name=form.attacker.data).first().id
            d_id = models.Player.query.filter_by(name=form.defender.data).first().id
            w_id = models.Player.query.filter_by(name=form.winner.data).first().id

            a_city_id = models.City.query.filter_by(name=form.attacking_city.data).first().id
            d_city_id = models.City.query.filter_by(name=form.defending_city.data).first().id

            a_class_id = models.Hsclass.query.filter_by(name=form.attacking_class.data).first().id
            d_class_id = models.Hsclass.query.filter_by(name=form.defending_class.data).first().id

            event = models.Event(a_id,
                                 d_id,
                                 w_id,
                                 a_class_id,
                                 d_class_id,
                                 a_city_id,
                                 d_city_id)

            event.process_event()

            return redirect(url_for('index'))
    return render_template('action.html',
                           form=form)
