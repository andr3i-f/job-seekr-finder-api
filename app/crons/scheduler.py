from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.core.config import get_settings

jobstores = {
    'default': SQLAlchemyJobStore(url=get_settings().scheduler_database_uri)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

def start_scheduler():
    scheduler.start()