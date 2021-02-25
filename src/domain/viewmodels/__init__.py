from pydantic.main import BaseModel, ModelMetaclass, create_model, ModelField
import re

class MetaValidator(ModelMetaclass):
    @property
    def EditValidator(cls):
        edit_validator = create_model(cls.__name__.replace("Validator", "EditValidator"), __base__=cls)
        for name, field in edit_validator.__fields__.items():
            field.required = False
            field.default = None
        return edit_validator


class BaseValidator(BaseModel, metaclass=MetaValidator):
    class Config:
        orm_mode = True
        alias_generator = lambda field_name: field_name.replace('_', '-')
        # alias_generator = lambda field_name: re.sub(
        #     r"_([a-zA-Z])", lambda x: x[1].upper(), field_name
        # )
        allow_population_by_field_name = True
