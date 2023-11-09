from flask import jsonify

from application.app_name.api.utils import utils_api
from application.app_name.configs import NAME, VERSION, STARTED_AT, HOSTNAME

import logging
log = logging.getLogger("app_name." + __name__)


@utils_api.route("/status", methods=['GET'])
def show_status():
    return jsonify({
        "hostname": HOSTNAME,
        "app-name": NAME,
        "version": VERSION,
        "started_at": STARTED_AT,
    })
