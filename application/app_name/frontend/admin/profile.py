from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, ProfilePage, ProfileForm, ProfilePasswordForm, FormDecider
from application.app_name.models.user import UsersModel


import logging

log = logging.getLogger("app_name." + __name__)
admin_profile = custom_blueprint(__name__, "admin_profile")


@page(admin_profile, "/profile", log=log)
class ProfilePage(ProfilePage):
    auth = True
    roles = ['manager']
    model = UsersModel
    title = "Profile"
    page_title = "Profile"
    form = FormDecider([ProfileForm, ProfilePasswordForm])
    profile_form = ProfileForm
    password_form = ProfilePasswordForm
    back_url = "admin_profile.index"

