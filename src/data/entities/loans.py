from pony import orm
from data.database import Entity
from data.entities.instruments import Instruments as InstrumentsEntity
from data.entities.students import Students as StudentsEntity

class Loans(Entity):
    intrument_id = orm.Set(InstrumentsEntity)
    student_id = orm.Set(StudentsEntity)
    lented_at = orm.Required(str)
    returned_at = orm.Optional(str)
