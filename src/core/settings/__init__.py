import sys
from pathlib import Path
from . import settings

cfg = settings.Settings(
    "app_name",
    "app_port",
    "app_allowed_hosts",
    "app_debug",
    "db_location",
    "db_port",
    "db_name",
    "db_user",
    "db_password"
).get_envs()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
