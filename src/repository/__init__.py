from core import cfg
from pony import orm

db = orm.Database()
db.bind(
    provider='sqlite',
    filename=':memory:'
    # host=cfg["db-location"]["value"],
    # user=cfg["db-user"]["value"],
    # passwd=cfg["db-password"]["value"],
    # db=cfg["db-name"]["value"]
    )
class DBClient:

    @classmethod
    def initialize(cls):
        from . import (instruments, loans, students, users)
        db.generate_mapping(create_tables=True)

from pony import orm
from models import db
from models.users import User
from validators import BaseValidator
from validators.users import UserValidator

class MetaController(type):

    @property
    def classname(cls):
        return cls.__name__.replace("Controller","")


class BaseController(metaclass=MetaController):
    Model = db.Entity
    Validator = BaseValidator

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
