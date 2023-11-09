from flask import redirect, url_for, flash

from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.utils import logout_user
from application.app_name.helpers import page, Page

import logging

log = logging.getLogger("app_name." + __name__)

admin_logout = custom_blueprint(__name__, "admin_logout")


@page(admin_logout, "/logout", log=log)
class LogoutPage(Page):
    auth = False

    def index(self):
        logout_user()
        flash("Successfully logged out!", 'success')
        return redirect(url_for('admin_login.index'))
