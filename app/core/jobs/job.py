from app.core.database_session import get_async_session

class Job:
    def __init__(self):
        self.id
        self.title
        self.source
        self.company_name
        self.employment_type
        self.experience_level
        self.url
        self.salary
        self.location
        
    def store_in_database(self):
        _db = get_async_session()

        

        pass

    def exists_in_database(self):
        # TODO: implement some sort of logic that takes into consideration some composite key and compares it with the current jobs found in the database
        # if it meets some criteria X, return true otherwise return false
        pass

    @staticmethod
    def create_job(title, source, company_name, employment_type, experience_level, url, salary, location):
        new_job = Job()
        new_job.title = title
        new_job.source = source
        new_job.company_name = company_name
        new_job.employment_type = employment_type
        new_job.experience_level = experience_level
        new_job.url = url
        new_job.salary = salary
        new_job.location = location

        return new_job

