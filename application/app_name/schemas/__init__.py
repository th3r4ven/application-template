import os
import importlib

from functools import wraps
from flask import request, abort
from marshmallow import ValidationError


def validate_request(schema):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            ValidationData(schema, request.json)
            return func(*args, **kwargs)
        return wrap
    return wrapper


class ValidationData:

    def __init__(self, schema, json_data):
        try:
            schema().load(json_data)
            return
        except ValidationError as err:
            abort(400, err.messages)


__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if not file.startswith('_'):
        mod_name = file[:-3]   # strip .py at the end
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
