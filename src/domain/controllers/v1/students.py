import traceback
from uuid import UUID

from domain.dtos.users import UserDTO
from domain.dtos.students import StudentDTO
from domain.controllers.auth import AuthController

from data.repositories.students import StudentRepository

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
    "name": "Nome do Aluno.",
    "surname": "Sobrenome do Aluno.",
    "ra": "Registro do Aluno.",
    "blocked": "Booleano para caso o aluno bloqueado para realizar outro emprestimo",
    "active": "Booleano para status de disponibilidade do aluno"
}

class StudentController:
    repository = StudentRepository()
    DTO = StudentDTO

    async def get(
        self,
        name: str = Query("", description=descriptions['name']),
        surname: str = Query("", description=descriptions['surname']),
        ra: str = Query("", description=descriptions['ra']),
        blocked: bool = Query(False, description=descriptions['blocked']), 
        active: bool =  Query(True, description=descriptions['active']),
        pagination: PaginationParams = Depends()
    ) -> Page[DTO]:
        try:
            return paginate(self.repository.query(
                name=name,
                surname=surname,
                ra=ra,
                blocked=blocked,
                active=active,
            ), pagination)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    async def get_by_id(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid'])
    ) -> DTO:
        try:
            student = self.repository.get(uuid)
            return student
        except self.repository.Exceptions.DoesNotExist:
            raise HTTPException(404, detail="Student not found")
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")

    async def get_instruments_loan(self): ...
    
    async def create(
        self,
        data: DTO.StudentPostSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin, "Only admins can create students"
            student = self.DTO(**data.dict(), updated_by=current_user)
            return self.repository.create(student)
        except AssertionError as e:
            raise HTTPException(403, detail=str(e))
        except self.repository.Exceptions.AlreadyExists:
            raise HTTPException(403, detail='Student already exists')
        except Exception:
            raise HTTPException(503, detail=f"An error occured: {traceback.format_exc()}")
    
    async def update(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        data: DTO.StudentPutSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            student = self.repository.get(uuid)
            for k, v in data.dict(exclude_none=True, exclude_unset=True).items():
                setattr(student, k, v)
            student.updated_by = current_user
            return self.repository.save(student)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
    
    async def delete(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> None:
        try:
            assert current_user.admin, "Only admins can delete users"
            student = self.repository.get(uuid)
            self.repository.delete(student)
        except (self.repository.Exceptions.DoesNotExist):
            raise HTTPException(404, detail=f"Instrument not found")
        except AssertionError as e:
            raise HTTPException(403, detail=str(e))
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
