from .base_scraper import BaseScraper
from app.core.config import get_settings

class Adzuna(BaseScraper):
    def __init__(self):
        BaseScraper.__init__()
        self.app_id = get_settings().adzuna.application_id
        self.app_key = get_settings().adzuna.application_key
        self.country = 'us'
        self.page = 1

        self.scraper_name = "Adzuna"
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

    def parse_response(self, res):
        res = res.json()
        found_jobs = []

        if 'results' not in res:
            # log some error here
            return
        
        #for job in res['results']:
        #

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



