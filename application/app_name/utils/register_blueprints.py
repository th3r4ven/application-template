from flask import Flask, Blueprint
import logging

log = logging.getLogger("app_name." + __name__)


def register_bp(app: Flask, blueprint):
    if type(blueprint) is list:
        for b in blueprint:
            app.register_blueprint(b)
            log.info(f"Registered Blueprint: {b.name}")
    else:
        app.register_blueprint(blueprint)
        log.info(f"Registered Blueprint: {blueprint.name}")


def custom_blueprint(module, name=None):
    if not name:
        name = module.split(".")[-1]
    return Blueprint(name, module)
