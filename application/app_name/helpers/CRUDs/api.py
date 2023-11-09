from sqlalchemy import or_
from flask import abort
from os import environ
from werkzeug.exceptions import NotFound

from application.app_name.crypt import encrypt
from application.app_name.models import db
from application.app_name.utils.handle_many_to_many_relationship import many_to_many_save_handler, \
    many_to_many_update_handler

import logging

log = logging.getLogger("app_name." + __name__)


def get_single_record(model):
    """

    Function responsible for retrieving a single record in the database,
    for example, a global configuration for the app.

    In case no data found, will return a 404 informing that no data was found.

    In case of any Exception raised when retrieving this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to recover the record;
    :return: Json Serialized model;
    """
    try:
        item = model.query.first_or_404()
        item.read()
        log.info(f"Single Model Found. ID: {item.id}")
        log.debug(f"Single Model Data: {item.serialized}")
        return {'data': item.serialized}
    except NotFound:
        return abort(404, "No record found")
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on reading single model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when reading your data, try again")


def save_single_record(model, data: dict):
    """

    Function responsible for saving or updating a single record in the database,
        for example, a global configuration for the app.

    In case no data found, will automatically create a new record and insert desired data.

    In case of any Exception raised when saving this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to recover the record;
    :param data: Data received from client that will be saved or updated;
    :return: Json Serialized model with status of success;
    """
    try:
        record = model.query.first()
        if not record:
            record = model()

        for k, v in data.items():
            record.__setattr__(k, v)

        data_to_return = record.serialized
        record.commit()
        log.info(f"Single Model saved. ID: {record.id}")
        log.debug(f"Single Model Data: {data_to_return}")
        data_to_return['id'] = record.id
        return {
            'status': ['success', 1, True],
            'data': data_to_return
        }

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on saving single model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when saving your data, try again")


def get_all_records(model, args=None, raw=False):
    """

    Function responsible for retrieving data from model, based on pagination.

    In case of any Exception raised when retrieving this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to recover the record;
    :param args: URL get params received from client to inform how many records will be displayed;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model with other additional data informing the client about the data returned;
    """
    try:
        if args is None:
            args = {}

        offset = int(args.get('offset', 0))
        limit = int(args.get('limit', 10))
        frm = args.get('from')
        to = args.get('to')

        query = model.query

        if to and not frm:
            query = query.filter(model.created <= to)
        elif frm and not to:
            query = query.filter(model.created >= frm)
        elif to and frm:
            query = query.filter(model.created.between(frm, to))

        items = query.offset(offset).limit(limit).all()

        resp = {"count": len(items), "offset": offset, "limit": limit, "data": {}}

        log.debug(f"Records found: {len(items)}")

        if raw:
            resp["data"] = [item.read() for item in items]
        else:
            resp["data"] = [item.read().serialized for item in items]

        return resp
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error while retrieving all model data. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred while retrieving your data, try again")


def save_record(model, data: dict, additional_model=None):
    """

    Function responsible for saving a record in the database.

    In case of any Exception raised when saving this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to save the record;
    :param data: Data received from client that will be saved;
    :param additional_model: Model used in case of N to N relationship;
    :return: Json Serialized model with status of success;
    """
    try:
        record = model()

        for k, v in data.items():
            if k == "roles" or k == "users" and type(v) is list and additional_model:
                record.__setattr__(k, many_to_many_save_handler(v, additional_model))
            else:
                record.__setattr__(k, v)

        data_to_return = record.serialized
        record.commit()
        log.info(f"Model saved. ID: {record.id}")
        log.debug(f"Model Data: {data_to_return}")
        data_to_return['id'] = record.id
        return {
            'status': ['success', 1, True],
            'data': data_to_return
        }

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on saving model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when saving your data, try again")


def filter_records(model, search, raw=False):
    """

    Function responsible for retrieving a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return a 404 informing that no data was found.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to filter the record;
    :param search: Identifier that will be used to search on database, can be id, email, username or name;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model;
    """
    try:

        query = model.query

        enc_identifier = encrypt(search)

        query = query.filter(or_(
            model.id == search,
            model.email == enc_identifier if hasattr(model, "email") else None,
            model.name == enc_identifier if hasattr(model, "name") else None,
            model.username == enc_identifier if hasattr(model, "username") else None
        ))

        item = query.first_or_404()
        log.info(f"Model found ID: {item.id}")
        item.read()
        log.debug(f"Model Data: {item.serialized}")

        if raw:
            return item
        return {"data": item.serialized}

    except NotFound:
        return abort(404, "No record found")
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on filtering model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when filtering your data, try again")


def update_record(model, identifier, data: dict, additional_model=None):
    """

    Function responsible for updating a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return a 404 informing that no data was found.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to filter the record;
    :param identifier: Identifier that will be used to search on database, can be id, email, username or name;
    :param data: Data received from client that will be saved;
    :param additional_model: Model used in case of N to N relationship;
    :return: Json Serialized model with status of success;
    """
    try:
        query = model.query

        enc_identifier = encrypt(identifier)

        query = query.filter(or_(
            model.id == identifier,
            model.email == enc_identifier if hasattr(model, "email") else None,
            model.name == enc_identifier if hasattr(model, "name") else None,
            model.username == enc_identifier if hasattr(model, "username") else None
        ))

        record = query.first_or_404()
        record.read()
        for k, v in data.items():
            if k == "roles" or k == "users" and type(v) is list and additional_model:
                record.__setattr__(k, many_to_many_update_handler(record, v, additional_model))
            else:
                record.__setattr__(k, v)

        data_to_return = record.serialized
        record.commit()
        log.info(f"Model Updated. ID: {record.id}")
        log.debug(f"Model Data: {data_to_return}")
        return {
            'status': ['success', 1, True],
            'data': data_to_return
        }
    except NotFound:
        return abort(404, "No record found")
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on updating model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when saving your data, try again")


def delete_record(model, identifier):
    """

    Function responsible for deleting a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return a 404 informing that no data was found.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and respond to client without a 500 server error code.

    :param model: Model that will be used to filter the record;
    :param identifier: Identifier that will be used to search on database, can be id, email, username or name;
    :return: Json Serialized model with status of success;
    """
    try:

        query = model.query

        enc_identifier = encrypt(identifier)

        query = query.filter(or_(
            model.id == identifier,
            model.email == enc_identifier if hasattr(model, "email") else None,
            model.name == enc_identifier if hasattr(model, "name") else None,
            model.username == enc_identifier if hasattr(model, "username") else None
        ))

        record = query.first_or_404()

        record.read()
        data_to_return = record.serialized
        record.delete()
        log.info(f"Model deleted. ID: {data_to_return['id']}")
        return {
            'status': ['success', 1, True],
            'data': data_to_return
        }

    except NotFound:
        return abort(404, "No record found")
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"Error on deleting model. Error: {e}")
        db.session.rollback()
        return abort(409, "An Error occurred when deleting your data, try again")
