import logging
import logging.handlers
from os import makedirs, path
from time import strftime
from flask import has_request_context, request


log = logging.getLogger("app_name." + __name__)

levels = {"notset": 0, "debug": 10, "info": 20, "warn": 30, "error": 40, "critical": 50}

app_handler, scheduler_handler = logging.Handler, logging.Handler


class AuditCustomFormatter(logging.Formatter):
    def __init__(self, default):
        self._default_formatter = default
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        if has_request_context() and hasattr(request, "audit_id"):
            record.msg = f"{request.audit_id} - {record.msg}"
        return self._default_formatter.format(record)


def configure_handlers(environ):
    global app_handler, scheduler_handler

    environment = environ.get('ENVIRONMENT', 'development').lower()

    default_formatter = logging.Formatter(f'{strftime("[%d/%b/%Y %H:%M:%S]")} %(levelname)s - %(name)s - %(message)s')

    if environment == 'production':
        if not path.exists('logs'):
            makedirs('logs')
        scheduler_handler = logging.handlers.TimedRotatingFileHandler('logs/scheduler.log', when='d', interval=1,
                                                                      backupCount=30)
        scheduler_handler.setFormatter(default_formatter)

        app_handler = logging.handlers.TimedRotatingFileHandler('logs/app.log', when='d', interval=1, backupCount=30)
        app_handler.setFormatter(AuditCustomFormatter(default_formatter))
    else:
        app_handler = logging.StreamHandler()
        app_handler.setFormatter(AuditCustomFormatter(default_formatter))

        scheduler_handler = logging.StreamHandler()
        scheduler_handler.setFormatter(default_formatter)


def add_handler(logger_name, handler, propagate=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.ERROR)
    logger.propagate = propagate
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(20)


def get_level(environ):
    level_name = environ.get('LOG_LEVEL', 'info').lower()
    if not level_name or level_name not in levels.keys():
        level_name = 'info'
    level = levels.get(level_name)
    return level


def disable_handlers(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.handlers = []
    logger.propagate = False


def configure_logger_for_environ(name):
    global app_handler, scheduler_handler
    add_handler('apscheduler.scheduler', scheduler_handler, propagate=False)
    add_handler('apscheduler.executors.default', scheduler_handler, propagate=False)
    add_handler('scheduler.', scheduler_handler, propagate=False)
    disable_handlers('werkzeug')
    disable_handlers('waitress')
    logger = logging.getLogger(name)
    logger.handler = []
    logger.propagate = False
    logger.addHandler(app_handler)


def configure_log_level(level):
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger_name = logger.name
        if logger_name.startswith('app_name'):
            logger.setLevel(level)


def configure_logging(environ):
    configure_handlers(environ)
    level = get_level(environ)
    logging.root.setLevel(level) or 20
    configure_logger_for_environ('app_name')
    configure_log_level(level)
