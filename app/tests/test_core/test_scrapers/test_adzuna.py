import pytest

from app.tests.factories.job_factory import JobFactory
from app.core.scrapers.adzuna import Adzuna


@pytest.mark.asyncio(loop_scope="session")
async def test_job_exists_in_database_expect_false(session):
    adzuna = Adzuna()
    job1 = JobFactory(source=adzuna.source)
    job2 = JobFactory(source=adzuna.source)

    session.add(job1)
    await session.commit()

    assert await adzuna.job_exists_in_database(job2, session) is False


@pytest.mark.asyncio(loop_scope="session")
async def test_job_exists_in_database_expect_true(session):
    adzuna = Adzuna()
    job = JobFactory(source=adzuna.source)

    session.add(job)
    await session.commit()

    assert await adzuna.job_exists_in_database(job, session) is True
