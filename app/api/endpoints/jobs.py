from fastapi import APIRouter, Depends, Request
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.deps import get_current_user
from app.core.consts import JobExperienceTypes
from app.core.limiter import limiter
from app.models import Job

router = APIRouter()


@router.get("")  # / translates to ../jobs
async def get_jobs(
    experience_level: JobExperienceTypes,
    location: str | None = None,
    session: AsyncSession = Depends(deps.get_session),
    _=Depends(get_current_user),
):
    # TODO: build query based on parameter, for now, we only care about experience_level
    # TODO: when implementing location, we need to set it to be equal to a certain regex
    # TODO: probably implement some sort of pagination feature
    jobs_query = select(Job).where(Job.experience_level == experience_level)
    result = await session.execute(jobs_query)
    jobs = result.scalars().all()
    return {"jobs": jobs}


@router.get("/limited-generic-jobs")
@limiter.limit("5/minute")
async def get_limited_jobs(
    request: Request,
    experience_level: JobExperienceTypes,
    skills: str | None = None,
    location: str | None = None,
    session: AsyncSession = Depends(deps.get_session),
):
    limited_jobs_query = (
        select(Job)
        .where(Job.experience_level == experience_level)
        .order_by(desc(Job.create_time))
        .limit(15)
    )
    result = await session.execute(limited_jobs_query)
    jobs = result.scalars().all()
    return {"jobs": jobs}


@router.get("/total-jobs")
async def get_total_jobs(session: AsyncSession = Depends(deps.get_session)):
    total_jobs_query = select(func.count()).select_from(Job)
    result = await session.execute(total_jobs_query)
    total_jobs = result.scalar()
    return {"total_jobs": total_jobs}
