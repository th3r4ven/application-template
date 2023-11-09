from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, SinglePage, SettingsForm
from application.app_name.models.settings import SettingsModel


import logging

log = logging.getLogger("app_name." + __name__)
admin_settings = custom_blueprint(__name__, "admin_settings")


@page(admin_settings, "/settings", log=log)
class SettingsPage(SinglePage):
    auth = True
    roles = ['admin']
    model = SettingsModel
    title = "Settings"
    page_title = "Settings"
    form = SettingsForm
    back_url = "admin_settings.index"
    custom_fields = ["editonly"]
    fields = [
        ["log_level", "Log Level"]
    ]
