from infra import cfg
from pony import orm

db = orm.Database()
db.bind(
    provider='mysql',
    host=cfg["db_location"]["value"],
    user=cfg["db_user"]["value"],
    passwd=cfg["db_password"]["value"],
    db=cfg["db_name"]["value"]
    )
class DBClient:

    @classmethod
    def initialize(cls):
        from data import (instruments, loans, students, users)
        db.generate_mapping(create_tables=True)

DBClient.initialize()