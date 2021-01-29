from pony import orm
from data import db

class Students(db.Entity):
    loan = orm.Set("Loans")
    uuid = orm.Required(str,max_len=36,unique=True)
    name = orm.Required(str,max_len=50,unique=True)
    surname = orm.Required(str,max_len=50,unique=True)
    ra = orm.Required(int,unique=True)
