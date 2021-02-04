from core import cfg
from pony import orm

db = orm.Database()
db.bind(
    provider='sqlite',
    filename=':memory:'
    # host=cfg["db-location"]["value"],
    # user=cfg["db-user"]["value"],
    # passwd=cfg["db-password"]["value"],
    # db=cfg["db-name"]["value"]
    )
class DBClient:

    @classmethod
    def initialize(cls):
        from . import (instruments, loans, students, users)
        db.generate_mapping(create_tables=True)
