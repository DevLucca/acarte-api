import sys
from pathlib import Path
from . import settings

cfg = settings.Settings(
    "app-name",
    "app-port",
    "app-debug",
    "db-location",
    "db-port",
    "db-name",
    "db-user",
    "db-password"
).get_envs()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
