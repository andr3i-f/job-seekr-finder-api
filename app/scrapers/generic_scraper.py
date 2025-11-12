from fastapi_utilities import repeat_every


class GenericScraper:
    def __init__(self):
        self.url = ""

    @repeat_every(seconds=3)
    def start(self):
        jobs_data = self.get_jobs()
        processed_jobs = self.process_job_data(jobs_data)
        self.post_jobs_to_database(processed_jobs)

    def get_jobs(self):
        pass

    def process_job_data(self, jobs_data):
        pass

    def post_jobs_to_database(self, processed_jobs):
        pass

    def build_params(self):
        pass
