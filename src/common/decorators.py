from functools import wraps
from flask import Blueprint, request, session, url_for, render_template, redirect
import src.config


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print('yo homey')
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        else:
            return func(*args, **kwargs)  # allow arguments and keyword arguments

    return decorated_function


def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print('yo homey')
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        elif session['email'] not in src.config.ADMINS:
            return redirect(url_for('unauthorized'))
        else:
            return func(*args, **kwargs)  # allow arguments and keyword arguments

    return decorated_function
