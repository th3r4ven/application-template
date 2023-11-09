from flask import render_template

from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, Page

import logging

log = logging.getLogger("app_name." + __name__)

admin_dashboard = custom_blueprint(__name__, "admin_dashboard")


@page(admin_dashboard, "/dashboard", log=log)
class DashboardPage(Page):
    auth = True
    roles = ['admin', 'manager']
    template = 'admin/dashboard.html'

    def index(self):
        return render_template(self.template)
