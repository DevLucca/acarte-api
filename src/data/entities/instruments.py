from pony import orm
from data.database import Entity
from domain.viewmodels.instruments import ResponseInstrumentSchema

class Instruments(Entity):
    schema = ResponseInstrumentSchema

    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    instument_id = orm.Required(str,max_len=50)
    name = orm.Required(str,max_len=50)
    instrument_type = orm.Required(str,max_len=50)
    notes = orm.Optional(str,max_len=1000)
    repair = orm.Required(bool)
    active = orm.Required(bool)
    created_at = orm.Required(str)
    updated_at = orm.Optional(str)
    deleted_at = orm.Optional(str)

