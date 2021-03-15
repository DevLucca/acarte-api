import datetime
from pony import orm
from uuid import UUID
from data import db_client
from data.entities.users import UsersEntity
from data.entities.students import StudentsEntity

class InstrumentsEntity(db_client.Entity):
    _table_ = 'instruments'
    
    loan = orm.Set("LoansEntity")
    uuid = orm.Required(UUID,unique=True)
    number = orm.Required(str,max_len=50)
    name = orm.Required(str,max_len=50)
    itype = orm.Required(str,max_len=50)
    notes = orm.Optional(str,max_len=1000, nullable=True)
    repair = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)
    updated_by = orm.Required(UsersEntity)
    student = orm.Required(StudentsEntity)

    orm.composite_key(name, number, itype)
