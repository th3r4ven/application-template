import random
import string
import logging
from time import strftime
from flask import request, has_request_context, Flask

log = logging.getLogger("app_name.")


def set_audit_id():
    if has_request_context():
        setattr(request, "audit_id", ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))


def access_log(response):
    if not request.path.startswith("/static") and request.path != "/favicon.ico":
        log.info('%s - %s %s %s', request.remote_addr, request.method, request.path, response.status_code)
    return response


def register_after_request_log(app: Flask):
    app.before_request(set_audit_id)
    app.after_request(access_log)
