from . import (
    config,
    logger
)

cfg = config.Config(
    "app-name",
    "app-port",
    "app-debug",
    "db-location",
    "db-name",
    "db-user",
    "db-password",
    "client-id",
    "client-secret"
).get_keys()