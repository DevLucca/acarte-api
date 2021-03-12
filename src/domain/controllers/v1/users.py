import traceback
from uuid import UUID

from domain.controllers.auth import AuthController
from domain.dtos.users import UserDTO

from data.repositories.users import UserRepository

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
    "name": "Nome do Usuário.",
    "username": "Username do Usuário.",
    "email": "Email do Usuário.",
    "active": "Booleano para status de disponibilidade do instrumento."
}

class UserController:
    repository = UserRepository()
    DTO = UserDTO
    
    async def get(
        self,
        name: str = Query(None, description=descriptions['name']),
        username: str = Query(None, description=descriptions['username']),
        email: str = Query(None, description=descriptions['email']),
        active: bool = Query(True, description=descriptions['active']),
        pagination: PaginationParams = Depends()
    ) -> Page[DTO]:
        try:
            return paginate(self.repository.query(
                name=name,
                username=username,
                email=email,
                active=active,
            ), pagination)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    def get_by_id(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        current_user: DTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin
            user = self.repository.get(uuid)
            return user
        except self.repository.Exceptions.DoesNotExist:
            raise HTTPException(404, detail="User not found")
        except AssertionError:
            raise HTTPException(403, detail='User is not an admin')
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")

    def create(
        self,
        data: DTO.UserPostSchema = Body(...),
        current_user: DTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin
            user = self.DTO(**data.dict())
            return self.repository.create(user)
        except AssertionError:
            raise HTTPException(403, detail='Only admins can create users')
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    def update(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        data: DTO.UserPutSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin or current_user.uuid == uuid, "Only self user or admin can update data"
            user = self.repository.get(uuid)
            assert user.username != 'admin', "User 'admin' can not be updated"
            if not user.admin:
                assert user.admin and data.admin, "Non admin user can not update admin field"
            for k, v in data.dict(exclude_none=True, exclude_unset=True).items():
                setattr(user, k, v)
            return self.repository.save(user)
        except AssertionError as e:
            raise HTTPException(403, detail=str(e))
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    def update_password(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        data: DTO.UserPutSchema = Body(...),
        current_user: UserDTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin or current_user.uuid == uuid, "Only self user or admin can update data"
            user = self.repository.get(uuid)
            assert user.username != 'admin', "User 'admin' can not be updated"
            if not user.admin:
                assert user.admin and data.admin, "Non admin user can not update admin field"
            for k, v in data.dict(exclude_none=True, exclude_unset=True).items():
                setattr(user, k, v)
            return self.repository.save(user)
        except AssertionError as e:
            raise HTTPException(403, detail=e)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
        
    def delete(
        self,
        uuid: UUID = Path(..., description=descriptions['uuid']),
        current_user: DTO = Depends(AuthController.scan_token)
    ) -> DTO:
        try:
            assert current_user.admin, "Only admins can delete users"
            user = self.repository.get(uuid)
            assert user.username != 'admin', "User 'admin' can not be deleted"
            self.repository.delete(user)
        except AssertionError as e:
            raise HTTPException(403, detail=e)
        except Exception:
            raise HTTPException(500, detail=f"An error occured: {traceback.format_exc()}")
