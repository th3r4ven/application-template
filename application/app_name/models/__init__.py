from flask_sqlalchemy import SQLAlchemy

import os
import importlib
import logging
log = logging.getLogger("app_name." + __name__)


db = SQLAlchemy(session_options={"autoflush": False})


__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if not file.startswith('_') and not file.startswith('default.py'):
        mod_name = file[:-3]   # strip .py at the end
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
