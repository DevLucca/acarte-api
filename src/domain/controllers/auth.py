from core import settings
from data.repositories.users import UserRepository
from data.repositories.settings import SettingsRepository
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.settings import cfg
from datetime import datetime, timedelta
from fastapi import (
    Depends,
    HTTPException,
    Request
)
from uuid import UUID
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing import Union, Tuple
from domain.dtos.auth import TokenSchema


class CustomOAuth2PwdBearer(OAuth2PasswordBearer):

    custom_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Not Authenticated",
        headers={"WWW-Authenticate": "JWT/Bearer"}
    )

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise self.custom_exception
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() not in ["jwt", "bearer"]:
            raise self.custom_exception
        return param


oauth_scheme = CustomOAuth2PwdBearer(tokenUrl="/auth/login")

class AuthController:
    settings = SettingsRepository()
    user_repo = UserRepository()

    def get_user_by_username(self, username: str):
        try:
            return self.user_repo.query(username=username)[0]
        except self.user_repo.Exceptions.DoesNotExist:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    # def verify_user(self, user: dict, password: str):
    #     if not user.verify_password(password):
    #         raise HTTPException(
    #             status_code=HTTP_401_UNAUTHORIZED,
    #             detail="Incorrect password"
    #         )

    def get_user(self, credentials: Tuple[str, str] = None, id: UUID = None):
        try: 
            if id:
                return self.user_repo.get(id)
            username, password = credentials
            user = self.get_user_by_username(username)
            # self.verify_user(user, password)
            return user
        except self.user_repo.Exceptions.DoesNotExist:
            raise HTTPException(404, 'User no longer exists')

    def create_token(self, user: dict):
        data = {
            "sub": {
                "user_uuid": str(user.uuid),
                "pin": False,
                "refresh": True
            },
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        self.token = jwt.encode(data, '234', algorithm="HS512")

    def authenticate(
        self,
        user_data: OAuth2PasswordRequestForm = Depends()
    ):
        try:
            assert user_data.client_id == self.settings.get("app_client_id") and user_data.client_secret == self.settings.get('app_client_secret'), "invalid client id or client secret"
            assert user_data.username or user_data.password, "Username or password missing"
            user = self.get_user(credentials=(user_data.username, user_data.password))
            self.create_token(user)
            return TokenSchema(access_token=self.token)
        except AssertionError as e:
            raise HTTPException(401, detail=str(e))

    @classmethod
    def scan_token(cls, token: str = Depends(oauth_scheme)):
        try:
            data = jwt.decode(token, '234', algorithms=[
                "HS512"]).get("sub")
            user_id = data.get("user_uuid")
            assert data
        except jwt.PyJWTError:
            raise HTTPException(401, detail="Invalid or expired token")
        except AssertionError:
            raise HTTPException(401, detail="Invalid token")
        auth = cls()
        return auth.get_user(id=user_id)
