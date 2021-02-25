from data.entities.instruments import Instruments as InstrumentsEntity
from data.entities.students import Students as StudentsEntity
from data.repositories import (
    BaseRepository, 
    orm, 
    orm_decorator
)

class InstrumentsRepository(BaseRepository):
    Entity = InstrumentsEntity
    StudentsEntity = StudentsEntity

    @classmethod
    @orm_decorator
    def get(cls, name, instrument_id, repair, active):
        objs = orm.select(i for i in cls.Entity 
        if i.name.startswith(name) 
        and i.instrument_id.startswith(instrument_id) 
        and i.repair == repair
        and i.active == active
        and i.deleted_at is None)
        return objs
    
    @classmethod
    @orm_decorator
    def get_student_loan(cls, uuid):
        obj = orm.get(
            s for s in cls.StudentsEntity for l in s.loan for i in l.instrument_id
            if i.uuid == uuid
            and i.active
            and i.deleted_at is None
            )
        return obj
