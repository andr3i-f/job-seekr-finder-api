import factory
from faker import Faker

from app.models import Job
from app.core.consts import JOB_EXPERIENCE_TYPES

fake = Faker()


class JobFactory(factory.Factory):
    class Meta:
        model = Job

    title = factory.LazyAttribute(lambda _: fake.job())
    source = "test"
    source_id = factory.sequence(lambda n: f"test-{n}")
    company_name = factory.LazyAttribute(lambda _: fake.company())
    experience_level = factory.Iterator(JOB_EXPERIENCE_TYPES)
    url = factory.LazyAttribute(lambda _: fake.url())
    salary = factory.LazyAttribute(lambda _: fake.random_int(60000, 160000))
    location = factory.LazyAttribute(lambda _: fake.city())
