from pony import orm
from data.database import Entity
from data.entities.instruments import Instruments as InstrumentsEntity
from data.entities.students import Students as StudentsEntity
import datetime

class Loans(Entity):
    instrument_id = orm.Set(InstrumentsEntity)
    student_id = orm.Set(StudentsEntity)
    uuid = orm.Required(str,max_len=36,unique=True)
    lented_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    returned_at = orm.Optional(datetime.datetime)
