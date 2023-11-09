
from application.app_name.helpers.forms.roles import RoleForm
from application.app_name.helpers.forms.login import LoginForm
from application.app_name.helpers.forms.users import UsersForm
from application.app_name.helpers.forms.settings import SettingsForm
from application.app_name.helpers.forms.profile import ProfileForm
from application.app_name.helpers.forms.profile_password import ProfilePasswordForm


class FormDecider:
    """
    This class should be used to determinate by validation which form to use
     when multiple forms if been used on the same page class.

     Example:
         On ProfilePage, we need to use 3 forms, so this decider will set the default form based on data informed
    """

    def __init__(self, forms):
        self.forms = forms

    def __call__(self, *args, **kwargs):
        return self

    def validate_form(self):
        for form in self.forms:
            form = form()
            if form.validate_form():
                return form.validate_form()

        return False

    @property
    def dump_errors(self):
        return ""
