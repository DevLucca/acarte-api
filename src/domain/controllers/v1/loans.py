import traceback
from uuid import UUID
from datetime import date, datetime

from domain.dtos.users import UserDTO
from domain.dtos.loans import LoanDTO
from domain.controllers.auth import AuthController

from data.repositories.loans import LoanRepository

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
    "lented_at": "Emprestado na data.",
    "returned_at": "Retornado na data."
}

class LoanController:
    repository = LoanRepository()
    DTO = LoanDTO

    async def get(
        self,
        instrument_uuid: UUID = Query(None, description=descriptions['uuid']),
        student_uuid: UUID = Query(None, description=descriptions['uuid']),
        lented_date: datetime = Query(None, description=descriptions['lented_at']),
        returned_date: datetime = Query(False, description=descriptions['returned_at']),
        pagination: PaginationParams = Depends()
    ) -> Page[DTO]:
        try:
            return paginate(self.repository.query(
                instrument_uuid=instrument_uuid,
                student_uuid=student_uuid,
                lented_at=lented_date,
                returned_at=returned_date
            ), pagination)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    async def get_by_id(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid'])
    ) -> DTO:
        try:
            loan = self.repository.get(uuid)
            return loan
        except (self.repository.Exceptions.DoesNotExist, AssertionError):
            raise HTTPException(404, detail="Loan not found")
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")

    async def create(
        self,
        data: DTO.LoanPostSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            print(data)
            loan = self.DTO(**data.dict(), updated_by=current_user)
            return self.repository.create(loan)
        except self.repository.Exceptions.AlreadyExists:
            raise HTTPException(403, detail='Loan already exists')
        except Exception:
            raise HTTPException(503, detail=f"An error occured: {traceback.format_exc()}")
    
    async def update(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        data: DTO.LoanPutSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            loan = self.repository.get(uuid)
            if data.is_returned: 
                loan.returned_at = datetime.now()
                loan.updated_by = current_user
            return self.repository.save(loan)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
