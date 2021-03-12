from pony import orm
from uuid import uuid4
from datetime import datetime

from domain.dtos.users import UserDTO
from domain.dtos.instruments import InstrumentDTO

from data.repositories import BaseRepository
from data.repositories.users import UserRepository
from data.entities.instruments import InstrumentsEntity

class InstrumentRepository(BaseRepository):
    Entity: type[InstrumentsEntity]
    DTO: type[InstrumentDTO]

    def __init__(self) -> None:
        self.Entity = InstrumentsEntity
        self.DTO = InstrumentDTO

    def query(self, **kwargs):
        stringed_filters = self._clean_filter_args(kwargs, "only")
        db_query = (
            orm.select(obj for obj in self.Entity
                       if orm.raw_sql(f"name LIKE '%%{stringed_filters.get('name', '')}%%'")
                       and orm.raw_sql(f"number LIKE '%%{stringed_filters.get('number', '')}%%'")
                       and orm.raw_sql(f"itype LIKE '%%{stringed_filters.get('itype', '')}%%'")
                       )
                .filter(**self._clean_filter_args(kwargs, "remove"))
                .order_by(self.Entity.created_at, self.Entity.id)
        )
        to_be_dto = []
        for db_obj in db_query:
            db_obj = db_obj.to_dict(related_objects=True)
            db_obj['updated_by'] = self._get_related_object(db_obj.get('updated_by'), UserRepository(), UserDTO)
            to_be_dto.append(self.DTO(**db_obj))
        return to_be_dto
    
    def get(self, id: any):
        db_obj = self._get_db_obj(id).to_dict(related_objects=True)
        db_obj['updated_by'] = self._get_related_object(db_obj.get('updated_by'), UserRepository(), UserDTO)
        return self.DTO(**db_obj)

    def create(self, dto):
        try:
            dto.uuid = uuid4()
            dto.created_at = datetime.now()
            user = dto.updated_by
            del dto.updated_by
            db_obj = self.Entity(**dto.dict(), updated_by=UserRepository()._get_db_obj(user.uuid))
            orm.commit()
            db_obj = db_obj.to_dict(related_objects=True)
            db_obj['updated_by'] = self._get_related_object(db_obj.get('updated_by'), UserRepository(), UserDTO)
            return self.DTO(**db_obj)
        except orm.core.TransactionIntegrityError:
            raise self.Exceptions.AlreadyExists

    def save(self, dto):
        db_obj = self._get_db_obj(dto.uuid)
        dto.updated_at = datetime.now()
        user = dto.updated_by
        del dto.updated_by
        db_obj.set(**dto.dict(), updated_by=UserRepository()._get_db_obj(user.uuid))
        orm.commit()
        db_obj = db_obj.to_dict(related_objects=True)
        db_obj['updated_by'] = self._get_related_object(db_obj.get('updated_by'), UserRepository(), UserDTO)
        return self.DTO(**db_obj)
