from pony import orm
from data import db

class Instruments(db.Entity):
    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    instument_id = orm.Required(str,max_len=50,unique=True)
    name = orm.Required(str,max_len=50)
    type = orm.Required(str,max_len=50)
    notes = orm.Optional(str,max_len=1000)
    repair = orm.Required(bool)
    active = orm.Required(bool)
    created_at = orm.Required(str)
    updated_at = orm.Optional(str)
    deleted_at = orm.Optional(str)