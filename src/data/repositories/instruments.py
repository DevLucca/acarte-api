from data.entities.instruments import Instruments
from domain.viewmodels.instruments import ResponseInstrumentSchema
from data.repositories import BaseRepository
from pony import orm
from fastapi import HTTPException

class InstrumentsRepository(BaseRepository):
    Model = Instruments
    Validator = ResponseInstrumentSchema

    @classmethod
    def get(cls, filters):
        try:
            with orm.db_session:
                
                obj = cls.Model
                print(obj[0])

                print(cls.Validator.from_orm(obj))
                return 
        except orm.ObjectNotFound:
            raise HTTPException(404,f"{cls.classname} not found.")

    @classmethod
    def create(cls, data):
        super().create(data)
