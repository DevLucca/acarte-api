from . import (config)

cfg = config.Config(
    "db_location",
    "db_name",
    "db_user",
    "db_password",
    "client_id",
    "client_secret"
).get_keys()