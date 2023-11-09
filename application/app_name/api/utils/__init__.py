import importlib
import os

from flask import Blueprint

utils_api = Blueprint("api", __name__, url_prefix="/api")


__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if not file.startswith('_'):
        mod_name = file[:-3]   # strip .py at the end
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
