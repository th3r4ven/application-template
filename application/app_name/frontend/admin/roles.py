from application.app_name.utils.register_blueprints import custom_blueprint
from application.app_name.helpers import page, FullPage, RoleForm
from application.app_name.models.role import RolesModel
from application.app_name.models.user import UsersModel


import logging

log = logging.getLogger("app_name." + __name__)
admin_roles = custom_blueprint(__name__, "admin_roles")


@page(admin_roles, "/roles", log=log)
class RolesPage(FullPage):
    auth = True
    roles = ['admin', 'manager']
    model = RolesModel
    additional_model = UsersModel
    title = "Roles"
    page_title = "Roles"
    form = RoleForm
    back_url = "admin_roles.index"
    custom_fields = ["copy_id"]
    fields = [
        ["name", "Name"],
        ["users_name", "Users"]
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

