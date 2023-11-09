from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, FullPage, UsersForm
from application.app_name.models.role import RolesModel
from application.app_name.models.user import UsersModel


import logging

log = logging.getLogger("app_name." + __name__)
admin_users = custom_blueprint(__name__, "admin_users")


@page(admin_users, "/users", log=log)
class UsersPage(FullPage):
    auth = True
    roles = ['admin', 'manager']
    model = UsersModel
    additional_model = RolesModel
    title = "Users"
    page_title = "Users"
    form = UsersForm
    back_url = "admin_users.index"
    custom_fields = ["copy_id"]
    fields = [
        ["username", "Name"],
        ["roles_name", "Roles"]
    ]

    def _get_all(self):
        try:
            query = self.model.query
            items = query.all()
            if not items:
                return []
            return [item.read().ft_serialized for item in items]

        except Exception as e:
            self.log.error(f"Error on getting roles. Error: {e}")
            return []

