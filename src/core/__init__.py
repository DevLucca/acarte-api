from . import (
    config
)

cfg = config.Config(
    "app-name",
    "app-port",
    "app-debug",
    "db-location",
    "db-port",
    "db-name",
    "db-user",
    "db-password"
).get_keys()
