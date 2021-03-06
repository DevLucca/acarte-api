from pony import orm
from src.core.settings import cfg

db_client = orm.Database()

db_client.bind(
    provider='mysql',
    host=cfg["db-location"]["value"],
    port=cfg["db-port"]["value"],
    user=cfg["db-user"]["value"],
    passwd=cfg["db-password"]["value"],
    db=cfg["db-name"]["value"]
)
