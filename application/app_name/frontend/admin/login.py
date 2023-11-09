from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, FormPage, LoginForm, ft_filter_record
from application.app_name.utils import check_for_logged_to_redirect, create_login_session
from application.app_name.models.user import UsersModel

from flask import render_template, flash, redirect, url_for
from os import getenv

import logging

log = logging.getLogger("app_name." + __name__)

admin_login = custom_blueprint(__name__, 'admin_login')


@page(admin_login, '/login', log)
class AdminLoginPage(FormPage):
    auth = False
    form = LoginForm
    template = 'login/auth.html'
    title = "Admin Login"
    back_url = "admin_login.index"

    def index(self):
        if check_for_logged_to_redirect(['admin', 'manager']):
            return redirect(url_for('admin_dashboard.index'))
        form = self.form()
        return render_template(
            self.template,
            title=self.title,
            form=form,
            idps=[],
            action=url_for("admin_login.submit")
        )

    def submit(self, data):
        email = data['email']
        passwd = data['password']

        if data['email'] == getenv('ADMIN_USERNAME') and passwd == getenv('ADMIN_PASSWORD'):
            data['roles'] = ['admin']
            data['name'] = 'admin'
            create_login_session(data)
            flash('Logged in with success!', 'success')
            return redirect(url_for('admin_dashboard.index'))

        user = ft_filter_record(UsersModel, email, raw=True)
        if user:
            if not user.validate_password(passwd):
                flash("Invalid Credentials", 'danger')
                return self.index()
            create_login_session(user.serialized)
            flash('Logged in with success!', 'success')
            return redirect(url_for('admin_dashboard.index'))

        flash("Invalid Credentials", 'danger')
        return redirect(url_for('admin_login.index'))
