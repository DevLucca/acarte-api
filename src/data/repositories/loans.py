from domain.dtos.loans import LoanDTO

from data.repositories import BaseRepository
from data.entities.loans import LoansEntity

class LoanRepository(BaseRepository):
    Entity: type[LoansEntity]
    DTO: type[LoanDTO]

    def __init__(self) -> None:
        self.Entity = LoansEntity
        self.DTO = LoanDTO
