from application.app_name.frontend.admin.login import admin_login
from application.app_name.frontend.admin.logout import admin_logout
from application.app_name.frontend.admin.dashboard import admin_dashboard
from application.app_name.frontend.admin.roles import admin_roles
from application.app_name.frontend.admin.users import admin_users
from application.app_name.frontend.admin.settings import admin_settings
from application.app_name.frontend.admin.profile import admin_profile

frontend_admin = [admin_login, admin_logout, admin_dashboard, admin_roles, admin_users, admin_settings, admin_profile]
