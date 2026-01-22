import pytest
from app.tests.factories.job_factory import JobFactory

@pytest.mark.asyncio(loop_scope="session")
async def test_job_exists_in_database_expect_false(session):
    job1 = JobFactory()
    job2 = JobFactory()

    session.add(job1)
    await session.commit()

    assert await job2.exists_in_database() is False