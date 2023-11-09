from sqlalchemy import or_

from application.app_name.crypt import encrypt

import logging

log = logging.getLogger("app_name." + __name__)


def many_to_many_save_handler(v, additional_model):
    dummy_list = []
    try:
        for item in v:
            enc_identifier = encrypt(item)
            dummy_value = additional_model.query.filter(or_(
                additional_model.id == item,
                additional_model.name == enc_identifier if hasattr(additional_model, "name") else None,
                additional_model.email == enc_identifier if hasattr(additional_model, "email") else None,
                additional_model.username == enc_identifier if hasattr(additional_model, "username") else None
            )).first()
            dummy_list.append(dummy_value) if dummy_value else ''

        return dummy_list
    except Exception as e:
        log.error(f"Error while getting data for many to many relationship. Error: {e}")
        return dummy_list


def many_to_many_update_handler(record, v, additional_model):
    dummy_list = []
    try:
        for item in v:
            enc_identifier = encrypt(item)
            dummy_value = additional_model.query.filter(or_(
                additional_model.id == item,
                additional_model.email == enc_identifier if hasattr(additional_model, "email") else None,
                additional_model.name == enc_identifier if hasattr(additional_model, "name") else None,
                additional_model.username == enc_identifier if hasattr(additional_model, "username") else None
            )).first()
            if dummy_value:
                if hasattr(record, 'roles') and dummy_value in record.roles:
                    dummy_list.remove(dummy_value)
                elif hasattr(record, 'users') and dummy_value in record.users:
                    dummy_list.remove(dummy_value)
                else:
                    dummy_list.append(dummy_value)

        return dummy_list
    except Exception as e:
        log.error(f"Error while getting data for many to many relationship. Error: {e}")
        return dummy_list
