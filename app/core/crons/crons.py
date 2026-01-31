from app.core.scrapers.adzuna import Adzuna

from .scheduler import scheduler

adzuna = Adzuna()


async def adzuna_scraper_cron():
    await adzuna.call()


scheduler.add_job(
    adzuna_scraper_cron,
    trigger="cron",
    hour=10,
    minute=30,
    id="adzuna_scraper_cron",
    misfire_grace_time=3600,
    replace_existing=True,
)
