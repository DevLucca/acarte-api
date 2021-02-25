from pony import orm
from core import cfg

class Client:

    db = orm.Database()
    binded = False
    mapped = False

    def start(self):
        if not self.binded:
            self.db.bind(
                    provider='mysql',
                    host=cfg["db-location"]["value"],
                    port=cfg["db-port"]["value"],
                    user=cfg["db-user"]["value"],
                    passwd=cfg["db-password"]["value"],
                    db=cfg["db-name"]["value"]
            )
            self.binded = True
        return self

    def generate_mapping(self):
        if not self.mapped:
            from data.entities import (instruments, loans, students)
        
            self.db.generate_mapping(check_tables=True, create_tables=True)
            self.mapped = True

client = Client()
Entity = client.db.Entity

# orm.sql_debug(True)
# orm.set_sql_debug(True)
