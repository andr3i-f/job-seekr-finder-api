from app.core.database_session import get_async_session
from app.models import Job as JobModel
from sqlalchemy import select, and_


class Job:
    def __init__(
        self,
        title,
        source,
        source_id,
        company_name,
        experience_level,
        url,
        salary,
        location,
    ):
        self.id = ""

        self.title = title
        self.source = source
        self.source_id = source_id
        self.company_name = company_name
        self.experience_level = experience_level
        self.url = url
        self.salary = salary
        self.location = location

    async def store_in_database(self):
        async with get_async_session() as db:
            job = JobModel(
                title=self.title,
                source=self.source,
                company_name=self.company_name,
                source_id=self.source_id,
                experience_level=self.experience_level,
                url=self.url,
                salary=self.salary,
                location=self.location,
            )

            db.add(job)
            await db.commit()

    async def exists_in_database(self):
        # TODO: expand on this functionality by adding additional checks. This should work well for Adzuna.
        async with get_async_session() as db:
            query = select(JobModel).where(
                and_(
                    JobModel.source_id == self.source_id, JobModel.source == self.source
                )
            )
            result = await db.execute(query)
            job = result.scalar_one_or_none()

        return job is not None

    @staticmethod
    def get_jobs():
        # TODO: Implement; if needed
        pass
