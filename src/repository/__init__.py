from core import cfg
from pony import orm

orm.sql_debug(True)

db = orm.Database()
db.bind(
    provider='mysql',
    host=cfg["db-location"]["value"],
    port=cfg["db-port"]["value"],
    user=cfg["db-user"]["value"],
    passwd=cfg["db-password"]["value"],
    db=cfg["db-name"]["value"]
    )

# from models.instruments import Instruments
# from validators import BaseValidator
# from validators.users import UserValidator

class MetaRepository(type):

    @property
    def classname(cls):
        return cls.__name__.replace("Repository","")


class BaseRepository(metaclass=MetaRepository):
    Model = db.Entity
    # Validator = BaseValidator

    @classmethod
    def create(cls, data:dict,raw:bool=False):
        try:
            with orm.db_session:
                obj = cls.Model(**data)
                orm.flush()

                if raw:
                    return obj

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
