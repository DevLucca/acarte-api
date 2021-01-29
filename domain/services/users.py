from controllers import BaseController
from models.users import UserDocument
from ..server.viewmodels.users import ResponseUserSchema

class Users():
    model = UserDocument
    schema = ResponseUserSchema

    @classmethod
    def create(cls, schema: dict) -> ResponseUserSchema:
        user = super().create(schema, raw=True)
        user.set_password()
        return cls.schema.from_orm(user)

    @classmethod
    def update(cls, id: str, schema:dict):
        user = super().update(id, schema, raw=True)
        if schema.get('password', False):
            user.set_password()
        return cls.schema.from_orm(user)

    @classmethod
    def delete(cls, id: str) -> None:
        user = cls.get(id, raw=True)
        user.active = False
        user.save()

    @classmethod
    def hard_delete(cls, id: str) -> None:
        user = cls.get(id, raw=True)
        user.delete()