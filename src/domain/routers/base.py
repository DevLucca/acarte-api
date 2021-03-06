from fastapi import (
    APIRouter, 
    Response
)

HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204

class BaseRouter(APIRouter):
  
    def post(self, *args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = HTTP_STATUS_CREATED
        return super().post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not "status_code" in kwargs:
            kwargs["status_code"] = HTTP_STATUS_NO_CONTENT
        if not "response_class" in kwargs:
            kwargs["response_class"] = Response
        return super().delete(*args, **kwargs)
