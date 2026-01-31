from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import get_settings

jobstores = {
    "default": SQLAlchemyJobStore(
        url=get_settings().scheduler_database_uri.render_as_string(hide_password=False)
    )
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="America/Los_Angeles")


def start_scheduler():
    scheduler.start()
