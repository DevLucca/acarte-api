from repository import db

class DBClient:

    @classmethod
    def initialize(cls):
        from models import (instruments, loans, students)
        db.generate_mapping(create_tables=True)
