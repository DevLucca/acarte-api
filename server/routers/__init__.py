from fastapi import APIRouter

class CustomRouter(APIRouter):
    def post(self, path, *, response_model=None, status_code=201, tags=None, dependencies=None, summary=None, description=None, response_description='Successful Response', responses=None, deprecated=None, operation_id=None, response_model_include=None, response_model_exclude=set(), response_model_by_alias=True, response_model_skip_defaults=None, response_model_exclude_unset=False, response_model_exclude_defaults=False, response_model_exclude_none=False, include_in_schema=True, response_class=None, name=None, callbacks=None):
        return super().post(path, response_model=response_model, status_code=status_code, tags=tags, dependencies=dependencies, summary=summary, description=description, response_description=response_description, responses=responses, deprecated=deprecated, operation_id=operation_id, response_model_include=response_model_include, response_model_exclude=response_model_exclude, response_model_by_alias=response_model_by_alias, response_model_skip_defaults=response_model_skip_defaults, response_model_exclude_unset=response_model_exclude_unset, response_model_exclude_defaults=response_model_exclude_defaults, response_model_exclude_none=response_model_exclude_none, include_in_schema=include_in_schema, response_class=response_class, name=name, callbacks=callbacks)

def get_filters(locals_: dict, excluded: list = []) -> dict:
    locals_ = {key:value for key, value in locals_.items() if 
                value is not None and key not in excluded}
    
    return locals_
