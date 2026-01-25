from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core import database_session
from app.core.security.jwt import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")

bearer_scheme = HTTPBearer(auto_error=True)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with database_session.get_async_session() as session:
        yield session


# TODO: Maybe convert this function to verify JWT token
# async def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     session: AsyncSession = Depends(get_session),
# ) -> User:
#     token_payload = verify_jwt_token(token)

#     user = await session.scalar(select(User).where(User.user_id == token_payload.sub))

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED
#         )
#     return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials

    try:
        payload = verify_jwt_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
