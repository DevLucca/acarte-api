import re
from uuid import UUID
from datetime import datetime
from domain.dtos import BaseDTO
from pydantic import EmailStr
from pydantic.fields import Field
from pydantic.class_validators import validator

class UserDTO(BaseDTO):
    id: int = None
    uuid: UUID = None
    name: str = None
    username: str = None
    email: str = None
    password: str = None
    admin: bool = False
    active: bool = None
    created_at: datetime = None

    class UserPostSchema(BaseDTO):
        name: str = Field(...)
        username: str = Field(...)
        email: EmailStr = Field(...)
        password: str = Field(None)
        admin: bool = Field(False)
        active: bool = Field(True)

        @validator("name")
        def validate_name(cls, val):
            assert val, 'name cannot be empty or missing'
            return val

        @validator("username")
        def validate_username(cls, val):
            assert val, 'usernmae cannot be empty or missing'
            return val
        
        @validator("email")
        def validate_email(cls, val):
            assert val, 'email pattern wrong or missing'
            return val
        
        @validator("password")
        def validate_password(cls, val):
            assert val, 'password cannot be empty or missing'
            return val

    class UserPasswordPutSchema(BaseDTO):
        password: str = Field(None)
        
    class UserPutSchema(BaseDTO):
        name: str = Field(None)
        username: str = Field(None)
        email: EmailStr = Field(None)
        admin: bool = Field(False)
        active: bool = Field(True)

    class UserResponseSchema(BaseDTO):
        uuid: UUID = Field(...)
        name: str = Field(...)
        username: str = Field(...)
        email: EmailStr = Field(...)
        admin: bool = Field(False)
        active: bool = Field(True)
        created_at: datetime = Field(...)
    
    class UserUpdatedByResponseSchema(BaseDTO):
        name: str = Field(...)
        username: str = Field(...)
