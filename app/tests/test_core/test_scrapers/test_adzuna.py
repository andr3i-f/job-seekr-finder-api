import pytest
import httpx

from app.tests.factories.job_factory import JobFactory
from app.core.scrapers.adzuna import Adzuna

from app.core.consts import JOB_EXPERIENCE_TYPES


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


@pytest.mark.asyncio(loop_scope="session")
async def test_adzuna_scraper_calls_api_returns_data_with_200_status(respx_mock):
    adzuna = Adzuna()
    salary_min, salary_max = 50000, 100000
    description = "test_description"
    job1 = JobFactory(source=adzuna.source)
    job2 = JobFactory(source=adzuna.source)

    respx_mock.get(adzuna.url).mock(
        return_value=httpx.Response(
            200,
            json={
                "results": [
                    {
                        "title": job1.title,
                        "id": job1.source_id,
                        "company": {"display_name": job1.company_name},
                        "description": description,
                        "redirect_url": job1.url,
                        "salary_min": salary_min,
                        "salary_max": salary_max,
                        "location": {"display_name": job1.location},
                    },
                    {
                        "title": job2.title,
                        "id": job2.source_id,
                        "company": {"display_name": job2.company_name},
                        "description": description,
                        "redirect_url": job2.url,
                        "salary_min": salary_min,
                        "salary_max": salary_max,
                        "location": {"display_name": job2.location},
                    },
                ]
            },
        )
    )

    await adzuna.call()
    EXPECTED_CALL_COUNT = len(JOB_EXPERIENCE_TYPES)
    assert respx_mock.calls.call_count == EXPECTED_CALL_COUNT


def test_build_params_expect_keys_to_be_properly_set():
    adzuna = Adzuna()

    actual_params = adzuna.build_params()

    assert "app_id" in actual_params.keys()
    assert "app_key" in actual_params.keys()

    assert actual_params["what"] == "Software Developer"
    assert actual_params["category"] == "it-jobs"


def test_build_header_is_properly_set():
    adzuna = Adzuna()

    actual_header = adzuna.build_header()

    assert actual_header["Accept"] == "application/json"


async def test_parse_response_gives_valid_job_list():
    adzuna = Adzuna()

    salary_min, salary_max = 50000, 100000
    description = "test_description"
    job1 = JobFactory(source=adzuna.source)
    job2 = JobFactory(source=adzuna.source)

    input = {
        "results": [
            {
                "title": job1.title,
                "id": job1.source_id,
                "company": {"display_name": job1.company_name},
                "description": description,
                "redirect_url": job1.url,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "location": {"display_name": job1.location},
            },
            {
                "title": job2.title,
                "id": job2.source_id,
                "company": {"display_name": job2.company_name},
                "description": description,
                "redirect_url": job2.url,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "location": {"display_name": job2.location},
            },
        ]
    }

    expected = [job1, job2]
    actual = await adzuna.parse_response(input)

    assert len(actual) == len(expected)
    assert actual[0].title == expected[0].title
    assert actual[0].title != expected[1].title


async def test_parse_response_without_salary_max_gives_valid_job_list():
    adzuna = Adzuna()

    salary_min = 50000
    description = "test_description"
    job1 = JobFactory(source=adzuna.source, salary=salary_min)

    input = {
        "results": [
            {
                "title": job1.title,
                "id": job1.source_id,
                "company": {"display_name": job1.company_name},
                "description": description,
                "redirect_url": job1.url,
                "salary_min": salary_min,
                "location": {"display_name": job1.location},
            },
        ]
    }

    expected = [job1]
    actual = await adzuna.parse_response(input)

    assert len(actual) == len(expected)
    assert actual[0].salary == expected[0].salary


async def test_parse_response_without_salary_min_gives_valid_job_list():
    adzuna = Adzuna()

    salary_max = 50000
    description = "test_description"
    job1 = JobFactory(source=adzuna.source, salary=salary_max)

    input = {
        "results": [
            {
                "title": job1.title,
                "id": job1.source_id,
                "company": {"display_name": job1.company_name},
                "description": description,
                "redirect_url": job1.url,
                "salary_max": salary_max,
                "location": {"display_name": job1.location},
            },
        ]
    }

    expected = [job1]
    actual = await adzuna.parse_response(input)

    assert len(actual) == len(expected)
    assert actual[0].salary == expected[0].salary


async def test_parse_response_without_salary_gives_valid_job_list():
    adzuna = Adzuna()

    description = "test_description"
    job1 = JobFactory(source=adzuna.source, salary=None)

    input = {
        "results": [
            {
                "title": job1.title,
                "id": job1.source_id,
                "company": {"display_name": job1.company_name},
                "description": description,
                "redirect_url": job1.url,
                "location": {"display_name": job1.location},
            },
        ]
    }

    expected = [job1]
    actual = await adzuna.parse_response(input)

    assert len(actual) == len(expected)
    assert actual[0].salary == expected[0].salary


async def test_parse_response_with_empty_input_returns_empty_list():
    adzuna = Adzuna()

    input = {}

    expected = []
    actual = await adzuna.parse_response(input)

    assert expected == actual
