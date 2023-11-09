from flask import jsonify, request

from application.app_name.api.v1 import api_v1
from application.app_name.utils.rbac_login import login_required
from application.app_name.schemas import validate_request
from application.app_name.schemas.settings import SettingsSchema
from application.app_name.helpers import get_single_record, save_single_record
from application.app_name.models.settings import SettingsModel

import logging
log = logging.getLogger("app_name." + __name__)


@api_v1.route("/settings", methods=['GET'])
@login_required(roles=['admin'])
def get_settings():
    return jsonify(get_single_record(SettingsModel))


@api_v1.route("/settings", methods=['POST'])
@login_required(roles=['admin'])
@validate_request(SettingsSchema)
def post_settings():
    return jsonify(save_single_record(SettingsModel, request.json)), 201
