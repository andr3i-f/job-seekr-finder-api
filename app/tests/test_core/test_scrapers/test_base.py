import pytest
import httpx

from app.core.scrapers.base_scraper import BaseScraper
from app.tests.factories.job_factory import JobFactory


def test_creating_base_scraper():
    # Overwrite abstract methods so constructing an object does not throw errors
    BaseScraper.__abstractmethods__ = set()

    base = BaseScraper()

    assert base.url == ""
    assert base.source == "BaseScraper"


@pytest.mark.asyncio(loop_scope="session")
async def test_base_call_method_is_called_once_returns_200_status(respx_mock):
    # Overwrite abstract methods so constructing an object does not throw errors
    BaseScraper.__abstractmethods__ = set()

    base = BaseScraper()

    respx_mock.get(base.url).mock(
        return_value=httpx.Response(200, json={"results": ["fake_job", "fake_job2"]})
    )

    await base.call()

    EXPECTED_CALL_COUNT = 1
    assert respx_mock.calls.call_count == EXPECTED_CALL_COUNT


@pytest.mark.asyncio(loop_scope="session")
async def test_base_store_potential_jobs_method_able_to_store_jobs(session):
    # Overwrite abstract methods so constructing an object does not throw errors
    BaseScraper.__abstractmethods__ = set()

    base = BaseScraper()

    job1 = JobFactory()
    job2 = JobFactory()
    input = [job1, job2]

    EXPECTED_NEW_JOBS_AMOUNT = 2

    assert await base.store_potential_jobs(input) == EXPECTED_NEW_JOBS_AMOUNT
