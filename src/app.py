from flask import Flask, render_template, redirect, url_for, session
from common.database import Database
from models.users.user import User
from alert_updater import get_update_and_send_email

__author__ = 'lbvene'


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'pensi'

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    if session['email']:
        user = User.find_by_email(session['email'])
        #alerts = Alert.find_by_user_email(user.email)
        alerts = user.get_alerts()
        return redirect(url_for('users.user_alerts', alerts=alerts))

    return render_template('home.html.j2')

from models.users.views import user_blueprint
from models.alerts.views import alert_blueprint
from models.stores.views import store_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
