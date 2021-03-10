import datetime
from pony import orm
from uuid import UUID
from data import db_client

class UsersEntity(db_client.Entity):
    _table_ = 'users'
    
    loans = orm.Set("LoansEntity")
    students = orm.Set("StudentsEntity")
    instruments = orm.Set("InstrumentsEntity")
    uuid = orm.Required(UUID,unique=True)
    name = orm.Required(str,max_len=50)
    username = orm.Required(str,max_len=10)
    email = orm.Required(str,max_len=30)
    password = orm.Required(str,max_len=50)
    admin = orm.Required(bool,sql_default=False)
    active = orm.Required(bool,sql_default=True)
    created_at = orm.Required(datetime.datetime,default=datetime.datetime.now())
    
    orm.composite_key(name, username, email)
