from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flasgger import Flasgger
from os import environ

from application.app_name.handlers import register_error_handler, register_after_request_log
from application.app_name.configs import configure_logging, get_config_by_environment, NAME, VERSION, STARTED_AT
from application.app_name.utils.register_blueprints import register_bp
from application.app_name.api import api_v1, utils_api
from application.app_name.frontend import frontend_admin
from application.app_name.models import db

import logging
log = logging.getLogger("app_name." + __name__)


def create_app():

    app = Flask(__name__)

    configure_logging(environ)
    log.info("Logs configuration is done")

    log.info("Configuring app environment")
    app.config.from_object(get_config_by_environment(environ)())

    log.info("Registering handlers")
    register_after_request_log(app)
    register_error_handler(app)
    log.info("Handlers registered successfully")

    log.info("Starting Blueprints registering")
    register_bp(app, api_v1)
    register_bp(app, utils_api)
    register_bp(app, frontend_admin)
    log.info("Finished Blueprints registering")

    log.info("Initiating Database model")
    db.init_app(app)

    Migrate(app, db, compare_type=True)

    log.info("Initiating API Docs yaml file")
    Flasgger(app, template_file='../apidocs.yaml')

    log.info("Initializing Form builder")
    Bootstrap5(app)

    log.info(f"{NAME}:{VERSION} Server Started Successfully at {STARTED_AT}")
    return app
