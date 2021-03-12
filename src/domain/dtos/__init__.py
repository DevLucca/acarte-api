from typing import TypeVar
from fastapi import Form, File, UploadFile
from pydantic.main import BaseModel, ModelMetaclass
import re, inspect

_T = TypeVar("_T")
def as_form(cls: _T) -> _T:
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = []
    for field in cls.__fields__.values():
        FormField = Form if field.outer_type_ is not UploadFile else File

        new_params.append(
            inspect.Parameter(
                field.alias,
                inspect.Parameter.KEYWORD_ONLY,
                default=(FormField(field.default) if not field.required else FormField(...)),
                annotation=field.outer_type_,
            )
        )

    def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

class MetaDTO(ModelMetaclass):
    def __new__(cls, *args, **kwargs):
        return as_form(super().__new__(cls, *args, **kwargs))


class BaseDTO(BaseModel, metaclass=MetaDTO):
    class Config:
        alias_generator = lambda field_name: re.sub(
            r"_([a-zA-Z])", lambda x: x[1].upper(), field_name
        )
        allow_population_by_field_name = True
