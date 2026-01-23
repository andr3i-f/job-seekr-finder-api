import requests
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database_session import get_async_session

from app.models import Job
from app.core.config import logger
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self):
        self.url = ""
        self.source = "BaseScraper"

    async def call(self):
        res = requests.get(
            self.url, params=self.build_params(), headers=self.build_header()
        )

        if res.status_code != 200:
            self.log_error(f"Error getting data - response code: {res.status_code}")

        res = res.json()
        found_jobs = await self.parse_response(res)

        if found_jobs:
            await self.store_potential_jobs(found_jobs)

    async def store_potential_jobs(self, found_jobs: list[Job]):
        new_jobs_found = 0

        async with get_async_session() as session:
            for job in found_jobs:
                if await self.job_exists_in_database(job, session):
                    continue

                new_jobs_found += 1
                session.add(job)

            await session.commit()

            if new_jobs_found > 0:
                self.log_info(f"Found {new_jobs_found} new jobs")

    @abstractmethod
    def build_params(self):
        pass

    @abstractmethod
    def build_header(self):
        pass

    @abstractmethod
    def parse_response(self, res) -> list[Job]:
        pass

    @abstractmethod
    async def job_exists_in_database(self, job: Job, session: AsyncSession) -> bool:
        pass

    def log_info(self, msg):
        logger.info(f"[{self.source}] {msg}")

    def log_error(self, msg):
        logger.error(f"[{self.source}] {msg}")
