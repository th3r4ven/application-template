from application.app_name.models import db
from application.app_name.models.default import DefaultModel
from application.app_name.configs import levels, configure_log_level

import logging
log = logging.getLogger("app_name." + __name__)


class SettingsModel(db.Model, DefaultModel):

    __tablename__ = 'settings'

    logLevel = db.Column(db.String(3072), default="info")

    @property
    def log_level(self):
        return self.logLevel

    @log_level.setter
    def log_level(self, level_name):
        if level_name not in levels.keys():
            level_name = 'info'
        level = levels.get(level_name)
        configure_log_level(level)
        self.logLevel = level_name

    @property
    def serialized(self):
        data = super().serialized

        if data.get('logLevel', False):
            data.pop('logLevel')
        data['log_level'] = self.log_level

        return data
