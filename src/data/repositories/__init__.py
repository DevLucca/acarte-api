from abc import ABCMeta
from datetime import datetime
import inspect
from uuid import UUID, uuid4
from types import FunctionType
from typing import Any, TypeVar
from functools import wraps
from pony import orm
from pony.orm import core

Callable_T = TypeVar("Callable_T")
def db_session(func: Callable_T) -> Callable_T:

    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await (orm.db_session(func))(*args, **kwargs)
    else:
        @wraps(func)
        def inner(*args, **kwargs):
            return orm.db_session(func)(*args, **kwargs)
    return inner

class MetaRepoDict(dict):
    OPERATIONS = ["_get_db_obj", "query", "get", "create", "save", "delete"]

    def __setitem__(self, k: str, v: ...) -> None:
        if isinstance(v, FunctionType) and k in self.OPERATIONS:
            return super().__setitem__(k, db_session(v))
        else: 
            return super().__setitem__(k, v)

class MetaRepository(ABCMeta):
    def __prepare__(metacls, *args, **kwargs):
        return MetaRepoDict()

    def __new__(cls, name: str, bases: list[type], namespace: MetaRepoDict):
        return super().__new__(cls, name, bases, dict(namespace))

class BaseRepository(metaclass=MetaRepository):
    Entity: type[core.Entity]
    DTO: type[None]

    class Exceptions:
        class DoesNotExist(Exception):
            def __init__(self, *, message: str = "") -> None:
                super().__init__()
                self.message = message

        class RelatedObjectDoesNotExist(Exception):
            def __init__(self, *,  field: str, message: str = "") -> None:
                super().__init__()
                self.message = message
                self.field = field

        class AlreadyExists(Exception):
            def __init__(self, *, message: str = "") -> None:
                super().__init__()
                self.message = message

    def _clean_filter_args(self, filters: dict, strings: str = None) -> dict:
        filters = {k: v for k, v in filters.items() if v is not None}
        if strings == "remove":
            filters = {k: v for k, v in filters.items() if type(v) != str}
        elif strings == "only":
            filters = {k: v for k, v in filters.items() if type(v) == str}
        return filters
        
    def _get_db_obj(self, id):
        try:
            if type(id) == str or type(id) == UUID:
                db_obj = self.Entity.get(uuid=id)
            else:
                db_obj = self.Entity[id]
            assert db_obj
            return db_obj
        except (orm.ObjectNotFound, AssertionError) as e:
            raise self.Exceptions.DoesNotExist(message=str(e))
        
    def _get_related_object(self, entity: dict, repository, dto):
        db_obj = repository._get_db_obj(entity.id)
        return dto(**db_obj.to_dict())

    def query(self, **kwargs):
        db_query = (
            orm.select(obj for obj in self.Entity)
                .filter(**self._clean_filter_args(kwargs, "remove"))
                .order_by(self.Entity.created_at, self.Entity.id)
        )
        stringed_filters = self._clean_filter_args(kwargs, "only")
        for k, v in stringed_filters.items():
            db_query = db_query.filter(lambda ob: getattr(ob,k).startswith(v))
        return [self.DTO(**db_obj.to_dict()) for db_obj in db_query]

    def get(self, id: Any):
        db_obj = self._get_db_obj(id)
        return self.DTO(**db_obj.to_dict(related_objects=True))
    
    def create(self, dto):
        try:
            dto.uuid = uuid4()
            dto.created_at = datetime.now()
            db_obj = self.Entity(**dto.dict())
            orm.commit()
            return self.DTO(**db_obj.to_dict())
        except orm.IntegrityError:
            raise self.Exceptions.AlreadyExists

    def save(self, dto):
        db_obj = self._get_db_obj(dto.uuid)
        dto.updated_at = datetime.now()
        db_obj.set(**dto.dict())
        orm.commit()
        return self.DTO(**db_obj.to_dict())

    def delete(self, dto) -> None:
        db_obj = self._get_db_obj(dto.id)
        db_obj.delete()
