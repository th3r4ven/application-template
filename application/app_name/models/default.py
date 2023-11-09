from application.app_name.models import db
from application.app_name.crypt import encrypt, decrypt

from datetime import datetime
from uuid import uuid4

import logging
log = logging.getLogger("app_name." + __name__)


def generate_uuid():
    return str(uuid4())


class DefaultModel(object):

    blacklist = ['id', '_sa_instance_state', 'hashed_password', 'created', 'updated', 'user_id', 'role_id']

    hide_list = ['_sa_instance_state', 'hashed_password']

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, index=True)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def commit(self):
        # db.session.close_all()
        for k, v in self.__dict__.items():
            if k not in self.blacklist:
                self.__setattr__(k, encrypt(v))
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self):
        for k, v in self.__dict__.items():
            if k not in self.blacklist:
                self.__setattr__(k, decrypt(v))
        return self

    @property
    def serialized(self):
        data = {}
        for k, v in self.__dict__.items():
            if k not in self.hide_list:
                if type(v) is datetime:
                    data[k] = v.strftime("%d/%m/%Y %H:%M:%S%z")
                else:
                    data[k] = v
        return data

    @property
    def ft_serialized(self):
        return self.serialized
