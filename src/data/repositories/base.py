from abc import ABCMeta, abstractmethod
import inspect
from types import FunctionType
from typing import TypeVar
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

    def _clean_filter_args(self, filters: dict) -> dict:
        return {k: v for k, v in filters.items() if v is not None}
        
    @abstractmethod
    def _get_db_obj(self, id):
        try:
            return self.Entity[id]
        except orm.ObjectNotFound:
            raise self.Exceptions.DoesNotExist

    @abstractmethod
    def query(self, **kwargs): ...

    @abstractmethod
    def get(self, id): ...

    @abstractmethod
    def create(self, dto): ...

    @abstractmethod
    def save(self, dto): ...

    @abstractmethod
    def delete(self, dto): ...
