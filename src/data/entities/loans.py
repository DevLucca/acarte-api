import datetime
from pony import orm
from uuid import UUID
from data import db_client
from data.entities.users import UsersEntity
from data.entities.students import StudentsEntity
from data.entities.instruments import InstrumentsEntity

class LoansEntity(db_client.Entity):
    _table_ = 'loans'
    
    instruments = orm.Set(InstrumentsEntity)
    student = orm.Required(StudentsEntity)
    uuid = orm.Required(UUID,unique=True)
    lented_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    returned_at = orm.Optional(datetime.datetime)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)
    updated_by = orm.Required(UsersEntity)
