from application.app_name.models import db
from application.app_name.models.default import DefaultModel
from application.app_name.models.user_role_association import UserRoleAssociation

from werkzeug.security import generate_password_hash, check_password_hash

import logging
log = logging.getLogger("app_name." + __name__)


class UsersModel(db.Model, DefaultModel):

    __tablename__ = 'users'

    username = db.Column(db.String(3072), unique=True, index=True)
    hashed_password = db.Column(db.String(128))
    phone = db.Column(db.String(3072), unique=True)
    email = db.Column(db.String(3072), unique=True, index=True)
    roles = db.relationship('RolesModel', secondary=UserRoleAssociation, back_populates="users")

    @property
    def serialized(self):
        data = super().serialized
        data['roles'] = [x.read().name for x in self.roles]
        return data

    @property
    def password(self):
        return "******"

    @password.setter
    def password(self, pswd):
        self.hashed_password = generate_password_hash(pswd)

    def validate_password(self, password):
        try:
            return check_password_hash(self.hashed_password, password)
        except Exception as e:
            log.error(f"Error validating user {self.username} password: {e}")
            return False

    @property
    def ft_serialized(self):
        data = self.serialized
        roles = self.roles
        data['roles'] = [x.id for x in roles]
        data['roles_name'] = [x.read().name for x in roles]
        return data
