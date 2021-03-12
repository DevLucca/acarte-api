from domain.dtos.users import UserDTO

from data.repositories import BaseRepository
from data.entities.users import UsersEntity

class UserRepository(BaseRepository):
    Entity: type[UsersEntity]
    DTO: type[UserDTO]

    def __init__(self) -> None:
        self.Entity = UsersEntity
        self.DTO = UserDTO
