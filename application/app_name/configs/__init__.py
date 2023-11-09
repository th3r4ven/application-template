from application.app_name.configs.logs import configure_logging, configure_log_level, levels
from application.app_name.configs.environment import get_config_by_environment

from socket import gethostname
from datetime import datetime
import yaml


HOSTNAME = str(gethostname())
STARTED_AT = str(datetime.now())

try:
    filename = "info.yaml"
    with open(filename, "rt") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        NAME = data.get("app-name")
        VERSION = data.get("app-version")
except FileNotFoundError as e:
    NAME = "n/a"
    VERSION = "n/a"
