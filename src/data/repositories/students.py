from domain.dtos.users import UserDTO

from data.repositories import BaseRepository
from data.entities.students import StudentsEntity

class StudentRepository(BaseRepository):
    Entity: type[StudentsEntity]
    DTO: type[UserDTO]

    def __init__(self) -> None:
        self.Entity = StudentsEntity
        self.DTO = UserDTO
