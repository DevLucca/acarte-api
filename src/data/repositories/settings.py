from pony import orm

from data.repositories import BaseRepository
from data.entities.settings import SettingsEntity

class SettingsRepository(BaseRepository):
    Entity: type[SettingsEntity]

    def __init__(self) -> None:
        self.Entity = SettingsEntity

    def get(self, key) -> tuple:
        db_obj = orm.get(setting for setting in self.Entity if setting.key == key)
        return db_obj
