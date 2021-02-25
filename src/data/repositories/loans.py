from data.entities.loans import Loans as LoansEntity
from data.repositories import (
    BaseRepository, 
    orm, 
    orm_decorator
)

class LoansRepository(BaseRepository):
    Entity = LoansEntity

    @classmethod
    @orm_decorator
    def get(cls, lented_date, returned_date, student_uuid, instrument_uuid):
        objs = orm.select(
            (l.uuid, i, s, l.lented_at, l.returned_at) for l in cls.Entity for i in l.instrument_id for s in l.student_id 
        )
        
        print(objs.get_sql())
        return objs
