from .base import BaseRepository
from src.data.entities.instruments import Instruments as InstrumentEntity
from ...domain.dtos.instruments import Instrument
from pony import orm
from uuid import UUID, uuid4

class InstrumentRepository(BaseRepository):
    Entity: type[InstrumentEntity]

    def __init__(self) -> None:
        self.Entity = InstrumentEntity

    def _get_db_obj(self, id: UUID) -> InstrumentEntity:
        return super()._get_db_obj(id)

    def query(self, **kwargs) -> list[Instrument]:
        db_query = (
            orm.select(service for service in self.Entity)
                .filter(**self._clean_filter_args(kwargs))
                .order_by(self.Entity.start)
        )
        return [Instrument(**db_obj.to_dict()) for db_obj in db_query]

    def get(self, id: UUID) -> Instrument:
        db_obj = self._get_db_obj(id)
        return Instrument(**db_obj.to_dict())

    def create(self, dto: Instrument) -> Instrument:
        dto.id = uuid4()
        db_obj = self.Entity(**dto.dict())
        orm.commit()
        return Instrument(**db_obj.to_dict())

    def save(self, dto: Instrument) -> Instrument:
        db_obj = self._get_db_obj(dto.id)
        db_obj.set(**dto.dict())
        orm.commit()
        return Instrument(**db_obj.to_dict())

    def delete(self, dto: Instrument) -> None:
        db_obj = self._get_db_obj(dto.id)
        db_obj.delete()
