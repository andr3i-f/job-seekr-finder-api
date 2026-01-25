import time
import requests

from jose import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.core.config import get_settings

JWT_ALGORITHM = "ES256"
JWKS_URL = get_settings().security.jwks_url + "/.well-known/jwks.json"
JWKS_TTL_12_HOURS = 60 * 60 * 12  # 12 Hours TTL
AUDIENCE = "authenticated"

_jwks_cache = {
    "keys": None,
    "fetched_at": 0
}

def get_jwks():
    now = time.time()

    if (
        _jwks_cache["keys"] is None or now - _jwks_cache["fetched_at"] > JWKS_TTL_12_HOURS
    ):
        res = requests.get(JWKS_URL)

        _jwks_cache["keys"] = res.json()
        _jwks_cache["fetched_at"] = now
    
    return _jwks_cache["keys"]


# Payload follows RFC 7519
# https://www.rfc-editor.org/rfc/rfc7519#section-4.1
class JWTTokenPayload(BaseModel):
    iss: str
    sub: str
    exp: int
    iat: int


class JWTToken(BaseModel):
    payload: JWTTokenPayload
    access_token: str


def verify_jwt_token(token: str) -> JWTTokenPayload:
    # Pay attention to verify_signature passed explicite, even if it is the default.
    # Verification is based on expected payload fields like "exp", "iat" etc.
    # so if you rename for example "exp" to "my_custom_exp", this is gonna break,
    # jwt.ExpiredSignatureError will not be raised, that can potentialy
    # be major security risk - not validating tokens at all.
    # If unsure, jump into jwt.decode code, make sure tests are passing
    # https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256
    raw_payload = jwt.decode(
        token,
        get_jwks(),
        algorithms=[JWT_ALGORITHM],
        options={"verify_signature": True},
        audience="authenticated"
    )

    return JWTTokenPayload(**raw_payload)
