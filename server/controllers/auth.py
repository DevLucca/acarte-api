from controllers.users import UserController
from models.users import UserDocument
import jwt
from fastapi.security import OAuth2PasswordBearer
from settings import PROJECT_KEY, USE_TWO_FACTOR, CLIENT_ID, CLIENT_SECRET
from datetime import datetime, timedelta
from fastapi import (
    Depends,
    HTTPException,
    Request
)
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing import Union, Tuple
from ..viewmodels.auth import TokenSchema

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

oauth_scheme = CustomOAuth2PwdBearer(tokenUrl="/token")

class AuthController:

    def get_user_by_id(self, id):
        return UserController.get(id, raw=True)

    def get_user_by_username(self, username: str):
        try:
            return list(UserDocument.scan(UserDocument.username == username))[0]
        except UserDocument.DoesNotExist:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    def verify_user(self, user: UserDocument, password: str):
        if not user.verify_password(password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

    def get_user(self, credentials: Tuple[str, str] = None, id: str = None):
        if id:
            return self.get_user_by_id(id)
        elif credentials:
            username, password = credentials
            user = self.get_user_by_username(username)
            self.verify_user(user, password)
            return user

    def create_token(self, user: UserDocument):
        data = {
            "sub": {
                "user_id": user.id,
                "pin": False,
                "refresh": False
            },
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        self.token = jwt.encode(data, PROJECT_KEY, algorithm="HS512")

    @classmethod
    def authenticate(cls, username: str, password: str, client_id: str, client_secret: str):
        if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
            raise HTTPException(403, detail="invalid client id or secret")
        auth = cls()
        if not username or not password:
            raise HTTPException(401, detail="Username or password missing")
        user = auth.get_user(credentials=(username, password))
        auth.create_token(user)
        return TokenSchema(access_token=auth.token, user_type=user.user_type)

    @classmethod
    def scan_token(cls, token: str = Depends(oauth_scheme)):
        try:
            data = jwt.decode(token, PROJECT_KEY, algorithms=[
                "HS512"]).get("sub")
            user_id = data.get("user_id")
            assert data
        except jwt.PyJWTError:
            raise HTTPException(401, detail="Invalid or expired token")
        except AssertionError:
            raise HTTPException(401, detail="Invalid token")
        auth = cls()
        return auth.get_user(id=user_id)
