from data.entities.students import Students as StudentsEntity
from data.entities.instruments import Instruments as InstrumentsEntity
from data.repositories import (
    BaseRepository, 
    orm, 
    orm_decorator
)

class StudentsRepository(BaseRepository):
    Entity = StudentsEntity
    InstrumentsEntity = InstrumentsEntity

    @classmethod
    @orm_decorator
    def get(cls, name, surname, ra, blocked, active):
        objs = orm.select(s for s in cls.Entity 
        if s.name.startswith(name) 
        and s.surname.startswith(surname)
        and s.ra.startswith(ra)
        and s.blocked == blocked
        and s.active == active
        and s.deleted_at is None)
        return objs

    @classmethod
    @orm_decorator
    def get_lent_instruments(cls, uuid):
        objs = orm.select(
            i for i in cls.InstrumentsEntity for l in i.loan for s in l.student_id
            if s.uuid == uuid
            and i.active
            and i.deleted_at is None
            and s.deleted_at is None
            )
        return objs
