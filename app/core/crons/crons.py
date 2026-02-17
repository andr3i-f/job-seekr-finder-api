from app.core.email.email import Email
from app.core.scrapers.adzuna import Adzuna

from .scheduler import scheduler

adzuna = Adzuna()
email = Email()


async def email_notifications_cron():
    await email.send_emails()


async def adzuna_scraper_cron():
    await adzuna.call()


scheduler.add_job(
    email_notifications_cron,
    trigger="cron",
    hour=20,
    minute=30,
    id="email_notifications_cron",
    misfire_grace_time=3600,
    replace_existing=True,
)

scheduler.add_job(
    adzuna_scraper_cron,
    trigger="cron",
    hour=10,
    minute=30,
    id="adzuna_scraper_cron",
    misfire_grace_time=3600,
    replace_existing=True,
)
