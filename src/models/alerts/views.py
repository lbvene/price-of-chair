from flask import Blueprint, render_template, request, session, redirect, url_for
from models.alerts.alert import Alert
from models.items.item import Item
import models.users.decorators as user_decorators

__author__ = 'lbvene'

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return "This is the alerts index."

@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def new_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)

        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_and_save_item_price()

        return redirect(url_for('.new_alert_success'))

    return render_template('alerts/new_alert.html.j2')

@alert_blueprint.route('/new_alert_success')
def new_alert_success():
    return render_template('alerts/new_alert_success.html.j2')

@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/edit_alert.html.j2', alert=alert)

@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('.deactivate_alert_success', alert_id=alert_id))

@alert_blueprint.route('/deactivate_success/<string:alert_id>')
def deactivate_alert_success(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/deactivate_alert_success.html.j2', alert=alert)

@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('.delete_alert_success', alert_id=alert_id))

@alert_blueprint.route('/delete_success')
def delete_alert_success():
    return render_template('alerts/delete_alert_success.html.j2')

@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('.activate_alert_success', alert_id=alert_id))

@alert_blueprint.route('/activate_success/<string:alert_id>')
def activate_alert_success(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/activate_alert_success.html.j2', alert=alert)

@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html.j2', alert=alert)

'''@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
'''

@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_and_save_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
