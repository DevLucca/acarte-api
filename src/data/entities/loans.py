import datetime
from pony import orm
from .. import db_client
from .instruments import Instruments as InstrumentsEntity
from .students import Students as StudentsEntity

class Loans(db_client.Entity):
    instruments = orm.Set(InstrumentsEntity)
    student = orm.Required(StudentsEntity)
    uuid = orm.Required(str,max_len=36,unique=True)
    lented_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    returned_at = orm.Optional(datetime.datetime)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)
