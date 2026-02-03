from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.deps import get_current_user
from app.models import Job

router = APIRouter()

@router.get("/limited-generic-jobs")
async def get_limited_jobs(session: AsyncSession = Depends(deps.get_session)):
    limited_jobs_query = select(Job).order_by(desc(Job.create_time)).limit(15).all()
    result = await session.execute(limited_jobs_query)
    return { "jobs": result } 


@router.get("/jobs")
async def get_jobs(session: AsyncSession = Depends(deps.get_session), _=Depends(get_current_user)):
    pass


