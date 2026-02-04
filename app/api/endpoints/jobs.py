from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.deps import get_current_user
from app.models import Job

router = APIRouter()

@router.get("/limited-generic-jobs")
async def get_limited_jobs(session: AsyncSession = Depends(deps.get_session)):
    limited_jobs_query = select(Job).order_by(desc(Job.create_time)).limit(15)
    result = await session.execute(limited_jobs_query)
    jobs = result.scalars().all()
    return { "jobs": jobs } 


@router.get("/jobs")
async def get_jobs(experience_level: str | None = None, location: str | None = None, session: AsyncSession = Depends(deps.get_session), _=Depends(get_current_user)):
    # TODO: build query based on parameter, for now, we only care about experience_level
    # TODO: when implementing location, we need to set it to be equal to a certain regex
    # TODO: probably implement some sort of pagination feature

    jobs_query = select(Job).where(Job.experience_level ==  experience_level)
    result = await session.execute(jobs_query)
    jobs = result.scalars.all()
    return { "jobs": jobs }
