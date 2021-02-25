from domain.controllers import BaseController
from data.repositories.instruments import InstrumentsRepository
from domain.viewmodels.instruments import ResponseInstrumentSchema, RegisterInstrumentSchema
from domain.viewmodels.students import ResponseStudentSchema
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
    "name": "Nome do Instrumento. Exemplo: Saxofone, Flauta, Trompete...",
    "instrument_id": "Numero do Instrumento. Exemplo: Saxofone 01, Saxofone 02, Flauta 01...",
    "repair": "Booleano para caso o instrumento esteja em reparo, portanto desabilitado para emprestimos.",
    "active": "Booleano para status de disponibilidade do instrumento."
}

class InstrumentController(BaseController):
    Repository = InstrumentsRepository
    Validator = ResponseInstrumentSchema
    StudentValidator = ResponseStudentSchema
    
    @classmethod
    async def get(
        cls,
        instrument_id: str = Query("", description=descriptions['instrument_id']),
        name: str = Query("", description=descriptions['name']),
        repair: bool = Query(False, description=descriptions['repair']),
        active: bool = Query(True, description=descriptions['active']),
        pagination: PaginationParams = Depends()
    ):
        return paginate([cls.Validator.from_orm(obj) for obj in cls.Repository.get(name, instrument_id, repair, active)], pagination)

    @classmethod
    def get_student_loan(
        cls, 
        uuid: str = Path(..., description=descriptions['uuid'])
    ):
        if not is_valid_uuid(uuid):
            raise HTTPException(406, 'Invalid UUID format')
        if (data := cls.Repository.get_student_loan(uuid)) is not None:
            return cls.StudentValidator.from_orm(data)

    @classmethod
    async def create(
        cls, 
        data: RegisterInstrumentSchema = Body(...)
    ):
        try:
            return cls.Repository.create(data.dict())
        except orm.TransactionIntegrityError as e:
            raise HTTPException(409, e.__str__())

    @classmethod
    async def update(
        cls,
        uuid: str = Path(..., description=descriptions['uuid']),
        update_data: RegisterInstrumentSchema = Body(...)
    ):
        try:
            if not is_valid_uuid(uuid):
                raise HTTPException(406, 'Invalid UUID format')
            return cls.Validator.from_orm(cls.Repository.update(uuid, update_data.dict()))
        except orm.ObjectNotFound:
            raise HTTPException(404, f"{cls.Repository.__name__.replace('Repository', '')[:-1]} not found")
        except orm.IntegrityError as e:
            raise HTTPException(409, e.__str__())
