from application.app_name.models import db
from datetime import timedelta
import logging

log = logging.getLogger("app_name." + __name__)

swagger_conf = {'title': 'API Docs - organization - app_name'}


def get_database_uri(environment):

    uri = f'mysql+pymysql://{environment["MYSQL_USER"]}:' \
          f'{environment["MYSQL_PASSWORD"]}' \
          f'@{environment["MYSQL_HOST"]}:{environment["MYSQL_PORT"]}/' \
          f'{environment["MYSQL_DATABASE"]}'

    return uri


def production_config(environment):
    return type('ProductionConfig', (object,), {
        "DEBUG": False,
        "TESTING": False,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": get_database_uri(environment),
        "SQLALCHEMY_BINDS": {'primary': get_database_uri(environment),
                             'background': get_database_uri(environment)
                             },
        "SECRET_KEY": environment['SECRET_KEY'],
        "SESSION_SQLALCHEMY": db,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def development_config(environment):
    return type('DevelopmentConfig', (object,), {
        "DEBUG": True,
        "TESTING": False,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///foo.db",
        # "SQLALCHEMY_DATABASE_URI": get_database_uri(environment),
        # "SQLALCHEMY_BINDS": {'primary': get_database_uri(environment),
        #                      'background': get_database_uri(environment)
        #                      },
        "SECRET_KEY": environment['SECRET_KEY'],
        "SESSION_SQLALCHEMY": db,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def testing_config(environment):
    return type('TestingConfig', (object,), {
        "DEBUG": False,
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_BINDS": {'primary': 'sqlite:///:memory:',
                             'background': 'sqlite:///:memory:'
                             },
        "SECRET_KEY": environment['SECRET_KEY'],
        "SESSION_SQLALCHEMY": db,
        "PERMANENT_SESSION_LIFETIME": timedelta(days=int(environment['PERMANENT_SESSION_LIFETIME'])),
        "SWAGGER": swagger_conf
    })


def get_config_by_environment(environment: dict):

    log.info("Checking app env vars")
    required_keys = ['FLASK_APP', 'ENVIRONMENT', 'SECRET_KEY', 'CRYPT_KEY', 'ADMIN_USERNAME', 'ADMIN_PASSWORD']
    prd_required_keys = ['MYSQL_HOST', 'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD']

    log.info("Checking required env vars")
    for key in required_keys:
        if key not in environment.keys():
            exit(f"Missing env var: {key}")
        if key == "CRYPT_KEY":
            if len(environment['CRYPT_KEY']) != 16:
                exit('Invalid CRYPT_KEY value, this key need to have 16 char length')

    if environment['ENVIRONMENT'] == 'production':
        log.info("Checking production required env vars")
        for key in prd_required_keys:
            if key not in environment.keys():
                exit(f"Missing env var: {key}")

    log.info("Checking optional env vars")
    environment['PERMANENT_SESSION_LIFETIME'] = str(environment.get("PERMANENT_SESSION_LIFETIME", 1460))
    environment['MYSQL_PORT'] = str(environment.get("MYSQL_PORT", 3306))

    configurations = {
        "development": development_config,
        "production": production_config,
        "testing": testing_config
    }

    env = environment.get('ENVIRONMENT')
    configuration = configurations.get(env)(environment)
    log.info(f"Environment Configuration set to: {env}")
    return configuration
