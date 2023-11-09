from flask import jsonify, request

from application.app_name.api.v1 import api_v1
from application.app_name.utils.rbac_login import login_required
from application.app_name.schemas import validate_request
from application.app_name.schemas.users import UsersSchema, UpdateUsersSchema
from application.app_name.helpers import get_all_records, save_record, update_record, filter_records, delete_record
from application.app_name.models.user import UsersModel
from application.app_name.models.role import RolesModel

import logging
log = logging.getLogger("app_name." + __name__)


@api_v1.route("/users", methods=['GET'])
@login_required(roles=['admin'])
def get_users():
    return jsonify(get_all_records(UsersModel, request.args))


@api_v1.route("/users", methods=['POST'])
@login_required(roles=['admin'])
@validate_request(UsersSchema)
def post_users():
    return jsonify(save_record(UsersModel, request.json, additional_model=RolesModel)), 201


@api_v1.route("/users/<identifier>", methods=['GET'])
@login_required(roles=['admin'])
def filter_user_by_id(identifier):
    return jsonify(filter_records(UsersModel, identifier))


@api_v1.route("/users/<identifier>", methods=['PUT'])
@login_required(roles=['admin'])
@validate_request(UpdateUsersSchema)
def put_user_by_id(identifier):
    return jsonify(update_record(UsersModel, identifier, request.json, additional_model=RolesModel))


@api_v1.route("/users/<identifier>", methods=['DELETE'])
@login_required(roles=['admin'])
def delete_user_by_id(identifier):
    return jsonify(delete_record(UsersModel, identifier))
