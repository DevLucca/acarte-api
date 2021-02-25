from pony import orm
import datetime
from data.database import Entity
from domain.viewmodels.instruments import ResponseInstrumentSchema

class Instruments(Entity):
    schema = ResponseInstrumentSchema

    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    instrument_id = orm.Required(str,max_len=50)
    name = orm.Required(str,max_len=50)
    instrument_type = orm.Required(str,max_len=50)
    notes = orm.Optional(str,max_len=1000,sql_default="''", nullable=True)
    repair = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    updated_at = orm.Optional(datetime.datetime)
    deleted_at = orm.Optional(datetime.datetime)

    orm.composite_key(name, instrument_id, instrument_type)
