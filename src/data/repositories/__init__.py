from core import cfg
from pony import orm
from data.database import Entity

class MetaRepository(type):

    @property
    def classname(cls):
        return cls.__name__.replace("Repository","")


class BaseRepository(metaclass=MetaRepository):
    Model = Entity
    # Validator = BaseValidator

    @classmethod
    def create(cls, data:dict,raw:bool=False):
        try:
            with orm.db_session:
                obj = cls.Model(**data)
                orm.flush()

                return cls.Validator.from_orm(obj)
        except orm.TransactionIntegrityError as error:
            raise HTTPException(400,error.args)

    @classmethod
    def get_by_id(cls,id:int,raw:bool = False):
        try:
            with orm.db_session:
                obj = cls.Model[id]
            
                if raw:
                    return obj

                return cls.Validator.from_orm(obj)
        except orm.ObjectNotFound:
            raise HTTPException(404,f"{cls.classname} not found.")

    @classmethod
    def list(cls,raw:bool = False):
        with orm.db_session:
            query = orm.select(user for user in User)

            if raw:
                return query
            return [cls.Validator.from_orm(obj) for obj in query]

    @classmethod
    def delete(cls,id:int):
        with orm.db_session:
            obj = cls.get_by_id(id,True)
            obj.delete()
