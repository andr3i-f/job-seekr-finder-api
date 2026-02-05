import asyncio

from sqlalchemy import func, select

from app.core.config import get_settings
from app.core.database_session import get_async_session
from app.tests.factories.job_factory import JobFactory


async def seed_jobs_on_dev_start(count: int = 25):
    if get_settings().general.env != "development":
        return

    async with get_async_session() as session:
        statement = select(func.count()).select_from(JobFactory._meta.model)
        existing = await session.execute(statement)
        existing = existing.scalar()

        if existing > 0:
            return

        jobs = JobFactory.create_batch(count)
        session.add_all(jobs)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_jobs_on_dev_start())
