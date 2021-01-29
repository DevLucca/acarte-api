from pony import orm
from data import db

class Users(db.Entity):
    uuid = orm.Required(str,max_len=36,unique=True)
    name = orm.Required(str,max_len=50)
    surname = orm.Optional(str,max_len=75)
    username = orm.Required(str,max_len=75)
    active = orm.Required(bool)
    created_at = orm.Required(str)
    updated_at = orm.Optional(str)
    deleted_at = orm.Optional(str)