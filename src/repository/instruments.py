from models.instruments import Instruments
from viewmodels.instruments import ResponseInstrumentSchema
from repository import BaseRepository
from repository import orm

class InstrumentsRepository(BaseRepository):
    Model = Instruments
    Validator = ResponseInstrumentSchema

    @classmethod
    def get(cls, filters):
        try:
            with orm.db_session:
                obj = cls.Model
                print(obj[1])

                print(cls.Validator.from_orm(obj))
                return 
        except orm.ObjectNotFound:
            raise HTTPException(404,f"{cls.classname} not found.")

    @classmethod
    def create(cls, data):
        super().create(data)
