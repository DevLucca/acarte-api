import os
from fastapi import APIRouter

def check_exists_folder(folder_path: str, create_if_not: bool = False) -> bool:
    return True

def check_exists_file(filename: str, create_if_not: bool = False) -> bool:
    if os.path.isfile(filename):
        return True
    elif create_if_not:
        open(filename,"w")
        return True
    else:
        return False

def check_env_by_name(envname: str) -> bool:
    return (lambda x: True if x != None else False)(os.getenv(envname))

class CustomRouter(APIRouter):
    def post(self,*args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = 201
        
        return super().post(*args, **kwargs)
    
    def delete(self,*args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = 204
        
        return super().delete(*args, **kwargs)

def get_filters(locals_: dict, excluded: list = []) -> dict:
    locals_ = {key:(value if type(value) != str else value.split(',')) for key, value in locals_.items() if 
                value is not None and key not in excluded}
    
    return locals_
