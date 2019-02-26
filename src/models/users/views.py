from flask import Blueprint, request, session, url_for, render_template, redirect

from src.models.users.user import User
import src.models.users.errors as user_errors
import src.common.decorators as decorators

base_model = 'users'
user_blueprint = Blueprint(base_model, __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
            else:  # error if bad email or password
                return render_template(base_model + '/' + 'login.html')
        except user_errors.UserError as e:
            return e.message

    else:  # it's a GET not a POST
        return render_template(base_model + '/' + 'login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except user_errors.UserError as e:
            return e.message
    #  it's a GET not a POST, OR pass through to here after unsuccessful post
    return render_template(base_model + '/' + 'register.html')


@user_blueprint.route('/alerts')
@decorators.requires_login  # redirect the user to users.login if session[email] is None
def user_alerts():
    user = User.get_from_db_by_email(session['email'])
    alerts = None
    if user is not None:
        user = User.db_to_rec(user)
        alerts = user.get_alerts()

    return render_template(base_model + '/' + 'alerts.html', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    #  home is defined in app.py
    return redirect(url_for("home"))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
