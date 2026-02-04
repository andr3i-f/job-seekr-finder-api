from fastapi import APIRouter

from app.api.endpoints import test
from app.api.endpoints import jobs

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
