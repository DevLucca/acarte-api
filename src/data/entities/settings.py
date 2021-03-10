import datetime
from pony import orm
from data import db_client

class SettingsEntity(db_client.Entity):
    _table_ = 'settings'
    
    key = orm.Required(str)
    value = orm.Required(str)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
