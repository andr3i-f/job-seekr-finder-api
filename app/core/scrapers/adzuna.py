from .base_scraper import BaseScraper
from app.core.config import get_settings
from app.core.jobs.job import Job

class Adzuna(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(self)
        self.app_id = get_settings().adzuna.application_id
        self.app_key = get_settings().adzuna.application_key
        self.country = 'us'
        self.page = 1

        self.source = "Adzuna"
        self.url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/{self.page}"

    def build_params(self):
        payload = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'results_per_page': 100,
            'what': 'Software Developer'
        }

        return payload

    def build_header(self):
        header = {
            'Accept': 'application/json'
        }

        return header

    async def parse_response(self, res):
        res = res.json()
        new_jobs_found = 0
        found_jobs = []

        if 'results' not in res:
            # log some error here
            return
        
        for found_job in res['results']:
            title = found_job['title']
            source_id = found_job['id']
            company_name = found_job['company']['display_name']
            experience_level = self.determine_experience_level(found_job['description'])
            url = found_job['redirect_url']
            salary = self.calculate_salary(found_job['salary_min'], found_job['salary_max'])
            location = found_job['location']['display_name']

            found_jobs.append(Job(
                title=title,
                source=self.source,
                source_id=source_id,
                company_name=company_name,
                experience_level=experience_level,
                url=url,
                salary=salary,
                location=location
            ))

        for job in found_jobs:
            if job.exists_in_database():
                pass

            new_jobs_found += 1
            await job.store_in_database()

        # log how many jobs we found
        print(f"{self.source} has found {new_jobs_found} more jobs")

    def calculate_salary(self, min, max):
        return (min + max) / 2
    
    def determine_experience_level(self, description):
        # some logic here that determines the experience level based on given description
        # potentially use some regex that can determine what we looking at
        
        return "Intern"

        

        # location
        # adzuna-id

    #     "id": "string",
    #   "title": "string",
    #   "description": "string",
    #   "created": "string",
    #   "redirect_url": "string",
    #   "adref": "string",
    #   "latitude": 0,
    #   "longitude": 0,
    #   "location": {
    #     "display_name": "string",
    #     "area": [
    #       "string"
    #     ]
    #   },
    #   "category": {
    #     "tag": "string",
    #     "label": "string"
    #   },
    #   "company": {
    #     "display_name": "string",
    #     "canonical_name": "string",
    #     "count": 0,
    #     "average_salary": 0
    #   },
    #   "salary_min": 0,
    #   "salary_max": 0,
    #   "salary_is_predicted": "0",
    #   "contract_time": "full_time",
    #   "contract_type": "permanent"



