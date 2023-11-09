from application.app_name.models import db
from application.app_name.models.default import DefaultModel
from application.app_name.models.user_role_association import UserRoleAssociation


import logging

log = logging.getLogger("app_name." + __name__)


class RolesModel(db.Model, DefaultModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(3072), unique=True)
    users = db.relationship('UsersModel', secondary=UserRoleAssociation, back_populates="roles")

    @property
    def serialized(self):
        data = super().serialized
        data['users'] = [x.read().username for x in self.users]
        return data

    @property
    def ft_serialized(self):
        data = self.serialized
        users = self.users
        data['users'] = [x.id for x in users]
        data['users_name'] = [x.read().username for x in users]
        return data

