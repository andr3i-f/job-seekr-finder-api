class Job:
    def __init__(self, title, source, company_name, experience_level, employment_type, description, url, salary, location, date_posted, valid_until):
        self.title = title
        self.source = source
        self.company_name = company_name
        self.employment_type = employment_type
        self.experience_level = experience_level
        self.description = description
        self.url = url
        self.salary = salary
        self.location = location
        self.date_posted = date_posted
        self.valid_until = valid_until

    def store_into_database(self):
        pass

    def exists_in_database(self):
        pass

    @staticmethod
    def load_jobs():
        pass

