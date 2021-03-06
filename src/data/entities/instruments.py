import datetime
from pony import orm
from .. import db_client

class Instruments(db_client.Entity):
    _table_ = "instruments"
    
    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    number = orm.Required(str,max_len=50)
    name = orm.Required(str,max_len=50)
    itype = orm.Required(str,max_len=50)
    notes = orm.Optional(str,max_len=1000,sql_default="''", nullable=True)
    repair = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)

    orm.composite_key(name, number, itype)
