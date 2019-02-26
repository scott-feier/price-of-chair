from flask import Blueprint, request, session, url_for, render_template, redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.common.decorators as decorators

base_model = 'alerts'
alert_blueprint = Blueprint(base_model, __name__)


@alert_blueprint.route('/')
def index():
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/create', methods=['GET', 'POST'])
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = request.form['price_limit']

        item = Item(name, url)
        item.load_price()
        item.save_to_db()

        alert = Alert(session['email'], price_limit, item._id)
        alert.save_to_db()
        alert.load_item_price()
#        return render_template(base_model + '/' + 'alert.html', alert=alert)

    #  it's a GET not a POST, OR pass through to here after POST
    return render_template(base_model + '/' + 'create_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def edit_alert(alert_id):
    alert = Alert.get_obj_from_db_by_id(alert_id)
    if request.method == 'POST':
        alert.price_limit = request.form['price_limit']

        alert.update_to_db()
        return redirect(url_for('users.user_alerts'))
#        return render_template(base_model + '/' + 'alert.html', alert=alert)
    else:
        #  it's a GET not a POST
        return render_template(base_model + '/' + 'edit_alert.html', alert=alert)


@alert_blueprint.route('/delete/<string:alert_id>')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def delete_alert(alert_id):
    Alert.del_from_db_by_id(alert_id)
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/deactivate/<string:alert_id>')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def deactivate_alert(alert_id):
    alert = Alert.get_obj_from_db_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def activate_alert(alert_id):
    alert = Alert.get_obj_from_db_by_id(alert_id)
    alert.activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/update/<string:alert_id>')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def update_alert(alert_id):
    alert = Alert.get_obj_from_db_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for('.show_alert', alert_id=alert_id))


@alert_blueprint.route('/show_alert/<string:alert_id>')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def show_alert(alert_id):
    alert = Alert.get_obj_from_db_by_id(alert_id)
    return render_template(base_model + '/' + 'alert.html', alert=alert)
