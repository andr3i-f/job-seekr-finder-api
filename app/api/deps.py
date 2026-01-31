from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import database_session
from app.core.security.jwt import JWTTokenPayload, verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")

bearer_scheme = HTTPBearer(auto_error=True)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with database_session.get_async_session() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> JWTTokenPayload:
    token = credentials.credentials

    try:
        payload = await verify_jwt_token(token)
        return payload
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
