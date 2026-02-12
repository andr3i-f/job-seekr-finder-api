from fastapi import APIRouter

from app.api.endpoints import jobs, resume, test

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
