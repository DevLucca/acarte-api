from data.repositories import BaseRepository
from domain.viewmodels import BaseValidator
from fastapi import (
    Path,
    HTTPException
)
from pony import orm
from core.utils import is_valid_uuid

descriptions = {
    "uuid": "Universally Unique Identifier."
}

class BaseController:
    Repository = BaseRepository
    Validator = BaseValidator

    @classmethod
    async def get_by_uuid(
        cls,
        uuid: str = Path(..., description=descriptions['uuid'])
    ):
        try:
            if not is_valid_uuid(uuid):
                raise HTTPException(406, 'Invalid UUID format')
            return cls.Validator.from_orm(cls.Repository.get_by_uuid(uuid))
        except orm.ObjectNotFound:
            raise HTTPException(404, f"{cls.Repository.__name__.replace('Repository', '')[:-1]} not found")

    @classmethod
    async def delete(
        cls,
        uuid: str = Path(..., description=descriptions['uuid'])
    ):
        try:
            if not is_valid_uuid(uuid):
                raise HTTPException(406, 'Invalid UUID format')
            cls.Repository.delete(uuid)
        except orm.ObjectNotFound:
            raise HTTPException(404, f"{cls.Repository.__name__.replace('Repository', '')[:-1]} not found")

