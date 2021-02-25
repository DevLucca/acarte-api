from pony import orm
from data.database import Entity
from uuid import uuid4
from datetime import datetime

class MetaRepository(type):

    @property
    def classname(cls):
        return cls.__name__.replace("Repository","")

def orm_decorator(callable):
        def internal_decorated(*args, **kwargs):
            try:
                with orm.db_session:
                    return_response = callable(*args, **kwargs)
                    orm.commit()
                    orm.flush()
                    return return_response
            except:
                orm.rollback()
        return internal_decorated

class BaseRepository(metaclass=MetaRepository):
    Entity = Entity
        
    @classmethod
    @orm_decorator
    def get_by_uuid(cls, uuid):
        try:
            obj = cls.Entity.get(uuid = uuid)
            assert obj is not None
            return obj
        except AssertionError:
            raise orm.ObjectNotFound(cls.Entity)

    @classmethod
    @orm_decorator
    def create(cls, data:dict):
        try:
            data['uuid'] = str(uuid4())
            obj = cls.Entity(**data)

            return obj
        except orm.TransactionIntegrityError as e:
            raise e

    @classmethod
    @orm_decorator
    def update(cls, uuid, updated_data):
        try:
            assert cls.is_deleted(uuid) is not True
            obj = cls.get_by_uuid(uuid)
            obj.set(updated_at=datetime.now(), **updated_data)

            return obj
        except AssertionError:
            raise orm.ObjectNotFound(cls.Entity)
        except orm.IntegrityError:
            raise orm.IntegrityError(cls.Entity)
    
    @classmethod
    @orm_decorator
    def delete(cls, uuid):
        try:
            obj = cls.get_by_uuid(uuid)
            obj.active = False
            obj.deleted_at = datetime.now()

            return obj
        except Exception as e:
            raise e

    @classmethod
    @orm_decorator
    def is_deleted(cls, uuid):
        try:
            if cls.get_by_uuid(uuid).deleted_at is None:
                return False
            return True
        except Exception as e:
            raise e
