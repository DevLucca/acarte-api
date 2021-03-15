import datetime
from pony import orm
from uuid import UUID
from data import db_client
from data.entities.users import UsersEntity

class StudentsEntity(db_client.Entity):
    _table_ = 'students'
    
    loan = orm.Set("LoansEntity")
    instruments = orm.Set("InstrumentsEntity")
    uuid = orm.Required(UUID,unique=True)
    name = orm.Required(str,max_len=50)
    surname = orm.Required(str,max_len=50)
    ra = orm.Required(str,unique=True)
    blocked = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)
    updated_by = orm.Required(UsersEntity)

    orm.composite_key(name, surname, ra)
