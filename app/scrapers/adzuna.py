import requests
from os import getenv

from .generic_scraper import GenericScraper
from .config import ADZUNA_URL


class Adzuna(GenericScraper):
    def __init__(self):
        self.country = "us"
        self.page = 1
        self.url = ADZUNA_URL.format(ISO_8601_country_code=self.country, page=self.page)

    def get_jobs(self):
        res = requests.get(self.url, self.build_params(), headers={'Accept': 'application/json'})

        print(res.status_code)
        print(res.json())

        return res
    
    def process_job_data(self, jobs_data):
        # name
        # company
        # potential salary (if applicable)
        # posting date
        return []

    def build_params(self):
        params = {
            "app_id": getenv("ADZUNA_APP_ID"),
            "app_key": getenv("ADZUNA_KEY"),
            "results_per_page": 10,
            "what": "software engineer",
            "where": "United States",
        }

        return params
