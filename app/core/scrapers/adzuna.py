from .base_scraper import BaseScraper
from app.core.config import get_settings
from app.models import Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_


class Adzuna(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(self)
        self.app_id = get_settings().adzuna.application_id
        self.app_key = get_settings().adzuna.application_key
        self.country = "us"
        self.page = 1

        self.source = "Adzuna"
        self.url = (
            f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/{self.page}"
        )

    def build_params(self):
        payload = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": 100,
            "what": "Software Developer",
            "category": "it-jobs",
        }

        return payload

    def build_header(self):
        header = {"Accept": "application/json"}

        return header

    async def parse_response(self, res) -> list[Job]:
        res = res.json()
        found_jobs = []

        if "results" not in res:
            self.log_error("Unable to parse response")
            return []

        for found_job in res["results"]:
            title = found_job["title"]
            source_id = found_job["id"]
            company_name = found_job["company"]["display_name"]
            experience_level = self.determine_experience_level(found_job["description"])
            url = found_job["redirect_url"]
            salary = self.calculate_salary(
                found_job["salary_min"], found_job["salary_max"]
            )
            location = found_job["location"]["display_name"]

            found_jobs.append(
                Job(
                    title=title,
                    source=self.source,
                    source_id=source_id,
                    company_name=company_name,
                    experience_level=experience_level,
                    url=url,
                    salary=salary,
                    location=location,
                )
            )

        return found_jobs

    def calculate_salary(self, salary_min, salary_max):
        if salary_min is None and salary_max is None:
            return None
        elif salary_min is None:
            return salary_max
        elif salary_max is None:
            return salary_min
        else:
            return (salary_min + salary_max) / 2

    def determine_experience_level(self, description):
        # TODO: Implement experience logic

        # some logic here that determines the experience level based on given description
        # potentially use some regex that can determine what we looking at
        # have a list of experience levels such as: Intern, New Graduate, Junior, ..., Senior

        return "Intern"

    async def job_exists_in_database(self, job: Job, session: AsyncSession):
        query = select(Job).where(
            and_(Job.source_id == job.source_id, Job.source == self.source)
        )

        result = await session.execute(query)
        found = result.scalar_one_or_none()

        return found is not None
