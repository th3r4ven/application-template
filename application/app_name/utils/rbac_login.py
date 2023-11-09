from flask import abort, request, session, flash, redirect, url_for
from functools import wraps
from os import getenv


def login_required(roles=[]):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):

            auth = request.authorization
            if auth and "admin" in roles and auth.username == getenv("ADMIN_USERNAME") and auth.password == getenv(
                        "ADMIN_PASSWORD"):
                return func(*args, **kwargs)
            return abort(401)

        return wrap

    return wrapper


def frontend_login_required(func, roles=[]):
    @wraps(func)
    def wrap(*args, **kwargs):

        for role in roles:
            if session.get('logged_in', False) and role in session.get('role'):
                return func(*args, **kwargs)

        flash("You dont have permission to access this page", "info")
        return redirect(url_for("admin_login.index"))

    return wrap


def logout_user():
    session.clear()


def create_login_session(data: dict):
    session.clear()
    session['id'] = data.get('id', None)
    session['role'] = data['roles']
    session['name'] = data.get('name', data.get('username'))
    session['email'] = data['email']
    session['logged_in'] = True


def check_for_logged_to_redirect(role):
    if session.get('logged_in', False):
        if type(role) is list:
            for r in role:
                if r in session.get('role', []):
                    return True
        else:
            return role in session.get('roles', [])

    return False
