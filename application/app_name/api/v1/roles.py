from flask import jsonify, request

from application.app_name.api.v1 import api_v1
from application.app_name.utils.rbac_login import login_required
from application.app_name.schemas import validate_request
from application.app_name.schemas.roles import RolesSchema, UpdateRolesSchema
from application.app_name.helpers import get_all_records, save_record, update_record, filter_records, delete_record
from application.app_name.models.user import UsersModel
from application.app_name.models.role import RolesModel

import logging
log = logging.getLogger("app_name." + __name__)


@api_v1.route("/roles", methods=['GET'])
@login_required(roles=['admin'])
def get_roles():
    return jsonify(get_all_records(RolesModel, request.args))


@api_v1.route("/roles", methods=['POST'])
@login_required(roles=['admin'])
@validate_request(RolesSchema)
def post_roles():
    return jsonify(save_record(RolesModel, request.json, additional_model=UsersModel)), 201


@api_v1.route("/roles/<identifier>", methods=['GET'])
@login_required(roles=['admin'])
def filter_role_by_id(identifier):
    return jsonify(filter_records(RolesModel, identifier))


@api_v1.route("/roles/<identifier>", methods=['PUT'])
@login_required(roles=['admin'])
@validate_request(UpdateRolesSchema)
def put_role_by_id(identifier):
    return jsonify(update_record(RolesModel, identifier, request.json, additional_model=UsersModel))


@api_v1.route("/roles/<identifier>", methods=['DELETE'])
@login_required(roles=['admin'])
def delete_role_by_id(identifier):
    return jsonify(delete_record(RolesModel, identifier))
