from fastapi import APIRouter

class CustomRouter(APIRouter):
    def post(self,*args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = 201
        
        return super().post(*args, **kwargs)
    
    def delete(self,*args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = 204
        
        return super().delete(*args, **kwargs)
