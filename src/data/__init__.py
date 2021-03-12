from pony import orm
from core.settings import cfg

db_client = orm.Database()

db_client.bind(
    provider='mysql',
    host=cfg.db_location.value,
    port=cfg.db_port.value,
    user=cfg.db_user.value,
    passwd=cfg.db_password.value,
    db=cfg.db_name.value
)
