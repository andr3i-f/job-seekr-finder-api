import factory
from faker import Faker

from app.models import Job

fake = Faker()


class JobFactory(factory.Factory):
    class Meta:
        model = Job

    title = factory.LazyAttribute(lambda _: fake.job())
    source = "test"
    source_id = factory.sequence(lambda n: f"test-{n}")
    company_name = factory.LazyAttribute(lambda _: fake.company())
    experience_level = factory.Iterator(["Intern", "Junior", "Mid", "Senior"])
    url = factory.LazyAttribute(lambda _: fake.url())
    salary = factory.LazyAttribute(lambda _: fake.random_int(60000, 160000))
    location = factory.LazyAttribute(lambda _: fake.city())
