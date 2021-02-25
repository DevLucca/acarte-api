from domain.controllers import BaseController
from data.repositories.loans import LoansRepository
from domain.viewmodels.loans import ResponseLoanSchema, RegisterLoanSchema
from fastapi import (
    Body,
    Path,
    Query,
    Depends,
    HTTPException
)
from pony import orm
from core.utils import is_valid_uuid
from fastapi_pagination import PaginationParams
from fastapi_pagination.paginator import paginate

descriptions = {
    "uuid": "Universally Unique Identifier.",
    "lented_at": "Emprestado na data.",
    "returned_at": "Retornado na data."
}

class LoanController(BaseController):
    Repository = LoansRepository
    Validator = ResponseLoanSchema
    
    @classmethod
    async def get(
        cls,
        lented_date: str = Query("", description=descriptions['lented_at']),
        returned_date: str = Query("", description=descriptions['returned_at']),
        instrument_uuid: str = Query("", description=descriptions['uuid']),
        student_uuid: str = Query("", description=descriptions['uuid']),
        pagination: PaginationParams = Depends()
    ):
        return paginate([cls.Validator.from_orm(obj) for obj in cls.Repository.get(lented_date, returned_date, instrument_uuid, student_uuid)], pagination)
    
    @classmethod
    async def create(
        cls, 
        data: RegisterLoanSchema = Body(...)
    ):
        try:
            return cls.Repository.create(data.dict())
        except orm.TransactionIntegrityError as e:
            raise HTTPException(409, e.__str__())

    @classmethod
    async def update(
        cls,
        uuid: str = Path(..., description=descriptions['uuid']),
        update_data: RegisterLoanSchema = Body(...)
    ):
        try:
            if not is_valid_uuid(uuid):
                raise HTTPException(406, 'Invalid UUID format')
            return cls.Validator.from_orm(cls.Repository.update(uuid, update_data.dict()))
        except orm.ObjectNotFound:
            raise HTTPException(404, f"{cls.Repository.__name__.replace('Repository', '')[:-1]} not found")
