from flask import request, session
from sqlalchemy import or_
from os import environ

from application.app_name.models import db
from application.app_name.crypt import encrypt
from application.app_name.utils.handle_many_to_many_relationship import many_to_many_save_handler, many_to_many_update_handler

import logging

log = logging.getLogger("DezOrganizada." + __name__)


def ft_get_single_record(model, raw=False):
    """

    Function responsible for retrieving a single record in the database,
    for example, a global configuration for the app.

    In case of any Exception raised when retrieving this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to recover the record;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model or model object;
    """
    try:
        item = model.query.first()
        if not item:
            return []
        item.read()
        log.info(f"FT Single Model Found. ID: {item.id}")
        log.debug(f"FT Single Model Data: {item.serialized}")
        if raw:
            return item
        return item.ft_serialized

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on reading single model. Error: {e}")
        db.session.rollback()
        return []


def ft_save_single_record(model, data: dict):
    """

    Function responsible for saving or updating a single record in the database,
        for example, a global configuration for the app.

    In case no data found, will automatically create a new record and insert desired data.

    In case of any Exception raised when saving this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to recover the record;
    :param data: Data received from client that will be saved or updated;
    :return: Json Serialized model;
    """
    try:
        record = model.query.first()
        if not record:
            record = model()

        for k, v in data.items():
            record.__setattr__(k, v)

        data_to_return = record.ft_serialized
        record.commit()
        log.info(f"FT Single Model saved. ID: {record.id}")
        log.debug(f"FT Single Model Data: {data_to_return}")
        return data_to_return

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on saving single model. Error: {e}")
        db.session.rollback()
        return []


def ft_get_all_records(model, raw=False):
    """

    Function responsible for retrieving data from model without pagination.

    In case of any Exception raised when retrieving this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to recover the record;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model or list of model object
    """
    try:
        query = model.query
        items = query.all()
        log.debug(f"Records found: {len(items)}")

        if raw:
            return [item.read() for item in items]
        return [item.read().ft_serialized for item in items]
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on reading all models. Error: {e}")
        db.session.rollback()
        return []


def ft_get_all_records_paginate(model, args=None, raw=False):
    """

    Function responsible for retrieving data from model with pagination.

    In case of any Exception raised when retrieving this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to recover the record;
    :param args: URL get params received from client to inform how many records will be displayed;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model or list of model object
    """
    try:
        if args is None:
            args = {}

        offset = int(args.get('offset', 0))
        limit = int(args.get('limit', 10))

        query = model.query
        session['total_count'] = query.count()
        items = query.offset(offset).limit(limit).all()

        log.debug(f"Records found: {len(items)}")
        if raw:
            return [item.read() for item in items]
        return [item.read().serialized for item in items]
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on reading all models by pagination. Error: {e}")
        db.session.rollback()
        return []


def ft_save_record(model, data: dict, additional_model=None):
    """

    Function responsible for saving a record in the database.

    In case of any Exception raised when saving this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to save the record;
    :param data: Data received from client that will be saved;
    :param additional_model: Model used in case of N to N relationship;
    :return: Json Serialized model
    """
    try:
        record = model()

        for k, v in data.items():
            if k == "roles" or k == "users" and type(v) is list and additional_model:
                record.__setattr__(k, many_to_many_save_handler(v, additional_model))
            else:
                record.__setattr__(k, v)

        data_to_return = record.ft_serialized
        record.commit()
        data_to_return['id'] = record.id
        log.info(f"FT Model saved. ID: {record.id}")
        log.debug(f"FT Model Data: {data_to_return}")
        return data_to_return

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on saving model. Error: {e}")
        db.session.rollback()
        return []


def ft_filter_record(model, search, raw=False):
    """

    Function responsible for retrieving a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return an empty list.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and return an empty list.

    :param model: Model that will be used to filter the record;
    :param search: Identifier that will be used to search on database, can be id, email, username or name;
    :param raw: Internal use, this param, if set to true, will make this function return the model object;
    :return: Json Serialized model;
    """
    try:
        query = model.query

        enc_search = encrypt(search)

        item = query.filter(or_(
            model.id == search,
            model.email == enc_search if hasattr(model, "email") else None,
            model.username == enc_search if hasattr(model, "username") else None,
            model.phone == enc_search if hasattr(model, "phone") else None
        )).first()

        if not item:
            return []

        log.info(f"FT Model found ID: {item.id}")
        item.read()
        log.debug(f"FT Model Data: {item.serialized}")
        if raw:
            return item
        return item.ft_serialized
    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on filtering model. Error: {e}")
        db.session.rollback()
        return []


def ft_update_record(model, identifier, data: dict, additional_model=None):
    """

    Function responsible for updating a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return a 404 informing that no data was found.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and return with an empty list.

    :param model: Model that will be used to filter the record;
    :param identifier: identifier: Identifier that will be used to search on database, can be id, email, username or name;
    :param data: Data received from client that will be saved;
    :param additional_model: Model used in case of N to N relationship;
    :return: Json Serialized Model
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

        record = query.first()

        if not record:
            return []

        for k, v in data.items():
            if k == "roles" or k == "users" and type(v) is list and additional_model is not None:
                record.__setattr__(k, many_to_many_update_handler(record, v, additional_model))
            else:
                record.__setattr__(k, v)

        record.read()
        data_to_return = record.ft_serialized
        record.commit()
        log.info(f"FT Model Updated. ID: {record.id}")
        log.debug(f"FT Model Data: {data_to_return}")
        return data_to_return

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on updating model. Error: {e}")
        db.session.rollback()
        return []


def ft_delete_record(model, identifier):
    """

    Function responsible for deleting a record in the database.

    This select query is dynamically built based on model attributes so can support multiple models and filters

    In case no data found, will return an empty list.

    In case of any Exception raised when searching this data or serializing it,
        will generate a log and return with an empty list.

    :param model: Model that will be used to filter the record;
    :param identifier: Identifier that will be used to search on database, can be id, email, username or name;
    :return: Json Serialized model;
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

        record = query.first()

        if not record:
            return []

        record.read()
        data_to_return = record.ft_serialized
        record.delete()
        log.info(f"FT Model deleted. ID: {data_to_return['id']}")

        return data_to_return

    except Exception as e:
        if hasattr(e, "hide_parameters") and environ.get("ENVIRONMENT", "").lower() == "production":
            e.hide_parameters = True
        log.error(f"FT Error on deleting model. Error: {e}")
        db.session.rollback()
        return []
