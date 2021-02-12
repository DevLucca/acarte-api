from pony import orm
from src import db
from models.instruments import Instruments
from models.students import Students

class Loans(db.Entity):
    intrument_id = orm.Set(Instruments)
    student_id = orm.Set(Students)
    lented_at = orm.Required(str)
    returned_at = orm.Optional(str)
