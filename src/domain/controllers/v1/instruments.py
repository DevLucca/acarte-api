import traceback
from uuid import UUID

from domain.dtos.users import UserDTO
from domain.dtos.instruments import InstrumentDTO
from domain.dtos.students import StudentDTO
from domain.controllers.auth import AuthController

from data.repositories.loans import LoanRepository
from data.repositories.students import StudentRepository
from data.repositories.instruments import InstrumentRepository

from fastapi import (
    Query, 
    Depends, 
    Body,
    Path,
    HTTPException
)
from fastapi_pagination import PaginationParams, Page
from fastapi_pagination.paginator import paginate

descriptions = {
    "uuid": "Universally Unique Identifier.",
    "name": "Nome do Instrumento. Exemplo: Saxofone, Flauta, Trompete...",
    "number": "Numero do Instrumento. Exemplo: Saxofone 01, Saxofone 02, Flauta 01...",
    "itype": "Tipo do Instrumento. Exemplo: Madeira, Metal, Percussao, Cordas...",
    "repair": "Booleano para caso o instrumento esteja em reparo, portanto desabilitado para emprestimos.",
    "active": "Booleano para status de disponibilidade do instrumento."
}

class InstrumentController:
    repository = InstrumentRepository()
    DTO = InstrumentDTO

    async def get(
        self,
        name: str = Query(None, description=descriptions['name']),
        number: str = Query(None, description=descriptions['number']),
        itype: str = Query(None, description=descriptions['itype']),
        repair: bool = Query(False, description=descriptions['repair']),
        active: bool = Query(True, description=descriptions['active']),
        pagination: PaginationParams = Depends()
    ) -> Page[DTO]:
        try:
            return paginate(self.repository.query(
                name=name,
                number=number,
                itype=itype,
                repair=repair,
                active=active,
            ), pagination)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    async def get_by_id(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid'])
    ) -> DTO:
        try:
            instrument = self.repository.get(uuid)
            return instrument
        except (self.repository.Exceptions.DoesNotExist, AssertionError):
            raise HTTPException(404, detail="Instrument not found")
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")

    async def get_student_loan(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid'])
    ) -> StudentDTO:
        try:
            loan = LoanRepository().query(instrument_uuid=uuid)
            assert loan, "Instrument is not lented"
            # assert loan.
            return StudentRepository().get(loan[0].student.id)
        except AssertionError as e:
            raise HTTPException(404, detail=str(e))
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
    
    async def create(
        self,
        data: DTO.InstrumentPostSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin, "Only admins can create instruments"
            instrument = self.DTO(**data.dict(), updated_by=current_user)
            return self.repository.create(instrument)
        except AssertionError as e:
            raise HTTPException(403, detail=str(e))
        except self.repository.Exceptions.AlreadyExists:
            raise HTTPException(403, detail='Instrument already exists')
        except Exception:
            raise HTTPException(503, detail=f"An error occured: {traceback.format_exc()}")
    
    async def update(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        data: DTO.InstrumentPutSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            instrument = self.repository.get(uuid)
            for k, v in data.dict(exclude_none=True, exclude_unset=True).items():
                setattr(instrument, k, v)
            instrument.updated_by = current_user
            return self.repository.save(instrument)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
    
    async def delete(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> None:
        try:
            assert current_user.admin, "Only admins can delete users"
            instrument = self.repository.get(uuid)
            self.repository.delete(instrument)
        except (self.repository.Exceptions.DoesNotExist):
            raise HTTPException(404, detail=f"Instrument not found")
        except AssertionError as e:
            raise HTTPException(403, detail=str(e))
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
