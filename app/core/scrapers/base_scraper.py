import requests
from app.core.jobs.job import Job
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

        found_jobs = await self.parse_response(res)

        if found_jobs:
            await self.store_potential_jobs(found_jobs)


    async def store_potential_jobs(self, found_jobs: list[Job]):
        new_jobs_found = 0
        
        for job in found_jobs:
            if await job.exists_in_database():
                continue

            new_jobs_found += 1
            await job.store_in_database()

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

    def log_info(self, msg):
        logger.info(f"[{self.source}] {msg}")

    def log_error(self, msg):
        logger.error(f"[{self.source}] {msg}")
