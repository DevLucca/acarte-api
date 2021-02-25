from domain.controllers import BaseController
from data.repositories.students import StudentsRepository
from domain.viewmodels.students import ResponseStudentSchema, RegisterStudentSchema
from domain.viewmodels.instruments import ResponseInstrumentSchema
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
    "name": "Nome do Aluno.",
    "surname": "Sobrenome do Aluno.",
    "ra": "Registro do Aluno.",
    "blocked": "Booleano para caso o aluno bloqueado para realizar outro emprestimo",
    "active": "Booleano para status de disponibilidade do aluno"
}

class StudentController(BaseController):
    Repository = StudentsRepository
    Validator = ResponseStudentSchema
    InstrumentValidator = ResponseInstrumentSchema
    
    @classmethod
    async def get(
        cls,
        name: str = Query("", description=descriptions['name']),
        surname: str = Query("", description=descriptions['surname']),
        ra: str = Query("", description=descriptions['ra']),
        blocked: bool = Query(False, description=descriptions['blocked']), 
        active: bool =  Query(True, description=descriptions['active']),
        pagination: PaginationParams = Depends()
    ):
        return paginate([cls.Validator.from_orm(obj) for obj in cls.Repository.get(name, surname, ra, blocked, active)], pagination)
    
    @classmethod
    async def get_lent_instrument(
        cls,
        uuid: str = Path(..., description=descriptions['uuid'])
    ):
        if not is_valid_uuid(uuid):
            raise HTTPException(406, 'Invalid UUID format')
        return [cls.InstrumentValidator.from_orm(obj) for obj in cls.Repository.get_lent_instruments(uuid)]

    @classmethod
    async def create(
        cls, 
        data: RegisterStudentSchema = Body(...)
    ):
        try:
            return cls.Repository.create(data.dict())
        except orm.TransactionIntegrityError as e:
            raise HTTPException(409, e.__str__())

    @classmethod
    async def update(
        cls,
        uuid: str = Path(..., description=descriptions['uuid']),
        update_data: RegisterStudentSchema = Body(...)
    ):
        try:
            if not is_valid_uuid(uuid):
                raise HTTPException(406, 'Invalid UUID format')
            return cls.Validator.from_orm(cls.Repository.update(uuid, update_data.dict()))
        except orm.ObjectNotFound:
            raise HTTPException(404, f"{cls.Repository.__name__.replace('Repository', '')[:-1]} not found")
