from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.api_router import api_router
from app.core.config import get_settings
from app.seed_dev import seed_jobs_on_dev_start
from app.core.limiter import limiter

app = FastAPI(
    title="minimal fastapi postgres template",
    version="6.1.0",
    description="https://github.com/rafsaf/minimal-fastapi-postgres-template",
    openapi_url="/openapi.json",
    docs_url="/",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router)

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().security.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guards against HTTP Host Header attacks
if get_settings().general.env == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=get_settings().security.allowed_hosts,
    )


@app.on_event("startup")
async def startup():
    await seed_jobs_on_dev_start()
