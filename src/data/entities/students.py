import datetime
from pony import orm
from .. import db_client

class Students(db_client.Entity):
    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    name = orm.Required(str,max_len=50)
    surname = orm.Required(str,max_len=50)
    ra = orm.Required(str,unique=True)
    blocked = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)

    orm.composite_key(name, surname, ra)
