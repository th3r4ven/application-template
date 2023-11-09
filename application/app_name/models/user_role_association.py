from application.app_name.models import db
from application.app_name.models.default import generate_uuid

from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, DateTime, Integer, String

import logging
log = logging.getLogger("app_name." + __name__)


UserRoleAssociation = Table(
    "user_role_association",
    db.Model.metadata,
    Column("id", String(length=36), primary_key=True, default=generate_uuid, index=True),
    Column("created", DateTime, default=datetime.now),
    Column("updated", DateTime, default=datetime.now, onupdate=datetime.now),
    Column("role_id", String(length=36), ForeignKey("roles.id"), nullable=True),
    Column("user_id", String(length=36), ForeignKey("users.id"), nullable=True),
    db.PrimaryKeyConstraint('role_id', 'user_id')
)
